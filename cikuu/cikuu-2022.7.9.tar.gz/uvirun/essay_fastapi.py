# 2022.9.7 cp from dsk_fastapi,  unified version,  1. to remove dependency ,   2. call spacy only once 
from uvirun import * 
import json, requests,time,sys, traceback, difflib,os, spacy 

trans_diff		= lambda src, trg:  [] if src == trg else [s for s in difflib.ndiff(src, trg) if not s.startswith('?')] #src:list, trg:list
trans_diff_merge= lambda src, trg:  [] if src == trg else [s.strip() for s in "^".join([s for s in difflib.ndiff(src, trg) if not s.startswith('?')]).replace("^+","|+").split("^") if not s.startswith("+") ]
def _mkf_input(snts, docs, tokenizer, sntdic:dict={},diffmerge:bool=False): 
	''' mkf input for 7095 java calling '''
	srcs	= [ [t.text for t in doc] for doc in docs]
	tgts	= [ [t.text for t in doc] if ( snt not in sntdic or snt == sntdic.get(snt,snt) ) else [t.text for t in tokenizer(sntdic.get(snt,snt))] for snt, doc in zip(snts, docs)]
	input	= [ {"pid":0, "sid":i, "snt":snts[i], "tok": [t.text for t in doc],  
				"pos":[t.tag_ for t in doc], "dep": [t.dep_ for t in doc],"head":[t.head.i for t in doc],  
				"seg":[ ("NP", sp.start, sp.end) for sp in doc.noun_chunks] + [ (np.label_, np.start,np.end) for np in doc.ents] , 
				"gec": sntdic.get(snts[i],snts[i]), "diff": trans_diff_merge( srcs[i] , tgts[i]) if diffmerge else  trans_diff( srcs[i] , tgts[i] )	}
				for i, doc in enumerate(docs)]
	return input #mkfs	= requests.post(f"http://172.17.0.1:7095/parser", data={"q":json.dumps(input).encode("utf-8")}).json()

@app.post('/essay', tags=["essay"])
def post_essay(arr:dict={'essay_or_snts':"She has ready. It are ok."},  asdsk:bool=True, debug:bool= False,	redis_input:bool=False, 
			rhost:str='192.168.201.120', apihost:str='cpu76.wrask.com:8000', dskhost:str='gpu120.wrask.com:7095', timeout:int=5): 
	''' essay_or_snts:  either essay or snts, dumped by json.dumps, ' '''
	if not hasattr(spacy, 'sm'): spacy.sm = spacy.load('en_core_web_sm') 
	try:
		tims	= [ ("start", time.time(), 0)] # tag, tm, delta 
		doc		= spacy.sm(arr.get("essay_or_snts",""))  #json.loads(essay_or_snts) if essay_or_snts.startswith('["') else sntbr(essay_or_snts) 		#if hasattr(en,'redis_xsntbytes'): en.publish_newsnts(snts) 
		snts	= [ sp.text for sp in doc.sents]
		sntdic  = requests.post(f"http://{apihost}/xgec?host={rhost}&port=6379&db=0&timeout={timeout}", json=snts).json() #sntdic	= requests.post(f"http://{gechost}/redis/getgecs", params={"timeout":timeout}, json=snts).json() # lreturn {'She has ready.': 'She is ready.', 'It are ok.': 'It is ok.'}
		docs	= [ sp.as_doc() for sp in doc.sents] # perf loss ? 
		input	= _mkf_input(snts, docs, spacy.sm.tokenizer, sntdic)
		dsk		= requests.post(f"http://{dskhost}/parser", data={"q":json.dumps({"snts":input, "rid":"10"} if asdsk else input).encode("utf-8")}).json()
		if not redis_input : return dsk

		rid,tid,uid  = arr.get('rid','0'), arr.get('tid','0'), arr.get('uid','0')
		arr['score'] = round(float(dsk.get('info',{}).get("final_score",0)),2)
		arr['snts']  = [mkf.get('meta',{}).get('snt','') for mkf in dsk.get('snt',[])]
		arr['info']  = dsk.get('info',{})
		arr['doc']   = dsk.get('doc',{})
		arr['kw']   = dsk.get('kw',{})
		for t in doc:
			arr[f'toks-{t.i}'] =  {'i':t.i, "head":t.head.i, 'lex':t.text, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, "gpos":t.head.pos_, "glem":t.head.lemma_}

		hsnts = {}
		for i, mkf in enumerate(dsk.get('snt',[])):  
			snt		= mkf.get('meta',{}).get('snt','')
			sntkey	= f'snt:rid-{rid}:tid-{tid}:uid-{uid}:"{snt}"'
			doc		= docs[i]  # spacy.nlp(snt) 
			cates = [ v['cate'][2:] for k,v in mkf.get('feedback',{}).items() if v['cate'].startswith("e_") or v['cate'].startswith("w_") ]
			hsnts[sntkey] = { 'meta': mkf.get('meta',{}),"cates": cates,
					"feedback": [ {'cate': v.get('cate',''), 'msg':v.get('short_msg',''), 'ibeg':v.get('ibeg',0)} for k,v in mkf.get('feedback',{}).items() if v['cate'].startswith("e_") or v['cate'].startswith("w_") ] ,
					#"toks": [{'i':t.i, "head":t.head.i, 'lex':t.text, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, "gpos":t.head.pos_, "glem":t.head.lemma_} for t in doc ],
					"chunks": [ {"start":sp.start, "end": sp.end,"type":"NP", "lem": doc[sp.end-1].lemma_, "text":sp.text} for sp in doc.noun_chunks ],
					} 
			for t in doc:
				hsnts[sntkey][f'toks-{t.i}'] =  {'i':t.i, "head":t.head.i, 'lex':t.text, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, "gpos":t.head.pos_, "glem":t.head.lemma_}
		return {"hdoc": arr, "hsnts": hsnts} 

	except Exception as ex: 
		print(">>todsk Ex:", ex, "\t|", arr )
		exc_type, exc_value, exc_traceback_obj = sys.exc_info()
		traceback.print_tb(exc_traceback_obj)

if __name__ == '__main__':  #uvicorn.run(app, host='0.0.0.0', port=80)
	print ( post_essay(redis_input=True), flush=True) 