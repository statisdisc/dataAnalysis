import numpy as np
from numerics import conductTransfersAdvective
from numerics import conductTransfersFlux

def fluidPE(eta, g=9.81, h=1.):
    "Potential energy"
    return eta*g*h
    
def totalPE(eta, g=9.81, h=1.):
    "Total potential energy"
    return fluidPE(eta[0], g=g, h=h) + fluidPE(eta[1], g=g, h=h)
    
def fluidIE(eta, theta, cv=800., exner=1.):
    "Internal energy"
    return cv*exner*eta*theta
    
def totalIE(eta, theta, cv=800., exner=1.):
    "Total internal energy"
    return fluidIE(eta[0], theta[0], cv=cv, exner=exner) + fluidIE(eta[1], theta[1], cv=cv, exner=exner)

def fluidKE(eta, u):
    "Kinetic energy"
    return 0.5*eta*u**2
    
def totalKE(eta, u):
    "Total kinetic energy"
    return fluidKE(eta[0], u[0]) + fluidKE(eta[1], u[1])
    
def totalEnergy(eta, theta, u, g=9.81, h=1e3, cv=800., exner=1.):
    "Compute the total energy"
    return totalPE(eta, g=g, h=h) + totalIE(eta, theta, cv=cv, exner=exner) + totalKE(eta, u)

def deltaE_advective(eta, theta, u, dt, S, alphaC, alphaM, alphaT, q, r, velocity_face=True):
    "Calculate the energy and momentum changes when using advective form transfers"
    
    etaNew, thetaNew, uNew = conductTransfersAdvective(
        eta, theta, u, dt, S, alphaC, alphaM, alphaT, q, r, 
        velocity_face=velocity_face
    )
    
    if velocity_face == True:
        uc = [reconstruct(u[0]), reconstruct(u[1])]
        ucNew = [reconstruct(uNew[0]), reconstruct(uNew[1])]
    else:
        uc = [u[0], u[1]]
        ucNew = [uNew[0], uNew[1]]
    
    E = totalEnergy(eta, theta, uc)
    ENew = totalEnergy(etaNew, thetaNew, ucNew)
    
    F = eta[0]*uc[0] + eta[1]*uc[1]
    FNew = etaNew[0]*ucNew[0] + etaNew[1]*ucNew[1]
    
    # if alphaC == 0 and alphaM == 1 and q=="n" and r=="n":
    # if alphaC == 1 and alphaM == 0 and q=="n+1" and r=="n+1":
        # print (FNew - F)/F
    
    return (ENew - E)/E, (FNew - F)/F, uNew
    
def deltaE_flux(eta, theta, u, dt, S, alphaC, alphaM, alphaT, velocity_face):
    "Calculate the energy and momentum changes when using flux form transfers"
    
    etaNew, thetaNew, uNew = conductTransfersFlux(
        eta, theta, u, dt, S, alphaC, alphaM, alphaT, 
        velocity_face=velocity_face
    )
    
    if velocity_face == True:
        uc = [reconstruct(u[0]), reconstruct(u[1])]
        ucNew = [reconstruct(uNew[0]), reconstruct(uNew[1])]
    else:
        uc = [u[0], u[1]]
        ucNew = [uNew[0], uNew[1]]

    E = totalEnergy(eta, theta, uc)
    ENew = totalEnergy(etaNew, thetaNew, ucNew)
    
    F = eta[0]*uc[0] + eta[1]*uc[1]
    FNew = etaNew[0]*ucNew[0] + etaNew[1]*ucNew[1]
    
    return (ENew - E)/E, (FNew - F)/F, uNew
    
def deltaE(eta, theta, u, dt, S, alphaC, alphaM, alphaT, q, r, velocity_face=True, momentum_eq="advective"):
    "Calculate the energy and momentum changes when conducting mass transfers"
    
    if momentum_eq == "advective":
        return deltaE_advective(eta, theta, u, dt, S, alphaC, alphaM, alphaT, q, r, velocity_face=velocity_face)
    elif momentum_eq == "flux":
        return deltaE_flux(eta, theta, u, dt, S, alphaC, alphaM, alphaT, velocity_face=velocity_face)
    
