import operator
from functools import partialmethod, total_ordering
from typing import Iterable, Optional, Union

from mido import Message, MetaMessage, bpm2tempo, tempo2bpm
from sortedcontainers import SortedSet

from .. import core
from ..constants import (CONTROL_DESCRIPTIONS, DEFAULT_TICKS_PER_BEAT,
                         INSTRUMENTS, KEYS)
from ..warps import optional_inplace

BASIC = ["Event"]

CHANNEL_EVENT = [
    "ChannelEvent", "NoteOff", "NoteOn", "NotePressure", "ControlChange",
    "ProgramChange", "ChannelPressure", "PitchBend"
]
META_EVENT = [
    "MetaEvent", "Text", "Copyright", "Lyric", "Marker", "CuePoint", "TrackName", "SetBpm",
    "TimeSignature", "KeySignature", "SequencerSpecific"
]
EXTRA = ["EventSet"]

__all__ = BASIC + CHANNEL_EVENT + META_EVENT + EXTRA


@total_ordering
class Event:

    def __init__(self, location: float = 0) -> None:
        self.location = location

    def _compare(self, a, b, op):
        _a = a.location
        _b = b.location
        return op(_a, _b)

    def __lt__(self, other: 'Event') -> bool:
        return self._compare(self, other, operator.lt)

    def __eq__(self, other: 'Event') -> bool:
        return self._compare(self, other, operator.eq)

    def shift(self, length: float = 0) -> 'Event':
        self.location += length
        return self

    @optional_inplace(True)
    def lshift(self, length: float = 0) -> 'Event':
        return self.shift(-length)

    __lshift__ = partialmethod(lshift, inplace=False)
    __ilshift__ = partialmethod(lshift, inplace=True)

    @optional_inplace(True)
    def rshift(self, length: float = 0) -> 'Event':
        return self.shift(length)

    __rshift__ = partialmethod(rshift, inplace=False)
    __irshift__ = partialmethod(rshift, inplace=True)

    @optional_inplace(True)
    def zoom(self, ration: float = 1) -> 'Event':
        self.location *= ration
        return self

    __xor__ = partialmethod(zoom, inplace=False)
    __ixor__ = partialmethod(zoom, inplace=True)

    @property
    def msg(self):
        return self.message()

    def copy(self):
        raise NotImplementedError

    def message(self):
        raise NotImplementedError

    def from_message(self):
        raise NotImplementedError


class ChannelEvent(Event):

    def __init__(self, location: float = 0, channel: int = 0) -> None:
        super().__init__(location)

        self.channel = channel

    def _compare(self, a, b, op):
        _a = (a.location, a.channel)
        _b = (b.location, b.channel)
        return op(_a, _b)

    def __hash__(self):
        return hash((self.__class__, self.location, self.channel))

    @optional_inplace(True)
    def at(self, channel: int) -> 'ChannelEvent':
        self.channel = channel
        return self

    __matmul__ = partialmethod(at, inplace=False)
    __imatmul__ = partialmethod(at, inplace=True)


class _NoteEvent(ChannelEvent):

    def __init__(
        self,
        note: Union[str, int, float],
        location: float = 0.,
        channel: int = 0,
    ) -> None:
        super().__init__(location, channel)
        if isinstance(note, str):
            self.value = core.convert.name2value(note)
        elif isinstance(note, int):
            self.value = note
        elif isinstance(note, float):
            self.value = core.convert.frequency2value(note)
        else:
            raise Exception("Unsupported note type！")
        self.channel = channel

    @optional_inplace(True)
    def up(self, n: int) -> '_NoteEvent':
        self.value += n
        return self

    __add__ = partialmethod(up, inplace=False)
    __iadd__ = partialmethod(up, inplace=True)

    @optional_inplace(True)
    def down(self, n: int) -> '_NoteEvent':
        self.value -= n
        return self

    __sub__ = partialmethod(down, inplace=False)
    __isub__ = partialmethod(down, inplace=True)


    @property
    def name(self) -> str:
        return core.convert.value2name(self.value)

    @name.setter
    def name(self, other: str) -> None:
        self.value = core.convert.name2value(other)

    @property
    def frequency(self) -> float:
        return core.convert.value2frequency(self.value)

    @frequency.setter
    def frequency(self, other: float) -> None:
        self.value = core.convert.frequency2value(other)
    
    @property
    def key(self) -> float:
        return KEYS[self.value%12]
    
    @property
    def octave(self) -> float:
        return self.value // 12 - 1

    def __hash__(self):
        return hash((self.__class__, self.value, self.location, self.channel))


class NoteOff(_NoteEvent):
    message_type = "note_off"

    def __init__(
        self,
        note: Union[str, int, float],
        velocity: int = 127,
        location: float = 0.,
        channel: int = 0,
    ) -> None:
        super().__init__(note, location=location, channel=channel)
        self.velocity = velocity

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name="{self.name}", value={self.value}, frequency={self.frequency:.2f}, velocity={self.velocity}, location={self.location:.2f}, channel={self.channel})'

    def message(self, ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> Message:
        return Message('note_off',
                       channel=self.channel,
                       note=self.value,
                       velocity=self.velocity,
                       time=core.convert.loc2tick(self.location,
                                                  ticks_per_beat))

    @classmethod
    def from_message(
            cls,
            msg: Message,
            ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> 'NoteOff':
        return cls(msg.note,
                   velocity=msg.velocity,
                   location=core.convert.tick2loc(msg.time, ticks_per_beat),
                   channel=msg.channel)

    def _compare(self, a, b, op):
        _a = (a.location, a.value, a.velocity, a.channel)
        _b = (b.location, b.value, b.velocity, b.channel)
        return op(_a, _b)

    def copy(self) -> 'NoteOff':
        return self.__class__(self.value,
                              velocity=self.velocity,
                              location=self.location,
                              channel=self.channel)


class NoteOn(_NoteEvent):
    message_type = "note_on"

    def __init__(
        self,
        note: Union[str, int, float],
        velocity: int = 127,
        location: float = 0.,
        channel: int = 0,
    ) -> None:
        super().__init__(note, location=location, channel=channel)
        self.velocity = velocity

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name="{self.name}", value={self.value}, frequency={self.frequency:.2f}, velocity={self.velocity}, location={self.location:.2f}, channel={self.channel})'

    def message(self, ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> Message:
        return Message('note_on',
                       channel=self.channel,
                       note=self.value,
                       velocity=self.velocity,
                       time=core.convert.loc2tick(self.location,
                                                  ticks_per_beat))

    @classmethod
    def from_message(cls,
                     msg: Message,
                     ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> 'NoteOn':
        return cls(msg.note,
                   velocity=msg.velocity,
                   location=core.convert.tick2loc(msg.time, ticks_per_beat),
                   channel=msg.channel)

    def _compare(self, a, b, op):
        _a = (a.location, a.value, a.velocity, a.channel)
        _b = (b.location, b.value, b.velocity, b.channel)
        return op(_a, _b)

    def copy(self) -> 'NoteOn':
        return self.__class__(self.value,
                              velocity=self.velocity,
                              location=self.location,
                              channel=self.channel)


class NotePressure(_NoteEvent):
    message_type = "polytouch"

    def __init__(
        self,
        note: Union[str, int, float],
        pressure: int = 127,
        location: float = 0.,
        channel: int = 0,
    ) -> None:
        super().__init__(note, location=location, channel=channel)
        self.pressure = pressure

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name="{self.name}", value={self.value}, frequency={self.frequency:.2f}, pressure={self.pressure}, location={self.location:.2f}, channel={self.channel})'

    def message(self, ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> Message:
        return Message('polytouch',
                       channel=self.channel,
                       note=self.value,
                       value=self.pressure,
                       time=core.convert.loc2tick(self.location,
                                                  ticks_per_beat))

    @classmethod
    def from_message(
            cls,
            msg: Message,
            ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> 'NotePressure':
        return cls(msg.note,
                   pressure=msg.pressure,
                   location=core.convert.tick2loc(msg.time, ticks_per_beat),
                   channel=msg.channel)

    def _compare(self, a, b, op):
        _a = (a.location, a.value, a.pressure, a.channel)
        _b = (b.location, b.value, b.pressure, b.channel)
        return op(_a, _b)

    def copy(self) -> 'NotePressure':
        return self.__class__(self.value,
                              pressure=self.pressure,
                              location=self.location,
                              channel=self.channel)


class ControlChange(ChannelEvent):
    message_type = "control_change"

    def __init__(self,
                 control: int,
                 value: int = 0,
                 location: float = 0,
                 channel: int = 0) -> None:
        super().__init__(location, channel)
        self.control = control
        self.value = value

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(control={self.control}, value={self.value}, description="{self.description}", location={self.location:.2f}, channel={self.channel})'

    @property
    def description(self):
        return CONTROL_DESCRIPTIONS[self.control]

    def message(self, ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> Message:
        return Message('control_change',
                       channel=self.channel,
                       control=self.control,
                       value=self.value,
                       time=core.convert.loc2tick(self.location,
                                                  ticks_per_beat))

    @classmethod
    def from_message(
            cls,
            msg: Message,
            ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> 'ControlChange':
        return cls(msg.control,
                   msg.value,
                   location=core.convert.tick2loc(msg.time, ticks_per_beat),
                   channel=msg.channel)

    def copy(self) -> 'ControlChange':
        return self.__class__(self.control,
                              self.value,
                              location=self.location,
                              channel=self.channel)


class ProgramChange(ChannelEvent):
    message_type = "program_change"

    def __init__(self,
                 inst: Union[str, int] = 0,
                 location: float = 0,
                 channel: int = 0) -> None:
        super().__init__(location, channel)
        if isinstance(inst, int):
            self.id = inst
        elif isinstance(inst, str):
            self.id = self._fuzzy_match(inst)

    @property
    def name(self) -> str:
        return INSTRUMENTS[self.id]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, name="{self.name}", location={self.location:.2f}, channel={self.channel})'

    def _fuzzy_match(self, inst: str):
        # TODO.
        for i, name in enumerate(INSTRUMENTS):
            if name == inst:
                return i
        return 0

    def message(self, ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> Message:
        return Message('program_change',
                       channel=self.channel,
                       program=self.id,
                       time=core.convert.loc2tick(self.location,
                                                  ticks_per_beat))

    @classmethod
    def from_message(
            cls,
            msg: Message,
            ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> 'ProgramChange':
        return cls(msg.program,
                   location=core.convert.tick2loc(msg.time, ticks_per_beat),
                   channel=msg.channel)

    def copy(self) -> 'ProgramChange':
        return self.__class__(self.id,
                              location=self.location,
                              channel=self.channel)

    @staticmethod
    def print_instruments():
        for idx, instrument in enumerate(INSTRUMENTS):
            print(f'{idx:<3d} {instrument}')


class ChannelPressure(ChannelEvent):
    message_type = "aftertouch"

    def __init__(self,
                 pressure: float = 0,
                 location: float = 0,
                 channel: int = 0) -> None:
        super().__init__(location, channel)
        self.pressure = pressure

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(pressure={self.pressure}, location={self.location:.2f}, channel={self.channel})'

    def message(self, ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> Message:
        return Message('aftertouch',
                       channel=self.channel,
                       value=self.pressure,
                       time=core.convert.loc2tick(self.location,
                                                  ticks_per_beat))

    @classmethod
    def from_message(
            cls,
            msg: Message,
            ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> 'ChannelPressure':
        return cls(msg.value,
                   location=core.convert.tick2loc(msg.time, ticks_per_beat),
                   channel=msg.channel)

    def copy(self) -> 'ChannelPressure':
        return self.__class__(self.pressure,
                              location=self.location,
                              channel=self.channel)


class PitchBend(ChannelEvent):
    message_type = "pitchwheel"

    def __init__(self,
                 pitch: float = 0.,
                 location: float = 0.,
                 channel: int = 0) -> None:
        super().__init__(location, channel)
        self.pitch = max(min(pitch, 1.), -1.)

    def __str__(self):
        return self.pitch

    def __repr__(self):
        return f'{self.__class__.__name__}(pitch={self.pitch:.2f}, location={self.location:.2f}, channel={self.channel})'

    def message(self, ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> Message:
        return Message('pitchwheel',
                       pitch=int(self.pitch * 8191),
                       channel=self.channel,
                       time=core.convert.loc2tick(self.location,
                                                  ticks_per_beat))

    @classmethod
    def from_message(
            cls,
            msg: Message,
            ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> 'PitchBend':
        if msg.pitch < 0:
            pitch = msg.pitch / 8192
        else:
            pitch = msg.pitch / 8191
        return cls(pitch,
                   location=core.convert.tick2loc(msg.time, ticks_per_beat),
                   channel=msg.channel)

    def copy(self) -> 'PitchBend':
        return self.__class__(self.pressure,
                              location=self.location,
                              channel=self.channel)

    def copy(self) -> 'PitchBend':
        return self.__class__(self.pitch,
                              location=self.location,
                              channel=self.channel)


class MetaEvent(Event):
    pass


class _TextMetaEvent(MetaEvent):

    def __init__(self, text="", location: float = 0.):
        super().__init__(location)
        self.text = text

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(text="{repr(self.text)[1:-1]}", location={self.location:.2f})'

    def message(self, ticks_per_beat=DEFAULT_TICKS_PER_BEAT) -> MetaMessage:
        return MetaMessage(self.message_type,
                           text=self.text,
                           time=core.convert.loc2tick(self.location,
                                                      ticks_per_beat))

    @classmethod
    def from_message(
            cls,
            msg: MetaMessage,
            ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> '_TextMetaEvent':
        return cls(msg.text,
                   location=core.convert.tick2loc(msg.time, ticks_per_beat))

    def copy(self) -> '_TextMetaEvent':
        return self.__class__(self.text, location=self.location)

    def __hash__(self):
        return hash((self.__class__, self.text, self.location))


class Text(_TextMetaEvent):
    message_type = "text"


class Copyright(_TextMetaEvent):
    message_type = "copyright"


class Lyric(_TextMetaEvent):
    message_type = "lyrics"


class Marker(_TextMetaEvent):
    message_type = "marker"


class CuePoint(_TextMetaEvent):
    message_type = "cue_marker"


class TrackName(MetaEvent):
    message_type = "track_name"

    def __init__(self, name="", location: float = 0.):
        super().__init__(location)
        self.name = name

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name="{repr(self.name)[1:-1]}", location={self.location:.2f})'

    def message(self, ticks_per_beat=DEFAULT_TICKS_PER_BEAT) -> MetaMessage:
        return MetaMessage(self.message_type,
                           name=self.name,
                           time=core.convert.loc2tick(self.location,
                                                      ticks_per_beat))

    @classmethod
    def from_message(
            cls,
            msg: MetaMessage,
            ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> 'TrackName':
        return cls(msg.name,
                   location=core.convert.tick2loc(msg.time, ticks_per_beat))

    def copy(self) -> 'TrackName':
        return self.__class__(self.name, location=self.location)

    def __hash__(self):
        return hash((self.__class__, self.name, self.location))


class SetBpm(MetaEvent):
    message_type = "set_tempo"

    def __init__(self, bpm: float = 120., location: float = 0.):
        super().__init__(location)
        self.bpm = bpm

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(bpm={self.bpm:.2f}, location={self.location:.2f})'

    def message(self, ticks_per_beat=DEFAULT_TICKS_PER_BEAT) -> MetaMessage:
        return MetaMessage("set_tempo",
                           tempo=bpm2tempo(self.bpm),
                           time=core.convert.loc2tick(self.location,
                                                      ticks_per_beat))

    @classmethod
    def from_message(cls,
                     msg: MetaMessage,
                     ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> 'SetBpm':
        return cls(bpm=tempo2bpm(msg.tempo),
                   location=core.convert.tick2loc(msg.time, ticks_per_beat))

    def copy(self) -> 'SetBpm':
        return self.__class__(self.bpm, location=self.location)

    def __hash__(self):
        return hash((self.__class__, self.bpm, self.location))


class TimeSignature(MetaEvent):
    message_type = "time_signature"

    def __init__(self, signature: str = "4/4", location: float = 0.):
        super().__init__(location)
        self.signature = signature

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(signature="{self.signature}", location={self.location:.2f})'

    @property
    def numerator(self) -> int:
        return int(self.signature.split('/')[0])

    @property
    def denominator(self) -> int:
        return int(self.signature.split('/')[1])

    def message(self, ticks_per_beat=DEFAULT_TICKS_PER_BEAT) -> MetaMessage:
        return MetaMessage("time_signature",
                           numerator=self.numerator,
                           denominator=self.denominator,
                           time=core.convert.loc2tick(self.location,
                                                      ticks_per_beat))

    @classmethod
    def from_message(
            cls,
            msg: MetaMessage,
            ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> 'TimeSignature':
        return cls(signature=f"{msg.numerator}/{msg.denominator}",
                   location=core.convert.tick2loc(msg.time, ticks_per_beat))

    def copy(self) -> 'TimeSignature':
        return self.__class__(self.signature, location=self.location)

    def __hash__(self):
        return hash((self.__class__, self.signature, self.location))


class KeySignature(MetaEvent):
    message_type = "key_signature"

    def __init__(self, signature: str = 'C', location: float = 0.):
        super().__init__(location)
        self.signature = signature

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(signature="{self.signature}", location={self.location:.2f})'

    def message(self, ticks_per_beat=DEFAULT_TICKS_PER_BEAT) -> MetaMessage:
        return MetaMessage("key_signature",
                           key=self.signature,
                           time=core.convert.loc2tick(self.location,
                                                      ticks_per_beat))

    @classmethod
    def from_message(
            cls,
            msg: MetaMessage,
            ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> 'KeySignature':
        return cls(signature=msg.key,
                   location=core.convert.tick2loc(msg.time, ticks_per_beat))

    def copy(self) -> 'KeySignature':
        return self.__class__(self.signature, location=self.location)

    def __hash__(self):
        return hash((self.__class__, self.signature, self.location))


class SequencerSpecific(MetaEvent):
    message_type = "sequencer_specific"

    def __init__(self, data, location: float = 0) -> None:
        super().__init__(location)
        self.data = data

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(data={self.data}, location={self.location:.2f})'
    
    def message(self, ticks_per_beat=DEFAULT_TICKS_PER_BEAT) -> MetaMessage:
        return MetaMessage("sequencer_specific",
                           key=self.signature,
                           time=core.convert.loc2tick(self.location,
                                                      ticks_per_beat))

    @classmethod
    def from_message(
            cls,
            msg: MetaMessage,
            ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> 'KeySignature':
        return cls(data=msg.data,
                   location=core.convert.tick2loc(msg.time, ticks_per_beat))
   
    def copy(self) -> 'SequencerSpecific':
        return self.__class__(self.data, location=self.location) 
    
    def __hash__(self):
        return hash((self.__class__, self.location))
    


class EventSet(SortedSet):

    def __init__(self, iterable: Optional[Iterable[Event]] = None, key=None):
        super().__init__(iterable=iterable, key=key)

    # borrowed from mido
    def __repr__(self):
        if len(self) == 0:
            events = ''
        elif len(self) == 1:
            events = f'[{repr(self[0])}]'
        else:
            events = f',\n  '.join(repr(m) for m in self)
            events = f'[\n  {events}\n]'
        return f'{self.__class__.__name__}({events})'

    __str__ = __repr__

    def __iter__(self):
        for event in self._list:
            yield event
        # the yielded note can be modifield, to update the order of events in SortedSet
        self.fix()

    def fix(self) -> None:
        events = list(self._list)
        self.clear()
        self.update(events)

    def add(self, value: Event) -> None:
        if isinstance(value, Event):
            if value in self:
                self.discard(value)
            super().add(value)

    _add = add
