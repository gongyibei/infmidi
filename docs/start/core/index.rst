Foundation
==========

- :doc:`Event <./event>`: MIDI events.
- :doc:`Note <./note>`  : A warpper of "note_off" and "note_on" ``Event``.
- :doc:`Clip <./clip>`  : The core object in infmidi; A container of ``Note`` and ``Event``, with rich high-level operations.
- :doc:`Track <./track>`: Inherited from ``Clip``, with additional properties (such as name, instrument and mute, etc.).
- :doc:`Midi <./midi>`: Help you to organize your song with multiple ``Track``.


.. toctree::
    :hidden:
    
    basic
    event
    note
    clip
    track
    midi

