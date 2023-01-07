# 2022.6.30 cp from uvicorn corpusly-19200:app --host 0.0.0.0 --port 19200 --reload
from uvirun import *
from util import likelihood

requests.eshost		= os.getenv('eshost', 'es.corpusly.com:9200')
# to be removed later, when cikuu is updated
kwic	= lambda cp, w, topk=3 : [ re.sub(rf"\b({w})\b", f"<b>{w}</b>", row[0]) for row in rows(f"select snt from {cp} where type = 'snt' and match (snt, '{w}') limit {topk}")]

@app.get('/es/typesum', tags=["es"])
def typesum(type:str='snt', cp:str='clec'):
	return requests.post(f"http://{requests.eshost}/_sql", json={"query":f"select count(*) from {cp} where type='{type}'"}).json()['rows'][0][0]

@app.get('/es/kpsum', tags=["es"])
def kpsum(kp:str="dobj:open_VERB:NOUN_door", cp:str='clec'):
	arr = requests.post(f"http://{requests.eshost}/{cp}/_search", json={
"query": {
  "bool":{
      "filter": [ 
      {"term":{"type":"snt"}},
      {"term":{"kps": kp}} #"dobj:open_VERB:NOUN_door"
        ]
  }
},   
"track_total_hits": True
}).json()
	return arr.get('hits',{}).get('total',{}).get("value",0) 

@app.get('/es/kpcnt', tags=["es"])
def kp_cnt(kps:str="ccomp:consider_VERB|dobj:consider_VERB|vtov:consider_VERB|vvbg:consider_VERB", cp:str='clec'):
	arr =  requests.post(f"http://{requests.eshost}/{cp}/_search", json={
	  "query": { "match": {"type": "snt"}   }, 
	  "track_total_hits": True,
	  "size":0,
	  "aggs": {
		"myagg": {
		  "terms": {
			"field": "kps",
			 "include": kps
		  }
		}
	  }
	}).json() 
	return [ (row['key'], row['doc_count']) for row in arr["aggregations"]["myagg"]["buckets"] ]
	#[('ccomp:consider_VERB', 114), ('dobj:consider_VERB', 81), ('vvbg:consider_VERB', 5), ('vtov:consider_VERB', 2)]

@app.get('/es/kpsnt', tags=["es"])
def kp_snt(kp:str="dobj:open_VERB:NOUN_door", cp:str='clec', topk:int=5):
	arr =  requests.post(f"http://{requests.eshost}/{cp}/_search", json={
"query": {
  "bool":{
      "filter": [ 
      {"term":{"type":"snt"}},
      {"term":{"kps":"dobj:open_VERB:NOUN_door"}}
        ]
  }
}
}).json()
	return [ row['_source']['snt'] for row in arr['hits']['hits'] ]

@app.get('/es/kpcntsnt', tags=["es"])
def kp_cnt_snt(kp:str="dobj:open_VERB:NOUN_door", cp:str='clec', topk:int=5):
	return requests.post(f"http://{requests.eshost}/{cp}/_search", json={
  "query": { "match": {"type": "snt"}   }, 
  "size":0,
  "aggs": {
    "myagg": {
      "terms": {
        "field": "kps",
         "include": kp  #"dobj:have_VERB:NOUN_dream"
      },
    "aggs" : {
                "snt" : {
                    "top_hits": { "_source": {"includes":"snt" }, "size": topk
                    }
                }
            }

    }
  }
}).json()["aggregations"]["myagg"]["buckets"][0]
# {'key': 'dobj:open_VERB:NOUN_door', 'doc_count': 28, 'snt': {'hits': {'total': {'value': 28, 'relation': 'eq'}, 'max_score': 2.5384653, 'hits': [{'_index': 'clec', '_type': '_doc', '_id': '5657', '_score': 2.5384653, '_source': {'snt': 'And I ran to the bus quickly, asked the driver open the door.'}}, {'_index': 'clec', '_type': '_doc', '_id': '47892', '_score': 2.5384653, '_source': {'snt': 'When you open the door you can see that on each side of the room there is a double-layer bed .Between the two book shelves there are two desks and two benches, at which I usually read and write .At one up coner of the room ,there is a TV set that by watching it I can known all the news of our country and the others of the world .'}}, {'_index': 'clec', '_type': '_doc', '_id': '58153', '_score': 2.5384653, '_source': {'snt': 'He had to get out of bed, get his canes, walk 12 feet, open the bedroom door, walk 43 feet, and open the front door -- all in 15 seconds.'}}, {'_index': 'clec', '_type': '_doc', '_id': '34992', '_score': 2.5384653, '_source': {'snt': 'It reformed the past economic system in our country and opened the door of our courtry to bring into anvanced sciente and technology.'}}, {'_index': 'clec', '_type': '_doc', '_id': '71183', '_score': 2.5384653, '_source': {'snt': 'Then television is introduced to us and opens the door for us to travel in those places and enables us to see what happens there, to hear what those people say, and to feel what they experience only on that little screen.'}}]}}}

@app.get('/es/trpcntsnt', tags=["es"])
def trp_cnt_snt(trp:str="dobj:open_VERB:NOUN_.*", cp:str='clec', term_size:int=1000, topk:int=1):
	arr = requests.post(f"http://{requests.eshost}/{cp}/_search", json={
  "query": { "match": {"type": "snt"}   }, 
  "track_total_hits": True, 
  "size":0,
  "aggs": {
    "myagg": {
      "terms": {
        "field": "kps",
         "include": trp, #"dobj:open_VERB:NOUN_.*"
		 "size":term_size 
      },
    "aggs" : {
                "snt" : {
                    "top_hits": { "_source": {"includes":"snt" }, "size":topk
                    }
                }
            }

    }
  }
}).json()
	return [ (row['key'], row['doc_count'], row['snt']['hits']['hits'][0]['_source']['snt']) for row in arr["aggregations"]["myagg"]["buckets"] ]


@app.get('/es/xcnt/{cp}/{type}/{column}')
def es_xcnt( column:str='lex', cp:str='dic', type:str='tok', where:str="", order:str="order by cnt desc limit 10",  name:str="es.corpusly.com:9200" ):
	''' where:  and lem='book'  | JSONCompactColumns
	* select lex,count(*) cnt from dic where type = 'tok' and lem= 'book' group by lex '''
	query  = f"select {column}, count(*) cnt from {cp} where type = '{type}' {where} group by {column} {order}"
	res = requests.post(f"http://{name}/_sql",json={"query": query}).json() 
	return [  { column: ar[0], "cnt": ar[1]} for ar in res['rows'] ] 

@app.get('/es/sqlrows')
def sqlrows(query="select lem, count(*) cnt  from gzjc where type = 'tok' and pos != 'PUNCT' group by lem order by cnt desc limit 10", perc_column:str=None):
	''' perc_column: cnt  
	# select gov, count(*) cnt from gzjc where type = 'tok' and lem='door' and pos='NOUN' and dep='dobj' group by gov
	# select lem, count(*) cnt from gzjc where type = 'tok' and gov='open_VERB' and pos='NOUN' and dep='dobj' group by lem
	'''
	res = requests.post(f"http://{requests.eshost}:{requests.esport}/_sql",json={"query": query}).json() 
	arr = [  dict(zip([ ar['name'] for ar in res['columns'] ] , ar)) for ar in res['rows'] ] 
	if perc_column:  
		sump = sum([ ar[perc_column] for ar in arr]) + 0.0001
		[ ar.update({'perc': round(ar[perc_column] / sump, 4) }) for ar in arr]
	return arr

@app.post('/es/sqlrows')
def es_sqlrows_post(querys:list=["show tables","select lem, count(*) cnt  from gzjc where type = 'tok' and pos != 'PUNCT' group by lem order by cnt desc limit 10"], asdic:bool=True):
	return {query: sqlrows(query) for query in querys} if asdic else [ sqlrows(query) for query in querys ]

@app.post('/es/rows')
def named_rows(arr:dict={'query':"select lem, count(*) cnt from dic where type='tok' and  tag='VBG' group by lem order by cnt desc ", 'columns':["lem", "tagcnt"]}):
	''' 2022.6.21 '''
	return [  dict(zip(arr['columns'], ar)) for ar in rows( arr.get('query', "") ) ] 

@app.get('/es/termcnt')
def es_query_termcnt(cps:str="clec,gzjc", query:str="select gov, count(*) cnt from __0__ where type = 'tok' and lem='door' and pos='NOUN' and dep='dobj' group by gov", topk:int=10 ):
	''' added 2022.6.19 '''
	map = defaultdict(dict)
	for cp in cps.strip().split(','): 
		sql = query.replace("__0__", cp ) 
		for row in rows(sql): # assume the first one is the key 
			for i in range(1, len(row)): 
				map[ row[0]][ f"{cp}_{i}" if i > 1 else cp] = row[i]
	df = pd.DataFrame(map).fillna(0).transpose()
	for col in df.columns:
		df[f"{col}_perc"] = round((df[col] / df[col].sum()) * 100, 2)
	if topk > 0 : df = df.sort_values(df.columns[0], ascending=False)
	arr = [ dict(dict(row), **{"term": index} ) for index, row in df.iterrows()] 
	return arr[0:topk] if topk > 0  else arr 

@app.get("/es/indexlist/")
def corpus_indexlist(verbose:bool=False):
	names =  [ar['name'] for ar in sqlrows("show tables")  if not ar['name'].startswith(".") and ar['type'] == 'TABLE' and ar['kind'] == 'INDEX'] # {"catalog":"elasticsearch","name": ".apm-custom-link", "type": "TABLE",    "kind": "INDEX"  },
	return [ dict( dict(rows(f"select type, count(*) cnt from {name} group by type")), **{"name":name} ) for name in names] if verbose else names

@app.get("/es/stats")
def corpus_stats(names:str=None, types:str="doc,snt,np,tok,trp,vp"):
	''' doc,snt,np,tok,simple_sent,vtov,vvbg,vp, added 2022.5.21 '''
	names = name.strip().split(',') if names else [ar['name'] for ar in sqlrows("show tables")  if not ar['name'].startswith(".") and ar['type'] == 'TABLE' and ar['kind'] == 'INDEX']
	types = types.replace(",", "','")
	return [ dict( dict(rows(f"select type, count(*) cnt from {name} where type in ('{types}') group by type")), **{"name":name} ) for name in names]

@app.get("/es/kwic")
def corpus_kwic(cp:str='dic', w:str="opened", topk:int=10, left_tag:str="<b>", right_tag:str="</b>"): # expected_tc:int=15,
	''' search snt using word,  | select snt,postag, tc from gzjc where type = 'snt' and match(snt, 'books') | 2022.6.19 '''
	return [ {"snt": re.sub(rf"\b({w})\b", f"{left_tag}{w}{right_tag}", snt), "tc": tc } for snt, postag, tc in rows(f"select snt, postag, tc from {cp.strip().split(',')[0]} where type = 'snt' and match (snt, '{w}') limit {topk}")]

@app.get("/es/mf")
def corpus_mf(cps:str="gzjc,clec", w:str="considered", topk:int=3, with_snt:bool=False):
	dic =  {cp: round(1000000 * phrase_num(w, cp) / (sntnum(cp)+0.1), 2 ) for cp in cps.strip().split(',') }
	return [ {"cp":cp, "mf":mf, "snts": json.dumps(kwic(cp, w, topk)) } for cp,mf in dic.items()] if with_snt else [ {"cp":cp, "mf":mf } for cp,mf in dic.items()]

@app.get("/es/srcsnts")
def corpus_srcsnts(query:str="select src from gzjc where type='tok' and lem='book' and pos='NOUN' limit 10",highlight:str='book', left_tag:str="<b>", right_tag:str="</b>"):  #, cp:str='gzjc'
	''' '''
	cp = query.split("where")[0].strip().split('from')[-1].strip()
	srclist = "','".join([ src for src, in rows(query)])
	return [{'snt':re.sub(rf"\b({highlight})\b", f"{left_tag}{highlight}{right_tag}", snt)} for snt, in rows(f"select snt from {cp} where type='snt' and src in ('{srclist}')")]

@app.get("/es/lempos/snts")
def lempos_snts(cp:str='gzjc', lem:str='book', pos:str='VERB', topk:int=3, left_tag:str="<b>", right_tag:str="</b>"): 
	''' "select snt from gzjc where type = 'snt' and kp = 'book_VERB' limit 2" , added 2022.6.24 '''
	query = f"select snt from {cp} where type = 'snt' and kp = '{lem}_{pos}' limit {topk}"
	return [{'snt':re.sub(rf"\b({lem})\b", f"{left_tag}{lem}{right_tag}", snt)} for snt, in rows(query)]	

@app.get("/es/trp/snts")
def trp_snts(cp:str='gzjc', word:str='door', rel:str='~dobj_VERB_NOUN', cur:str='open',  topk:int=3): 
	query = f"select snt from {cp} where type = 'snt' and kp = '{rel[1:]}/{cur} {word}' limit {topk}" if rel.startswith('~') else f"select snt from {cp} where type = 'snt' and kp = '{rel}/{word} {cur}' limit {topk}"
	print (query, flush=True)
	return [{'snt':snt} for snt, in rows(query)]

@app.get("/es/match_phrase")
def corpus_match_phrase(phrase:str='opened the box', cp:str='clec', topk:int=10):  return match_phrase(phrase, cp, topk)
@app.get("/es/match_phrase_num")
def corpus_phrase_num(phrase:str='opened the box', cp:str='clec', topk:int=10): return phrase_num(phrase, cp, topk)["hits"]["total"]["value"]

@app.get("/es/nearby")
def corpus_nearby(lem:str="environment", corpus:str='spin', poslist:str="'NOUN','ADJ','VERB'", topk:int=20):
	''' words nearby '''
	rows = requests.post(f"http://{requests.eshost}:{requests.esport}/_sql",json={"query": f"select src from {corpus} where type = 'tok' and lem = '{lem}'"}).json()['rows']
	snts = "','".join([row[0] for row in rows])
	res = requests.post(f"http://{requests.eshost}:{requests.esport}/_sql",json={"query": f"select lem from {corpus} where type = 'tok'  and pos in ({poslist}) and src in ('{snts}')" }).json()['rows']
	si = Counter() 
	[si.update({row[0]:1}) for row in res if row[0] != lem and not row[0] in spacy.stoplist ]
	return Counter({ s:i * spacy.wordidf.get(s, 0) for s,i in si.items()}).most_common(topk)


@app.get('/es/attach_dsk')
def attach_dsk(idxname:str='essay'):  
	dsk		= requests.post(f"http://{gecdskhost}/gecdsk", json=arr).json()
	snts	= [mkf.get('meta',{}).get('snt','') for mkf in dsk.get('snt',[])]
	arr.update({"type":"doc", "did": did, "sntnum":len(snts), "score":float(dsk.get('info',{}).get("final_score",0)), "snts": json.dumps(snts) })
	newdoc.es.index(index = index,  id = did, body = arr)
	newdoc.es.index(index = index,  id = f"{did}-dims", body = dict(dsk.get('doc',{}), **{"type":"dims", "did":did}) )

if __name__ == "__main__":   #uvicorn.run(app, host='0.0.0.0', port=80)
	#print (trp_cnt_snt())	
	#print (cursor_rows("select rid,uid, essay from essay")) 

	requests.post(f"http://{requests.eshost}/essay/_delete_by_query?conflicts=proceed", json={"query": { "match": {"type": "dsk"} }}).text
	for rid,uid, essay in cursor_rows("select rid,uid, essay from essay where rid='230537' "):
		dsk		= requests.post(f"http://gpu120.wrask.com:8180/gecdsk", json={"essay_or_snts":essay, "rid":rid, "uid":uid}).json()
		snts	= [mkf.get('meta',{}).get('snt','') for mkf in dsk.get('snt',[])]
		requests.put(f"http://{requests.eshost}/essay/_doc/rid-{rid}:uid-{uid}:dsk", json={"type":"dsk", "did":f"rid-{rid}:uid-{uid}", "sntnum":len(snts), "score":float(dsk.get('info',{}).get("final_score",0)), "snts": json.dumps(snts) })
		requests.put(f"http://{requests.eshost}/essay/_doc/rid-{rid}:uid-{uid}:dims", json=dict(dsk.get('doc',{}), **{"type":"dims", "did":f"rid-{rid}:uid-{uid}"}) 

'''
GET /gzjc/_search
{
  "query": {
    "match": {"type":"frame"}
  },
  	"track_total_hits": true,
	  "size":0,
	  "aggs": {
		"myagg": {
		  "terms": {
			"field": "frame",
			 "include": "return.*"
		  }
		}
	  }
}
'''