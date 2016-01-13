'''
Created on May 31, 2013

@author: timmahrt

Contains utilities for extracting, creating, and manipulating pitch files in
praat.
'''

import os
from os.path import join, splitext

from praatio import tgio
from praatio import pitch_and_intensity
from praatio import praat_scripts

from promo.morph_utils import utils
from promo.morph_utils import audio_scripts
from promo.morph_utils import plot_morphed_data
from promo.morph_utils import morph_sequence


def getPitchForIntervals(data, tgFN, tierName):
    '''
    Preps data for use in f0Morph
    '''
    tg = tgio.openTextGrid(tgFN)
    data = tg.tierDict[tierName].getValuesInIntervals(data)
    data = [dataList for _, dataList in data]

    return data


def f0Morph(fromWavFN, fromPitchFN, toPitchFN, numSteps,
            outputName, doPlotPitchSteps, fromPitchData, toPitchData,
            outputMinPitch, outputMaxPitch, praatEXE):
    '''
    Resynthesizes the pitch track from a source to a target wav file

    fromPitchData and toPitchData should be segmented according to the
    portions that you want to morph.  The two lists must have the same
    number of sublists.

    Occurs over a three-step process.

    This function can act as a template for how to use the function
    morph_sequence.morphChunkedDataLists to morph pitch contours or
    other data.
    '''
    pitchPath = os.path.split(fromPitchFN)[0]

    fromName = splitext(os.path.split(fromPitchFN)[1])[0]
    toName = splitext(os.path.split(toPitchFN)[1])[0]

    fromDuration = audio_scripts.getSoundFileDuration(fromWavFN)

    # Iterative pitch tier data path
    pitchTierPath = join(pitchPath, "pitchTiers")
    resynthesizedPath = join(pitchPath, "f0ResynthesizedWavs")
    for tmpPath in [pitchTierPath, resynthesizedPath]:
        utils.makeDir(tmpPath)

    # 1. Prepare the data for morphing - acquire the segments to merge
    # (Done elsewhere, with the input fed into this function)

    # 2. Morph the fromData to the toData
    finalOutputList = morph_sequence.morphChunkedDataLists(fromPitchData,
                                                           toPitchData,
                                                           numSteps)

    fromPitchData = [row for subList in fromPitchData for row in subList]
    toPitchData = [row for subList in toPitchData for row in subList]

    # 3. Save the pitch data and resynthesize the pitch
    mergedDataList = []
    for i in xrange(0, len(finalOutputList)):
        outputPitchList = finalOutputList[i]
        pitchFN = "%s_%d.PitchTier" % (toName, i)
        pitchFNFullPath = join(pitchTierPath, pitchFN)
        outputFN = join(resynthesizedPath, "%s_f0_%d_%d.wav" % (outputName,
                                                                numSteps,
                                                                i + 1))
        
        pitch_and_intensity.writePitchTier(pitchTierPath, pitchFN,
                                           outputPitchList,
                                           0, fromDuration)

        outputTime, outputVals = zip(*outputPitchList)
        mergedDataList.append((outputTime, outputVals))
        
        praat_scripts.resynthesizePitch(praatEXE, fromWavFN, pitchFNFullPath,
                                        outputFN, outputMinPitch,
                                        outputMaxPitch)

    # 4. (Optional) Plot the generated contours
    if doPlotPitchSteps:
        fromTime, fromVals = zip(*fromPitchData)
        toTime, toVals = zip(*toPitchData)

        plot_morphed_data.plotF0((fromTime, fromVals),
                                 (toTime, toVals),
                                 mergedDataList,
                                 join(pitchTierPath,
                                      "%s_%d.png" % (fromName, 1)))
