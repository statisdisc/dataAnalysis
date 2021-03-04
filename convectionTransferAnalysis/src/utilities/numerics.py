import numpy as np

def interpolate(h):
    "Interpolate values from cell centers to cell faces"
    return 0.5*(h + np.roll(h,1))
    
def reconstruct(h):
    "Reconstruct values at cell centers using values on the cell faces"
    return 0.5*(h + np.roll(h,-1))

def epsilon_ij(i,j,S,alpha,dt):
    "Coefficient 1 for flux form transfer"
    numerator = 1. + dt*( alpha*S[j][i] - (1.-alpha)*S[i][j] )
    denominator = 1. + alpha*dt*( S[j][i] + S[i][j] )
    return numerator/denominator
    
def lambda_ij(i,j,S,alpha,dt):
    "Coefficient 2 for flux form transfer"
    numerator = dt*S[i][j]
    denominator = 1. + alpha*dt*( S[j][i] + S[i][j] )
    return numerator/denominator
    
def nu_ij(i,j,S,alpha,dt,h_old,h_new,q,r):
    "Coefficient for advective form transfer"
    
    h = [0.,0.]
    if q == "n" and r == "n":
        numerator = dt * S[i][j] * h_old[i] / h_old[j]
        denominator = 1. + alpha*dt*( S[i][j] * h_old[i]/h_old[j] + S[j][i] * h_old[j]/h_old[i] )
        return numerator/denominator
    elif q == "n" and r == "n+1":
        numerator = dt * S[i][j] * h_old[i] / h_new[j]
        denominator = 1. + alpha*dt*( S[i][j] * h_old[i]/h_new[j] + S[j][i] * h_old[j]/h_new[i] )
        return numerator/denominator
    elif q == "n+1" and r == "n":
        numerator = dt * S[i][j] * h_new[i] / h_old[j]
        denominator = 1. + alpha*dt*( S[i][j] * h_new[i]/h_old[j] + S[j][i] * h_new[j]/h_old[i] )
        return numerator/denominator
    elif q == "n+1" and r == "n+1":
        numerator = dt * S[i][j] * h_new[i] / h_new[j]
        denominator = 1. + alpha*dt*( S[i][j] * h_new[i]/h_new[j] + S[j][i] * h_new[j]/h_new[i] )
        return numerator/denominator
    else:
        raise ValueError("q and r must have values n or n+1")

def conductTransfersAdvective(eta, theta, u, dt, S, alphaC, alphaM, alphaT, q, r, velocity_face=True):
    "Complete entire transfer process for advective form transfers"
    
    eta_new = [eta[0].copy(),eta[1].copy()]
    etaf = [interpolate(eta_new[0]), interpolate(eta_new[1])]
    etaf_new = [interpolate(eta_new[0]), interpolate(eta_new[1])]
    theta_new = [theta[0].copy(),theta[1].copy()]
    u_new = [u[0].copy(),u[1].copy()]
    Sf = [[0*S[0][1],interpolate(S[0][1])],[interpolate(S[1][0]),0*S[1][0]]]

    #Conduct mass transfers first
    eta_new[0] = epsilon_ij(0,1,S,alphaC,dt)*eta[0] + lambda_ij(1,0,S,alphaC,dt)*eta[1]
    eta_new[1] = epsilon_ij(1,0,S,alphaC,dt)*eta[1] + lambda_ij(0,1,S,alphaC,dt)*eta[0]
        
    etaf_new[0] = interpolate( eta_new[0] )
    etaf_new[1] = interpolate( eta_new[1] )
    
    #Conduct temperature and velocity transfers on cell faces
    nu_01 = nu_ij(0,1,S,alphaT,dt,eta,eta_new,q,r)
    nu_10 = nu_ij(1,0,S,alphaT,dt,eta,eta_new,q,r)
    
    theta_new[0] = (1.-nu_10)*theta[0] + nu_10*theta[1]
    theta_new[1] = (1.-nu_01)*theta[1] + nu_01*theta[0]
    
    if velocity_face == True:
        nu_01 = nu_ij(0,1,Sf,alphaM,dt,etaf,etaf_new,q,r)
        nu_10 = nu_ij(1,0,Sf,alphaM,dt,etaf,etaf_new,q,r)
        
    u_new[0] = (1.-nu_10)*u[0] + nu_10*u[1]
    u_new[1] = (1.-nu_01)*u[1] + nu_01*u[0]
    
    return eta_new, theta_new, u_new
    
def conductTransfersFlux(eta, theta, u, dt, S, alphaC, alphaM, alphaT, velocity_face=True):
    "Complete entire transfer process for flux form transfers"
    
    eta_new = [eta[0].copy(),eta[1].copy()]
    etaf = [interpolate(eta_new[0]), interpolate(eta_new[1])]
    etaf_new = [interpolate(eta_new[0]), interpolate(eta_new[1])]
    theta_new = [theta[0].copy(),theta[1].copy()]
    u_new = [u[0].copy(),u[1].copy()]
    Sf = [[0*S[0][1],interpolate(S[0][1])],[interpolate(S[1][0]),0*S[1][0]]]

    #Conduct mass transfers first
    eta_new[0] = epsilon_ij(0,1,S,alphaC,dt)*eta[0] + lambda_ij(1,0,S,alphaC,dt)*eta[1]
    eta_new[1] = epsilon_ij(1,0,S,alphaC,dt)*eta[1] + lambda_ij(0,1,S,alphaC,dt)*eta[0]
        
    etaf_new[0] = interpolate( eta_new[0] )
    etaf_new[1] = interpolate( eta_new[1] )
    
    #Conduct temperature and velocity transfers on cell faces
    theta_new[0] = ( epsilon_ij(0,1,S,alphaC,dt)*eta[0]*theta[0] + lambda_ij(1,0,S,alphaC,dt)*eta[1]*theta[1] )/eta_new[0]
    theta_new[1] = ( epsilon_ij(1,0,S,alphaC,dt)*eta[1]*theta[1] + lambda_ij(0,1,S,alphaC,dt)*eta[0]*theta[0] )/eta_new[1]
    
    if velocity_face == True:
        u_new[0] = ( epsilon_ij(0,1,Sf,alphaC,dt)*etaf[0]*u[0] + lambda_ij(1,0,Sf,alphaC,dt)*etaf[1]*u[1] )/etaf_new[0]
        u_new[1] = ( epsilon_ij(1,0,Sf,alphaC,dt)*etaf[1]*u[1] + lambda_ij(0,1,Sf,alphaC,dt)*etaf[0]*u[0] )/etaf_new[1]
    else:
        u_new[0] = ( epsilon_ij(0,1,S,alphaC,dt)*eta[0]*u[0] + lambda_ij(1,0,S,alphaC,dt)*eta[1]*u[1] )/eta_new[0]
        u_new[1] = ( epsilon_ij(1,0,S,alphaC,dt)*eta[1]*u[1] + lambda_ij(0,1,S,alphaC,dt)*eta[0]*u[0] )/eta_new[1]
        
    return eta_new, theta_new, u_new