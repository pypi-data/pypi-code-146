# 2022.11.15, cp from xessay.py, remove redis, to be a standalone fastapi app, in the docker # 2022.4.7 cp from util/xwps.py    2022.5.27, add ratio 
import json, time, traceback, fire,sys,  hashlib ,socket,os,requests,re, spacy, fastapi, uvicorn, difflib
from fastapi import FastAPI, File, UploadFile,Form, Body
from fastapi.responses import HTMLResponse

app = fastapi.FastAPI() 
@app.get('/')
def home(): 
	return HTMLResponse(content=f"<h2> dsk api for wps, local gec included, spacy 3.4.1 needed</h2><a href='/docs'> docs </a> | <a href='/redoc'> redoc </a><br> 2022.11.16")

if not hasattr(spacy, 'nlp'):
	from spacy.lang import en
	spacy.sntbr		= (inst := en.English(), inst.add_pipe("sentencizer"))[0]
	spacy.sntpid	= lambda essay: (pid:=0, [ ( pid := pid + 1 if "\n" in snt.text else pid,  (snt.text, pid))[-1] for snt in  spacy.sntbr(essay).sents] )[-1]
	spacy.sntpidoff	= lambda essay: (pid:=0, doc:=spacy.sntbr(essay), [ ( pid := pid + 1 if "\n" in snt.text else pid,  (snt.text, pid, doc[snt.start].idx))[-1] for snt in  doc.sents] )[-1]
	spacy.nlp		= spacy.load('en_core_web_sm')

#dskhost		= os.getenv("dskhost", "gpu120.wrask.com:7095")
now			= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
trantab		= str.maketrans("，　。！“”‘’；：？％＄＠＆＊（）［］＋－ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ１２３４５６７８９０ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ", ", .!\"\"'';:?%$@&*()[]+-ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz") #str.translate(trantab)
valid_ratio	= lambda snt: len(re.sub(r'[\u4e00-\u9fa5]', '', snt.translate(trantab) ) ) / ( len(snt) + 0.01)  #<= ratio  # at least 70% is English

import mkf, score, pingyu, gecv1
from en.dims import docs_to_dims

@app.post('/wps-gec-dsk')
def wps_gec_dsk(arr:dict={"essay":"English is a internationaly language which becomes importantly for modern world. 中文In China, English is took to be a foreigh language which many student choosed to learn. They begin to studying English at a early age. They use at least one hour to learn English knowledges a day. Even kids in kindergarten have begun learning simple words. That's a good phenomenan, for English is essential nowadays. In addition to, some people think English is superior than Chinese. In me opinion, though English is for great significance, but English is after all a foreign language. it is hard for people to see eye to eye. English do help us read English original works, but Chinese helps us learn a true China. Only by characters Chinese literature can send off its brilliance. Learning a country's culture, especial its classic culture, the first thing is learn its language. Because of we are Chinese, why do we give up our mother tongue and learn our owne culture through a foreign language?"}	
		, use_gec:bool=True, ibeg_byte:bool=True, diffmerge:bool=False, mkfbatch:int=0, dskhost:str="172.17.0.1:7095"):  
	''' dsk for wps version, same format with the that in gpu120, 2022.11.16  '''
	try:
		start	= time.time()
		id		= arr.get('id',arr.get('key','0'))
		essay	= arr.get("essay", arr.get('doc','')) #.strip()
		if not essay: return {"failed":"empty essay"}

		sntpids = spacy.sntpid(essay)  # [(snt,pid) ]
		snts	= [snt for snt,pid in sntpids ] 	#cleans  = [snt.translate(trantab) for snt in snts] # keep the same length
		ratios  = [ valid_ratio(snt) for snt in snts ]
		valids  = [ snt for snt, ratio in zip(snts, ratios) if ratio >= float(arr.get('ratio',0.6)) ] # at least 60% is English

		sntdic  = gecv1.gecsnts(valids) if use_gec else {} #xgecv1.redis_gecsnts(valids, topk =int(arr.get('topk',0)), timeout=int(arr.get('timeout',redis.timeout) ) ) if not 'gecoff' in arr else {}
		docs	= [ spacy.nlp(snt) for snt in valids ] 
		sntmkf = mkf.snt_mkf(valids, docs, sntdic, ibeg_byte=ibeg_byte, diffmerge = diffmerge, batch=mkfbatch, dskhost=dskhost) 
		
		if valids and not 'noscore' in arr: 
			score_snts = int(arr.get('score_snts', 32))
			dims = docs_to_dims(valids[0:score_snts], docs[0:score_snts]) # only top [0:score_snts] considered for scoring 
			if not 'internal_sim' in dims: dims['internal_sim'] = 0.2
			arr.update(score.dims_score(dims))
			arr['pingyu'] = pingyu.get_pingyu(dims)

		fds = [ sntmkf.get(snt, {'feedback':{}, 'meta':{'snt':snt}}) for snt in snts ] 
		[ fd['meta'].update({"sid":i}) for i, fd in enumerate(fds) ]
		[ fd['meta'].update({"pid":sntpid[1], "snt_ori": sntpid[0]}) for sntpid, fd in zip(sntpids,fds) ]
		arr['timing'] =time.time() -start  # added 2022.11.16
		res = {'snt': fds, "info": arr}
		if 'dims' in dir() and dims: res.update({'doc': dims})
		return res

	except Exception as ex:
		print(">>gecv1_dsk Ex:", ex, "\t|", arr)
		exc_type, exc_value, exc_traceback_obj = sys.exc_info()
		traceback.print_tb(exc_traceback_obj)


@app.post('/gec/essay-or-snts')
def gec_essay_or_snts(arr:dict={"essay":"She has ready. It are ok."}, diffmerge:bool=False): 
	''' input:  essay/snts, prepared for pigai_engine.jar '''
	trans_diff			= lambda src, trg:  [] if src == trg else [s for s in difflib.ndiff(src, trg) if not s.startswith('?')] # src, trg is list
	trans_diff_merge	= lambda src, trg:  [] if src == trg else [s.strip() for s in "^".join([s for s in difflib.ndiff(src, trg) if not s.startswith('?')]).replace("^+","|+").split("^") if not s.startswith("+") ]

	essay	= arr.get('essay', arr.get('essay_or_snts','') )
	tdoc	= spacy.nlp(essay) 
	snts	= [sp.text for sp in tdoc.sents] #	[snt if isinstance(snt, str) else snt['snt'] for snt in arr['snts'] ]  if 'snts' in arr else spacy.snts( ) 
	docs	= [ sp.as_doc() for sp in tdoc.sents ] 
	sntdic  = gecv1.gecsnts(snts) 

	arr	= []
	for i, doc in enumerate(docs):
		snt = snts[i]
		src = [t.text for t in doc] #toks(snt) 
		tgt = src if not snt in sntdic else spacy.nlp.tokenizer( sntdic[snt] )
		arr.append({"pid":0, "sid":i, "snt":snt, "tok": src, "offset":-1,"len":-1,"re_sntbr":False,
	"pos":[t.tag_ for t in doc], "dep": [t.dep_ for t in doc],"head":[t.head.i for t in doc],  #"tag":[t.tag_ for t in doc],
	"seg":[ ("NP", sp.start, sp.end) for sp in doc.noun_chunks] + [ (np.label_, np.start,np.end) for np in doc.ents] , 
	"gec": tgt,  #	"gecp": maptoks[ arrtoks[i] ][0][1], 
	"diff": trans_diff_merge( src , tgt) if diffmerge else trans_diff( src , tgt) 	}) 
	return arr

if __name__ == '__main__':
	print( wps_gec_dsk(dskhost='gpu120.wrask.com:7095')['info']['timing'])
	uvicorn.run(app, host='0.0.0.0', port=7000)