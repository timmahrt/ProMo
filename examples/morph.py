
import os
from os.path import join

from praatio import pitch_and_intensity

from promo import f0_morph
from promo import duration_morph

# Define the arguments for the code
path = r"C:\Users\Tim\Dropbox\workspace\prosodyMorph\examples\files"
praatEXE = r"C:\Praat.exe"
minPitch = 50
maxPitch = 350
numSteps = 3

fromName = "mary1"
toName = "mary2"
fromFN = fromName + ".wav"
toFN = toName + ".wav"

fromPitchFN = fromName + ".txt"
toPitchFN = toName + ".txt"

fromTGFN = join(path, os.path.splitext(fromFN)[0] + ".TextGrid")
toTGFN = join(path, os.path.splitext(toFN)[0] + ".TextGrid")

# Prepare the data for morphing
# 1st load it into memory
fromPitch = pitch_and_intensity.audioToPI(path, fromFN, path,
                                          fromPitchFN, praatEXE, minPitch,
                                          maxPitch, forceRegenerate=False)
toPitch = pitch_and_intensity.audioToPI(path, toFN, path,
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
f0_morph.f0Morph(fromWavFN=join(path, fromFN),
                 fromPitchFN=join(path, fromPitchFN),
                 toPitchFN=join(path, toPitchFN),
                 numSteps=numSteps,
                 outputName="%s_%s" % (fromName, toName),
                 doPlotPitchSteps=True,
                 fromPitchData=fromPitch,
                 toPitchData=toPitch,
                 outputMinPitch=minPitch,
                 outputMaxPitch=maxPitch,
                 praatEXE=praatEXE)

# duration_morph.durationMorph(join(path, fromFN),
#                              join(path, toFN),
#                              path,
#                              numSteps,
#                              tierName,
#                              plotFlag=True,
#                              outputMinPitch=minPitch,
#                              outputMaxPitch=maxPitch,
#                              praatEXE=praatEXE)
