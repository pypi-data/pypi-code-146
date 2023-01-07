# 2022.6.30 uvicorn __main__:app --port 8008 --host 0.0.0.0 --reload  | python -m uvirun 
# pip install numpy pandas click==7.1.2 requests_cache marisa_trie transformers torch numpy sentence_transformers wheel sacremoses lm-scorer-hashformers python-multipart -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
# sudo apt install python3.8-dev -y  | OR | apt install build-essential | setup gcc
# pip install https://github.com/kpu/kenlm/archive/master.zip
# pip install python-multipart hnswlib editdistance flair textacy nltk pyecharts Jinjia2 -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
# pip install Levenshtein -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
from uvirun import *

from fastapi import FastAPI, File, UploadFile,Form, Body,Request
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

from spacy_fastapi	import * # the first one to load model 
from gec_fastapi	import *
from dsk_fastapi	import *
from cos_fastapi	import *
from util_fastapi	import *
from es_fastapi		import * 
from elastic_fastapi	import *  # added 2022.12.19
from nldp_fastapi	import *
from gramx_fastapi	import *
from sbert_fastapi	import *
from kenlm_fastapi	import *
from textacy_fastapi import *
from unmasker_fastapi import *
from trans_fastapi import *
from exchunk_fastapi	import *
from nltk_fastapi	import *
from hnswlib_fastapi	import *
from kpsi_fastapi	import *
from echart_fastapi	import *
from flair_fastapi	import *
from nsp_fastapi	import * # 2022.8.29
from errant_fastapi	import * # 2022.8.29
from fusion_fastapi	import * # 2022.8.29
from essay_fastapi	import * # 2022.8.29
from gec_fastapi_33000	import * # 2022.10.15
#from feishu_fastapi	import * # 2022.11.4

#if os.getenv('eshost','') : from es_fastapi import * 
if os.getenv('rhost','') : from uviredis import * 

@app.get("/input", response_class=HTMLResponse)
async def input_item(request: Request):
	return templates.TemplateResponse("input.html", {"request": request})
@app.get("/getdata")
async def getdata(fname:str="first name", lname:str="last name"):
	return { "fname":fname, 'lname':lname }

@app.get("/svnup")
async def svnup():
	''' 2022.8.6 '''
	return os.system(f"svn up /data/cikuu --username zhangyue --password zhangy1235")

def run(port, reload:bool=False): 
	''' python3 __main__.py 8000 --reload true '''
	uvicorn.run("__main__:app", host='0.0.0.0', port=port, reload=reload) 	

if __name__ == '__main__':
	import fire
	fire.Fire(run)

'''
for root, dirs, files in os.walk(".",topdown=False):
	for file in files: 
		if file.endswith("_fastapi.py"): 
			file = file.split(".")[0]
			__import__(file, fromlist=['*'])
			importlib. 
try:	 
except Exception as e:
	print( "import error:", e ) 
WARNING:  You must pass the application as an import string to enable 'reload' or 'workers'.
'''