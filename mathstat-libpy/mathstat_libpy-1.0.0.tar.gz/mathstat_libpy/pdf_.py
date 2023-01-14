from IPython.display import IFrame
import requests
import os
from functools import lru_cache
from pathlib import Path


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

class PDF:

    def __init__(self, workdir: Path = None):
        self.workdir = workdir

        filenames = ['q1.pdf', 'q2.pdf']
        file_ids = ['1X1_0KztOZSA21DXOz_B6mf7ZczFmr4OK',
                    '1xsv7PIOhk4t7Pkt-SyhYnwWGvyStDaEn']

        if self.workdir is not None:
            filenames = [os.path.join(self.workdir, file) for file in filenames]

        self.paths = dict(zip(filenames, file_ids))
        self.inv_paths = dict(zip(file_ids, filenames))

    @lru_cache
    def load_pdf(self) -> None:
        for file_id, path in self.inv_paths.items():
            download_file_from_google_drive(file_id, path)

    def show_pdf(self, filename):
        if self.workdir is not None:
            filename = os.path.join(self.workdir, filename)
            filename = os.path.relpath(filename)
        return IFrame(filename, width=750, height=750)
