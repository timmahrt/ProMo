'''
Created on Jun 29, 2016

@author: Tim
'''

try:
    import numpy as np
except ImportError:
    hasNumpy = False
else:
    hasNumpy = True

 
def _numpyCheck():
    if not hasNumpy:
        raise ImportError("Numpy required to do data interpolation. "
                          "Install numpy or don't use data interpolation")


def quadraticInterpolation(valueList2d, numDegrees, n,
                           startTime=None, endTime=None):
    '''
    Generates a series of points on a smooth curve that cross the given points
    
    numDegrees - the degrees of the fitted polynomial
               - the curve gets weird if this value is too high for the input
    n - number of points to output
    startTime/endTime/n - n points will be generated at evenly spaced
                          intervals between startTime and endTime
    '''
    _numpyCheck()
    
    x, y = zip(*valueList2d)
    
    if startTime is None:
        startTime = x[0]
    if endTime is None:
        endTime = x[-1]
    
    polyFunc = np.poly1d(np.polyfit(x, y, numDegrees))
    
    newX = np.linspace(startTime, endTime, n)
    
    retList = [(n, polyFunc(n)) for n in newX]
    
    return retList
