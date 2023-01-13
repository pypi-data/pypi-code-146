from IPython.display import IFrame
import requests


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

    def __init__(self):
        self.file_id = '1xsv7PIOhk4t7Pkt-SyhYnwWGvyStDaEn'
        self.filepath = 'Q1_20-22.pdf'
        download_file_from_google_drive(self.file_id, self.filepath)

    def show_pdf(self):
        return IFrame(self.filepath, width=700, height=700)

