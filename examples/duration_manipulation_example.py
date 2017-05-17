'''
Created on Jan 18, 2016

@author: Tim
'''

import os
from os.path import join

from promo import duration_morph
from promo.morph_utils import utils

# Define the arguments for the code
root = join('.', "files")
# praatEXE = r"C:\Praat.exe"  # Windows
praatEXE = "/Applications/Praat.app/Contents/MacOS/Praat"  # Mac

minPitch = 50
maxPitch = 350
stepList = utils.generateStepList(3)

fromName = "mary1"
toName = "mary2"
fromWavFN = join(root, fromName + ".wav")
toWavFN = join(root, toName + ".wav")

fromPitchFN = fromName + ".txt"
toPitchFN = toName + ".txt"

tierName = "PhonAlign"

fromTGFN = join(root, fromName + ".TextGrid")
toTGFN = join(root, toName + ".TextGrid")

outputPath = join(root, "duration_morph")
utils.makeDir(outputPath)
outputName = "%s_%s_dur_morph" % (fromName, toName)
outputTG = join(outputPath, "%s.TextGrid" % outputName)
outputImageFN = join(outputPath, "%s.png" % outputName)
filterFunc = None
includeUnlabeledRegions = False

# Morph the duration from one file to another
durationParams = duration_morph.getMorphParameters(fromTGFN,
                                                   toTGFN,
                                                   tierName,
                                                   filterFunc,
                                                   includeUnlabeledRegions)
morphedTG = duration_morph.textgridMorphDuration(fromTGFN, toTGFN)
morphedTG.save(outputTG)
duration_morph.changeDuration(fromWavFN,
                              durationParams,
                              stepList,
                              outputName,
                              outputMinPitch=minPitch,
                              outputMaxPitch=maxPitch,
                              praatEXE=praatEXE)

# Increase duration of all segments by 20 percent
twentyPercentMore = lambda x: (x * 1.20)
outputName = "%s_20_percent_more" % fromName
outputTG = join(outputPath, "%s.TextGrid" % outputName)
outputImageFN = join(outputPath, "%s.png" % outputName)
filterFunc = None
includeUnlabeledRegions = True
durationParams = duration_morph.getManipulatedParamaters(fromTGFN,
                                                         tierName,
                                                         twentyPercentMore,
                                                         filterFunc,
                                                         includeUnlabeledRegions)

duration_morph.changeDuration(fromWavFN,
                              durationParams,
                              stepList,
                              outputName,
                              outputMinPitch=minPitch,
                              outputMaxPitch=maxPitch,
                              praatEXE=praatEXE)
