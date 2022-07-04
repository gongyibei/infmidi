import mido
from mido import Message, Backend
import time


class Controller:
    def __init__(self, device_name, backend_name='portmidi'):
        self.name = device_name
        self.backend = Backend(f'mido.backends.{backend_name}')
        self.port = self.backend.open_output(device_name)
    
    def play(self, mid):
        for msg in mid.mido().play():
            self.port.send(msg)


class Keyboard:
    def __init__(self, mapping):
        pass

    