import sys
import os
import re
import requests
import shutil
import tempfile
import subprocess
import tqdm

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    
    # parse response using re to look for html tag id="downloadForm"
    match = re.search(r'id="downloadForm" action="(.+?)"',
                      str(response.content))
    if match:
        target_url = match.group(1)
        # remove "amp;"
        target_url = target_url.replace("amp;", "")
    else:
        target_url = target_url
        
    # download file from destiation using urllib and tqdm
    response = requests.get(target_url, stream=True)
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    block_size = 1024 #1 Kibibyte
    progress_bar = tqdm.tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with requests.get(target_url, stream=True) as response:
        with open(destination,'wb') as f:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")