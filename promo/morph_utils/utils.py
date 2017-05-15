'''
Created on Apr 2, 2015

@author: tmahrt
'''

import os

from praatio import tgio


def getIntervals(fn, tierName, filterFunc=None,
                 includeUnlabeledRegions=False):
    '''
    Get information about the 'extract' tier, used by several merge scripts
    '''

    tg = tgio.openTextgrid(fn)
    
    tier = tg.tierDict[tierName]
    if includeUnlabeledRegions is True:
        tier = tgio._fillInBlanks(tier)

    entryList = tier.entryList
    if filterFunc is not None:
        entryList = [entry for entry in entryList if filterFunc(entry)]

    return entryList


def makeDir(path):
    
    if not os.path.exists(path):
        os.mkdir(path)
        

def generateStepList(numSteps, includeZero=False):
    
    assert(numSteps > 0)
    
    stepList = []
    if includeZero:
        stepList.append(0)
        
    for i in range(numSteps):
        stepList.append((i + 1) / float((numSteps)))
        
    return stepList
