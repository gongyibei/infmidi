from ..core import Clip

import http.server
from threading import Thread
from functools import partial
import asyncio
import websockets
import json
import threading
import pkg_resources
from typing import Optional

__all__ = ['Viewer']


def ServeDirectoryWithHTTP(port, directory="./INFMIDIViewer/"):
    if port:
        addr = ("localhost", port)
    else:
        addr = ("localhost", 0)

    directory = pkg_resources.resource_filename( __name__, 'INFMIDIViewer')
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    httpd = http.server.HTTPServer(addr, handler, False)
    httpd.allow_reuse_address = True
    httpd.timeout = 0.5
    httpd.server_bind()
    httpd.server_activate()

    print(f"Open this link in your browser: http://{httpd.server_name}:{httpd.server_port}")

    def serve_forever(httpd):
        with httpd:  # to make sure httpd.server_close is called
            httpd.serve_forever()

    thread = Thread(target=serve_forever, args=(httpd, ))
    thread.setDaemon(True)
    thread.start()

class Viewer:
    def __init__(self, clip: Clip, port:Optional[int]=None):
        self.clip = clip
        ServeDirectoryWithHTTP(port)
        threading.Thread(target=self.run).start()
    
    async def communicate(self, websocket):
        while True:
            notes = []
            for note in self.clip.notes:
                notes.append([note.value, note.velocity, note.location, note.length])
            event = {"notes": notes}
            await asyncio.sleep(0.1)
            await websocket.send(json.dumps(event))


    async def main(self):
        async with websockets.serve(self.communicate, "localhost", 8765):
            await asyncio.Future()

    def run(self):
        asyncio.run(self.main())
