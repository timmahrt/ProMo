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
import sys

from praatio.utilities import utils

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
    
    def setUp(self):
        unittest.TestCase.setUp(self)

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
