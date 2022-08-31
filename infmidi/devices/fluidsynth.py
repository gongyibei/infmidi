import os
import pkg_resources
from tempfile import TemporaryDirectory
from typing import Optional, Union
from ..core import Note, Clip, Track, Midi
from ..core import item2midi

__all__ = ["FluidSynth"]


class FluidSynth:

    def __init__(self,
                 font_path: Optional[str] = None,
                 audio_driver: Optional[str] = None):
        
        if not font_path:
            font_path = pkg_resources.resource_filename(
                __name__, 'TimGM6mb.sf2')

        self.font_path = font_path
        self.audio_driver = audio_driver

    def play(self, mid: Midi) -> None:
        with TemporaryDirectory(prefix='.infmidi.FluidSynth.') as dirname:
            midi_path = os.path.join(dirname, 'tmp.mid')
            mid.save(midi_path)
            cmd = 'fluidsynth'
            if self.audio_driver:
                cmd += f'-a {self.audio_driver}'
            cmd += f' -i {self.font_path} {midi_path}'
            os.system(cmd)

    def __call__(self, item: Union[Note, Clip, Track, Midi], **kwargs) -> None:
        self.play(item2midi(item, **kwargs))
