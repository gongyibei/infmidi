INFMIDI
=======

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License: MIT

.. image:: https://img.shields.io/badge/pypi-0.1.1-blue
    :target: https://pypi.org/project/infmidi/0.1.1

.. image:: https://readthedocs.org/projects/infmidi/badge/?version=latest
    :target: https://infmidi.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


INFMIDI is a MIDI editing library written in Python，with a lot of advanced syntax to help you quickly edit and generate MIDI files. You can also use it to assist in arranging and composing music with code.


.. image:: https://raw.githubusercontent.com/gongyibei/infmidi/master/assets/example.gif


Documentation
-------------
`English <https://infmidi.readthedocs.io/en/latest/>`_  | `中文文档 <https://infmidi.readthedocs.io/zh/latest/>`_ .

- `🔌 Installation <https://infmidi.readthedocs.io/en/latest/start/install.html>`_ - Here are the detailed installation instructions (``pip install infmidi``).
- `🚀 Quick start <https://infmidi.readthedocs.io/en/latest/start/quickstart.html>`_ - Here are a few examples to get you started quickly.
- `🎹 Fundation <https://infmidi.readthedocs.io/en/latest/start/core/index.html>`_ - Introduction to core objects (``Event``, ``Note``, ``Clip``, ``Track`` and ``Midi``).
- `🎸 Generator <https://infmidi.readthedocs.io/en/latest/start/generator/index.html>`_ - Functions to generate ``Clip`` object quickly.
- `🎨 Effects <https://infmidi.readthedocs.io/en/latest/start/effects/index.html>`_ - Functions to process ``Clip`` object.
- `📻 Devices <https://infmidi.readthedocs.io/en/latest/start/devices/index.html>`_ -  Objects to play MIDI and to interact with DAWs.
- `🎼 Examples <https://infmidi.readthedocs.io/en/latest/start/examples/index.html>`_  - Examples to learn INFMIDI.
- `📑 Cheat sheet <https://infmidi.readthedocs.io/en/latest/start/cheat.html>`_ - Cheat sheets of core obejcts, music theory and MIDI protocol.


Features
--------

- **Absolute time** - Esaily insert note and event at any time point.

.. code:: python
    
    # Add C4 on beat 8.
    clip += Note('C4', location=8)


- **Time slicing** - Modify notes for a specific time period.

.. code:: python
    
    # Raise notes from beats 8 to 16 by 4 semitones.
    clip[8:16] += 4

- **Generator** - Functions to generate music clip quickly.

.. code:: python

    # Generate chord progression with sheet.
    progression = sheet('C4:M7 A4:m9 | F4:M7 G4:7')

- **Effects** - Functions to process MIDI.

.. code:: python

    # Add delay effect to clip.
    delay(clip, n=3, length=0.5, decay=0.9)

Related projects
----------------

- `mido <https://github.com/mido/mido>`_ - A library for working with MIDI messages and ports. (INFMIDI is based on mido)
- `music21 <https://github.com/cuthbertLab/music21>`_ - A Toolkit for Computational Musicology.
- `pretty-midi <https://github.com/craffel/pretty-midi>`_ - Utility functions for handling MIDI data in a nice/intuitive way.
- `musicpy <https://github.com/Rainbow-Dreamer/musicpy>`_ - A music programming language in Python designed to write music in very handy syntax through music theory and algorithms.
- `muspy <https://github.com/salu133445/muspy>`_ - A toolkit for symbolic music generation.


Licence
-------
MIT License © 2022 `gongyibei <https://github.com/gongyibei/>`_.
