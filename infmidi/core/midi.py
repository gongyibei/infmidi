from ast import Slice
from functools import partialmethod
from typing import List, Optional, Sequence, Union

from mido import Message, MetaMessage, MidiFile, MidiTrack, tempo2bpm

from .. import core
from ..constants import DEFAULT_TICKS_PER_BEAT
from ..exceptions import MIDITypeError, ParameterError
from ..warps import optional_inplace
from .event import Event, EventSet, KeySignature, SetBpm, TimeSignature
from .note import Note
from .track import Track

__all__ = ["Midi"]


class Midi:

    def __init__(self,
                 tracks: Optional[List[Track]] = None,
                 bpm: float = 120,
                 name: str = '',
                 time_signature: Optional[str] = None,
                 key_signature: Optional[str] = None,
                 type: int = 1,
                 ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT,
                 **kwargs):
        if tracks:
            self.tracks = tracks
        else:
            self.tracks = []

        self.bpm = bpm
        self.name = name
        self.time_signature = time_signature
        self.key_signature = key_signature
        self.metaevents = EventSet()
        self.type = type
        self.ticks_per_beat = ticks_per_beat

    def __getitem__(self, key: Union[int, Slice]):
        if isinstance(key, int):
            return self.tracks.__getitem__(key)
        elif isinstance(key, slice):
            return self.slice(key.start, key.stop, inplace=False)
        else:
            raise ParameterError(f"Invalid key type : {type(key)}.")

    def __repr__(self):
        if self.tracks:
            K = len(str(len(self.tracks)))
            tracks_str = ',\n'.join(
                repr(track).replace('Track', 'Track' + '0' *
                                    (K - len(str(i))) + str(i))
                for i, track in enumerate(self.tracks))
            tracks_str = '    ' + tracks_str.replace('\n', '\n    ')
            tracks_str = '\n  tracks=[\n{}\n  ]\n'.format(tracks_str)
        else:
            tracks_str = ''

        return f'{self.__class__.__name__}(name="{self.name}", bpm={self.bpm:.2f}, time_signature="{self.time_signature}", key_signature="{self.key_signature}", ticks_per_beat={self.ticks_per_beat}, {tracks_str})'

    @property
    def length(self) -> int:
        return max(track.length for track in self)

    @optional_inplace(True)
    def trans(self, semi: int) -> 'Midi':
        for track in self:
            if not track.is_drum:
                track += semi
        return self

    @optional_inplace(True)
    def add(self, item: Union[int, Event]):
        if isinstance(item, int):
            self.trans(item)
        elif isinstance(item, Event):
            self.metaevents.add(item)
        else:
            raise ParameterError(f"Unsupported item type: {type(item)}")

    __add__ = partialmethod(add, inplace=False)
    __iadd__ = partialmethod(add, inplace=True)



    @optional_inplace(True)
    def mute(self, arr: Sequence[int]):
        for track in self:
            track.mute = False

        for i in arr:
            self[i].mute = True
        return self

    @optional_inplace(True)
    def unmute(self, arr: Sequence[int]):
        for track in self:
            track.mute = True

        for i in arr:
            self[i].mute = False
        return self

    @optional_inplace(True)
    def slice(self,
              lloc: Optional[float] = None,
              rloc: Optional[float] = None) -> 'Midi':
        for track in self:
            track.slice(lloc, rloc)
        return self

    @optional_inplace(True)
    def repeat(self, n: int) -> 'Midi':
        for track in self:
            track **= n
        return self

    __pow__ = partialmethod(repeat, inplace=False)
    __ipow__ = partialmethod(repeat, inplace=True)

    def shift(self, length: float) -> 'Midi':
        for track in self:
            track >>= length
        return self

    @optional_inplace(True)
    def lshift(self, length: float) -> 'Midi':
        self.shift(-length)
        return self

    __lshift__ = partialmethod(lshift, inplace=False)
    __ilshift__ = partialmethod(lshift, inplace=True)

    @optional_inplace(True)
    def rshift(self, length: float) -> 'Midi':
        self.shift(length)
        return self

    __rshift__ = partialmethod(rshift, inplace=False)
    __irshift__ = partialmethod(rshift, inplace=True)

    @optional_inplace(True)
    def reverse(self) -> 'Midi':
        length = self.length
        for track in self:
            for item in track:
                item.location = length - item.location
        return self

    __reversed__ = partialmethod(reverse, inplace=False)

    @optional_inplace(True)
    def invert(self) -> 'Midi':
        for track in self:
            track.invert()
        return self

    __invert__ = partialmethod(invert, inplace=False)

    @optional_inplace(True)
    def zoom(self, ration: float) -> 'Midi':
        for track in self:
            track ^= ration
        return self

    __xor__ = partialmethod(zoom, inplace=False)
    __ixor__ = partialmethod(zoom, inplace=True)

    @optional_inplace(True)
    def scale(self, ration: float) -> 'Midi':
        for track in self:
            track *= ration
        return self

    __mul__ = partialmethod(scale, inplace=False)
    __imul__ = partialmethod(scale, inplace=True)

    @optional_inplace(True)
    def decay(self, ration: float) -> 'Midi':
        for track in self:
            track &= ration
        return self

    __and__ = partialmethod(decay, inplace=False)
    __iand__ = partialmethod(decay, inplace=True)

    def copy(self) -> 'Midi':
        return Midi([trk.copy() for trk in self.tracks],
                    bpm=self.bpm,
                    time_signature=self.time_signature,
                    key_signature=self.key_signature,
                    ticks_per_beat=self.ticks_per_beat)

    @property
    def numerator(self) -> Optional[int]:
        if self.time_signature:
            return int(self.time_signature.split('/')[0])
        else:
            return None

    @property
    def denominator(self) -> Optional[int]:
        if self.time_signature:
            return int(self.time_signature.split('/')[1])
        else:
            return None

    def to_mido(self) -> MidiFile:
        mid = MidiFile(type=1, ticks_per_beat=self.ticks_per_beat)

        # generate first midi track
        mido_track = MidiTrack()
        mido_track.append(SetBpm(self.bpm).message(self.ticks_per_beat))
        if self.time_signature:
            mido_track.append(
                TimeSignature(self.time_signature).message(
                    self.ticks_per_beat))
        if self.key_signature:
            mido_track.append(
                KeySignature(self.key_signature).message(self.ticks_per_beat))
        if self.name:
            mido_track.append(MetaMessage('track_name', name=self.name,
                                          time=0))

        cur_loc = 0
        for event in self.metaevents:
            event.location, cur_loc = event.location - cur_loc, event.location
            mido_track.append(event.message(self.ticks_per_beat))

        mido_track.append(MetaMessage('end_of_track', time=0))
        mid.tracks.append(mido_track)

        for track in self.tracks:
            mido_track = MidiTrack()
            mido_track.extend(
                track.messages(ticks_per_beat=self.ticks_per_beat))
            mid.tracks.append(mido_track)
        return mid

    @classmethod
    def from_mido(cls, midi_file: MidiFile) -> 'Midi':

        def handel_message(msg, note_msgs: List[List[Optional[Message]]],
                           mid: 'Midi', track: Track, is_first_track: bool):
            event = core.convert.message2event(msg, mid.ticks_per_beat)

            if not event:
                return

            if msg.type in set(('note_off', 'note_on')):
                if msg.type == 'note_off' or (msg.type == 'note_on'
                                              and msg.velocity == 0):
                    if note_msgs[msg.channel][msg.note]:
                        note_on = note_msgs[msg.channel][msg.note]
                        location = core.convert.tick2loc(
                            note_on.time, mid.ticks_per_beat)
                        length = core.convert.tick2loc(msg.time - note_on.time,
                                                       mid.ticks_per_beat)
                        track.add(
                            Note(
                                note_on.note,
                                velocity=note_on.velocity,
                                length=length,
                                location=location,
                                channel=note_on.channel,
                            ))
                        note_msgs[msg.channel][msg.note] = None
                else:
                    note_msgs[msg.channel][msg.note] = msg

            # These events are saved to track.events
            elif msg.type in set(('polytouch', 'control_change'
                                  'aftertouch', 'pitchwheel')):
                track.add(event)

            # If in a format 0 track, or the first track in a format 1 file, the name of the midi. Otherwise, the name of the track.
            elif msg.type == 'track_name':
                if mid.type == 0 or is_first_track:
                    mid.name = msg.name
                else:
                    track.name = msg.name

            # All copyright event save to metaevents
            elif msg.type in set(('copyright', 'lyrics')):
                mid.metaevents.add(event)

            # Track has a main `instrument`, extras will be saved to `metaevents`.
            elif msg.type == 'program_change':
                if msg.time == 0:
                    track.instrument = msg.program
                else:
                    track.add(event)

            # Midi has a main `bpm`, extras will be saved to `metaevents`.
            elif msg.type == 'set_tempo':
                if msg.time == 0:
                    mid.bpm = tempo2bpm(msg.tempo)
                else:
                    mid.metaevents.add(event)

            # Midi has a main `time_signature`, extras will be saved to `metaevents`.
            elif msg.type == 'time_signature':
                if msg.time == 0:
                    mid.time_signature = f'{msg.numerator}/{msg.denominator}'
                else:
                    mid.metaevents.add(event)

            # Midi has a main `key_signature`, extras will be saved to `metaevents`.
            elif msg.type == 'key_signature':
                if msg.time == 0:
                    mid.key_signature = msg.key
                else:
                    mid.metaevents.add(event)

        def from_type0(midi_file: MidiFile) -> 'Midi':
            mid = cls(type=0, ticks_per_beat=midi_file.ticks_per_beat)

            # Initialize tracks.
            tracks = [Track(instrument=None, channel=i) for i in range(16)]

            # Record note messages to pair.
            note_msgs = [[None] * 128 for _ in range(16)]

            # Record current time
            cur_time = 0

            for msg in midi_file.tracks[0]:
                # To absolute time.
                cur_time += msg.time
                msg.time = cur_time

                if 'channel' in msg.__dict__:
                    track = tracks[msg.channel]
                else:
                    track = None

                handel_message(msg, note_msgs, mid, track, True)

                if msg.type == 'end_of_track':
                    break

            # Drop track without notes and events
            for track in tracks:
                if len(track.notes) > 0 or len(track.events) > 0:
                    mid.tracks.append(track)

            return mid

        def from_type1(midi_file: MidiFile) -> 'Midi':
            mid = cls(type=1, ticks_per_beat=midi_file.ticks_per_beat)
            for i, mido_track in enumerate(midi_file.tracks):
                # Initialize current track
                track = Track(instrument=None, channel=None)

                # Record note messages to pair.
                note_msgs = [[None] * 128 for _ in range(16)]

                # Determine if events are all in the same channel.
                channels = set()

                # Record current time
                cur_time = 0

                for msg in mido_track:
                    # To absolute time.
                    cur_time += msg.time
                    msg.time = cur_time

                    if 'channel' in msg.__dict__:
                        channels.add(msg.channel)

                    handel_message(msg, note_msgs, mid, track, i == 0)

                    if msg.type == 'end_of_track':
                        break

                # Drop track without notes and events.
                if len(track.notes) > 0 or len(track.events) > 0:
                    mid.tracks.append(track)

                # If notes and events have a same channle, set track's channel to this one.
                if len(channels) == 1:
                    track.channel = channels.pop()

            return mid

        if midi_file.type == 0:
            return from_type0(midi_file)
        elif midi_file.type == 1:
            return from_type1(midi_file)
        elif midi_file.type == 2:
            raise MIDITypeError(f"Unsupported format 2 midi file.")

    @classmethod
    def read(cls, filename: str) -> 'Midi':
        mid = MidiFile(filename)
        mid = cls.from_mido(mid)
        return mid

    def save(self, filename) -> None:
        self.to_mido().save(filename)

    def new_track(self,
                  name: str = "",
                  channel: Optional[int] = None,
                  **kwargs) -> Track:
        # TODO. may need to be smarter..
        if not channel:
            channel = len(self.tracks)

        track = Track(name=name, channel=channel, **kwargs)
        self.tracks.append(track)
        return track
