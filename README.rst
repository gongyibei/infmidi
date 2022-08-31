INFMIDI
=======
Manipulate midi and create music with a simple and high level interface.

Installation
------------

If you only need basic features, such as reading, editing, processing and saving midi files. 

::

    pip install infmidi

If you need extra features, such as playing, ploting and interacting. 

::

    pip install "infmidi[all]"

Overview
--------

Basic
^^^^^

- ``Event``: MIDI events.
- ``Note``: A warpper of "note_off" and "note_on" ``Event``.
- ``Clip``: A container of ``Note`` and ``Event``, with rich high-level operations.
- ``Track``: Inherited from ``Clip``, with additional properties (such as name, instrument and mute, etc.).
- ``Midi``: Help you to organize your song with multiple ``Track``.

Extras
^^^^^^

- ``generator``: Functions to generate Clip object quickly.
- ``effects``: Functions to process Clip object.
- ``devices``: Objects to play Midi object and to interact with DAWs.
- ``utils``: Other usefull functions, such as plot Midi object.

Examples
--------

Basic
^^^^^

Create ``Note`` object.

.. code-block:: python
    
    Note('A4') # Note(name="A4", value=69, freq=440.00, location=0.00, length=1.00, velocity=127, channel=0)

    # Different way to initialize.
    Note('A4') == Note(69) == Note(440.) # True

    # Raise the note by 8 semitones.
    Note('A4') + 8

    # Delay the note 8 beats.
    Note('A4') >> 8


Create and  manipulate ``Clip``  object

.. code-block:: python

    from infmidi import Note, clip, clip

    clip = Clip()

    # Add notes to clip.
    for i in range(127):
        # `+=` is an alias of clip.add()
        clip += Note(i, velocity=i, locationa=i)

    # Get a copy of the first 8 beats.
    new = clip[:8]

    # Concat the clip with a new
    clip |= new

    # Raise the first 8 beats notes by 8 semitones.
    clip[:8] += 10

    # Delay the first 8 beats notes and events 16 beats.
    clip[:8] >>= 16

    # Clear the notes and events for the first 8 beats.
    clip[:8] = None 

    # Repeate the clip 4 times.
    clip **= 4

    # More operations
    ..


Write your own song.

.. code-block:: python

    from infmidi import Midi
    song = song = Midi(name='My song', bpm=123, time_signature='4/4')

    track1 = song.new_track(name='Melody track', instrument='Acoustic Guitar(steel)')

    # Create some clips and add to track
    ..

    track2 = song.new_track(name='Chord track', instrument='Acoustic Grand Piano')

    # Create some clips and add to track
    ..

    track3 = song.new_track(name='Drum track', is_drum=True)

    # Create some clips and add to track
    ..



Read and save midi file.

.. code-block:: python

    from infmidi import Midi
    mid = Midi.read('/path/to/xxx.mid')

    # do some changes
    ...

    mid.save('/path/to/xxx.mid')


Generator
^^^^^^^^^

Generate chord ``clip`` with ``chord()``.

.. code-block:: python 

    from infmidi.generate import sheet
    
    # Using full name to create chord clip.
    Cm7 = chord('C4:m7')

    # Using root name and chord type to create chord clip.
    CM7 = chord('C4', 'M7')

    # Using intervals to create chord clip.
    C7 = chord('C4', [4, 3, 3])

    # Using degrees to create chord clip.
    CmM7 = chord('C4', ['1', 'b3', '5', '7'])
    


Generate progression ``clip`` with ``sheet()``

.. code-block:: python 

    from infmidi.generator import sheet
    from infmidi.utils import plot

    txt = '''
        A4:m7 | D4:m9   | G4:7 | C4:M7     |
        F4:M7 | B3:m7-5 | E4:7 | A4:m7 A4:7
    '''

    progression = sheet(txt)
    plot(progression)

.. image:: https://github.com/gongyibei/infmidi/blob/master/assets/readme/sheet1.png

Generate drum ``clip`` with ``sheet()``

.. code-block:: python 

    # Inspired by lisp language :), elements in bars and parentheses divide the current length equally.
    HitHat = sheet('0 H 0 H | 0 H 0 (H H H) | 0 H 0 H | (0 H) (H H H)', length_per_bar=2)
    Snare  = sheet('0 0 S 0 | 0 0 S 0       | 0 0 S 0 |  0    (S 0)  ', length_per_bar=2)
    Kick   = sheet('K       | K K 0 0       | K       | (K K)  0     ', length_per_bar=2)

    # Mix drum clips.
    drum = Kick + Snare + HitHat

    plot(drum ** 2)



.. image:: https://github.com/gongyibei/infmidi/blob/master/assets/readme/sheet2.png

More generator functions comming soon ...

Effects
^^^^^^^

.. code-block:: python

    from infmidi import Midi
    from infmidi.effects import scale_map

    filename = '/path/to/xxx.mid'
    mid = Midi.read(filename)
    for track in mid.tracks:
        if track.is_drum:
            continue
        scale_map(track, key='C', scale='宫', inplace=True)

More effect functions comming soon ...

Devices
^^^^^^^

.. code-block:: python

    from infmidi.devices import FluidSynth
    synth = FluidSynth('/path/to/xxx.sf2')

    # to generate your item (Note, Clip, Track or Midi).
    ...

    synth(item)

More devices comming soon ...

Utils
^^^^^

.. code-block:: python

    from infmidi.utils import plot

    # to generate your item (Note, Clip, Track or Midi).
    ...

    plot(item)


Licence
-------
INFMIDI is released under the terms of the `MIT license
<http://en.wikipedia.org/wiki/MIT_License>`_.
