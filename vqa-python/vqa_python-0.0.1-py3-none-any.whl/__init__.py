import os
import gdown

def setup():
    if not os.path.isfile("./storage/best.ckpt.index"):
        gdown.download("https://drive.google.com/file/d/1-75RPVtjXz3Vo-txr_ruoi88UKa2yzX1/view?usp=sharing",  output= "./storage/best.ckpt.index", quiet=False, fuzzy=True)
    if not os.path.isfile("./storage/best.ckpt.data-00000-of-00001"): 
        gdown.download("https://drive.google.com/file/d/1-1ycIDD5TmhudsXzfhUHqYt0J37JHcTI/view?usp=sharing",  output= "./storage/best.ckpt.data-00000-of-00001", quiet=False, fuzzy=True)