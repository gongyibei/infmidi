import math
import re

from typing import Iterable, List, Optional, Union
from mido import Message

from ..exceptions import ParameterError
from . import event
from .clip import Clip
from .midi import Midi
from .event import Event
from .note import Note
from .track import Track
from ..constants import DRUM_SOUNDS, KEY_TO_INDEX, KEYS, DEFAULT_TICKS_PER_BEAT, MESSAGE_TYPE_TO_EVENT_TYPE

__all__ = [
    "loc2tick",
    "tick2loc",
    "loc2second",
    "second2loc",
    "value2name",
    "name2value",
    "value2frequency",
    "frequency2value",
    "key2index",
    "message2event",
    "messages2events",
    "note2clip",
    "note2track",
    "note2midi",
    "clip2track",
    "clip2track",
    "clip2midi",
    "track2midi",
    "item2midi",
]


def loc2tick(loc: float, ticks_per_beat: int) -> int:
    return round(loc * ticks_per_beat)


def tick2loc(ticks, ticks_per_beat: int) -> float:
    return ticks / ticks_per_beat


def loc2second(loc: float, bpm: float) -> float:
    return 60 / bpm * loc


def second2loc(second: float, bpm: float) -> float:
    return second * bpm / 60


# borrowed from librosa
def name2value(name: str) -> int:
    match = re.match(
        r'^(?P<key>[A-Ga-g])'
        r'(?P<acc>[#b]*)'
        r'(?P<oct>[+-]?\d+)?', name)
    if not match:
        raise ParameterError(f'Invalid note name: {name}')

    key = match.group('key').upper()
    acc = match.group('acc')
    oct = match.group('oct')

    # default to 4.
    oct = int(oct) if oct else 4

    value = KEY_TO_INDEX[key] + 12 * (oct + 1)

    for ch in acc:
        if ch == '#':
            value += 1
        elif ch == 'b':
            value -= 1

    return value


def value2name(value: int) -> str:
    key = KEYS[value % 12]
    oct = int(value / 12) - 1
    name = f'{key:s}{oct:0d}'
    return name


def value2frequency(value: int) -> float:
    return 440.0 * (2.0**((value - 69.0) / 12.0))


def frequency2value(freq: float) -> int:
    return round(12 * (math.log2(freq) - math.log2(440.0)) + 69)


def key2index(key:str, root:str='C') -> int:
    key_idx = KEYS.index(key)
    root_idx = KEYS.index(root)
    return (key_idx - root_idx) % 12 


def drum2value(drum: str) -> int:
    try:
        idx = DRUM_SOUNDS.index(drum)
    except:
        raise ParameterError(f"Invalid drum name: {drum}.")

    return idx + 35


def message2event(
        msg: Message,
        ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> Optional[Event]:
    if msg.type in MESSAGE_TYPE_TO_EVENT_TYPE:
        return eval("event." + MESSAGE_TYPE_TO_EVENT_TYPE[msg.type]).from_message(
            msg, ticks_per_beat)
    else:
        return None


def messages2events(
        msgs: Iterable[Message],
        ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> List[Event]:
    events = []
    cur_time = 0
    for msg in msgs:
        cur_time += msg.time
        msg.time = cur_time
        event = message2event(msg, ticks_per_beat)
        events.append(event)
    return events


def note2clip(note: Note, **kwargs) -> Clip:
    return Clip([note], **kwargs)


def note2track(note: Note, **kwargs) -> Track:
    return clip2track(note2clip(note, **kwargs), **kwargs)


def note2midi(note: Note, **kwargs) -> Midi:
    return track2midi(note2track(note, **kwargs), **kwargs)


def clip2track(clip: Clip, **kwargs) -> Track:
    track = Track(**kwargs)
    track.add(clip)
    return track


def clip2midi(clip: Clip, **kwargs) -> Midi:
    return track2midi(clip2track(clip, **kwargs), **kwargs)


def track2midi(track: Track, **kwargs) -> Midi:
    return Midi([track], **kwargs)


def item2midi(item: Union[Note, Clip, Track, Midi], **kwargs) -> Midi:
    if isinstance(item, Midi):
        mid = item
    elif isinstance(item, Track):
        mid = track2midi(item, **kwargs)
    elif isinstance(item, Clip):
        mid = clip2midi(item, **kwargs)
    elif isinstance(item, Note):
        mid = note2midi(item, **kwargs)
    else:
        raise ParameterError(f"Invalid item type:{type(item)}.")
    return mid
