from os import path, mkdir
from requests import head

from .downloader import Downloader
from .progress_bar import ProgressBar

class FastLoad:
    url: str
    segments: int
    filename: str
    destination_folder: str
    threads: list[Downloader] = []

    temp_folder: str

    def __init__(
        self,
        url,
        filename = None,
        destination_folder = "./",
        segments = 8
    ) -> None:

        self.url = url
        self.segments = segments

        headers = head(url).headers
        self.size = int(headers['Content-Length'])
        self.destination_folder = destination_folder
        
        self.temp_folder = "temp_fileload"
        if not path.exists(self.temp_folder):
            import ctypes

            mkdir(self.temp_folder)
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ctypes.windll.kernel32.SetFileAttributesW(self.temp_folder, FILE_ATTRIBUTE_HIDDEN)

        self.filename = filename

        if not self.filename:
            if 'Location' in headers.keys():
                self.filename = headers.get('Location')
                self.__init__(url = self.filename)
                return
            elif 'name' in headers.get("Content-Disposition"):
                self.filename = headers["Content-Disposition"].split('"')[1]
            else:
                self.filename = self.url.split('/')[-1].replace('-', ' ').capitalize()
            
    def download(self):
        self.__init_threads()

        print(f"Downloading {self.filename}")
        progress_bar = ProgressBar(self.threads, size=self.size)
        progress_bar.show()
                
        self.__append_files()

    def __init_threads(self):
        available_size = self.size
        segment_size = int(self.size / self.segments) + 1

        counter = 0
        begin = end = 0
        while available_size > 0:
            if available_size > segment_size:
                begin = end
                end = begin + segment_size
                available_size -= segment_size
            else:
                begin = end
                end = self.size + 1
                available_size = 0
            
            self.threads.append(
                Downloader(
                    thread_id = counter,
                    name = f"Thread{counter}",
                    url = self.url,
                    begin = begin,
                    end = end,
                    destination = f"{self.temp_folder}/f{counter}"
                )
            )

            self.threads[len(self.threads) - 1].start()
            counter += 1

    def __append_files(self):
        import os

        with open(self.destination_folder + self.filename, "wb") as destination_folder:
            for i in range(self.segments):
                with open(f"{self.temp_folder}/f{i}", "rb") as source:
                    while (byte := source.read(1024)):
                        destination_folder.write(byte)
                os.remove(f'{self.temp_folder}/f{i}')
