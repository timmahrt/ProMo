'''
Created on Sep 18, 2013

@author: timmahrt

Given two lists of tuples of the form [(value, time), (value, time)], morph
can iteratively transform the values in one list to the values in the other
while maintaining the times in the first list.

Both time scales are placed on a relative scale.  This assumes that the times
may be different and the number of samples may be different but the 'events'
occur at the same relative location (half way through, at the end, etc.).

Both dynamic time warping and morph, align two data lists in time.  However,
dynamic time warping does this by analyzing the event structure and aligning
events in the two signals as best it can
(i.e. it changes when events happen in relative time while morph preserves
when events happen in relative time).
'''


class RelativizeSequenceException(Exception):

    def __init__(self, dist):
        super(RelativizeSequenceException, self).__init__()
        self.dist = dist

    def __str__(self):
        return "You need at least two unique values to make " + \
            "a sequence relative. Input: %s" % repr(self.dist)


def makeSequenceRelative(absVSequence):
    '''
    Puts every value in a list on a continuum between 0 and 1

    Also returns the min and max values (to reverse the process)
    '''

    if len(absVSequence) < 2 or len(set(absVSequence)) == 1:
        raise RelativizeSequenceException(absVSequence)

    minV = min(absVSequence)
    maxV = max(absVSequence)
    relativeSeq = [(value - minV) / (maxV - minV) for value in absVSequence]

    return relativeSeq, minV, maxV


def makeSequenceAbsolute(relVSequence, minV, maxV):
    '''
    Makes every value in a sequence absolute
    '''

    return [(value * (maxV - minV)) + minV for value in relVSequence]


def _makeTimingRelative(absoluteDataList):
    '''
    Given normal pitch tier data, puts the times on a scale from 0 to 1

    Input is a list of tuples of the form
    ([(time1, pitch1), (time2, pitch2),...]

    Also returns the start and end time so that the process can be reversed
    '''

    timingSeq = [row[0] for row in absoluteDataList]
    valueSeq = [list(row[1:]) for row in absoluteDataList]

    relTimingSeq, startTime, endTime = makeSequenceRelative(timingSeq)
    
    relDataList = [tuple([time, ] + row) for time, row
                   in zip(relTimingSeq, valueSeq)]

    return relDataList, startTime, endTime


def _makeTimingAbsolute(relativeDataList, startTime, endTime):
    '''
    Maps values from 0 to 1 to the provided start and end time

    Input is a list of tuples of the form
    ([(time1, pitch1), (time2, pitch2),...]
    '''

    timingSeq = [row[0] for row in relativeDataList]
    valueSeq = [list(row[1:]) for row in relativeDataList]
    
    absTimingSeq = makeSequenceAbsolute(timingSeq, startTime, endTime)

    absDataList = [tuple([time, ] + row) for time, row
                   in zip(absTimingSeq, valueSeq)]

    return absDataList


def _getSmallestDifference(inputList, targetVal):
    '''
    Returns the value in inputList that is closest to targetVal
    
    Iteratively splits the dataset in two, so it should be pretty fast
    '''
    targetList = inputList[:]
    retVal = None
    while True:
        # If we're down to one value, stop iterating
        if len(targetList) == 1:
            retVal = targetList[0]
            break
        halfPoint = int(len(targetList) / 2.0) - 1
        a = targetList[halfPoint]
        b = targetList[halfPoint + 1]
        
        leftDiff = abs(targetVal - a)
        rightDiff = abs(targetVal - b)
        
        # If the distance is 0, stop iterating, the targetVal is present
        # in the inputList
        if leftDiff == 0 or rightDiff == 0:
            retVal = targetVal
            break
        
        # Look at left half or right half
        if leftDiff < rightDiff:
            targetList = targetList[:halfPoint + 1]
        else:
            targetList = targetList[halfPoint + 1:]
         
    return retVal
        
    
def _getNearestMappingIndexList(fromValList, toValList):
    '''
    Finds the indicies for data points that are closest to each other.

    The inputs should be in relative time, scaled from 0 to 1
    e.g. if you have [0, .1, .5., .9] and [0, .1, .2, 1]
    will output [0, 1, 1, 2]
    '''

    indexList = []
    for fromTimestamp in fromValList:
        smallestDiff = _getSmallestDifference(toValList, fromTimestamp)
        i = toValList.index(smallestDiff)
        indexList.append(i)

    return indexList


def morphDataLists(fromList, toList, stepList):
    '''
    Iteratively morph fromList into toList using the values 0 to 1 in stepList
    
    stepList: a value of 0 means no change and a value of 1 means a complete
    change to the other value
    '''

    # If there are more than 1 pitch value, then we align the data in
    # relative time.
    # Each data point comes with a timestamp.  The earliest timestamp is 0
    # and the latest timestamp is 1.  Using this method, for each relative
    # timestamp in the source list, we find the closest relative timestamp
    # in the target list.  Just because two pitch values have the same index
    # in the source and target lists does not mean that they correspond to
    # the same speech event.
    fromListRel, fromStartTime, fromEndTime = _makeTimingRelative(fromList)
    toListRel = _makeTimingRelative(toList)[0]

    # If fromList has more points, we'll have flat areas
    # If toList has more points, we'll might miss peaks or valleys
    fromTimeList = [dataTuple[0] for dataTuple in fromListRel]
    toTimeList = [dataTuple[0] for dataTuple in toListRel]
    indexList = _getNearestMappingIndexList(fromTimeList, toTimeList)
    alignedToPitchRel = [toListRel[i] for i in indexList]

    for stepAmount in stepList:
        newPitchList = []

        # Perform the interpolation
        for fromTuple, toTuple in zip(fromListRel, alignedToPitchRel):
            fromTime, fromValue = fromTuple
            toTime, toValue = toTuple

            # i + 1 b/c i_0 = 0 = no change
            newValue = fromValue + (stepAmount * (toValue - fromValue))
            newTime = fromTime + (stepAmount * (toTime - fromTime))

            newPitchList.append((newTime, newValue))

        newPitchList = _makeTimingAbsolute(newPitchList, fromStartTime,
                                           fromEndTime)

        yield stepAmount, newPitchList


def morphChunkedDataLists(fromDataList, toDataList, stepList):
    '''
    Morph one set of data into another, in a stepwise fashion

    A convenience function.  Given a set of paired data lists,
    this will morph each one individually.

    Returns a single list with all data combined together.
    '''

    assert(len(fromDataList) == len(toDataList))

    # Morph the fromDataList into the toDataList
    outputList = []
    for x, y in zip(fromDataList, toDataList):

        # We cannot morph a region if there is no data or only
        # a single data point for either side
        if (len(x) < 2) or (len(y) < 2):
            continue

        tmpList = [outputPitchList for _, outputPitchList
                   in morphDataLists(x, y, stepList)]
        outputList.append(tmpList)

    # Transpose list
    finalOutputList = outputList.pop(0)
    for subList in outputList:
        for i, subsubList in enumerate(subList):
            finalOutputList[i].extend(subsubList)

    return finalOutputList


def morphAveragePitch(fromDataList, toDataList):
    '''
    Adjusts the values in fromPitchList to have the same average as toPitchList
    
    Because other manipulations can alter the average pitch, morphing the pitch
    is the last pitch manipulation that should be done
    
    After the morphing, the code removes any values below zero, thus the
    final average might not match the target average.
    '''
    
    timeList, fromPitchList = zip(*fromDataList)
    toPitchList = [pitchVal for _, pitchVal in toDataList]
    
    # Zero pitch values aren't meaningful, so filter them out if they are
    # in the dataset
    fromListNoZeroes = [val for val in fromPitchList if val > 0]
    fromAverage = sum(fromListNoZeroes) / float(len(fromListNoZeroes))
    
    toListNoZeroes = [val for val in toPitchList if val > 0]
    toAverage = sum(toListNoZeroes) / float(len(toListNoZeroes))
    
    newPitchList = [val - fromAverage + toAverage for val in fromPitchList]
    
#     finalAverage = sum(newPitchList) / float(len(newPitchList))
    
    # Removing zeroes and negative pitch values
    retDataList = [(time, pitchVal) for time, pitchVal
                   in zip(timeList, newPitchList)
                   if pitchVal > 0]
    
    return retDataList


def morphRange(fromDataList, toDataList):
    '''
    Changes the scale of values in one distribution to that of another
    
    ie The maximum value in fromDataList will be set to the maximum value in
    toDataList.  The 75% largest value in fromDataList will be set to the
    75% largest value in toDataList, etc.
    
    Small sample sizes will yield results that are not very meaningful
    '''
    
    # Isolate and sort pitch values
    fromPitchList = [dataTuple[1] for dataTuple in fromDataList]
    toPitchList = [dataTuple[1] for dataTuple in toDataList]
    
    fromPitchListSorted = sorted(fromPitchList)
    toPitchListSorted = sorted(toPitchList)
    
    # Bin pitch values between 0 and 1
    fromListRel = makeSequenceRelative(fromPitchListSorted)[0]
    toListRel = makeSequenceRelative(toPitchListSorted)[0]
    
    # Find each values closest equivalent in the other list
    indexList = _getNearestMappingIndexList(fromListRel, toListRel)
    
    # Map the source pitch to the target pitch value
    # Pitch value -> get sorted position -> get corresponding position in
    # target list -> get corresponding pitch value = the new pitch value
    retList = []
    for time, pitch in fromDataList:
        fromI = fromPitchListSorted.index(pitch)
        toI = indexList[fromI]
        newPitch = toPitchListSorted[toI]
        
        retList.append((time, newPitch))
    
    return retList
