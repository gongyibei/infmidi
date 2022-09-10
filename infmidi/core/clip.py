import math
from ast import Slice
from functools import partialmethod
from itertools import chain
from typing import Iterable, List, Optional, Union

from mido import Message

from ..constants import DEFAULT_TICKS_PER_BEAT
from ..exceptions import ParameterError
from ..warps import optional_inplace
from .event import ChannelEvent, Event, EventSet
from .note import Note, NoteSet

__all__ = [
    "Clip",
]


class Clip:

    def __init__(self,
                 items: Optional[Iterable[Union[Note, Event, 'Clip']]] = None,
                 **kwargs) -> None:
        self.notes = NoteSet()
        self.events = EventSet()
        if items:
            for item in items:
                self.add(item)

    def __iter__(self):
        for item in chain(self.notes, self.events):
            yield item

    @property
    def n_notes(self):
        return len(self.notes)

    @property
    def n_events(self):
        return len(self.events)

    @property
    def notes_length(self) -> float:
        if self.notes:
            last_note = self.notes[-1]
            return math.ceil(last_note.location + last_note.length)
        else:
            return 0

    @property
    def events_length(self) -> float:
        if self.events:
            last_event = self.events[-1]
            return math.ceil(last_event.location)
        else:
            return 0

    @property
    def length(self) -> float:
        return max(self.notes_length, self.events_length)


    def __setitem__(self, key: Slice, item: Union[Event, Note,
                                                  'Clip']) -> None:
        if isinstance(key, slice):
            lloc = key.start if key.start else 0
            rloc = key.stop if key.stop else self.length
            self.clear(lloc, rloc)
            self.add(item, lloc)
        else:
            raise Exception(f"Invalid key type: {type(key)}.")

    def __getitem__(self, key: Slice) -> 'Clip':
        if isinstance(key, slice):
            return self.slice(key.start, key.stop, inplace=False)
        else:
            raise ParameterError(f"Invalid key type : {type(key)}.")

    def __contains__(self, item: Union[Note, Event]) -> bool:
        if isinstance(item, Note):
            return item in self.notes
        if isinstance(item, Event):
            return item in self.events

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(n_notes={self.n_notes}, n_events={self.n_events}, length={self.length})'

    def copy_notes(self):
        return NoteSet(note.copy() for note in self.notes)

    def copy_events(self):
        return EventSet(event.copy() for event in self.events)

    def copy(self):
        clip = self.__class__()
        clip.notes = self.copy_notes()
        clip.events = self.copy_events()
        return clip

    @optional_inplace(True)
    def slice(self,
              lloc: Optional[float] = None,
              rloc: Optional[float] = None) -> 'Clip':
        lloc = 0 if lloc is None else lloc
        rloc = self.length if rloc is None else rloc
        reverse = False
        if lloc > rloc:
            lloc, rloc = rloc, lloc
            reverse = True

        l = self.notes.bisect_left(Note(0, location=lloc))
        r = self.notes.bisect_left(Note(0, location=rloc))
        notes = self.notes[l:r]
        for note in notes:
            note <<= lloc
        self.notes = NoteSet(notes)

        l = self.events.bisect_left(ChannelEvent(location=lloc))
        r = self.events.bisect_left(ChannelEvent(location=rloc))
        events = self.events[l:r]
        for event in events:
            event <<= lloc
        self.events = EventSet(events)
        if reverse:
            self.reverse()
        return self

    def _add_event(self,
                   event: Event,
                   location: Optional[float] = None) -> None:
        if location:
            event.location = location
        self.events.add(event)

    def _add_note(self, note: Note, location: Optional[float] = None) -> None:
        if location:
            note.location = location
        self.notes.add(note)

    def _add_clip(self,
                  clip: 'Clip',
                  location: Optional[float] = None) -> None:
        for item in clip:
            if location:
                item.location += location
            if isinstance(item, Event):
                self._add_event(item)
            elif isinstance(item, Note):
                self._add_note(item)

    def up(self, n: int) -> 'Clip':
        for note in self.notes:
            note += n
        return self

    trans = up

    @optional_inplace(True)
    def add(
        self,
        item: Union[int, Event, Note, 'Clip'],
        location: Optional[float] = None,
    ) -> 'Clip':

        if 'copy' in item.__dir__():
            item = item.copy()
        if isinstance(item, Event):
            self._add_event(item, location)
        elif isinstance(item, Note):
            self._add_note(item, location)
        elif isinstance(item, Clip):
            self._add_clip(item, location)
        elif isinstance(item, int):
            self.up(item)
        return self

    __add__ = partialmethod(add, location=None, inplace=False)
    __iadd__ = partialmethod(add, location=None, inplace=True)

    @optional_inplace(True)
    def down(self, n: int) -> 'Clip':
        for note in self.notes:
            note -= n
        return self

    @optional_inplace(True)
    def sub(
        self,
        item: Union[int, Event, Note],
    ) -> 'Clip':

        if 'copy' in item.__dir__():
            item = item.copy()
        if isinstance(item, Event):
            self.events.remove(item)
        elif isinstance(item, Note):
            self.notes.remove(item)
        elif isinstance(item, int):
            self.down(item)
        return self

    __sub__ = partialmethod(sub, inplace=False)
    __isub__ = partialmethod(sub, inplace=True)

    @optional_inplace(True)
    def remove(
        self,
        item: Union[Event, Note],
    ) -> 'Clip':
        if isinstance(item, Event):
            self.events.remove(item)
        elif isinstance(item, Note):
            self.notes.remove(item)
        return self

    @optional_inplace(True)
    def discard(
        self,
        item: Union[Event, Note],
    ) -> 'Clip':
        if isinstance(item, Event):
            self.events.discard(item)
        elif isinstance(item, Note):
            self.notes.discard(item)
        return self

    @optional_inplace(True)
    def concat(self, clip: 'Clip') -> 'Clip':
        self._add_clip(clip.copy(), self.length)
        return self

    __or__ = partialmethod(concat, inplace=False)
    __ior__ = partialmethod(concat, inplace=True)

    @optional_inplace(True)
    def extend(self, clips: Iterable['Clip']) -> 'Clip':
        for clip in clips:
            self.concat(clip)
        return self

    @optional_inplace(True)
    def repeat(self, n: int) -> 'Clip':
        clip = self.copy()
        for _ in range(n - 1):
            self |= clip
        return self

    __pow__ = partialmethod(repeat, inplace=False)
    __ipow__ = partialmethod(repeat, inplace=True)

    def shift(self, length: float) -> 'Clip':
        for item in self:
            item >>= length
        return self

    @optional_inplace(True)
    def lshift(self, length: float) -> 'Clip':
        self.shift(-length)
        return self

    __lshift__ = partialmethod(lshift, inplace=False)
    __ilshift__ = partialmethod(lshift, inplace=True)

    @optional_inplace(True)
    def rshift(self, length: float) -> 'Clip':
        self.shift(length)
        return self

    __rshift__ = partialmethod(rshift, inplace=False)
    __irshift__ = partialmethod(rshift, inplace=True)

    @optional_inplace(True)
    def at(self, channel: int) -> 'Clip':
        for item in self:
            if 'channel' in item.__dir__():
                item.channel = channel
        return self

    __matmul__ = partialmethod(at, inplace=False)
    __imatmul__ = partialmethod(at, inplace=True)

    @optional_inplace(True)
    def reverse(self) -> 'Clip':
        length = self.length
        for item in self:
            if isinstance(item, Note):
                item.location = length - (item.location + item.length)
            else:
                item.location = length - item.location
        return self

    __reversed__ = partialmethod(reverse, inplace=False)

    @optional_inplace(True)
    def invert(self) -> 'Clip':
        max_value = max(note.value for note in self.notes)
        min_value = min(note.value for note in self.notes)
        for note in self.notes:
            note.value = min_value + max_value - note.value
        return self

    __invert__ = partialmethod(invert, inplace=False)

    @optional_inplace(True)
    def zoom(self, ration: float) -> 'Clip':
        for item in self:
            item ^= ration
        return self

    __xor__ = partialmethod(zoom, inplace=False)
    __ixor__ = partialmethod(zoom, inplace=True)

    @optional_inplace(True)
    def scale(self, ration: float) -> 'Clip':
        for note in self.notes:
            note *= ration
        return self

    __mul__ = partialmethod(scale, inplace=False)
    __imul__ = partialmethod(scale, inplace=True)

    @optional_inplace(True)
    def decay(self, ration: float) -> 'Clip':
        for note in self.notes:
            note &= ration
        return self

    __and__ = partialmethod(decay, inplace=False)
    __iand__ = partialmethod(decay, inplace=True)

    @optional_inplace(True)
    def quantify(self, precision: int) -> 'Clip':
        for item in self:
            item.location = math.ceil(item.location / precision) * precision
        return self

    def clear(self,
              lloc: Optional[float] = None,
              rloc: Optional[float] = None) -> 'Clip':
        lloc = 0 if lloc is None else lloc
        rloc = self.length if rloc is None else rloc
        notes = NoteSet()
        events = EventSet()
        for item in self:
            loc = item.location
            if not (loc >= lloc and loc < rloc):
                notes.add(item)
                events.add(item)
        self.notes = notes
        self.events = events
        return self

    def _to_reltime(self, msgs: List[Message]) -> None:
        now = 0
        for i in range(len(msgs)):
            msgs[i].time -= now
            now += msgs[i].time

    @property
    def msgs(self) -> List[Message]:
        return self.messages()

    def messages(self,
                 ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT,
                 mode='reltime') -> List[Message]:
        msgs = []
        for note in self.notes:
            if note.location >= 0:
                msgs.extend(note.messages(ticks_per_beat))
        for event in self.events:
            if event.location >= 0:
                msgs.append(event.message(ticks_per_beat))

        msgs.sort(key=lambda msg: (msg.time, msg.__dict__.setdefault(
            "note", 0), msg.__dict__.setdefault("velocity", 0)))
        if mode == 'reltime':
            self._to_reltime(msgs)
        return msgs
