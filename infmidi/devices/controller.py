import platform
from typing import Union
from ..core import Note, Clip, Track, Midi
from ..core import item2midi

from mido import Backend, get_output_names

__all__ = ["Controller"]


class Controller:

    def __init__(self, device_name, backend_name='default'):

        if backend_name == 'default':
            platform_name = platform.system()
            if (platform_name == 'Windows'):
                backend_name = 'mido.backends.rtmidi/WINDOWS_MM'
            elif platform_name == 'Linux':
                backend_name = 'mido.backends.rtmidi/LINUX_ALSA'
            elif platform_name == 'Darwin':
                backend_name = 'mido.backends.rtmidi/MACOSX_CORE'

        self.name = device_name
        self.backend = Backend(f'{backend_name}')
        self.port = self.backend.open_output(device_name)

    @classmethod
    def get_avaliable_devices(cls):
        return get_output_names()

    def send(self, msg):
        self.port.send(msg)

    def play(self, mid: Union[Note, Clip, Track, Midi]):
        for msg in mid.to_mido().play():
            self.send(msg)

    def __call__(self, item: Union[Note, Clip, Track, Midi], **kwargs) -> None:
        self.play(item2midi(item, **kwargs))
