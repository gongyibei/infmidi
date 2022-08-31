Foundation
============
.. currentmodule:: infmidi


Overview
--------

Event

- :class:`Event <infmidi.core.event.Event>`
- :class:`ChannelEvent <infmidi.core.event.ChannelEvent>`
- :class:`NoteOn <infmidi.core.event.NoteOn>`
- :class:`NoteOff <infmidi.core.event.NoteOff>`
- :class:`NotePressure <infmidi.core.event.NotePressure>`
- :class:`ControlChange <infmidi.core.event.ControlChange>`
- :class:`ProgramChange <infmidi.core.event.ProgramChange>`
- :class:`ChannelPressure <infmidi.core.event.ChannelPressure>`
- :class:`PitchBend <infmidi.core.event.PitchBend>`

:class:`Midi <infmidi.core.midi.Midi>` is equivalent to a song, :class:`Track <infmidi.core.track.Track>` is equivalent to a track, :class:`Clip <infmidi.core.clip.Clip>` is equivalent to a paragraph in a track, and :class:`Note <infmidi.core.note.Note>` is equivalent to the note you play.

- :class:`Note <infmidi.core.note.Note>`: include :class:`NoteOn <infmidi.core.event.NoteOn>` and :class:`NoteOff <infmidi.core.event.NoteOff>` two event.
- :class:`Clip <infmidi.core.clip.Clip>`: a container of :class:`Note <infmidi.core.note.Note>` and :class:`Event <infmidi.core.event.Event>`.
- :class:`Track <infmidi.core.track.Track>`: a container of :class:`Clip <infmidi.core.clip.Clip>`.
- :class:`Midi <infmidi.core.midi.Midi>`: help you to organize your song with multiple :class:`Track <infmidi.core.track.Track>`; read and save to midi file by calling :meth:`read() <infmidi.core.midi.Midi.read>`   and :meth:`save() <infmidi.core.midi.Midi.save>`.



.. toctree::
    :hidden:
    
    basic
    event
    note
    clip
    track
    midi
    cheat

