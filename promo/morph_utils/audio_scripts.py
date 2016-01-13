'''
Created on Aug 23, 2014

@author: tmahrt
'''

import wave


def getSoundFileDuration(fn):
    '''
    Returns the duration of a wav file (in seconds)
    '''
    audiofile = wave.open(fn, "r")
    
    params = audiofile.getparams()
    framerate = params[2]
    nframes = params[3]
    
    duration = float(nframes) / framerate
    return duration
