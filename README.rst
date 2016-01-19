
---------
ProMo (Prosody Morph)
---------

A library for manipulating pitch and duration in an algorithmic way, for
resynthesizing speech.

This library can be used to resynthesize pitch  in natural speech using pitch
contours taken from other speech samples, generated pitch contours,
or through algorithmic manipulations of the source pitch contour.


Common Use Cases
================

What can you do with this library?

Apply the pitch or duration from one speech sample to another.

- pitch alignment happens both in time and in amount

- morphing is granular (10%, 50%, 100%, 150%, etc. of target)

Pitch morphing:

image:: examples/files/mary1_mary2_f0_morph.png

[Pitch morphing](examples/files/mary1_mary2_f0_morph.png)

Duration morphing:

image:: examples/files/mary1_mary2_dur_morph.png

[Duration morphing](examples/files/mary1_mary2_dur_morph.png)

Major revisions
================

Ver 1.0 (January 19, 2016)

- first public release.

Beta (July 1, 2013)

- first version which was utilized in the my dissertation work


Requirements
==============

``Python 2.7.*`` or above

``Python 3.3.*`` or above

My praatIO library is used extensively and can be downloaded 
`here <https://github.com/timmahrt/praatIO>`_


Usage
=========

See /examples for example usages


Installation
================

Navigate to the directory this is located in and type::

    python setup.py install

If python is not in your path, you'll need to enter the full path e.g.::

    C:\Python27\python.exe setup.py install

