
-----------------------
ProMo (Prosody Morph)
-----------------------

.. image:: https://img.shields.io/badge/license-MIT-blue.svg?
   :target: http://opensource.org/licenses/MIT
   
A library for manipulating pitch and duration in an algorithmic way, for
resynthesizing speech.

This library can be used to resynthesize pitch in natural speech using pitch
contours taken from other speech samples, generated pitch contours,
or through algorithmic manipulations of the source pitch contour.

.. sectnum::
.. contents::

Common Use Cases
================

What can you do with this library?

Apply the pitch or duration from one speech sample to another.

- alignment happens both in time and in hertz

    - after the morph process, the source pitch points will be at the same
      absolute pitch and relative time as they are in the target file 
      
    - time is relative to the start and stop time of the interval being
      considered (e.g. the pitch value at 80% of the duration of the interval).
      Relative time is used so that the source and target files don't have to
      be the same length.

    - temporal morphing is a minor effect if the sampling frequency is high
      but it can be significant when, for example, using a stylized pitch
      contour with few pitch samples.

- modifications can be done between entire wav files or between
  corresponding intervals as specified in a textgrid or other annotation
  (indicating the boundaries of words, stressed vowels, etc.)

    - the larger the file, the less useful the results are likely to be
      without using a transcript of some sort
      
    - the transcripts do not have to match in lexical content, only in the
      number of intervals  (same number of words or phones, etc.)

- modifications can be scaled (it is possible to generate a wav file with
  a pitch contour that is 30% or 60% between the source and target contours).

- resynthesis is performed by Praat.

- pitch can be obtained from praat (such as by using praatio)
  or from other sources (e.g. ESPS getF0)

- plots of the resynthesis (such as the ones below) can be generated


Illustrative example
======================

Consider the phrase "Mary rolled the barrel".  In the first recording
(examples/mary1.wav), "Mary rolled the barrel" was said in response
to a question such as "Did John roll the barrel?".  On the other hand,
in the second recording (examples/mary2.wav) the utterance was said 
in response to a question such as "What happened yesterday".

"Mary" in "mary1.wav" is produced with more emphasis than in "mary2.wav".
It is longer and carries a more drammatic pitch excursion.  Using 
ProMo, we can make mary1.wav spoken similar to mary2.wav, even
though they were spoken in a different way and by different speakers.

Duration and pitch carry meaning.  Change these, and you can change the
meaning being conveyed.

``Note that modifying pitch and duration too much can introduce artifacts. 
Such artifacts can be heard even in pitch morphing mary1.wav to mary2.wav.``

Pitch morphing (examples/pitch_morph_example.py):

    The following image shows morphing of pitch from mary1.wav to mary2.wav
    on a word-by-word level
    in increments of 33% (33%, 66%, 100%).  Note that the morph adjusts the
    temporal dimension of the target signal to fit the duration of the source
    signal (the source and generated contours are equally shorter 
    than the target contour).  This occurs at the level of the file unless
    the user specifies an equal number of segments to align in time
    (e.g. using word-level transcriptions, as done here, or phone-level
    transcriptions, etc.)

.. image:: examples/files/mary1_mary2_f0_morph.png
   :width: 500px

Duration morphing (examples/duration_manipulation_example.py):

    The following image shows morphing of duration from mary1.wav to mary2.wav
    on a word-by-word basis in increments of 33% (33%, 66%, 100%).
    This process can operate over an entire file or, similar to pitch morphing,
    with annotated segments, as done in this example.

.. image:: examples/files/mary1_mary2_dur_morph.png
   :width: 500px

    
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

If you on Windows, you can use the installer found here (check that it is up to date though)
`Windows installer <http://www.timmahrt.com/python_installers>`_

Otherwise, to manually install, after downloading the source from github, from a command-line shell, navigate to the directory containing setup.py and type::

    python setup.py install

If python is not in your path, you'll need to enter the full path e.g.::

    C:\Python27\python.exe setup.py install


Citing ProMo
===============

If you use ProMo in your research, please cite it like so:

Tim Mahrt. ProMo: The Prosody-Morphing Library.
https://github.com/timmahrt/ProMo, 2016.


Acknowledgements
================

Development of ProMo was possible thanks to NSF grant **BCS 12-51343** to
Jennifer Cole, José I. Hualde, and Caroline Smith and to the A*MIDEX project
(n° **ANR-11-IDEX-0001-02**) to James Sneed German funded by the
Investissements d’Avenir French Government program,
managed by the French National Research Agency (ANR).
