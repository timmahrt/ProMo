'''
Created on Apr 2, 2015

@author: tmahrt
'''

import os

from praatio import tgio


def getIntervals(fn, tierName, filterFunc=None):
    '''
    Get information about the 'extract' tier, used by several merge scripts
    '''

    if filterFunc is None:
        filterFunc = lambda x: True

    tg = tgio.openTextGrid(fn)
    tier = tg.tierDict[tierName]

    entryList = tier.entryList
    if filterFunc is not None:
        entryList = [entry for entry in entryList if filterFunc(entry)]

    return entryList


def makeDir(path):
    
    if not os.path.exists(path):
        os.mkdir(path)
        

def generateStepList(numSteps):
    
    assert(numSteps > 0)
    
    stepList = []
    for i in range(numSteps):
        stepList.append((i + 1) / float((numSteps)))
        
    return stepList
