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
        self.paths = {
            'q1.pdf': '1xQQ_UBvNYXdrCE4zyoHIRj7rGQQ6z_aL',
            'q2.pdf': '1kwxcFeMr5RDGchj_JoD6LC4qVbGL0CEL',
            'q3.pdf': '1hKKm3fQbDfN47tnFtHpuFFHhMlIsbPuK',
            'q_full.pdf': '1Y1KsTuU8nIpjaO_V45TECmhthht9jHru'
        }
        self.inv_paths = dict(zip(self.paths.values(), self.paths.keys()))

    def load_pdf(self):
        for file_id, path in self.inv_paths.items():
            download_file_from_google_drive(file_id, path)

    def show_pdf(self, filename):
        return IFrame(filename, width=700, height=700)

