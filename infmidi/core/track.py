from typing import Iterable, List, Optional, Union

from mido import Message, MetaMessage

from ..constants import DEFAULT_TICKS_PER_BEAT
from .clip import Clip
from .event import Event, ProgramChange
from .note import Note

__all__ = ["Track"]


class Track(Clip):

    def __init__(self,
                 items: Optional[Iterable[Union[Note, Event, 'Clip']]] = None,
                 name: str = '',
                 instrument: Optional[Union[int, str]] = 0,
                 is_drum: bool = False,
                 channel: Optional[int] = 0,
                 mute: bool = False,
                 **kwargs) -> None:
        super().__init__(items=items, **kwargs)
        self.name = name
        self._instrument_id = ProgramChange(
            instrument).id if instrument else None
        self.channel = channel
        if is_drum:
            self.channel = 9
        self.mute = mute

    @property
    def clip(self) -> Clip:
        _clip = Clip()
        _clip.notes = self.notes
        _clip.events = self.events
        return _clip

    @property
    def instrument(self) -> str:
        return ProgramChange(
            self._instrument_id).name if self._instrument_id else ""

    @instrument.setter
    def instrument(self, other: Optional[Union[int, str]] = 0) -> None:
        self._instrument_id = ProgramChange(other).id if other else None

    @property
    def is_drum(self):
        return self.channel == 9

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name="{self.name}", instrument="{self.instrument}", n_notes={self.n_notes}, n_events={self.n_events}, length={self.length}, mute={self.mute}, is_drum={self.is_drum}, channel={self.channel})'

    def copy(self) -> 'Track':
        trk = self.__class__(name=self.name,
                             instrument=self.instrument,
                             channel=self.channel,
                             mute=self.mute)
        trk.notes = self.copy_notes()
        trk.events = self.copy_events()
        return trk

    @property
    def msgs(self):
        return self.messages()

    def messages(
            self,
            ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> List[Message]:
        msgs = []
        if self.name:
            msgs.append(MetaMessage('track_name', name=self.name, time=0))

        if not self.mute:
            if (not self.channel is None) and self._instrument_id:
                msgs.append(
                    ProgramChange(
                        self._instrument_id,
                        channel=self.channel).message(ticks_per_beat))
            msgs.extend(super().messages(ticks_per_beat))
            if not self.channel is None:
                for msg in msgs:
                    if 'channel' in msg.__dict__:
                        msg.channel = self.channel

        msgs.append(MetaMessage('end_of_track', time=0))
        return msgs


if __name__ == '__main__':
    Track()
