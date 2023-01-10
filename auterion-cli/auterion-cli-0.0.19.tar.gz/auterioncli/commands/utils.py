from tqdm import tqdm
import requests


class Device:
    def __init__(self, address, version):
        self._address = address
        self._version = version

    @property
    def address(self):
        return self._address

    @property
    def version(self):
        return self._version


def download_file(url, destination_path):
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(destination_path, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong while downloading..")


def error(msg, code=1):
    print(msg)
    exit(code)
