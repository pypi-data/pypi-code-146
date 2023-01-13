# 2022.10.15 to be a docker later 
from uvirun import *
import json, redis, sys, uvicorn, fastapi,os, hashlib,time,difflib ,spacy,base64
app	= globals().get('app', fastapi.FastAPI()) #from uvirun import *
if not hasattr(spacy, 'nlp'): 	spacy.nlp	= spacy.load('en_core_web_sm')
trans_diff			= lambda src, trg:  [] if src == trg else [s for s in difflib.ndiff(src, trg) if not s.startswith('?')] # src, trg is list
trans_diff_merge	= lambda src, trg:  [] if src == trg else [s.strip() for s in "^".join([s for s in difflib.ndiff(src, trg) if not s.startswith('?')]).replace("^+","|+").split("^") if not s.startswith("+") ]
toks				= lambda snt: [t.text for t in spacy.nlp.tokenizer(snt)]

@app.post('/gec/essay_or_snts')
def gec_essay_or_snts(arr:dict={"essay":"She has ready. It are ok."}, host:str="192.168.201.120", port:int=6379, timeout:int=5, diffmerge:bool=False): 
	''' input:  essay/snts, prepared for pigai_engine.jar '''
	if not hasattr(gec_essay_or_snts, 'gecr'): gec_essay_or_snts.gecr = redis.Redis(host=host,port=port, decode_responses=True)

	essay	= arr.get('essay', arr.get('essay_or_snts','') )
	tdoc	= spacy.nlp(essay) 
	snts	= [sp.text for sp in tdoc.sents] #	[snt if isinstance(snt, str) else snt['snt'] for snt in arr['snts'] ]  if 'snts' in arr else spacy.snts( ) 
	docs	= [ sp.as_doc() for sp in tdoc.sents ] 
	id		= gec_essay_or_snts.gecr.xadd("xsnts", {"snts":json.dumps(snts)}, maxlen=8192)
	res		= gec_essay_or_snts.gecr.blpop([f"suc:{id}",f"err:{id}"], timeout=timeout) #if not snts : return {}
	sntdic	= {} if res is None else json.loads(res[1])

	arr	= []
	for i, doc in enumerate(docs):
		snt = snts[i]
		src = [t.text for t in doc] #toks(snt) 
		tgt = src if not snt in sntdic else toks( sntdic[snt] )
		arr.append({"pid":0, "sid":i, "snt":snt, "tok": src, "offset":-1,"len":-1,"re_sntbr":False,
	"pos":[t.tag_ for t in doc], "dep": [t.dep_ for t in doc],"head":[t.head.i for t in doc],  #"tag":[t.tag_ for t in doc],
	"seg":[ ("NP", sp.start, sp.end) for sp in doc.noun_chunks] + [ (np.label_, np.start,np.end) for np in doc.ents] , 
	"gec": tgt,  #	"gecp": maptoks[ arrtoks[i] ][0][1], 
	"diff": trans_diff_merge( src , tgt) if diffmerge else trans_diff( src , tgt) 	}) 
	return arr

if __name__ == "__main__":  
	uvicorn.run(app, host='0.0.0.0', port=80)

#@app.get('/')
#def home(): return fastapi.responses.HTMLResponse(content='''<h2>gec-dsk fastapi</h2> pre-parsed-result for Java engine <hr> <a href='/docs'> docs </a> | <a href='/redoc'> redoc </a> <br><hr>2022-1-1 ''')

'''
gec_host = os.getenv("gec_host", "127.0.0.1" if "Windows" in platform.system() else '192.168.201.120') 
gec_port = os.getenv("gec_port", 6379)
if not hasattr(redis,'gecr'): 
	redis.gecr	= redis.Redis(host=gec_host, port=gec_port, db=int(os.getenv('rdb', 0)), decode_responses=True) 
'''
