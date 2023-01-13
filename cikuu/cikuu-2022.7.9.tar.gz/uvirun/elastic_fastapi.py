# 2022.12.19 cp from es_fastapi.py 
from uvirun import *
import en
from so import config
from elasticsearch import Elasticsearch,helpers
requests.elastic	= os.getenv("elastic", "172.17.0.1:9200") 
requests.es	= Elasticsearch([ f"http://{requests.elastic}"]) 

rows	= lambda query:  requests.post(f"http://{requests.elastic}/_sql",json={"query": query}).json() 
rowsdic = lambda query: ( res:=rows(query),  [  dict(zip([ ar['name'] for ar in res['columns'] ] , ar)) for ar in res.get('rows',[]) ] )[-1] #[{"lem": "the", "cnt": 7552},{"lem": "be","cnt": 5640},
sntsum	= lambda cp: rows(f"select count(*) cnt from {cp} where type = 'snt'")[0][0] 
lexsum	= lambda cp: rows(f"select count(*) cnt from {cp} where type = 'tok'")[0][0] 

@app.get('/query', tags=["elastic"])
def elastic_query(sql:str='show tables'):
	return requests.post(f"http://{requests.elastic}/_sql",json={"query": sql}).json()

@app.get("/elastic/newindex", tags=["elastic"])
def elastic_new_index(index:str='testidx'):
	requests.delete(f"http://{requests.elastic}/{index}")
	return requests.put(f"http://{requests.elastic}/{index}", json=config).text

@app.get("/elastic/newdoc", tags=["elastic"])
def elastic_addnew(essay:str="She has ready. It are ok. The justice delayed is justice denied. I plan to go swimming.", rid:str='0', uid:str='0'
		, index:str="dsk", gecdsk:str='hw6.jukuu.com:7000',refresh_index:bool=False):  
	''' assuming: index already exists, 2022.7.30 '''
	if refresh_index: requests.es.indices.delete(index=index)
	if not requests.es.indices.exists(index=index): requests.es.indices.create(index=index, body=config) 

	prefix	= f"http://{requests.elastic}/{index}"
	did		= f"rid-{rid}:uid-{uid}" # filename is a kind of uid 
	requests.post(f"{prefix}/_delete_by_query?conflicts=proceed", json={"query": { "match": { "did": did} }}).text

	dsk		= requests.post(f"http://{gecdsk}/gecdsk", params={"essay_or_snts":essay}).json()
	snts	= [mkf.get('meta',{}).get('snt','') for mkf in dsk.get('snt',[])]
	#hits = { ar["_id"] for ar in requests.get(f"{prefix}/_search", params={"query":{"terms": {"_id": [ f"snt:{snt}" for snt in snts ] }}} ).json().get("hits",{}).get("hits",[]) }
	for idx, mkf in enumerate(dsk['snt']):
		snt = mkf['meta'].get('snt','').strip()
		doc = spacy.nlp(snt) 
		requests.put(f"{prefix}/_doc/snt:{snt}", json={"snt":snt, "type":"snt", "did": did, "rid":rid, "uid":uid , "tc": len(doc), 'postag': en.es_postag(doc) } ) #if snt and not f"snt:{snt}" in hits: 
		
		[ requests.put(f"{prefix}/_doc/{did}-snt-{idx}-tok-{t.i}", json={"did": did, "rid":rid, "uid":uid, 'type':'tok', 'i':t.i, "head":t.head.i, 'lex':t.text, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, "gpos":t.head.pos_, "glem":t.head.lemma_}) for t in doc ]
		[ requests.put(f"{prefix}/_doc/{did}-snt-{idx}-np-{sp.start}", json={"did": did, "rid":rid, "uid":uid, 'type':'np',"lem": doc[sp.end-1].lemma_, "start":sp.start, "end":sp.end, "chunk":sp.text} ) for sp in doc.noun_chunks]
		for k,v in mkf.get('feedback',{}).items(): 
			if v.get('cate','').startswith( ("e_","w_") ):
				arrcate = {"did": did, "rid":rid, "uid":uid, "type":"cate", "src":snt, "cate":v.get('cate',''), "topcate": v.get('cate','').split('.')[0][2:], "ibeg": v.get('ibeg',-1),"kp": v.get('kp',''), "msg":v.get("short_msg","")}
				requests.put(f"{prefix}/_doc/{did}-snt-{idx}-{v['cate']}", json=arrcate)

		for lem, pos, type, chunk in en.kp_matcher(doc): #brink:NOUN:pp:on the brink
			requests.put(f"{prefix}/_doc/{did}-snt-{idx}-{type}-{chunk}", json={"did": did, "rid":rid, "uid":uid, 'type':type,"lem": lem, "pos":pos,"chunk":chunk})
		for trpx, row in en.dep_matcher(doc): #[('svx', [1, 0, 2])] ## consider:VERB:vnpn:**** 
			verbi = row[0] #consider:VERB:be_vbn_p:be considered as
			requests.put(f"{prefix}/_doc/{did}-snt-{idx}-{trpx}-{verbi}", json={"did": did, "rid":rid, "uid":uid, 'type':trpx,"lem": doc[verbi].lemma_, "pos":doc[verbi].pos_,}) #_kps.append(f"{trpx}:{doc[verbi].pos_}_{doc[verbi].lemma_}")
	
	arr = {"essay":essay, "type":"doc", "did": did, "rid":rid, "uid":uid, "sntnum":len(snts), "score":float(dsk.get('info',{}).get("final_score",0)), "snts": snts }
	requests.put(f"{prefix}/_doc/{did}", json=arr )
	requests.put(f"{prefix}/_doc/{did}-dim", json=dict(dsk.get('doc',{}), **{"type":"dim", "did":did,"rid":rid, "uid":uid,}))
	return arr 

@app.get("/elastic/batch-test", tags=["elastic"])
def elastic_batch_test(refresh_index:bool=False):  
	''' 2022.12.19 '''
	essays = requests.get("http://minio.penly.cn/yulk/230537.json").json()
	for row in essays: 
		essay = row['essay']
		elastic_addnew(essay, row['rid'], row['uid']) 
	return len(essays) 

if __name__ == "__main__":   #uvicorn.run(app, host='0.0.0.0', port=80)
	pass