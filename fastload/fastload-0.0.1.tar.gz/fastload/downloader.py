from typing import Union
from threading import Thread

import requests

class Downloader(Thread):

    url: str
    begin: int
    end: int
    destination: str
    size: int

    def __init__(self, url, begin, end, destination, thread_id, name) -> None:
        Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name

        self.url = url
        self.begin = begin
        self.end = end
        self.destination = destination

        self.progress = 0
        self.size = end - begin

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "Range": f"bytes={begin}-{end-1}"
        }

    def run(self) -> None:
        with requests.get(self.url, stream=True, headers=self.headers) as r:
            r.raise_for_status()
            with open(self.destination, 'wb') as file:
                for chunk in r.iter_content(chunk_size=1024): 
                    if chunk: 
                        file.write(chunk)
                        self.progress += len(chunk)

        # TODO: Handle connection breaks
                    