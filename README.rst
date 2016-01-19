
-----------------------
ProMo (Prosody Morph)
-----------------------

A library for manipulating pitch and duration in an algorithmic way, for
resynthesizing speech.

This library can be used to resynthesize pitch in natural speech using pitch
contours taken from other speech samples, generated pitch contours,
or through algorithmic manipulations of the source pitch contour.


Common Use Cases
================

What can you do with this library?

Apply the pitch or duration from one speech sample to another.

- alignment happens both in time and in amount

    - for many applications the temporal quality won't matter, but for 
      situations with stylized pitch, etc. where there are few data points, 
      data points (and thus pitch events) will move in time.

- morphing is granular (10%, 50%, 100%, 150%, etc. of target)

- resynthesis is performed by Praat.

- pitch can be obtained from praat (such as by using praatio)
  or from other sources (e.g. ESPS getF0)

- plots of the resynthesis (such as the ones below) can be generated

Pitch morphing:

    The following image shows morphing of pitch from one speech file to another
    in increments of 30% (33%, 66%, 100%).  Note that the morph adjusts the
    temporal dimension of the target signal to fit the duration of the source
    signal.  This occurs at the level of the file unless the user specifies an
    equal number of segments to align in time (e.g. using word-level or
    phone-level transcriptions)

.. image:: examples/files/mary1_mary2_f0_morph.png
    :width: 650

Duration morphing:

    The following image shows morphing of duration from one speech file to
    another in increments of 30% (33%, 66%, 100%).  Can operate over an
    entire file or, similar to pitch morphing, with annotated segments.

.. image:: examples/files/mary1_mary2_dur_morph.png
    :width: 650

    
Major revisions
================

Ver 1.0 (January 19, 2016)

- first public release.

Beta (July 1, 2013)

- first version which was utilized in my dissertation work


Requirements
==============

``Python 2.7.*`` or above

``Python 3.3.*`` or above

My praatIO library is used extensively and can be downloaded 
`here <https://github.com/timmahrt/praatIO>`_

Matplotlib is needed if you want to plot graphs.
`Matplotlib download <http://matplotlib.org/>`_


Usage
=========

See /examples for example usages


Installation
================

Navigate to the directory this is located in and type::

    python setup.py install

If python is not in your path, you'll need to enter the full path e.g.::

    C:\Python27\python.exe setup.py install
