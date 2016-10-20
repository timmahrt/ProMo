'''
Created on Oct 20, 2016

@author: tmahrt

Runs integration tests

The examples were all written as scripts.  They weren't meant to be 
imported or run from other code.  So here, the integration test is just
importing the scripts, which causes them to execute.  If the code completes
with no errors, then the code is at least able to complete.

Testing whether or not the code actually did what it is supposed to is
another issue and will require some refactoring.

prosody morph requires praat to do the final manipulation.  For the
integration tests run without access to praat, that last step
will be skipped (and unverified) however the test will still pass.
'''

import unittest
import os
from os.path import join
import sys

from praatio.utilities import utils
from promo import duration_morph
from promo.morph_utils import utils as morph_utils

cwd = os.path.dirname(os.path.realpath(__file__))
_root = os.path.split(cwd)[0]
sys.path.append(_root)


class IntegrationTests(unittest.TestCase):
    """Integration tests"""


    def test_add_tiers(self):
        """Running 'duration_manipulation_example.py'"""
        print("\nduration_manipulation_example.py" + "\n" + "-" * 10)
        try:
            import duration_manipulation_example
        except utils.FileNotFound:
            pass

    def test_calculate_duration(self):
        """Running 'pitch_morph_example.py'"""
        print("\npitch_morph_example.py" + "\n" + "-" * 10)
        try:
            import pitch_morph_example
        except utils.FileNotFound:
            pass

    def test_delete_vowels(self):
        """Running 'pitch_morph_to_pitch_contour.py'"""
        print("\npitch_morph_to_pitch_contour.py" + "\n" + "-" * 10)
        try:
            import pitch_morph_to_pitch_contour
        except utils.FileNotFound:
            pass

    def test_getMorphParameters(self):
        filterFunc = None
        includeUnlabeledRegions = False
        duration_morph.getMorphParameters(self.fromTGFN,
                                          self.toTGFN,
                                          self.tierName,
                                          filterFunc,
                                          includeUnlabeledRegions)

    def test_getManipulatedParameters(self):
        twentyPercentMore = lambda x: (x * 1.20)
        filterFunc = None
        includeUnlabeledRegions = True
        duration_morph.getManipulatedParamaters(self.fromTGFN,
                                                self.tierName,
                                                twentyPercentMore,
                                                filterFunc,
                                                includeUnlabeledRegions)

    def test_changeDuration(self):
        filterFunc = None
        includeUnlabeledRegions = False
        durationParams = duration_morph.getMorphParameters(self.fromTGFN,
                                                           self.toTGFN,
                                                           self.tierName,
                                                           filterFunc,
                                                           includeUnlabeledRegions)

        stepList = morph_utils.generateStepList(3)
        outputName = "mary1_dur_morph"
        # praatEXE = r"C:\Praat.exe"  # Windows
        praatEXE = "/Applications/Praat.app/Contents/MacOS/Praat"  # Mac
        try:
            duration_morph.changeDuration(self.fromWavFN,
                                          durationParams,
                                          stepList,
                                          outputName,
                                          outputMinPitch=self.minPitch,
                                          outputMaxPitch=self.maxPitch,
                                          praatEXE=praatEXE)
        except utils.FileNotFound:
            pass
        
    def test_textgridMorphDuration(self):
        duration_morph.textgridMorphDuration(self.fromTGFN, self.toTGFN)

    def test_textgridManipulateDuration(self):
        filterFunc = None
        includeUnlabeledRegions = False
        durationParams = duration_morph.getMorphParameters(self.fromTGFN,
                                                           self.toTGFN,
                                                           self.tierName,
                                                           filterFunc,
                                                           includeUnlabeledRegions)
        
        duration_morph.outputMorphTextgrids(self.fromTGFN,
                                            durationParams,
                                            [1, ],
                                            join(self.root,
                                                 "outputName.TextGrid"))

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.root = join(".", "files")
        
        self.fromWavFN = join(self.root, "mary1.wav")
        self.fromTGFN = join(self.root, "mary1.TextGrid")
        self.toTGFN = join(self.root, "mary2.TextGrid")
        self.tierName = "PhonAlign"
        self.minPitch = 50
        self.maxPitch = 350
        
        root = os.path.join(_root, "files")
        self.oldRoot = os.getcwd()
        os.chdir(_root)
        self.startingList = os.listdir(root)
        self.startingDir = os.getcwd()

    def tearDown(self):
        '''Remove any files generated during the test'''
        #unittest.TestCase.tearDown(self)
        
        root = os.path.join(".", "files")
        endingList = os.listdir(root)
        endingDir = os.getcwd()
        rmList = [fn for fn in endingList if fn not in self.startingList]
        
        if self.oldRoot == root:
            for fn in rmList:
                fnFullPath = os.path.join(root, fn)
                if os.path.isdir(fnFullPath):
                    os.rmdir(fnFullPath)
                else:
                    os.remove(fnFullPath)
        
        os.chdir(self.oldRoot)


if __name__ == '__main__':
    unittest.main()
