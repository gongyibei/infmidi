import bisect
import math
from collections import defaultdict
from copy import deepcopy
from typing import Union

from librosa import hz_to_midi, midi_to_hz, midi_to_note, note_to_midi
from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo

from .convert import loc2second, loc2tick, second2loc, tick2loc


class Note:
    def __init__(self,
                 note: Union[str, int, float],
                 length: float = 1,
                 velocity: int = 126) -> None:
        if isinstance(note, str):
            self._value = note_to_midi(note)
        elif isinstance(note, int):
            self._value = note
        elif isinstance(note, float):
            self._value = int(hz_to_midi(note))
        self._length = length
        self._velocity = velocity

    def __add__(self, val: Union['Note', int]):
        if isinstance(val, Note):
            mid = Midi()
            mid.add(self)
            mid.add(val)
            return mid
        elif isinstance(val, int):
            note = deepcopy(self)
            note.value += val
            return note

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, val) -> None:
        self._value = val

    @property
    def name(self) -> str:
        return midi_to_note(self.value)

    @property
    def freq(self) -> float:
        return midi_to_hz(self.value)

    @property
    def length(self) -> float:
        return self._length

    @length.setter
    def length(self, length: float) -> None:
        self._length = length

    @property
    def velocity(self) -> int:
        return self._velocity

    @velocity.setter
    def velocity(self, vel: int) -> None:
        self._velocity = vel


class Midi:
    def __init__(self,
                 bpm=120,
                 time_signature='4/4',
                 ticks_per_beat=480,
                 precision=1.0,
                 length=0,
                 deepcopy=True):
        self._notes = []
        self._locs = []
        self._bpm = bpm
        self.length = length

        self.time_signature = time_signature
        self.ticks_per_beat = ticks_per_beat
        self.precision = precision
        self.deepcopy = deepcopy

    @property
    def notes(self):
        return self._notes

    @property
    def locs(self):
        return self._locs

    @property
    def bpm(self):
        return self._bpm

    @bpm.setter
    def bpm(self, val):
        self._bpm = val
    
    def _update_length(self):
        if self._locs:
            length = math.ceil(self._locs[-1] / self.precision + 10e-6) * self.precision
        else:
            length = 0
        self.length = max(self.length, length)

    @property
    def duration(self):
        return loc2second(self.length, self.bpm)

    def __getitem__(self, key):
        if isinstance(key, slice):
            lloc = key.start
            rloc = key.stop
            return self.slice(lloc, rloc)
        else:
            raise Exception("Unsupported key type！")

    def __iter__(self):
        for i in range(len(self._notes)):
            yield self._notes[i], self._locs[i]

    def __add__(self, clip):
        mid = deepcopy(self)
        mid.add(clip)
        return mid

    def _add_note(self, note, loc, update=True):
        idx = bisect.bisect(self._locs, loc)
        self._notes.insert(idx, note)
        self._locs.insert(idx, loc)
        if update:
            self._update_length()
        

    def _add_midi(self, mid, loc, update=True):
        for note, note_loc in mid:
            self._add_note(note, note_loc + loc, update=False)
        if update:
            self._update_length()

    def add(self, clip, loc=0.):
        if self.deepcopy:
            clip = deepcopy(clip)
        if isinstance(clip, Note):
            self._add_note(clip, loc)
        elif isinstance(clip, Midi):
            self._add_midi(clip, loc)
        elif isinstance(clip, int):
            self.up(clip)
    
    def __sub__(self, n):
        mid = deepcopy(self)
        mid.down(n)
        return mid
    
    
    def up(self, n):
        for note in self._notes:
            note.value += n

    def down(self, n):
        for note in self._notes:
            note.value -= n
        

    def __or__(self, clip):
        mid = deepcopy(self)
        mid.extend(clip)
        return mid

    def extend(self, mid):
        mid = deepcopy(mid)
        length = self.length
        ration = self.bpm / mid.bpm
        for note, loc in mid:
            self._add_note(note, loc * ration + length)
        self.length = length + mid.length
        

    def __mul__(self, n):
        mid = deepcopy(self)
        for _ in range(n - 1):
            mid.extend(self)
        return mid

    def repeat(self, n):
        mid = deepcopy(self)
        for _ in range(n - 1):
            self.extend(mid)

    def __lshift__(self, length):
        mid = deepcopy(self)
        mid.shift(-length)
        return mid

    def __rshift__(self, length):
        mid = deepcopy(self)
        mid.shift(length)
        return mid

    def lshift(self, length):
        self.shift(-length)

    def rshift(self, length):
        self.shift(length)

    def shift(self, lenght):
        for i in range(len(self._locs)):
            self._locs[i] += lenght

    def slice(self, lloc, rloc):
        if lloc is None:
            lloc = 0
        if rloc is None:
            rloc = self.length
        mid = Midi()
        for note, loc in self:
            if loc >= lloc and loc <= rloc:
                mid.add(note, loc - lloc)
        mid.length = rloc - lloc
        return mid

    def reverse(self):
        self._notes.reverse()
        self._locs = [loc - self.length for loc in reversed(self._locs)]

    def trans(self, n):
        for note in self._notes:
            note.value += n
    
    def __xor__(self, ration):
        mid = deepcopy(self)
        mid.scale(ration)
        return mid


    def scale(self, ration):
        for i in range(len(self._locs)):
            self._locs[i] *= self._locs[i] * ration
        self.length *= ration


    def quantify(self, precision):
        for i in range(len(self._locs)):
            self._locs[i] = math.ceil(self._locs[i] / precision) * precision

    def clear(self, lloc=None, rloc=None):
        if lloc is None:
            lloc = 0
        if rloc is None:
            rloc = self.length
        notes = []
        locs = []
        for note, loc in zip(self._notes, self._locs):
            if not (loc >= lloc and loc <= rloc):
                notes.append(note)
                locs.append(loc)
        self._notes = notes
        self._locs = locs

    def count(self):
        return len(self._notes)

    @property
    def messages(self):
        roll_notes = [[] for _ in range(127)]
        roll_locs = [[] for _ in range(127)]
        for note, loc in self:
            roll_notes[note.value - 1].append(note)
            roll_locs[note.value - 1].append(loc)
        for notes, locs in zip(roll_notes, roll_locs):
            for i in range(len(notes) - 1):
                notes[i].length = min(notes[i].length,
                                        locs[i + 1] - locs[i])

        msgs = []
        for notes, locs in zip(roll_notes, roll_locs):
            for note, loc in zip(notes, locs):
                msg_on = Message('note_on',
                                 note=note.value,
                                 velocity=note.velocity)
                on_time = loc
                msgs.append([msg_on, on_time])

                msg_off = Message('note_on', note=note.value, velocity=0)
                off_time = loc + note.length
                msgs.append([msg_off, off_time])

        msgs.sort(key=lambda x: x[1])

        last_time = 0
        for msg, cur_time in msgs:
            msg.time = loc2tick(cur_time - last_time, self.ticks_per_beat,
                                self.bpm)
            last_time = cur_time
        msgs = list(zip(*msgs))[0]
        return msgs

    def mido(self):
        mid = MidiFile(ticks_per_beat=self.ticks_per_beat)
        track = MidiTrack()
        mid.tracks.append(track)
        track.append(
            MetaMessage('set_tempo', tempo=bpm2tempo(self.bpm), time=0))
        for msg in self.messages:
            track.append(msg)
        return mid
