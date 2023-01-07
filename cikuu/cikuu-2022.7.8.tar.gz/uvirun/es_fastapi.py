# 2022.7.2 cp from es_fastapi.py 
from uvirun import *
requests.eshost	= os.getenv("eshost", "172.17.0.1:9200") # host & port , es.corpusly.com | 172.17.0.1 | gpu55.wrask.com

@app.get('/es/rows', tags=["es"])
def rows(query="select lem, count(*) cnt  from gzjc where type = 'tok' and pos != 'PUNCT' group by lem order by cnt desc limit 10", raw:bool=False
	, sum_query:str=None, add_cp:bool=False):
	''' # select snt from dic where type = 'snt' and kp = 'book_VERB' limit 2 
	# sum_query: select count(*) from gzjc where type='snt' '''
	res = requests.post(f"http://{requests.eshost}/_sql",json={"query": query}).json() 
	if raw: return res['rows']  
	si = [  dict(zip([ ar['name'] for ar in res['columns'] ] , ar)) for ar in res.get('rows',[]) ]  #[{"lem": "the", "cnt": 7552},{"lem": "be","cnt": 5640},
	if sum_query is not None: 
		sumi = requests.post(f"http://{requests.eshost}/_sql",json={"query": sum_query}).json()['rows'][0][0]
		[row.update({"sumi":sumi}) for row in si] #return [  dict( dict(zip([ ar['name'] for ar in res['columns'] ] , ar)), **{"sumi":sumi}) for ar in res.get('rows',[]) ] 
	if add_cp: 
		cp = query.split("where")[0].split("from")[-1].strip()
		[row.update({"cp":cp}) for row in si]
	return si #return [  dict(zip([ ar['name'] for ar in res['columns'] ] , ar)) for ar in res.get('rows',[]) ] 

sntsum	= lambda cp: rows(f"select count(*) cnt from {cp} where type = 'snt'", raw=True )[0][0] 
lexsum	= lambda cp: rows(f"select count(*) cnt from {cp} where type = 'tok'", raw=True )[0][0] 

@app.get('/es/groupby', tags=["es"])
def es_groupby(key:str="lem", index:str='gzjc', where:str="type = 'tok' and pos != 'PUNCT' group by lem order by cnt desc limit 10"):
	''' # select snt from dic where type = 'snt' and kp = 'book_VERB' limit 2, 2022.8.4 '''
	res = requests.post(f"http://{requests.eshost}/_sql",json={"query": f"select {key}, count(*) cnt from {index} where {where}"}).json() 
	return [  dict(zip([ ar['name'] for ar in res['columns'] ] , ar)) for ar in res.get('rows',[]) ]  #[{"lem": "the", "cnt": 7552},{"lem": "be","cnt": 5640},

@app.get('/es/count', tags=["es"])
def rows_count(cp:str='gzjc', type:str='snt'):
	return [ {"cnt": requests.post(f"http://{requests.eshost}/_sql",json={"query": f"select count(*) from {cp} where type = '{type}'"}).json()['rows'][0][0]} ]   

@app.get('/es/sum/{cps}/{type}', tags=["es"])
def es_sum(cps:str='gzjc,clec', type:str="snt"):
	'''  cps: gzjc,clec   type:snt   
	# [{'cp':'gzjc', 'snt': 8873}, {'cp':'clec', 'snt': 75322}] '''
	return [{"cp": cp, type: requests.post(f"http://{requests.eshost}/_sql",json={"query": f"select count(*) from {cp} where type ='{type}'"}).json()['rows'][0][0]} for cp in cps.strip().split(',')]

@app.get("/es/kwic", tags=["es"])
def corpus_kwic(cp:str='dic', w:str="opened", topk:int=10, left_tag:str="<b>", right_tag:str="</b>"): 
	''' search snt using word,  | select snt,postag, tc from gzjc where type = 'snt' and match(snt, 'books') | 2022.6.19 '''
	return [] if topk <= 0 else [ {"snt": re.sub(rf"\b({w})\b", f"{left_tag}{w}{right_tag}", snt), "tc": tc } for snt, postag, tc in rows(f"select snt, postag, tc from {cp.strip().split(',')[0]} where type = 'snt' and match (snt, '{w}') limit {topk}", raw=True)]

@app.get('/es/outer_join', tags=["es"])
def es_outer_join(cps:str="clec,gzjc", query:str="select gov, count(*) cnt from clec where type = 'tok' and lem='door' and pos='NOUN' and dep='dobj' group by gov",  ): #perc:bool=False
	''' [{'cp0_1': 1.0, 'cp1_1': 0.0, 'word': 'clean_VERB'}, {'cp0_1': 11.0, 'cp1_1': 1.0, 'word': 'close_VERB'}, {'cp0_1': 2.0, 'cp1_1': 0.0, 'word': 'enter_VERB'}, {'cp0_1': 3.0, 'cp1_1': 0.0, 'word': 'have_VERB'}, {'cp0_1': 1.0, 'cp1_1': 0.0, 'word': 'keep_VERB'}, {'cp0_1': 3.0, 'cp1_1': 0.0, 'word': 'knock_VERB'}, {'cp0_1': 1.0, 'cp1_1': 0.0, 'word': 'lock_VERB'}, {'cp0_1': 31.0, 'cp1_1': 1.0, 'word': 'open_VERB'}, {'cp0_1': 1.0, 'cp1_1': 0.0, 'word': 'pull_VERB'}, {'cp0_1': 1.0, 'cp1_1': 0.0, 'word': 'push_VERB'}, {'cp0_1': 3.0, 'cp1_1': 0.0, 'word': 'reach_VERB'}, {'cp0_1': 1.0, 'cp1_1': 0.0, 'word': 'rush_VERB'}, {'cp0_1': 1.0, 'cp1_1': 1.0, 'word': 'shut_VERB'}, {'cp0_1': 1.0, 'cp1_1': 0.0, 'word': 'slam_VERB'}, {'cp0_1': 1.0, 'cp1_1': 0.0, 'word': 'unlock_VERB'}, {'cp0_1': 2.0, 'cp1_1': 0.0, 'word': 'watch_VERB'}, {'cp0_1': 0.0, 'cp1_1': 1.0, 'word': 'find_VERB'}, {'cp0_1': 0.0, 'cp1_1': 1.0, 'word': 'leave_VERB'}] '''
	cps = cps.strip().split(',')
	map = defaultdict(dict)
	for i, cp in enumerate(cps): 
		for row in rows(query.replace(cps[0], cp ) , raw=True): # assume the first one is the key 
			for j in range(1, len(row)): 
				map[ row[0]][ f"cp{i}_{j}"] = row[j]
	df = pd.DataFrame(map).fillna(0).transpose()
	return [ dict(dict(row), **{"word": index} ) for index, row in df.iterrows()]  #return arr[0:topk] if topk > 0  else arr 

@app.get("/es/stats", tags=["es"])
def corpus_stats(names:str=None, types:str="doc,snt,np,tok,trp,vp"):
	''' doc,snt,np,tok,simple_sent,vtov,vvbg,vp, added 2022.5.21 '''
	names = name.strip().split(',') if names else [ar['name'] for ar in sqlrows("show tables")  if not ar['name'].startswith(".") and ar['type'] == 'TABLE' and ar['kind'] == 'INDEX']
	types = types.replace(",", "','")
	return [ dict( dict(rows(f"select type, count(*) cnt from {name} where type in ('{types}') group by type")), **{"name":name} ) for name in names]

@app.get("/es/phrase", tags=["es"])
def match_phrase(phrase:str='opened the box', cp:str='clec', topk:int=10): 	
	return requests.post(f"http://{requests.eshost}/{cp}/_search/", json={"query": {  "match_phrase": { "snt": phrase }  } , "size": topk}).json()
@app.get("/es/phrase_num", tags=["es"])
def phrase_num(phrase:str='opened the box',  cp:str='clec', topk:int=10): 
	return match_phrase(phrase, cp, topk)["hits"]["total"]["value"]

@app.get("/es/mf", tags=["es"])
def corpus_mf(cps:str="gzjc,clec", w:str="considered", topk:int=3):
	dic =  {cp: round(1000000 * phrase_num(w, cp=cp) / (sntsum(cp)+0.1), 2 ) for cp in cps.strip().split(',') }
	return [ {"cp":cp, "mf":mf } for cp,mf in dic.items()]

@app.get("/es/newindex", tags=["es"])
def new_index(index:str='testidx'):
	from so import config
	requests.delete(f"http://{requests.eshost}/{index}")
	return requests.put(f"http://{requests.eshost}/{index}", json=config).text

@app.post("/es/addnew", tags=["es"])
def es_addnew(arr:dict={"essay_or_snts":"She has ready. It are ok. The justice delayed is justice denied. I plan to go swimming.", "rid":0, "uid":0}
		, index:str="exam", gecdskhost:str='gpu120.wrask.com:8180'):  
	''' assuming: index already exists, 2022.7.30 '''
	import en
	url = f"http://{requests.eshost}/{index}"
	rid,uid = arr.get('rid',0), arr.get('uid',0)
	did		= f"rid-{rid}:uid-{uid}" # filename is a kind of uid 
	requests.post(f"http://{requests.eshost}/{index}/_delete_by_query?conflicts=proceed", json={"query": { "match": { "did": did} }}).text

	dsk		= requests.post(f"http://{gecdskhost}/gecdsk", json=arr).json()
	for idx, mkf in enumerate(dsk['snt']):
		arrlex = mkf.get("meta",{}).get("lex_list",'').split()
		si = {}
		for k,v in mkf.get('feedback',{}).items(): 
			if v['cate'].startswith('e_') or v['cate'].startswith('w_'):
				si[ v['ibeg'] ] = v['cate'].split(".")[0]
		for i, w in enumerate(arrlex):
			requests.put(f"http://{requests.eshost}/{index}/_doc/{did}:dsk-{idx * 1000 + i}", json ={"did":did,"i":idx * 1000 + i,  "type":"dsktag"
			, "labels": [si[i]] if i in si else [], "text":w, } )

	doc		= spacy.nlp(arr.get('essay_or_snts',''))
	snts	= [mkf.get('meta',{}).get('snt','') for mkf in dsk.get('snt',[])]
	arr.update({"type":"doc", "dsk":json.dumps(dsk), "json":json.dumps(doc.to_json()), "did": did, "rid":rid, "uid":uid, "sntnum":len(snts), "score":float(dsk.get('info',{}).get("final_score",0)), "snts": json.dumps(snts) })
	requests.put(f"http://{requests.eshost}/{index}/_doc/{did}", json=arr )
	requests.put(f"http://{requests.eshost}/{index}/_doc/{did}-dims", json=dict(dsk.get('doc',{}), **{"type":"dims", "did":did}))

	# add tag ,essay-level offset
	[ requests.put(f"http://{requests.eshost}/{index}/_doc/{did}:ctag-NP-{doc[np.start].idx}", json={"did":did, "type":"ctag", "ctag": "NP", "start":doc[np.start].idx, "len":len(np.text), "chunk": np.text} ) for np in doc.noun_chunks if np.end - np.start > 1]
	[ requests.put(f"http://{requests.eshost}/{index}/_doc/{did}:ctag-tok-{t.idx}", json ={"did":did, "type":"ctag", "ctag": t.pos_, "start":t.idx, "len":len(t.text), "chunk": t.text} ) for t in doc if t.pos_ not in ('X','PUNCT', 'SPACY')]
	[ requests.put(f"http://{requests.eshost}/{index}/_doc/{did}:toktag-{t.idx}", json ={"did":did,"i":t.i,  "type":"toktag", "labels": [t.pos_] if t.pos_ in ('VERB','NOUN','ADJ','ADV','CCONJ') else [], "text":t.text, } ) for t in doc ]

	# 非谓语动词
	arr = [ {"did":did,"i":t.i,  "type":"vtag", "labels":[], "text":t.text} for t in doc]
	for name, start,end in matchers['vtov'](doc) :
		arr[start].update({"labels":['vtov'], "text": doc[start:end].text}) 
		for i in range(start+1, end): arr[i].update({"text":""})
	for name, start,end in matchers['vvbg'](doc) :
		arr[start].update({"labels":['vvbg'], "text": doc[start:end].text}) 
		for i in range(start+1, end): arr[i].update({"text":""})
	[ arr[t.i].update({"labels":['VBN']}) for t in doc if t.tag_ == 'VBN' ]
	[ requests.put(f"http://{requests.eshost}/{index}/_doc/{did}:vtag-{t['i']}", json=t) for t in arr  if t['text'] ]

	for i, sent in enumerate(doc.sents):
		sdoc = sent.as_doc()
		labels = ['简单句' if len([t for t in sdoc if t.pos_ == 'VERB' and t.dep_ != 'ROOT']) <= 0 else '复杂句']
		if len([t for t in sdoc if t.dep_ == 'conj' and t.head.dep_ == 'ROOT']) > 0 : labels.append("复合句")
		requests.put(f"http://{requests.eshost}/{index}/_doc/{did}:stag-{i}", json={"type":"stag", "i": i, "did": did, "rid":rid, "uid":uid, "id": f"{did}:stag-{i}", "text": sdoc.text, "labels": labels})
	return arr 

@app.post("/es/newdoc", tags=["es"])
def newdoc(arr:dict={"essay_or_snts":"The quick fox jumped over the lazy dog. The justice delayed is justice denied. She is very happy.", "rid":0, "uid":0}
		, index:str="shexam", gecdskhost:str='gpu120.wrask.com:8180' , refresh_index:bool=False ):  
	''' 2022.7.11 '''
	if not hasattr(newdoc, 'es'):
		from so import config
		from elasticsearch import Elasticsearch,helpers
		newdoc.es	= Elasticsearch([ f"http://{requests.eshost}"])  
	if refresh_index: newdoc.es.indices.delete(index=index)
	if not newdoc.es.indices.exists(index=index): newdoc.es.indices.create(index=index, body=config) 

	from en.esjson import sntdoc_idsour #2022.7.10
	did		= f"rid-{arr.get('rid',0)}:uid-{arr.get('uid',0)}" # filename is a kind of uid 
	requests.post(f"http://{requests.eshost}/{index}/_delete_by_query?conflicts=proceed", json={"query": { "match": { "did": did} }}).text

	dsk		= requests.post(f"http://{gecdskhost}/gecdsk", json=arr).json()
	snts	= [mkf.get('meta',{}).get('snt','') for mkf in dsk.get('snt',[])]
	arr.update({"type":"doc", "did": did, "sntnum":len(snts), "score":float(dsk.get('info',{}).get("final_score",0)), "snts": json.dumps(snts) })
	newdoc.es.index(index = index,  id = did, body = arr)
	newdoc.es.index(index = index,  id = f"{did}-dims", body = dict(dsk.get('doc',{}), **{"type":"dims", "did":did}) )

	for i,mkf in enumerate(dsk.get('snt',[])):  
		snt = mkf.get('meta',{}).get('snt','')
		doc = spacy.nlp(snt)
		[ newdoc.es.index(index = index,  id = f"{did}:" + ar["_id"], body = dict(ar['_source'], **{"did":did})) for ar in sntdoc_idsour( f"{did}:sid-{i})", snt, doc ) ]  
		[ newdoc.es.index(index = index,  id = f"{did}:sid-{i})-{v['ibeg']}", body = dict( v, **{"type":"cate", "did":did, "memo":snt, "src":f"{did}:sid-{i})"}))  for k,v in mkf.get('feedback',{}).items() if f"{did}:sid-{i})".startswith("e_") or v['cate'].startswith("w_") ]

	# add tag ,essay-level offset
	doc = spacy.nlp(arr.get('essay_or_snts',''))
	[ newdoc.es.index(index = index,  id = f"{did}:ctag-NP-{doc[np.start].idx}", body ={"did":did, "type":"ctag", "ctag": "NP", "start":doc[np.start].idx, "len":len(np.text), "chunk": np.text} ) for np in doc.noun_chunks if np.end - np.start > 1]
	[ newdoc.es.index(index = index,  id = f"{did}:ctag-tok-{t.idx}", body ={"did":did, "type":"ctag", "ctag": t.pos_, "start":t.idx, "len":len(t.text), "chunk": t.text} ) for t in doc if t.pos_ not in ('X','PUNCT', 'SPACY')]
	# clause 
	for v in [t for t in doc if t.pos_ == 'VERB' and t.dep_ != 'ROOT' ] : # non-root
		children = list(v.subtree)
		start = children[0].i  	#end = children[-1].i 
		cl = " ".join([c.text for c in v.subtree]) 	#spans.append ([doc[start].idx, doc[start].idx + len(cl), v.dep_])
		newdoc.es.index(index = index,  id = f"{did}:ctag-cl-{doc[start].idx})", body ={"did":did, "type":"ctag", "ctag": f"cl.{v.dep_}", "start":doc[start].idx, "len":len(cl), "chunk": cl} )
	# AP, VP 
	from en.terms import matchers
	for name, start,end in matchers['ap'](doc) :
		newdoc.es.index(index = index,  id = f"{did}:ctag-AP-{doc[start].idx}", body ={"did":did, "type":"ctag", "ctag": "AP", "start":doc[start].idx, "len":len(doc[start:end].text), "chunk": doc[start:end].text} )
	for name, start,end in matchers['vp'](doc) :
		newdoc.es.index(index = index,  id = f"{did}:ctag-VP-{doc[start].idx}", body ={"did":did, "type":"ctag", "ctag": "VP", "start":doc[start].idx, "len":len(doc[start:end].text), "chunk": doc[start:end].text} )
	# 非谓语动词
	for name, start,end in matchers['vtov'](doc) :
		newdoc.es.index(index = index,  id = f"{did}:ctag-vtov-{doc[start].idx}", body ={"did":did, "type":"ctag", "ctag": "vtov", "start":doc[start].idx, "len":len(doc[start:end].text), "chunk": doc[start:end].text} )
	for name, start,end in matchers['vvbg'](doc) :
		newdoc.es.index(index = index,  id = f"{did}:ctag-vvbg-{doc[start].idx}", body ={"did":did, "type":"ctag", "ctag": "vvbg", "start":doc[start].idx, "len":len(doc[start:end].text), "chunk": doc[start:end].text} )
	[newdoc.es.index(index = index,  id = f"{did}:ctag-VBN-{t.idx})", body ={"did":did, "type":"ctag", "ctag": "VBN", "start":t.idx, "len":len(t.text), "chunk": t.text} ) for t in doc if t.tag_ == 'VBN']

	for i, sent in enumerate(doc.sents):
		sdoc = sent.as_doc()
		stag = ["简单句" if len([t for t in sdoc if t.pos_ == 'VERB' and t.dep_ != 'ROOT']) <= 0 else "复杂句"] 
		if len([t for t in sdoc if t.dep_ == 'conj' and t.head.dep_ == 'ROOT']) > 0: stag.append("复合句")
		newdoc.es.index(index = index,  id = f"{did}:stag-{i}", body ={"did":did, "type":"stag", "stag": stag, "id": f"{did}:stag-{i})","src":f"{did}:sid-{i})", "start":doc[sent.start].idx, "len":len(sent.text), "chunk": sent.text} )
	return arr 

@app.post("/es/uploadfile/", tags=["es"])
async def create_upload_file(index:str="shexam", rid:int=0, file: UploadFile = File(...), refresh_index:bool = False):
	''' folder is the index name '''
	content = await file.read()
	return indexdoc({'essay_or_snts':content.decode().strip(),'rid':rid, 'uid':file.filename}, index=index, refresh_index=refresh_index)  

@app.get("/es/hyb-snt", tags=["es"])
def hyb_snt(hyb:str='_decide to save', index:str='c4-a0', size:int= 1000):
	''' 2022.12.16 '''
	sql= { "query": {  "match_phrase": { "postag": hyb  } },  "_source": ["postag"], "size":  size}
	res = requests.post(f"http://{requests.eshost}/{index}/_search/", json=sql).json()
	data= []
	for ar in res['hits']['hits']: 
		postag =  ar["_source"]['postag'] #the_the_DT_DET adventures_adventure_NNS_NOUN of_of_IN_ADP
		snt = " ".join([item.split('_')[0] for item in postag.strip().split(' ')])
		data.append(snt) 
	return {"hyb": hyb, "index":index, "size":size, "data":data}

@app.get("/es/chunk-snt", tags=["es"])
def chunk_snt(chunk:str='decided to save', index:str='c4-a0', size:int= 10):
	''' 2022.12.16 '''
	sql= { "query": {  "match_phrase": { "postag": chunk  } },  "_source": ["postag"], "size":  size}
	res = requests.post(f"http://{requests.eshost}/{index}/_search/", json=sql).json()
	data= []
	for ar in res['hits']['hits']: 
		postag =  ar["_source"]['postag'] #the_the_DT_DET adventures_adventure_NNS_NOUN of_of_IN_ADP
		snt = " ".join([item.split('_')[0] for item in postag.strip().split(' ')])
		snt = re.sub(rf'\b({chunk})\b', r'<b>\g<0></b>', snt)
		data.append(snt) 
	return {"chunk": chunk, "index":index, "size":size, "data":data}

addpat	= lambda s : f"{s}_[^ ]*" if not s.startswith('_') else f"[^ ]*{s}[^ ]*"   # if the last one, add $ 
rehyb   = lambda hyb: ' '.join([ addpat(s) for s in hyb.split()])  #'the_[^ ]* [^ ]*_NNS_[^ ]* of_[^ ]*'
heads   = lambda chunk:  ' '.join([s.split('_')[0].lower() for s in chunk.split()])		#the_the_DT_DET adventures_adventure_NNS_NOUN of_of_IN_ADP
@app.get("/es/hybchunk", tags=["es"])
def hybchunk(hyb:str='the _NNS of', index:str='dic', size:int= -1, topk:int=30):
	''' the _NNS of -> {the books of: 13, the doors of: 7} , added 2021.10.13 '''
	sql= { "query": {  "match_phrase": { "postag": hyb  } },  "_source": ["postag"], "size":  size}
	res = requests.post(f"http://{requests.eshost}/{index}/_search/", json=sql).json()
	si = Counter()
	repat = rehyb(hyb)
	for ar in res['hits']['hits']: 
		postag =  ar["_source"]['postag']
		m= re.search(repat,postag) #the_the_DT_DET adventures_adventure_NNS_NOUN of_of_IN_ADP
		if m : si.update({ heads(m.group()):1})
	data  = [{"gram":s, "count":i} for s,i in si.most_common(topk)]
	return {"hyb": hyb, "index":index, "topk":topk, "data":data}

@app.get("/es/hyb-vp", tags=["es"])
def hyb_vp(hyb:str='_VERB _NP from _VBG', index:str='c4-a0', size:int= -1, topk:int=30):
	''' {prohibit _NP from _VBG: 13, keep _NP from _VBG: 7} , added 2021.12.12 '''
	sql= { "query": {  "match_phrase": { "postag": hyb  } },  "_source": ["postag"], "size":  size}
	res = requests.post(f"http://{requests.eshost}/{index}/_search/", json=sql).json()
	si = Counter()
	repat = rehyb(hyb)
	for ar in res['hits']['hits']: 
		postag =  ar["_source"]['postag']
		m= re.search(repat,postag) #the_the_DT_DET adventures_adventure_NNS_NOUN of_of_IN_ADP
		v = m.group().split('_')[1]
		if m : si.update({ f"{v}{hyb}".replace("_VERB",""):1})
	data  = [{"gram":s, "count":i} for s,i in si.most_common(topk)]
	return {"hyb": hyb, "index":index, "topk":topk, "data":data}

@app.get("/es/aggs", tags=["es"])
def es_aggs(pattern:str='~dobj:door_NOUN:VERB_.*', index:str='dic', field:str='kps', size:int= 1000, asrow:bool=True):
	''' {"key" : "~dobj:door_NOUN:VERB_open",  "doc_count" : 252} '''
	arr = requests.post(f"http://{requests.eshost}/{index}/_search/", json={
  "size":0,
  "aggs": {
    "myagg": {
      "terms": {
        "field": field,
         "include": pattern , #"~dobj:door_NOUN:VERB_.*",
         "size":size
      }
    }
  }
}).json()
	rows = [ ( row['key'], row['doc_count'])  for row in arr['aggregations']['myagg']['buckets']]
	return rows if asrow else [ {"key":s, "count":i} for s,i in rows ]

@app.get('/es/keyness', tags=["es"])
def es_keyness(pattern='~dobj:door_NOUN:VERB_.*', cps:str='clec', cpt:str='dic', sepa:str=None, field:str='kps', size:int= 1000): 
	''' return (word, srccnt, tgtcnt, srcsum, tgtsum, keyness), sepa=_/:,  2022.8.25 '''
	from util import likelihood
	try:
		data_src = es_aggs(pattern, cps, field, size)
		data_tgt = es_aggs(pattern, cpt, field, size)

		df = pd.DataFrame({cps: dict(data_src), cpt: dict(data_tgt)}).fillna(0)
		df[f'{cps}_sum'] = sum([i for s,i in data_src])  # rows_count(cps) 
		df[f'{cpt}_sum'] = sum([i for s,i in data_tgt])
		df = df.sort_values(df.columns[0], ascending=False) #.astype(int)
		return [ {"index": index.split(sepa)[-1] 
		,cps:int(row[cps]),f'{cps}_sum':int(row[f'{cps}_sum'])
		,cpt:int(row[cpt]),f'{cpt}_sum':int(row[f'{cpt}_sum']) 
		,'keyness':likelihood(row[cps],row[cpt],row[f'{cps}_sum'],row[f'{cpt}_sum'])}  for index, row in df.iterrows()] 
	except Exception as e:
		print("es_keyness ex:", e) 
		return []

@app.get('/es/sntkps', tags=["es"])
def snt_kps(text:str="She has ready. It are ok. The justice delayed is justice denied. I plan to go swimming.", did:str=None): 
	''' parse kps for es indexing , 2022.8.26 '''
	import hashlib,en
	tdoc = spacy.nlp(text)
	if did is None : did  = hashlib.md5(text.strip().lower().encode("utf-8")).hexdigest()
	id_source = {} # used for es PUT 
	for sid, snt in enumerate(tdoc.sents): 
		doc = snt.as_doc() 
		postag = "_^ " + ' '.join([ f"_{t.pos_}_{t.tag_}" if t.pos_ in ('PROPN','NUM','X','SPACE','PUNCT') else f"{t.text.lower()}_{t.lemma_}_{t.pos_}_{t.tag_}" for t in doc])

		_kps = []
		[ _kps.append(f"{t.pos_}:{t.lemma_}") for t in doc]  # VERB:book
		[ _kps.append(f"_{t.lemma_}:{t.text.lower()}") for t in doc]  # _book:booked,  added 2022.8.21
		[ _kps.append(f"{t.tag_}:{t.pos_}_{t.lemma_}") for t in doc]  # VBD:VERB_book,  added 2022.8.25
		[ _kps.append(f"{t.dep_}:{t.head.pos_}_{t.head.lemma_}:{t.pos_}_{t.lemma_}") for t in doc if t.pos_ not in ('PUNCT')]  # 
		[ _kps.append(f"~{t.dep_}:{t.pos_}_{t.lemma_}:{t.head.pos_}_{t.head.lemma_}") for t in doc if t.pos_ not in ('PUNCT')]  # 
		[ _kps.append(f"NP:{doc[sp.end-1].pos_}_{doc[sp.end-1].lemma_}:{sp.text.lower()}") for sp in doc.noun_chunks ]
		_kps.append( f"stype:" +  "simple_snt" if en.simple_sent(doc) else "complex_snt" )
		if en.compound_snt(doc) : _kps.append("stype:compound_snt")

		# [('pp', 'on the brink', 2, 5), ('ap', 'very happy', 9, 11)]
		for lem, pos, type, chunk in en.kp_matcher(doc): #brink:NOUN:pp:on the brink
			_kps.append(f"{type}:{pos}_{lem}:{chunk}")
		for trpx, row in en.dep_matcher(doc): #[('svx', [1, 0, 2])] ## consider:VERB:vnpn:**** 
			verbi = row[0] #consider:VERB:be_vbn_p:be considered as
			_kps.append(f"{trpx}:{doc[verbi].pos_}_{doc[verbi].lemma_}")
			if trpx == 'sva' and doc[row[0]].lemma_ == 'be': # fate is sealed, added 2022.7.25   keep sth. stuck
				_kps.append(f"sbea:{doc[row[1]].pos_}_{doc[row[1]].lemma_}:{doc[row[2]].pos_}_{doc[row[2]].lemma_}")
			
		# last to be called, since NP is merged
		for row in en.verbnet_matcher(doc): #[(1, 0, 3, 'NP V S_ING')]
			if len(row) == 4: 
				verbi, ibeg, iend, chunk = row
				if doc[verbi].lemma_.isalpha() : 
					_kps.append(f"verbnet:{doc[verbi].pos_}_{doc[verbi].lemma_}:{chunk}")

		for name,ibeg,iend in en.post_np_matcher(doc): #added 2022.7.25
			if name in ('v_n_vbn','v_n_adj'): 
				_kps.append(f"{name}:{doc[ibeg].pos_}_{doc[ibeg].lemma_}:{doc[ibeg].lemma_} {doc[ibeg+1].lemma_} {doc[ibeg+2].text}")

		id_source[f"{did}-{sid}"] = {'type':'snt', 'snt':snt.text.strip(), 'postag':postag,  'did':did, 'src': f"{did}-{sid}",  'tc': len(doc), 'kps': list(set(_kps)) }  
	return id_source

@app.get('/es/termsnts', tags=["es"], response_class=HTMLResponse)
def es_termsnts(term:str="dobj:VERB_open:NOUN_door", cp:str='en',  term_name:str='kps',  snt_field:str='snt', hl_words:str="open,door", topk:int=10, sntsum:bool=True): 
	''' return HTML <ol><li> , 2022.9.7 '''
	from dic import lemma_lex
	res		= requests.post(f"http://{requests.eshost}/{cp}/_search",json={"query": {"term": {term_name:term} }}).json() 
	cnt		= res["hits"]["total"]["value"]
	snts    = [ ar['_source'][snt_field] for ar in res["hits"]["hits"]]
	words	= '|'.join([ '|'.join(list(lemma_lex.lemma_lex[w])) for w in hl_words.strip().split(',') if w in lemma_lex.lemma_lex])
	arr		= [re.sub(rf'\b({words})\b', r'<font color="red">\g<0></font>', snt, flags=re.IGNORECASE) if words else snt for snt in snts]
	html	= "\n".join([f"<li>{snt}</li>" for snt in arr])
	return HTMLResponse(content=f"<ol> <b>{cnt}</b> Sentences {html}</ol>" if sntsum else f"<ol>{html}</ol>")

@app.post('/es/dsk', tags=["es"])
def es_dsk(dsk:dict={}, did:str=None): # http://minio.penly.cn/yulk/test.dsk
	''' to be filled into es, 2022.9.8 '''
	import hashlib,en
	if did is None : did  = hashlib.md5(json.dumps(dsk).encode("utf-8")).hexdigest()

	actions = [] 
	info = dsk.get('info',{})
	actions.append( {"_id": did, "_source": dict(info, **{"type":"doc", "snts":[mkf.get('meta',{}).get('snt','') for mkf in dsk.get('snt',[])], 'score': round(float(dsk.get('info',{}).get("final_score",0)),2)}) } ) 
	actions.append( {"_id": did +"-dim", "_source": dict(dsk.get('doc',{}), **{"type":"dim"} ) } ) 
	actions.append( {"_id": did +"-kw", "_source": dict(dsk.get('kw',{}), **{"type":"kw"} ) } ) 

	for i, mkf in enumerate(dsk.get('snt',[])):  
		snt		= mkf.get('meta',{}).get('snt','')
		doc		= spacy.nlp(snt) 
		#cates = [ v['cate'][2:] for k,v in mkf.get('feedback',{}).items() if v['cate'].startswith("e_") or v['cate'].startswith("w_") ]
		actions.append( {"_id": f"{did}-{i}", "_source": dict(dsk.get('kw',{}), **{"type":"kw"} ) } ) 
		#[ actions.append( {"_id": f"{did}-{i}-fd-{v.get('ibeg',0)}", "_source": {"type":"feedback",'cate': v.get('cate',''), 'msg':v.get('short_msg',''), 'ibeg':v.get('ibeg',0)} ) for k,v in mkf.get('feedback',{}).items() if v['cate'].startswith("e_") or v['cate'].startswith("w_") ]
		#	"chunks": [ {"start":sp.start, "end": sp.end,"type":"NP", "lem": doc[sp.end-1].lemma_, "text":sp.text} for sp in doc.noun_chunks ],
		#for t in doc:		sntdic[sntkey][f'toks-{t.i}'] =  {'i':t.i, "head":t.head.i, 'lex':t.text, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, "gpos":t.head.pos_, "glem":t.head.lemma_}
	return actions

if __name__ == "__main__":   #uvicorn.run(app, host='0.0.0.0', port=80)
	#print ( es_keyness("VERB:.*", sepa=':'), flush=True) 
	print ( es_dsk())