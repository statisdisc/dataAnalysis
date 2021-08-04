import time

def timeElapsed(function):
    '''
    Compute the time taken for a function to execute
    
    :param function: The function to be measured.
    :return: The same function wrapped in the time elapsed procedure.
    '''
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = function(*args, **kwargs)
        t2 = time.time()
        print(f'Elapsed time: {t2 - t1:.3f}s')
        
        return result
    
    return wrapper
