# 2022.12.29  uvicorn c4es:app --host 0.0.0.0 --port 8000 --reload
import fastapi,uvicorn,requests,re,os
from collections import Counter

app		= fastapi.FastAPI()
from fastapi.middleware.cors import CORSMiddleware  #https://fastapi.tiangolo.com/zh/tutorial/cors/
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

requests.eshost	= os.getenv("eshost", "172.17.0.1:9200") # host & port , es.corpusly.com | 172.17.0.1 | gpu55.wrask.com
sntsum	= lambda cp: rows(f"select count(*) cnt from {cp} where type = 'snt'", raw=True )[0][0] 
lexsum	= lambda cp: rows(f"select count(*) cnt from {cp} where type = 'tok'", raw=True )[0][0] 

@app.get('/')
def home():  return fastapi.responses.HTMLResponse(content=f"<h2> c4es </h2><a href='/docs'> docs </a> | <a href='/redoc'> redoc </a><br>last update: 2022.12.29")

@app.get('/es/rows', tags=["es"])
def rows(query="select lem, count(*) cnt  from gzjc where type = 'tok' and pos != 'PUNCT' group by lem order by cnt desc limit 10", raw:bool=False):
	''' sum_query: select count(*) from gzjc where type='snt' '''
	res = requests.post(f"http://{requests.eshost}/_sql",json={"query": query}).json() 
	return res['rows']  if raw else  [  dict(zip([ ar['name'] for ar in res['columns'] ] , ar)) for ar in res.get('rows',[]) ]  #[{"lem": "the", "cnt": 7552},{"lem": "be","cnt": 5640},

@app.get("/es/kwic", tags=["es"])
def corpus_kwic(cp:str='c4-*', w:str="opened", topk:int=10, left_tag:str="<b>", right_tag:str="</b>"): 
	''' search snt using word,  | select snt,postag, tc from gzjc where type = 'snt' and match(snt, 'books') | 2022.6.19 '''
	return [] if topk <= 0 else [ {"snt": re.sub(rf"\b({w})\b", f"{left_tag}{w}{right_tag}", snt), "tc": tc } for snt, postag, tc in rows(f"select snt, postag, tc from {cp.strip().split(',')[0]} where type = 'snt' and match (snt, '{w}') limit {topk}", raw=True)]

@app.get("/es/phrase", tags=["es"])
def match_phrase(phrase:str='opened the box', cp:str='c4-*', topk:int=10): 	
	return requests.post(f"http://{requests.eshost}/{cp}/_search/", json={"query": {  "match_phrase": { "snt": phrase }  } , "size": topk}).json()
@app.get("/es/phrase_num", tags=["es"])
def phrase_num(phrase:str='opened the box',  cp:str='c4-*', topk:int=10): 
	return match_phrase(phrase, cp, topk)["hits"]["total"]["value"]

@app.get("/es/hyb-snt", tags=["es"])
def hyb_snt(hyb:str='_decide to save', index:str='c4-*', size:int= 1000):
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
def chunk_snt(chunk:str='decided to save', index:str='c4-*', size:int= 10):
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
def hybchunk(hyb:str='_in that moment , _NP _VERB', index:str='c4-*', size:int= -1, topk:int=30):
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
	return {"hit-total": res["hits"]["total"]["value"],  "hyb": hyb, "index":index, "topk":topk, "data":data}

@app.get("/es/hyb-vp", tags=["es"])
def hyb_vp(hyb:str='_VERB _NP from _VBG', index:str='c4-*', size:int= -1, topk:int=30):
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

@app.get("/es/given-term", tags=["es"])
def must_filter_cnt(index:str="c4-*", given:str="from the early years", term:str="_memory"):
	''' '''
	arr = requests.post(f"http://{requests.eshost}/{index}/_search/", json={
  "query": {
    "bool": {
      "must":   {"match_phrase": {"postag": given  }},
       "filter": {  "term": { "postag":term    }    }
    }
  }
}).json() 
	return  {"term": term, "count": arr["hits"]["total"]["value"]}

@app.get("/es/given-terms", tags=["es"])
def es_given_terms(index:str='c4-*', given:str='from the early years', terms:str="_memory,_idea"):
	''' 2022.12.29 '''
	data = [ must_filter_cnt(index, given, term) for term in terms.strip().split(',') ]
	return { "index":index, "given": given, "terms": terms, "data": data }

if __name__ == "__main__":   #uvicorn.run(app, host='0.0.0.0', port=80)
	uvicorn.run(app, host='0.0.0.0', port=9202)