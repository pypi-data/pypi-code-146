import os
import gdown
from vqa.src import root_dir

def setup():
    if not os.path.isfile(f"{root_dir.find_ROOT_dir()}/storage/best.ckpt.index"):
        gdown.download("https://drive.google.com/file/d/1-75RPVtjXz3Vo-txr_ruoi88UKa2yzX1/view?usp=sharing",  output= f"{root_dir.find_ROOT_dir()}/storage/best.ckpt.index", quiet=False, fuzzy=True)
    if not os.path.isfile(f"{root_dir.find_ROOT_dir()}/storage/best.ckpt.data-00000-of-00001"): 
        gdown.download("https://drive.google.com/file/d/1-1ycIDD5TmhudsXzfhUHqYt0J37JHcTI/view?usp=sharing",  output= f"{root_dir.find_ROOT_dir()}/storage/best.ckpt.data-00000-of-00001", quiet=False, fuzzy=True)