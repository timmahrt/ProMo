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
        durationTier = dataio.PointObject(durationPointList, dataio.DURATION,
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


def getMorphParameters(fromTGFN, toTGFN, tierName, outputTGFN=None,
                       outputImageFN=None, stepListForImage=None):
    '''
    Get intervals for source and target audio files
    
    Use this information to find out how much to stretch/shrink each source
    interval
    '''
    
    if stepListForImage is None:
        stepListForImage = [1, ]
    if outputTGFN is not None:
        utils.makeDir(os.path.split(outputTGFN)[0])
    if outputImageFN is not None:
        utils.makeDir(os.path.split(outputImageFN)[0])
            
    fromExtractInfo = utils.getIntervals(fromTGFN, tierName)
    toExtractInfo = utils.getIntervals(toTGFN, tierName)

    durationParameters = []
    for fromInfoTuple, toInfoTuple in zip(fromExtractInfo, toExtractInfo):
        fromStart, fromEnd = fromInfoTuple[:2]
        toStart, toEnd = toInfoTuple[:2]

        # Praat will ignore a second value appearing at the same time as
        # another so we give each start a tiny offset to distinguish intervals
        # that start and end at the same point
        toStart += PRAAT_TIME_DIFF
        fromStart += PRAAT_TIME_DIFF

        ratio = (toEnd - toStart) / float((fromEnd - fromStart))

        ratioTuple = (fromStart, fromEnd, ratio)
        durationParameters.append(ratioTuple)
    
    # Create the adjusted textgrids
    if outputTGFN is not None:
        adjustedTG = textgridMorphDuration(fromTGFN,
                                           toTGFN)
        adjustedTG.save(outputTGFN)
    
    # Create the plot of the morph
    if outputImageFN is not None:
        _plotResults(durationParameters, fromTGFN, toTGFN,
                     tierName, stepListForImage,
                     outputImageFN)
    
    return durationParameters


def getManipulatedParamaters(tgFN, tierName, modFunc,
                             outputTGFN=None, outputImageFN=None,
                             stepListForImage=None):
    '''
    Get intervals for source and target audio files
    
    Use this information to find out how much to stretch/shrink each source
    interval.
    '''
    
    if stepListForImage is None:
        stepListForImage = [1, ]
    if outputTGFN is not None:
        utils.makeDir(os.path.split(outputTGFN)[0])
    
    if outputImageFN is not None:
        utils.makeDir(os.path.split(outputTGFN)[0])
    
    fromExtractInfo = utils.getIntervals(tgFN, tierName)
    
    durationParameters = []
    for fromInfoTuple in fromExtractInfo:
        fromStart, fromEnd = fromInfoTuple[:2]
        toStart, toEnd = modFunc(fromStart, fromEnd)

        # Praat will ignore a second value appearing at the same time as
        # another so we give each start a tiny offset to distinguish intervals
        # that start and end at the same point
        toStart += PRAAT_TIME_DIFF
        fromStart += PRAAT_TIME_DIFF

        ratio = (toEnd - toStart) / float((fromEnd - fromStart))

        ratioTuple = (fromStart, fromEnd, ratio)
        durationParameters.append(ratioTuple)
    
    # Create the adjusted textgrids
    if outputTGFN is not None:
        adjustedTG = textgridManipulateDuration(tgFN, modFunc)
        adjustedTG.save(outputTGFN)
    
    # Create the plot of the manipulation
    if outputTGFN is not None and outputImageFN is not None:
        _plotResults(durationParameters, tgFN, outputTGFN,
                     tierName, stepListForImage,
                     outputImageFN)

    return durationParameters


def _plotResults(durationParameters, fromTGFN, toTGFN, tierName,
                 stepList, outputPNGFN):

    # Containers
    fromDurList = []
    toDurList = []
    actDurList = []
    labelList = []

    fromExtractInfo = utils.getIntervals(fromTGFN, tierName)
    toExtractInfo = utils.getIntervals(toTGFN, tierName)

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

    fromTG = tgio.openTextGrid(fromTGFN)
    toTG = tgio.openTextGrid(toTGFN)
    adjustedTG = tgio.Textgrid()

    for tierName in fromTG.tierNameList:
        fromTier = fromTG.tierDict[tierName]
        toTier = toTG.tierDict[tierName]
        adjustedTier = fromTier.morph(toTier)
        adjustedTG.addTier(adjustedTier)

    return adjustedTG


def textgridManipulateDuration(tgFN, modFunc, filterFunc=None):

    tg = tgio.openTextGrid(tgFN)

    # By default, all regions are manipulated (except silence)
    if filterFunc is None:
        filterFunc = lambda x: True

    adjustedTG = tgio.Textgrid()

    for tierName in tg.tierNameList:
        fromTier = tg.tierDict[tierName]
        adjustedTier = fromTier.manipulate(modFunc, filterFunc)
        adjustedTG.addTier(adjustedTier)

    return adjustedTG
