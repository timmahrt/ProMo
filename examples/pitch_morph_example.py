
import os
from os.path import join

from praatio import pitch_and_intensity

from promo import f0_morph
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

fromTGFN = join(path, os.path.splitext(fromWavFN)[0] + ".TextGrid")
toTGFN = join(path, os.path.splitext(toWavFN)[0] + ".TextGrid")

# Prepare the data for morphing
# 1st load it into memory
fromPitch = pitch_and_intensity.audioToPI(path, fromWavFN, path,
                                          fromPitchFN, praatEXE, minPitch,
                                          maxPitch, forceRegenerate=False)
toPitch = pitch_and_intensity.audioToPI(path, toWavFN, path,
                                        toPitchFN, praatEXE, minPitch,
                                        maxPitch, forceRegenerate=False)

# 2nd remove intensity values
fromPitch = [(time, pitch) for time, pitch, _ in fromPitch]
toPitch = [(time, pitch) for time, pitch, _ in toPitch]

# 3rd select which sections to align.
# We'll use textgrids for this purpose.
tierName = "TokensAlign"
fromPitch = f0_morph.getPitchForIntervals(fromPitch, fromTGFN, tierName)
toPitch = f0_morph.getPitchForIntervals(toPitch, toTGFN, tierName)

# Run the morph process
f0_morph.f0Morph(fromWavFN=join(path, fromWavFN),
                 pitchPath=path,
                 stepList=stepList,
                 outputName="%s_%s_f0_morph" % (fromName, toName),
                 doPlotPitchSteps=True,
                 fromPitchData=fromPitch,
                 toPitchData=toPitch,
                 outputMinPitch=minPitch,
                 outputMaxPitch=maxPitch,
                 praatEXE=praatEXE)

# Or for more control over the steps:
stepList = [0.10, ]  # 10% morph
# Run the morph process
f0_morph.f0Morph(fromWavFN=join(path, fromWavFN),
                 pitchPath=path,
                 stepList=stepList,
                 outputName="%s_%s_f0_morph" % (fromName, toName),
                 doPlotPitchSteps=True,
                 fromPitchData=fromPitch,
                 toPitchData=toPitch,
                 outputMinPitch=minPitch,
                 outputMaxPitch=maxPitch,
                 praatEXE=praatEXE)
