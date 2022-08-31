Event
=====


NoteOn & NoteOff & NotePressure
-------------------------------

Import

    >>> from infmidi import NoteOn, NoteOff, NotePressure

Initialize ``NoteOn``

    >>> NoteOn('A4')
    NoteOn(name="A4", value=69, freq=440.00, velocity=127, location=0.00, channel=0)

Initialize ``NoteOff``

    >>> NoteOff('A4')
    NoteOff(name="A4", value=69, freq=440.00, velocity=127, location=0.00, channel=0)

Initialize ``NotePressure``



    >>> NotePressure('A4')
    NotePressure(name="A4", value=69, freq=440.00, pressure=127, location=0.00, channel=0)


ControlChange
-------------

Import

    >>> from infmidi import ControlChange as CC


Initialize 

    >>> CC(0, 66)
    >>> ControlChange(control=0, value=66, description="Bank Select", location=0.00, channel=0)

ProgramChange
-------------

Import

    >>> from infmidi import ProgramChange as PC

Initialize 

    >>> PC(0)
    ProgramChange(id=0, name="Acoustic Grand Piano", location=0.00, channel=0)
    >>> PC("Acoustic Guitar(nylon)")
    ProgramChange(id=24, name="Acoustic Guitar(nylon)", location=0.00, channel=0)

.. hint:: 

    The attribute ``id`` and ``name`` are bound, click :doc:`here <./cheat>` to check the correspondence between the two.

ChannelPressure
---------------

Import

    >>> from infmidi import ChannelPressure as CP


Initialize 

    >>> CP(66, channel=10)
    ChannelPressure(pressure=66, location=0.00, channel=10)



PitchBend
---------

Import

    >>> from infmidi import PitchBend as PB


Initialize 

    >>> PB(0.5)
    PitchBend(pitch=0.50, location=0.00, channel=0)



https://mido.readthedocs.io/en/latest/message_types.html#parameter-types

.. todo:: 
    
    MetaEvent
