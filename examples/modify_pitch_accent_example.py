"""
Created on Jan 26, 2017

This file contains two examples demonstrating the use
of the module modify_pitch_accent

@author: Tim
"""

import os
from os.path import join

from praatio import textgrid
from praatio import data_points
from praatio import audio
from praatio import pitch_and_intensity
from praatio import praat_scripts
from praatio import praatio_scripts
from praatio.utilities import constants

from promo.morph_utils import modify_pitch_accent


def toStr(inputNum):
    if inputNum < 0:
        retStr = "%02d" % inputNum
    else:
        retStr = "+%02d" % inputNum

    return retStr


root = os.path.abspath(join(".", "files"))
rootOutputPath = join(root, "modify_pitch_accent")
praatEXE = r"C:\Praat.exe"  # Windows path


####################################
# 1st example - a simple example
# Create more emphasis on the subject
####################################

tgFN = "mary1.TextGrid"
wavFN = "mary1.wav"
pitchIntensityFN = "mary1.txt"
originalPitchFN = "mary1.pitch"
outputWavFN = "mary1_accented.wav"
outputPitchFN = "mary1_accented.pitch"
minPitch = 75
maxPitch = 450

if not os.path.exists(rootOutputPath):
    os.mkdir(rootOutputPath)

# 1st - get pitch
piList = pitch_and_intensity.extractPI(
    join(root, wavFN),
    join(rootOutputPath, pitchIntensityFN),
    praatEXE,
    minPitch,
    maxPitch,
)
pitchList = [(timeV, pitchV) for timeV, pitchV, _ in piList]

dur = audio.WavQueryObj(join(root, wavFN)).getDuration()
pointObj = data_points.PointObject2D(pitchList, constants.DataPointTypes.PITCH, 0, dur)
pointObj.save(join(rootOutputPath, originalPitchFN))


# 2nd - get region to manipulate.  Let's make the subject more emphatic!
tg = textgrid.openTextgrid(join(root, "mary1.TextGrid"), includeEmptyIntervals=False)
tier = tg.tierDict["words"]
start, stop, _ = tier.entryList[0]  # Getting info for the first word

targetPitchList = [
    (timeV, pitchV) for timeV, pitchV in pitchList if timeV >= start and timeV <= stop
]

# 3rd - make manipulation
accent = modify_pitch_accent.PitchAccent(targetPitchList)
accent.addPlateau(0.05)  # Peak is dragged out for 0.05 seconds
accent.adjustPeakHeight(60)  # Plateau is raised by 60 hz
accent.shiftAccent(-0.03)  # Recenter the plateau around the original peak

# 4th - integrate results
moddedPitchList = accent.reintegrate(pitchList)

# 5th - resynthesize
praat_scripts.resynthesizePitch(
    praatEXE,
    join(root, wavFN),
    join(rootOutputPath, outputPitchFN),
    join(rootOutputPath, outputWavFN),
    minPitch,
    maxPitch,
    pointList=moddedPitchList,
)


####################################
# 2nd example - a more complicated example
# Incrementally create more (or less) emphasis on the subject
# with a 3 by 3 by 3 matrix of different changes
####################################

# 1st and 2nd -- already done above

# 3rd - make manipulation

outputFN = join(rootOutputPath, os.path.splitext(outputWavFN)[0] + "_s%s_h%s_p%s")

for plateauAmount in [0.0, 0.04, 0.08]:
    for heightAmount in [0, 40, 80]:
        for shiftAmount in [0.0, 0.04, 0.08]:

            accent = modify_pitch_accent.PitchAccent(targetPitchList)
            accent.addPlateau(plateauAmount)
            accent.adjustPeakHeight(heightAmount)
            accent.shiftAccent(shiftAmount)

            # 4th - integrate results
            moddedPitchList = accent.reintegrate(pitchList)

            # 5th - resynthesize the wav file
            outputName = outputFN % (
                toStr(shiftAmount * 1000),
                toStr(heightAmount),
                toStr(plateauAmount * 1000),
            )
            wavOutputFN = outputName + ".wav"
            pitchOutputFN = outputName + ".pitch"
            praat_scripts.resynthesizePitch(
                praatEXE,
                join(root, wavFN),
                pitchOutputFN,
                wavOutputFN,
                minPitch,
                maxPitch,
                pointList=moddedPitchList,
            )
