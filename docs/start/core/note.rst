Note
====

:class:`Note <infmidi.core.note.Note>` include :class:`NoteOn <infmidi.core.event.NoteOn>` and :class:`NoteOff <infmidi.core.event.NoteOff>` two event.
.. The ``location`` of :class:`NoteOn <infmidi.core.event.NoteOn>` and :class:`NoteOff <infmidi.core.event.NoteOff>` is determined by the two properties of :class:`Note <infmidi.core.note.Note>`, ``location`` and ``length``.


Import
------

.. code-block:: python

    >>> from infmidi import Note


Initialize
----------

.. admonition:: C4=60 or 72?
    :class: note

    pass


There are different ways to initialize a :class:`Note <infmidi.core.note.Note>`.

.. code-block:: python


    >>> Note('A4')
    Note(name="A4", value=69, freq=440.00, location=0.00, length=1.00, velocity=127, channel=0)
    >>> Note('A4') == Note(69) == Note(440.)
    True


.. hint:: 

    The three attributes (``name``, ``value`` and ``freq``) are associated. Change one of them, and the other two will also change.



Manipulate
----------

Use ``-`` or ``+`` to change the value.

.. code-block:: python

    >>> Note('A4') - 12 == Note('A3')
    True
    >>> Note('A4') + 12 == Note('A5')
    True
    >>> Note('A4') + 8
    Note(name="F5", value=77, freq=698.46, location=0.00, length=1.00, velocity=127, channel=0)


Use ``>>`` or ``<<`` to change the location.

.. code-block:: python

    >>> Note('A4', location=2.) >> 4
    Note(name="A4", value=69, freq=440.00, location=6.00, length=1.00, velocity=127, channel=0)
    >>> Note('A4', location=4.) << 2
    Note(name="A4", value=69, freq=440.00, location=2.00, length=1.00, velocity=127, channel=0)

Use ``^`` and ``*`` to zoom and scale the note.

.. code-block:: python

    >>> Note('A4', location=2., length=3.) ^ 3
    Note(name="A4", value=69, freq=440.00, location=6.00, length=9.00, velocity=127, channel=0)
    >>> Note('A4', location=2., length=3.) * 3
    Note(name="A4", value=69, freq=440.00, location=2.00, length=9.00, velocity=127, channel=0)

Use ``@`` to select the channel.

.. code-block:: python

    >>> Note('A4', channel=7)
    Note(name="A4", value=69, freq=440.00, location=0.00, length=1.00, velocity=127, channel=7)
    >>> Note('A4', channel=7) @ 12
    Note(name="A4", value=69, freq=440.00, location=0.00, length=1.00, velocity=127, channel=12)

.. hint:: 

    All operators above have an inpalce version and an method version, click :doc:`here <../cheat>` to see the cheat sheet.


Get message
-----------

.. code-block:: python

    >>> note = Note('A4') >> 4
    >>> note.msg_on
    Message('note_on', channel=0, note=69, velocity=127, time=1920)
    >>> note.msg_off
    Message('note_on', channel=0, note=69, velocity=0, time=2400)
    >>> note.msgs
    [ Message('note_on', channel=0, note=69, velocity=127, time=1920), Message('note_on', channel=0, note=69, velocity=0, time=2400)]


