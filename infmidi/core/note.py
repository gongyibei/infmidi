import operator
from collections import defaultdict
from functools import partialmethod, total_ordering
from typing import Iterable, List, Optional, Union

from mido import Message
from sortedcontainers import SortedSet

from ..constants import DEFAULT_TICKS_PER_BEAT, KEYS
from ..warps import optional_inplace
from .event import NoteOff, NoteOn

__all__ = [
    "Note",
    "NoteSet",
]


@total_ordering
class Note:

    def __init__(
        self,
        note: Union[str, int, float],
        velocity: int = 127,
        length: float = 1.,
        location: float = 0.,
        channel: int = 0,
    ) -> None:
        self._note_on = NoteOn(note,
                               velocity=velocity,
                               location=location,
                               channel=channel)
        self.length = length

    @property
    def name(self) -> str:
        return self._note_on.name

    @name.setter
    def name(self, other: str) -> None:
        self._note_on.name = other

    @property
    def value(self) -> int:
        return self._note_on.value

    @value.setter
    def value(self, other: int) -> None:
        self._note_on.value = other

    @property
    def frequency(self) -> float:
        return self._note_on.frequency

    @frequency.setter
    def frequency(self, other: float) -> None:
        self.frequency = other

    @property
    def key(self) -> float:
        return self._note_on.key

    @property
    def octave(self) -> float:
        return self._note_on.octave

    @property
    def velocity(self) -> int:
        return self._note_on.velocity

    @velocity.setter
    def velocity(self, value: int) -> None:
        self._note_on.velocity = value

    @property
    def location(self) -> float:
        return self._note_on.location

    @location.setter
    def location(self, value: float) -> None:
        self._note_on.location = value

    @property
    def channel(self) -> int:
        return self._note_on.channel

    @channel.setter
    def channel(self, channel: int) -> None:
        self._note_on.channel = channel

    def copy(self) -> 'Note':
        return self.__class__(self.value,
                              velocity=self.velocity,
                              length=self.length,
                              location=self.location,
                              channel=self.channel)

    def _compare(self, a, b, op):
        _a = (a.location, a.value, a.channel)
        _b = (b.location, b.value, b.channel)
        return op(_a, _b)

    def __lt__(self, other: 'Note') -> bool:
        return self._compare(self, other, operator.lt)

    def __eq__(self, other: 'Note') -> bool:
        return self._compare(self, other, operator.eq)

    def __hash__(self):
        return hash((self.__class__, self.value, self.location, self.channel))

    def shift(self, length: float = 0) -> 'Note':
        self.location += length
        return self

    @optional_inplace(True)
    def lshift(self, length: float = 0) -> 'Note':
        return self.shift(-length)

    __lshift__ = partialmethod(lshift, inplace=False)
    __ilshift__ = partialmethod(lshift, inplace=True)

    @optional_inplace(True)
    def rshift(self, length: float = 0) -> 'Note':
        return self.shift(length)

    __rshift__ = partialmethod(rshift, inplace=False)
    __irshift__ = partialmethod(rshift, inplace=True)

    @optional_inplace(True)
    def up(self, n: int) -> 'Note':
        self._note_on.value += n
        return self

    __add__ = partialmethod(up, inplace=False)
    __iadd__ = partialmethod(up, inplace=True)

    @optional_inplace(True)
    def down(self, n: int) -> 'Note':
        self._note_on.value -= n
        return self

    __sub__ = partialmethod(down, inplace=False)
    __isub__ = partialmethod(down, inplace=True)

    @optional_inplace(True)
    def zoom(self, ration: float) -> 'Note':
        self.location *= ration
        self.length *= ration
        return self

    __xor__ = partialmethod(zoom, inplace=False)
    __ixor__ = partialmethod(zoom, inplace=True)

    @optional_inplace(True)
    def scale(self, ration: float) -> 'Note':
        self.length *= ration
        return self

    __mul__ = partialmethod(scale, inplace=False)
    __imul__ = partialmethod(scale, inplace=True)

    @optional_inplace(True)
    def decay(self, ration: float) -> 'Note':
        self.velocity = int(self.velocity * ration)
        return self

    __and__ = partialmethod(decay, inplace=False)
    __iand__ = partialmethod(decay, inplace=True)

    @optional_inplace(True)
    def at(self, channel: int) -> 'Note':
        self._note_on.channel = channel
        return self

    __matmul__ = partialmethod(at, inplace=False)
    __imatmul__ = partialmethod(at, inplace=True)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'Note(name="{self.name}", value={self.value}, frequency={self.frequency:.2f}, velocity={self.velocity}, length={self.length:.2f}, location={self.location:.2f}, channel={self.channel})'

    @property
    def note_on(self) -> NoteOn:
        return self._note_on

    @property
    def note_off(self) -> NoteOff:
        return NoteOff(self.value,
                       location=self.location + self.length,
                       velocity=0,
                       channel=self.channel)

    @property
    def msg_on(self) -> Message:
        return self._note_on.msg

    @property
    def msg_off(self) -> Message:
        return self.note_off.msg

    @property
    def msgs(self) -> List[Message]:
        return [self.msg_on, self.msg_off]

    def messages(
            self,
            ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> List[Message]:
        msg_on = self.note_on.message(ticks_per_beat)
        msg_off = self.note_off.message(ticks_per_beat)
        return [msg_on, msg_off]


class _FixedNoteSet(SortedSet):

    def _fix_note(self, note: Note) -> None:
        idx = self.index(note)
        if idx > 0:
            last = self[idx - 1]
            last.length = min(last.length, note.location - last.location)
        if idx < len(self) - 1:
            next = self[idx + 1]
            note.length = min(note.length, next.location - note.location)

    def add(self, note: Note) -> None:
        if isinstance(note, Note):
            if note in self:
                self.discard(note)
            super().add(note)
            self._fix_note(note)

    _add = add


class NoteSet(SortedSet):

    def __init__(self, iterable: Optional[Iterable[Note]] = None, key=None):
        self.mat = defaultdict(lambda: defaultdict(_FixedNoteSet))
        super().__init__(iterable=iterable, key=key)

    def __iter__(self):
        for note in self._list:
            yield note
        # the yielded note can be modifield, to update the order of notes in SortedSet
        self.fix()

    # borrowed from mido
    def __repr__(self) -> str:
        if len(self) == 0:
            notes = ''
        elif len(self) == 1:
            notes = f'[{repr(self[0])}]'
        else:
            notes = f',\n  '.join(repr(m) for m in self)
            notes = f'[\n  {notes}\n]'
        return f'{self.__class__.__name__}({notes})'

    __str__ = __repr__

    def fix(self) -> None:
        notes = list(self._list)
        self.clear()
        self.update(notes)

    def update(self, notes: List[Note]) -> None:
        super().update(notes)
        for note in notes:
            self.mat[note.channel][note.value].add(note)
    __ior__ = update
    _update = update

    def add(self, note: Note) -> None:
        if isinstance(note, Note):
            if note in self:
                self.discard(note)
            super().add(note)
            self.mat[note.channel][note.value].add(note)

    _add = add

    def clear(self) -> None:
        super().clear()
        self.mat = defaultdict(lambda: defaultdict(_FixedNoteSet))

    def copy(self) -> None:
        notes = super().copy()
        notes.mat = self.mat.copy()
        return notes

    def pop(self, index: int = -1) -> Note:
        note = super().pop(index)
        self.mat[note.channel][note.value].remove(note)
        return note

    def discard(self, note: Note) -> None:
        super().discard(note)
        self.mat[note.channel][note.value].discard(note)

    def remove(self, note: Note) -> None:
        super().remove(note)
        self.mat[note.channel][note.value].remove(note)
