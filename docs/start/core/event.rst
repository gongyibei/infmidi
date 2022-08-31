Event
=====


Channel events
--------------

NoteOff
^^^^^^^

You should want to use :doc:`Note <./note>` to add ``NoteOff`` and ``NoteOn`` event.

    >>> from infmidi import NoteOff
    >>> NoteOff('A4')
    NoteOff(name="A4", value=69, frequency=440.00, velocity=127, location=0.00, channel=0)


NoteOn
^^^^^^

You should want to use :doc:`Note <./note>` to add ``NoteOff`` and ``NoteOn`` event.

    >>> from infmidi import NoteOn
    >>> NoteOn('A4')
    NoteOn(name="A4", value=69, frequency=440.00, velocity=127, location=0.00, channel=0)


NotePressure
^^^^^^^^^^^^
    
Using ``clip.add()`` to add ``NotePressure``.

    >>> from infmidi import NotePressure
    >>> NotePressure('A4')
    NotePressure(name="A4", value=69, frequency=440.00, pressure=127, location=0.00, channel=0)


.. todo:: 

    Include this event in :doc:`Note <./note>`.




ControlChange
^^^^^^^^^^^^^

Using ``clip.add()`` to add ``NotePressure``.

    >>> from infmidi import ControlChange as CC
    >>> CC(0, 66)
    >>> ControlChange(control=0, value=66, description="Bank Select", location=0.00, channel=0)

.. hint:: 

    See :doc:`cheat/CC <../cheat>` to check the full list of control types.


ProgramChange
^^^^^^^^^^^^^

Using ``clip.add()`` to add ``ProgramChange``.

    >>> from infmidi import ProgramChange as PC
    >>> PC(0)
    ProgramChange(id=0, name="Acoustic Grand Piano", location=0.00, channel=0)
    >>> PC("Acoustic Guitar(nylon)")
    ProgramChange(id=24, name="Acoustic Guitar(nylon)", location=0.00, channel=0)

.. hint:: 

    See :doc:`cheat/GM Instrument <../cheat>` to check the full list of GM Instruments.

ChannelPressure
^^^^^^^^^^^^^^^

Using ``clip.add()`` to add ``ChannelPressure``.

    >>> from infmidi import ChannelPressure as CP
    >>> CP(66, channel=10)
    ChannelPressure(pressure=66, location=0.00, channel=10)


PitchBend
^^^^^^^^^

Using ``clip.add()`` to add ``PitchBend``.

    >>> from infmidi import PitchBend as PB
    >>> PB(0.5)
    PitchBend(pitch=0.50, location=0.00, channel=0)


.. todo::

    Include this event in :doc:`Note <./note>` to create microtones.

https://mido.readthedocs.io/en/latest/message_types.html#parameter^types


Sysex events
------------

TODO.
^^^^^

Meta events
-----------

Text
^^^^

Copyright
^^^^^^^^^

Lyric
^^^^^

Marker
^^^^^^

CuePoint
^^^^^^^^

TrackName
^^^^^^^^^

SetBpm
^^^^^^

TimeSignature
^^^^^^^^^^^^^

If your midi file only has one main time signature, using like ``Midi(time_signature="4/4")`` to initialize your ``Midi`` object. Or rather, using ``mid.add(TimeSignature("3/4"), location)`` to add extra time signatures at ``location`` beats.

    >>> from infmidi import TimeSignature
    >>> TimeSignature('4/4')
    >>> TimeSignature(signature="4/4", location=0.00)
    >>> signature = TimeSignature('3/4')
    >>> signature.numerator
    >>> 3
    >>> signature.denominator
    >>> 4


KeySignature
^^^^^^^^^^^^

If your midi file only has one main key signature, use like ``Midi(key_signature="C#")`` to initialize your ``Midi`` object. Otherwise, use ``mid.add(KeySignature("C#"), location)`` to add extra key signatures at ``location`` beats.

    >>> from infmidi import KeySignature
    >>> KeySignature('C#')
    >>> KeySignature(signature="C#", location=0.00)


SequencerSpecific
^^^^^^^^^^^^^^^^^