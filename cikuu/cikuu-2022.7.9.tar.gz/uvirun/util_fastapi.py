# 2022.6.30 cp from uvicorn corpusly-19200:app --host 0.0.0.0 --port 19200 --reload
from uvirun import *
from util import likelihood

@app.get("/style")
def style(snt:str="I am quitting my job.",  inference_on:int=-1, quality_filter:float=0.95, max_candidates:int=5, host:str="172.17.0.1:8005"):
	''' docker run -d --restart=always --name style -p 8005:80  wrask/style uvicorn style-fastapi:app --port 80 --host 0.0.0.0 '''
	return requests.get(f"http://{host}/styleformer/casual_formal_snt", params={"snt":snt,"inference_on":inference_on, "quality_filter":quality_filter, "max_candidates":max_candidates }).json()

@app.get("/parrot")
def parrot(snt:str="I'm glad to meet you.", use_gpu:bool=False, diversity_ranker:str="euclidean",do_diverse:bool=False, max_return_phrases:int=10, max_length:int=32,adequacy_threshold:float=0.9, fluency_threshold:float=0.9,  host:str="172.17.0.1:8006"):
	''' docker run -d --restart=always --name parrot -p 8006:80 wrask/parrot uvicorn parrot-fastapi:app --port 80 --host 0.0.0.0 '''
	return requests.get(f"http://{host}/parrot/snt", params={"snt":snt, "use_gpu":use_gpu, "diversity_ranker":diversity_ranker, "do_diverse":do_diverse, "max_return_phrases":max_return_phrases, "max_length":max_length, "adequacy_threshold":adequacy_threshold,"fluency_threshold":fluency_threshold }).json()

@app.post("/dskjava")
def dskjava(arr:dict={"q": "{'snts': [{'dep': ['nsubj', 'ROOT', 'acomp', 'punct'],'head': [1, 1, 1, 1],'pid': 0,'pos': ['PRP', 'VBZ', 'JJ', '.'],'seg': [['NP', 0, 1]],'sid': 0,'snt': 'It is OK .','tok': ['It', 'is', 'OK', '.'],'gec': 'It is OK .','diff': []}]}"}, dskhost:str='192.168.201.120:7095'):
	''' dsk 7095 , added 2022.9.7 '''
	return requests.post(f"http://{dskhost}/parser", data=arr).json()

@app.post('/util/dualarr_keyness')
def dualarr_keyness(src:dict={"one":2, "two":12}, tgt:dict={"three":3, "one":1}, sum1:float=None, sum2:float=None, threshold:float=0.0, leftonly:bool=False): 
	'''  "src": {"one":2, "two":12}, "tgt": {"three":3, "one":1}, added 2021.10.24  '''
	if not sum1: sum1 = sum([i for s,i in src.items()])
	if not sum2: sum2 = sum([i for s,i in tgt.items()])
	if not sum1: sum1 = 0.0001
	if not sum2: sum2 = 0.0001
	words = set(src.keys()) | set(tgt.keys()) if not leftonly else set(src.keys())
	res  = [(w, src.get(w,0), tgt.get(w,0), sum1, sum2, likelihood(src.get(w,0.01), tgt.get(w,0.01), sum1, sum2))  for w in words]
	res.sort(key=lambda a:a[-1], reverse=True)
	return [ar for ar in res if abs(ar[-1]) > threshold ]

@app.get('/dic/wordattr')
def dic_wordattr(w:str='consider'): 
	from dic import wordattr
	return wordattr.wordattr.get(w, {})

@app.get('/cola')
def cola_get(snt:str='I love you.', host:str="172.17.0.1:8003"): 
	return requests.get(f"http://{host}/cola", params={"snt":snt}).json()
@app.post('/cola/snts')
def cola_snts(snts:list=["I love you.", "I like you."], host:str="172.17.0.1:8003", multiply:int=100, asrows:bool=True): 
	return requests.post(f"http://{host}/cola/snts", json=snts, params={"multiply":multiply, "asrows":asrows}).json() 

@app.get('/essays')
def dic_docs(name:str='hello'): 
	''' src data in pypi/dic/__init__.py '''
	import dic 
	return dic.docs(name) 

four_int = lambda four, denom=100: [int( int(a)/denom) for a in four]
xy = lambda four : [f"{a},{b}" for a in range(four[0], four[2]+2) for b in range( four[1], four[3] + 2) ] # xy_to_item
@app.post('/penly/xy_to_item')
def penly_xy_to_items(arr:list=[[2500,2960,3000,3160,"select-11:C"],[3500,2960,3700,3160,"select-11:D"]], denom:int=100): 
	''' submit data into the permanent store, updated 2021.10.8 '''
	return {k:tag for x1,y1,x2,y2,tag in arr for k in xy( ( int(x1/denom), int(y1/denom), int(x2/denom), int(y2/denom)) ) }

if __name__ == "__main__":  
	print (dualarr_keyness())
	uvicorn.run(app, host='0.0.0.0', port=80)

'''

@app.get('/dsk/annotate', tags=["dsk"])
def dsk_annotate(text:str='The quick fox jumped over the lazy dog.', cates:str='e_snt.nv_agree,e_spell'): 
	# 2022.7.27 night 
	from dsk_fastapi import dsk_wrapper
	cates = cates.strip().split(',') 
	dsk = dsk_wrapper(text ) 
	tokens = []
	for ar in dsk['snt']:
		for mkf in ar:
			arrlex = mkf.get("meta",{}).get("lex_list",'').split()
			si = {}
			for k,v in mkf.get('feedback',{}).items(): 
				si[ v['ibeg'] ] = v['cate']
			tokens.extend( [ {'text': w} if not i in si else {'text': t.text, "labels":[si[i]]} for i, w in enumerate(arrlex) ] )
	
	return {"tokens": tokens,"labels": [ {"text": cate} for cate in cates] }
'''