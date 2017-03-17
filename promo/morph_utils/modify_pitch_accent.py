'''
Created on Jan 26, 2017

This convenience code that makes it easy to manipulate
characteristics of a pitch accent.  It is flexible in how
it is used (on a stylized pitch contour or raw values and
as a single step or in a piecewise manner).

See examples/modify_pitch_accent_example.py for example usage.

NOTE: By pitch accent, I mean a single hill or peak, surrounded
by less intense values to the left and right.  Some of the
functions make reference to the max value in the dataset, so if you
have multiple peaks or a downward slope, etc. you may get strange
results.

@author: Tim
'''
import copy
    
    
def _deletePoints(f0List, start, end):
    return [(timeV, f0V) for timeV, f0V in f0List
            if timeV < start or timeV > end]


class PitchAccent(object):
    
    def __init__(self, pointList):
        
        self.pointList = copy.deepcopy(pointList)
        
        self.netLeftShift = 0
        self.netRightShift = 0
        
        pitchList = [f0V for _, f0V in self.pointList]
        minV = min(pitchList)
        maxV = max(pitchList)
        
        self.peakI = pitchList.index(maxV)
    
        timeList = [timeV for timeV, _ in self.pointList]
        self.minT = min(timeList)
        self.maxT = max(timeList)
    
    
    def adjustPeakHeight(self, heightAmount):
        '''
        Adjust peak height
        
        The foot of the accent is left unchanged and intermediate
        values are linearly scaled
        '''
        if heightAmount == 0:
            return
        
        pitchList = [f0V for _, f0V in self.pointList]
        minV = min(pitchList)
        maxV = max(pitchList)
        scale = lambda x, y: x + y * (x - minV) / float(maxV - minV)
        
        self.pointList = [(timeV, scale(f0V, heightAmount))
                          for timeV, f0V in self.pointList]
    
    def addPlateau(self, plateauAmount, pitchSampFreq=None):
        '''
        Add a plateau
        
        A negative plateauAmount will move the peak backwards.
        A positive plateauAmount will move the peak forwards.
        
        All points on the side of the peak growth will also get moved.
        i.e. the slope of the peak does not change.  The accent gets
        wider instead.
        
        If pitchSampFreq=None, the plateau will only be specified by
        the start and end points of the plateau
        '''
        if plateauAmount == 0:
            return
        
        maxPoint = self.pointList[self.peakI]
        
        # Define the plateau
        if pitchSampFreq is not None:
            numSteps = abs(int(plateauAmount / pitchSampFreq))
            timeChangeList = [stepV * pitchSampFreq
                              for stepV in
                              range(0, numSteps + 1)]
        else:
            timeChangeList = [plateauAmount, ]
            
        # Shift the side being pushed by the plateau
        if plateauAmount < 0:  # Plateau moves left of the peak
            leftSide = self.pointList[:self.peakI]
            rightSide = self.pointList[self.peakI:]
            
            plateauPoints = [(maxPoint[0] + timeChange, maxPoint[1])
                             for timeChange in timeChangeList]
            leftSide = [(timeV + plateauAmount, f0V)
                        for timeV, f0V in leftSide]
            self.netLeftShift += plateauAmount
            
        elif plateauAmount > 0:  # Plateau moves right of the peak
            leftSide = self.pointList[:self.peakI + 1]
            rightSide = self.pointList[self.peakI + 1:]
            
            plateauPoints = [(maxPoint[0] + timeChange, maxPoint[1])
                             for timeChange in timeChangeList]
            rightSide = [(timeV + plateauAmount, f0V)
                         for timeV, f0V in rightSide]
            self.netRightShift += plateauAmount
        
        self.pointList = leftSide + plateauPoints + rightSide
                   
    def shiftAccent(self, shiftAmount):
        '''
        Move the whole accent earlier or later
        '''
        if shiftAmount == 0:
            return
        
        self.pointList = [(time + shiftAmount, pitch)
                          for time, pitch in self.pointList]
        
        # Update shift amounts
        if shiftAmount < 0:
            self.netLeftShift += shiftAmount
        elif shiftAmount >= 0:
            self.netRightShift += shiftAmount
    
    def deleteOverlapping(self, targetList):
        '''
        Erase points from another list that overlap with points in this list
        '''
        start = self.pointList[0][0]
        stop = self.pointList[-1][0]
        
        if self.netLeftShift < 0:
            start += self.netLeftShift
            
        if self.netRightShift > 0:
            stop += self.netRightShift
            
        targetList = _deletePoints(targetList, start, stop)
        
        return targetList
    
    def reintegrate(self, fullPointList):
        '''
        Integrates the pitch values of the accent into a larger pitch contour
        '''
        # Erase the original region of the accent
        fullPointList = _deletePoints(fullPointList, self.minT, self.maxT)
        
        # Erase the new region of the accent
        fullPointList = self.deleteOverlapping(fullPointList)
        
        # Add the accent into the full pitch list
        outputPointList = fullPointList + self.pointList
        outputPointList.sort()
        
        return outputPointList
