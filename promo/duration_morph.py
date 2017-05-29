'''
Created on Jun 5, 2013

@author: timmahrt
'''

import os
from os.path import join
import copy

from praatio import tgio
from praatio import praat_scripts
from praatio import dataio

from promo.morph_utils import utils
from promo.morph_utils import audio_scripts
from promo.morph_utils import plot_morphed_data

# This value is used to differentiate a praat interval boundary that marks
# the start of one region and the end of another.
PRAAT_TIME_DIFF = 0.000001


class NoLabeledRegionFoundException(Exception):

    def __init__(self, tgFN):
        super(NoLabeledRegionFoundException, self).__init__()
        self.tgFN = tgFN

    def __str__(self):
        return "No labeled region fitting the specified criteria for tg: " + \
            self.tgFN


def changeDuration(fromWavFN, durationParameters, stepList, outputName,
                   outputMinPitch, outputMaxPitch, praatEXE):
    '''
    Uses praat to morph duration in one file to duration in another

    Praat uses the PSOLA algorithm
    '''

    rootPath = os.path.split(fromWavFN)[0]

    # Prep output directories
    outputPath = join(rootPath, "duration_resynthesized_wavs")
    utils.makeDir(outputPath)
    
    durationTierPath = join(rootPath, "duration_tiers")
    utils.makeDir(durationTierPath)

    fromWavDuration = audio_scripts.getSoundFileDuration(fromWavFN)

    durationParameters = copy.deepcopy(durationParameters)
    # Pad any gaps with values of 1 (no change in duration)
    
    # No need to stretch out any pauses at the beginning
    if durationParameters[0][0] != 0:
        tmpVar = (0, durationParameters[0][0] - PRAAT_TIME_DIFF, 1)
        durationParameters.insert(0, tmpVar)

    # Or the end
    if durationParameters[-1][1] < fromWavDuration:
        durationParameters.append((durationParameters[-1][1] + PRAAT_TIME_DIFF,
                                   fromWavDuration, 1))

    # Create the praat script for doing duration manipulation
    for stepAmount in stepList:
        durationPointList = []
        for start, end, ratio in durationParameters:
            percentChange = 1 + (ratio - 1) * stepAmount
            durationPointList.append((start, percentChange))
            durationPointList.append((end, percentChange))
        
        outputPrefix = "%s_%0.3g" % (outputName, stepAmount)
        durationTierFN = join(durationTierPath,
                              "%s.DurationTier" % outputPrefix)
        outputWavFN = join(outputPath, "%s.wav" % outputPrefix)
        durationTier = dataio.PointObject2D(durationPointList, dataio.DURATION,
                                            0, fromWavDuration)
        durationTier.save(durationTierFN)
        
        praat_scripts.resynthesizeDuration(praatEXE,
                                           fromWavFN,
                                           durationTierFN,
                                           outputWavFN,
                                           outputMinPitch, outputMaxPitch)


def getBareParameters(wavFN):
    wavDuration = audio_scripts.getSoundFileDuration(wavFN)
    return [(0, wavDuration, ''), ]


def getMorphParameters(fromTGFN, toTGFN, tierName,
                       filterFunc=None, useBlanks=False):
    '''
    Get intervals for source and target audio files
    
    Use this information to find out how much to stretch/shrink each source
    interval.
    
    The target values are based on the contents of toTGFN.
    '''
    
    if filterFunc is None:
        filterFunc = lambda entry: True  # Everything is accepted
    
    fromEntryList = utils.getIntervals(fromTGFN, tierName,
                                       includeUnlabeledRegions=useBlanks)
    toEntryList = utils.getIntervals(toTGFN, tierName,
                                     includeUnlabeledRegions=useBlanks)

    fromEntryList = [entry for entry in fromEntryList if filterFunc(entry)]
    toEntryList = [entry for entry in toEntryList if filterFunc(entry)]

    assert(len(fromEntryList) == len(toEntryList))

    durationParameters = []
    for fromEntry, toEntry in zip(fromEntryList, toEntryList):
        fromStart, fromEnd = fromEntry[:2]
        toStart, toEnd = toEntry[:2]

        # Praat will ignore a second value appearing at the same time as
        # another so we give each start a tiny offset to distinguish intervals
        # that start and end at the same point
        toStart += PRAAT_TIME_DIFF
        fromStart += PRAAT_TIME_DIFF
        
        ratio = (toEnd - toStart) / float((fromEnd - fromStart))
        durationParameters.append((fromStart, fromEnd, ratio))
    
    return durationParameters


def getManipulatedParamaters(tgFN, tierName, modFunc,
                             filterFunc=None, useBlanks=False):
    '''
    Get intervals for source and target audio files
    
    Use this information to find out how much to stretch/shrink each source
    interval.
    
    The target values are based on modfunc.
    '''
    
    fromExtractInfo = utils.getIntervals(tgFN, tierName, filterFunc,
                                         useBlanks)
    
    durationParameters = []
    for fromInfoTuple in fromExtractInfo:
        fromStart, fromEnd = fromInfoTuple[:2]
        toStart, toEnd = modFunc(fromStart), modFunc(fromEnd)

        # Praat will ignore a second value appearing at the same time as
        # another so we give each start a tiny offset to distinguish intervals
        # that start and end at the same point
        toStart += PRAAT_TIME_DIFF
        fromStart += PRAAT_TIME_DIFF

        ratio = (toEnd - toStart) / float((fromEnd - fromStart))

        ratioTuple = (fromStart, fromEnd, ratio)
        durationParameters.append(ratioTuple)

    return durationParameters


def outputMorphTextgrids(fromTGFN, durationParameters, stepList,
                         outputTGName):

    if outputTGName is not None:
        utils.makeDir(os.path.split(outputTGName)[0])

    # Create the adjusted textgrids
    if outputTGName is not None:
        
        for stepFactor in stepList:
            
            stepDurationParameters = [(start,
                                       end,
                                       1 + (ratio - 1) * stepFactor)
                                      for start, end, ratio
                                      in durationParameters]
            adjustedTG = textgridManipulateDuration(fromTGFN,
                                                    stepDurationParameters)
            
            outputTGFN = "%s_%0.3g.TextGrid" % (outputTGName, stepFactor)
            adjustedTG.save(outputTGFN)


def outputMorphPlot(fromTGFN, toTGFN, tierName, durationParameters, stepList,
                    outputImageFN):
    
    if outputImageFN is not None:
        utils.makeDir(os.path.split(outputImageFN)[0])
        
    # Create the plot of the morph
    if outputImageFN is not None:
        _plotResults(durationParameters, fromTGFN, toTGFN,
                     tierName, stepList, outputImageFN,
                     None, False)


def _plotResults(durationParameters, fromTGFN, toTGFN, tierName,
                 stepList, outputPNGFN, filterFunc,
                 includeUnlabeledRegions):

    # Containers
    fromDurList = []
    toDurList = []
    actDurList = []
    labelList = []

    fromExtractInfo = utils.getIntervals(fromTGFN, tierName, filterFunc,
                                         includeUnlabeledRegions)
    toExtractInfo = utils.getIntervals(toTGFN, tierName, filterFunc,
                                       includeUnlabeledRegions)

    # Get durations
    for fromInfoTuple, toInfoTuple in zip(fromExtractInfo, toExtractInfo):
        fromStart, fromEnd = fromInfoTuple[:2]
        toStart, toEnd = toInfoTuple[:2]

        labelList.append(fromInfoTuple[2])
        fromDurList.append(fromEnd - fromStart)
        toDurList.append(toEnd - toStart)

    # Get iterpolated values
    for stepAmount in stepList:
        tmpDurList = []
        for fromStart, fromEnd, ratio in durationParameters:
            dur = (fromEnd - fromStart)
            percentChange = 1 + (ratio - 1) * stepAmount
            tmpDurList.append(dur * percentChange)

        actDurList.append(tmpDurList)

    # Plot data
    plot_morphed_data.plotDuration(fromDurList, toDurList, actDurList,
                                   labelList, outputPNGFN)


def textgridMorphDuration(fromTGFN, toTGFN):
    '''
    A convenience function.  Morphs interval durations of one tg to another.
    
    This assumes the two textgrids have the same number of segments.
    '''
    fromTG = tgio.openTextgrid(fromTGFN)
    toTG = tgio.openTextgrid(toTGFN)
    adjustedTG = tgio.Textgrid()

    for tierName in fromTG.tierNameList:
        fromTier = fromTG.tierDict[tierName]
        toTier = toTG.tierDict[tierName]
        adjustedTier = fromTier.morph(toTier)
        adjustedTG.addTier(adjustedTier)

    return adjustedTG


def textgridManipulateDuration(tgFN, ratioList):

    tg = tgio.openTextgrid(tgFN)

    adjustedTG = tgio.Textgrid()

    for tierName in tg.tierNameList:
        fromTier = tg.tierDict[tierName]
        
        adjustedTier = None
        if isinstance(fromTier, tgio.IntervalTier):
            adjustedTier = _morphIntervalTier(fromTier, ratioList)
        elif isinstance(fromTier, tgio.PointTier):
            adjustedTier = _morphPointTier(fromTier, ratioList)
        
        assert(adjustedTier is not None)
        adjustedTG.addTier(adjustedTier)

    return adjustedTG


def _getTimeDiff(start, stop, ratio):
    '''Returns the time difference between interval and interval*ratio'''
    return (ratio - 1) * (stop - start)


def _morphPointTier(tier, ratioList):
    
    cumulativeAdjustAmount = 0
    i = 0
    newEntryList = []
    for timestamp, label in tier.entryList:
        
        # Advance to the manipulation interval that coincides with the
        # current point or appears after it
        while i < len(ratioList) and timestamp > ratioList[i][1]:
            rStart, rStop, ratio = ratioList[i]
            cumulativeAdjustAmount += _getTimeDiff(rStart, rStop, ratio)
            i += 1
        
        newTime = timestamp + cumulativeAdjustAmount
        
        # Alter the time if the point is within a manipulation interval
        if i < len(ratioList):
            rStart, rStop, ratio = ratioList[i]
            if timestamp > rStart and timestamp <= rStop:
                newTime += _getTimeDiff(rStart, timestamp, ratio)
        
        newEntryList.append((newTime, label))
    
    maxT = tier.maxTimestamp + cumulativeAdjustAmount
    return tier.new(entryList=newEntryList, maxTimestamp=maxT)


def _morphIntervalTier(tier, ratioList):
    
    cumulativeAdjustAmount = 0
    i = 0
    newEntryList = []
    for start, stop, label in tier.entryList:
        
        # Syncronize the manipulation and data intervals so that they
        # are either overlapping or the manipulation interval is farther
        # in the future.  This accumulates the effect of past
        # manipulations so we know how much to offset timestamps
        # for the current interval.
        while (i < len(ratioList) and start > ratioList[i][0] and
               start >= ratioList[i][1]):
            rStart, rStop, ratio = ratioList[i]
            cumulativeAdjustAmount = _getTimeDiff(rStart, rStop, ratio)
            i += 1
        
        newStart = start + cumulativeAdjustAmount
        newStop = stop + cumulativeAdjustAmount
        
        # Manipulate the interval further if there is overlap with a
        # manipulation interval
        while i < len(ratioList):
            rStart, rStop, ratio = ratioList[i]
            
            # currAdjustAmount is the ratio modified by percent change
            # e.g. if the ratio is a boost of 1.2 but percent change is
            # 0.5, ratio = 1.1 (it loses half of its effect)
            
            # Adjusting the start position based on overlap with the
            # current adjust interval
            if start <= rStart:
                pass
            elif start > rStart and start <= rStop:
                newStart += _getTimeDiff(rStart, start, ratio)
                
            # Adjusting the stop position based on overlap with the
            # current adjust interval
            if stop >= rStop:
                newStop += _getTimeDiff(rStart, rStop, ratio)
            elif stop < rStop and stop >= rStart:
                newStop += _getTimeDiff(rStart, stop, ratio)
            
            # If we are beyond the current manipulation interval,
            # then we need to move to the next one
            if stop >= rStop:
                cumulativeAdjustAmount += _getTimeDiff(rStart, rStop, ratio)
                i += 1
            # Otherwise, we are done manipulating the current interval
            elif stop < rStop:
                break
        
        newEntryList.append((newStart, newStop, label))
    
    newMax = tier.maxTimestamp + cumulativeAdjustAmount
    return tier.new(entryList=newEntryList, maxTimestamp=newMax)
