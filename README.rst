INFMIDI
=======

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License: MIT

.. image:: https://img.shields.io/badge/pypi-0.1.0-blue
    :target: https://pypi.org/project/infmidi/0.1.0

.. image:: https://readthedocs.org/projects/infmidi/badge/?version=latest
    :target: https://infmidi.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


INFMIDI is a MIDI editing library written in Python，with a lot of advanced syntax to help you quickly edit and generate MIDI files. You can also use it to assist in arranging and composing music with code.

Documentation
-------------
`English <https://infmidi.readthedocs.io/en/latest/>`_  | `中文文档 <https://infmidi.readthedocs.io/zh/latest/>`_ .

- `🔌 Install <https://infmidi.readthedocs.io/zh/latest/start/install.html>`_ : Here are the detailed installation instructions. If you only need basic features use ``pip install infmidi`` to install.
- `🚀 Quick start <https://infmidi.readthedocs.io/zh/latest/start/quickstart.html>`_ : Here are a few examples to get you started quickly with websockets.
- `🎹 Fundation <https://infmidi.readthedocs.io/zh/latest/start/core/index>`_: Introduction to core objects (``Event``, ``Note``, ``Clip``, ``Track`` and ``Midi``).
- `🎸 Generator <https://infmidi.readthedocs.io/zh/latest/start/generator/index>`_ : Functions to generate Clip object quickly.
- `🎨 Effects <https://infmidi.readthedocs.io/zh/latest/start/effects/index>`_ : Functions to process Clip object.
- `📻 Devices <https://infmidi.readthedocs.io/zh/latest/start/devices/index>`_ :  Objects to play MIDI and to interact with DAWs.
- `🎼 Examples <https://infmidi.readthedocs.io/zh/latest/start/examples/index>`_ : Examples to learn INFMIDI.
- `📑 Cheat sheet <https://infmidi.readthedocs.io/zh/latest/start/cheat>`_ : Cheat sheets of core obects, music theory and MIDI protocol.


Features
--------

- **Absolute time**: Esaily insert note and event at any time point.

.. code:: python
    
    # add C4 on beat 8
    clip += Note('C4', location=8)


- **Time slicing**: Modify notes for a specific time period

.. code:: python
    
    # Raise notes from beats 8 to 16 by 4 semitones.
    clip[8:16] += 4

- **Generator**: Functions to generate music clip quickly.

.. code:: python

    # Generate chord progression with sheet.
    progression = sheet('C4:M7 A4:m9 | F4:M7 G4:7')

- **Effects**: Functions to process MIDI.

.. code:: python

    # Add delay effect to clip.
    delay(clip, n=3, length=0.5, decay=0.9)


Licence
-------
INFMIDI is released under the terms of the `MIT license
<http://en.wikipedia.org/wiki/MIT_License>`_.
