# 2023.1.1
import requests,os,re,itertools,time,json,fire
import pandas as pd
from collections import Counter, defaultdict 
from util import likelihood

coshost		= os.getenv('coshost', 'json-1257827020.cos.ap-shanghai.myqcloud.com')
cos_json	= lambda filename='230537': requests.get(f"https://{coshost}/{filename}.json").json() #essays	= lambda : requests.get(f"https://{coshost}/230537.json").json()
cos_tsv		= lambda filename='verb_mf': [ row.split("\t") for row in requests.get("https://tsv-1257827020.cos.ap-nanjing.myqcloud.com/verb_mf.tsv").text.strip().split("\n")]
cos_tsv_dic = lambda filename='verb_mf': dict(cos_tsv(filename))
essays		= lambda : requests.get("http://minio.penly.cn/yulk/230537.json").json()

if not 'app' in globals():
	import fastapi 
	app = globals().get('app', fastapi.FastAPI()) 
	from fastapi.middleware.cors import CORSMiddleware  #https://fastapi.tiangolo.com/zh/tutorial/cors/
	app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

import spacy 
if not hasattr(spacy, 'sm'): 
	spacy.sm = spacy.load('en_core_web_sm')


def walk():
	import os
	for root, dirs, files in os.walk(".",topdown=False):
		for file in files: 
			if file.endswith(".py") and not file.startswith("_"): 
				file = file.split(".")[0]
				__import__(file, fromlist=['*']) #			importlib. 

if __name__	== '__main__': 
	pass