"""


An example of morphing the pitch in one file to that in another
"""
import os
from os.path import join

from praatio import pitch_and_intensity

from promo import f0_morph
from promo.morph_utils import utils

# Define the arguments for the code
root = os.path.abspath(join(".", "files"))
praatEXE = r"C:\Praat.exe"  # Windows path
# praatEXE = "/Applications/Praat.app/Contents/MacOS/Praat"  # Mac path

minPitch = 50
maxPitch = 350
stepList = utils.generateStepList(3)

fromName = "mary1"
toName = "mary2"
fromWavFN = fromName + ".wav"
toWavFN = toName + ".wav"

fromPitchFN = fromName + ".txt"
toPitchFN = toName + ".txt"

fromTGFN = join(root, os.path.splitext(fromWavFN)[0] + ".TextGrid")
toTGFN = join(root, os.path.splitext(toWavFN)[0] + ".TextGrid")

# Prepare the data for morphing
# 1ST load it into memory
fromPitch = pitch_and_intensity.extractPI(
    join(root, fromWavFN),
    join(root, fromPitchFN),
    praatEXE,
    minPitch,
    maxPitch,
    forceRegenerate=False,
)
toPitch = pitch_and_intensity.extractPI(
    join(root, toWavFN),
    join(root, toPitchFN),
    praatEXE,
    minPitch,
    maxPitch,
    forceRegenerate=False,
)

# 2ND remove intensity values
fromPitch = [(time, pitch) for time, pitch, _ in fromPitch]
toPitch = [(time, pitch) for time, pitch, _ in toPitch]

# 3RD select which sections to align.
# We'll use textgrids for this purpose.
tierName = "words"
fromPitch = f0_morph.getPitchForIntervals(fromPitch, fromTGFN, tierName)
toPitch = f0_morph.getPitchForIntervals(toPitch, toTGFN, tierName)

pitchTier = pitch_and_intensity.extractPitchTier(
    join(root, fromWavFN),
    join(root, "mary1.PitchTier"),
    praatEXE,
    minPitch,
    maxPitch,
    forceRegenerate=True,
)
# FINALLY: Run the morph process
f0_morph.f0Morph(
    fromWavFN=join(root, fromWavFN),
    pitchPath=root,
    stepList=stepList,
    outputName="%s_%s_f0_morph" % (fromName, toName),
    doPlotPitchSteps=True,
    fromPitchData=fromPitch,
    toPitchData=toPitch,
    outputMinPitch=minPitch,
    outputMaxPitch=maxPitch,
    praatEXE=praatEXE,
    sourcePitchDataList=pitchTier.pointList,
)

####################
# The remaining examples below demonstrate the use of
# f0_morph.f0Morph() with different arguments.  It may
# be helpful for your work.  However, you can safely comment
# out or delete the code below to keep things simple.
####################


# Or for more control over the steps:
stepList = [
    0.10,
]  # 10% morph
# Run the morph process
f0_morph.f0Morph(
    fromWavFN=join(root, fromWavFN),
    pitchPath=root,
    stepList=stepList,
    outputName="%s_%s_f0_morph" % (fromName, toName),
    doPlotPitchSteps=True,
    fromPitchData=fromPitch,
    toPitchData=toPitch,
    outputMinPitch=minPitch,
    outputMaxPitch=maxPitch,
    praatEXE=praatEXE,
)

# And, as shown in the next four examples,
# we can reset the speaker's pitch range and mean pitch back to their own
stepList = [
    1.0,
]

# Source's mean pitch, target's pitch range
f0_morph.f0Morph(
    fromWavFN=join(root, fromWavFN),
    pitchPath=root,
    stepList=stepList,
    outputName="%s_%s_f0_morph_w_average" % (fromName, toName),
    doPlotPitchSteps=True,
    fromPitchData=fromPitch,
    toPitchData=toPitch,
    outputMinPitch=minPitch,
    outputMaxPitch=maxPitch,
    praatEXE=praatEXE,
    keepPitchRange=False,
    keepAveragePitch=True,
)

# Target's mean pitch, source's pitch range
f0_morph.f0Morph(
    fromWavFN=join(root, fromWavFN),
    pitchPath=root,
    stepList=stepList,
    outputName="%s_%s_f0_morph_w_range" % (fromName, toName),
    doPlotPitchSteps=True,
    fromPitchData=fromPitch,
    toPitchData=toPitch,
    outputMinPitch=minPitch,
    outputMaxPitch=maxPitch,
    praatEXE=praatEXE,
    keepPitchRange=True,
    keepAveragePitch=False,
)

# Source's mean pitch, source's pitch range
outputName = "%s_%s_f0_morph_w_range_and_average" % (fromName, toName)
f0_morph.f0Morph(
    fromWavFN=join(root, fromWavFN),
    pitchPath=root,
    stepList=stepList,
    outputName=outputName,
    doPlotPitchSteps=True,
    fromPitchData=fromPitch,
    toPitchData=toPitch,
    outputMinPitch=minPitch,
    outputMaxPitch=maxPitch,
    praatEXE=praatEXE,
    keepPitchRange=True,
    keepAveragePitch=True,
)

# Target's mean pitch, target's pitch range (default behavior)
f0_morph.f0Morph(
    fromWavFN=join(root, fromWavFN),
    pitchPath=root,
    stepList=stepList,
    outputName="%s_%s_f0_morph_w_regular" % (fromName, toName),
    doPlotPitchSteps=True,
    fromPitchData=fromPitch,
    toPitchData=toPitch,
    outputMinPitch=minPitch,
    outputMaxPitch=maxPitch,
    praatEXE=praatEXE,
    keepPitchRange=False,
    keepAveragePitch=False,
)
