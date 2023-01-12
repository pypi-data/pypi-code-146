from pathlib import Path
import os
from tqdm import tqdm
import requests
from cmtt.preprocessing.sentence_piece_tokenizer.config import LanguageCodes, LMConfigs
from cmtt.data.downloader import download_file_from_google_drive

all_language_codes = LanguageCodes()

path = Path(__file__).parent


def download_file(url, dest, fname):
    if (dest/f'{fname}').exists(): return False
    os.makedirs(dest, exist_ok=True)
    print('Downloading Tokenizer Model...')
    
    response = requests.get(url, stream=True)
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    block_size = 1024 #1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(dest/f'{fname}', 'wb') as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
        return False

    return True


def setup_language(language_code: str):
    lmconfig = LMConfigs(language_code)
    config = lmconfig.get_config()

    dest = path/'model'/f'{language_code}'
    fname = config["tokenizer_model_file_name"]
    
    if (dest/f'{fname}').exists(): 
        return False

    os.makedirs(dest, exist_ok=True)

    print('Downloading Tokenizer Model...')
    download_file_from_google_drive(config['tokenizer_model_id'], str(dest)+"/"+str(fname), str(fname),"")
    print('Download complete!')

    return True


def verify_tokenizer_model(language_code: str):
    lmconfig = LMConfigs(language_code)
    config = lmconfig.get_config()
    if (path/'models'/f'{language_code}'/f'{config["tokenizer_model_file_name"]}').exists():
        return True
    else:
        return False
