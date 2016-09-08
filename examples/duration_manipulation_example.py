'''
Created on Jan 18, 2016

@author: Tim
'''

import os
from os.path import join

from promo import duration_morph
from promo.morph_utils import utils

# Define the arguments for the code
# Windows paths
path = r"C:\Users\Tim\Dropbox\workspace\prosodyMorph\examples\files"
praatEXE = r"C:\Praat.exe"

# Mac paths
path = "/Users/tmahrt/Dropbox/workspace/prosodyMorph/examples/files"
praatEXE = "/Applications/Praat.app/Contents/MacOS/Praat"

minPitch = 50
maxPitch = 350
stepList = utils.generateStepList(3)

fromName = "mary1"
toName = "mary2"
fromWavFN = fromName + ".wav"
toWavFN = toName + ".wav"

fromPitchFN = fromName + ".txt"
toPitchFN = toName + ".txt"

tierName = "TokensAlign"

fromTGFN = join(path, os.path.splitext(fromWavFN)[0] + ".TextGrid")
toTGFN = join(path, os.path.splitext(toWavFN)[0] + ".TextGrid")

outputPath = join(path, "duration_morph")
outputName = "%s_%s_dur_morph" % (fromName, toName)
outputTG = join(outputPath, "%s.TextGrid" % outputName)
outputImageFN = join(outputPath, "%s.png" % outputName)
filterFunc = None
includeUnlabeledRegions = False

# Morph the duration from one file to another
durationParams = duration_morph.getMorphParameters(join(path, fromTGFN),
                                                   join(path, toTGFN),
                                                   tierName,
                                                   filterFunc,
                                                   includeUnlabeledRegions)
duration_morph.changeDuration(join(path, fromWavFN),
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
durationParams = duration_morph.getManipulatedParamaters(join(path, fromTGFN),
                                                         tierName,
                                                         twentyPercentMore,
                                                         filterFunc,
                                                         includeUnlabeledRegions)

duration_morph.changeDuration(join(path, fromWavFN),
                              durationParams,
                              stepList,
                              outputName,
                              outputMinPitch=minPitch,
                              outputMaxPitch=maxPitch,
                              praatEXE=praatEXE)
