# 2022.9.10
from api.common import *
requests.eshost	= os.getenv('eshost', '172.17.0.1:9200') #wrask.com

iphrase = lambda q="_be in force|_wish it to be", cp='c4-*', field='postag': [ (hyb, requests.post(f"http://{requests.eshost}/{cp}/_search", json={   "query": {  "match_phrase": { field: hyb    }   } } ).json()['hits']['total']['value'] ) for hyb in q.strip().split('|') ]
iterm  = lambda term="NOUN:force", cp='en', field='kps':requests.post(f"http://{requests.eshost}/{cp}/_search", json={   "query": {  "term": { field: term    }   } } ).json()['hits']['total']['value']
sntsum = lambda cp='clec': requests.post(f"http://{requests.eshost}/_sql", json={"query":f"select count(*) from {cp} where type='snt'"}).json()['rows'][0][0]
match_phrase = lambda hyb="_be in force", cp='en', field='postag': requests.post(f"http://{requests.eshost}/{cp}/_search", json={   "query": {  "match_phrase": { field: hyb    }   } } ).json()
phrase_snt = lambda hyb="_be in force", cp='en', field='postag': [ ar['_source']['snt']  for ar in match_phrase(hyb,cp,field)['hits']['hits'] ]

esrows	= lambda query, size=1000: requests.post(f"http://{requests.eshost}/_sql",json={"query": query,"fetch_size": size}).json().get('rows',[])
estables = lambda : [row[1] for row in esrows("show tables") if not row[1].startswith(".")]

rows	= lambda query, fetch_size=1000: requests.post(f"http://{requests.eshost}/_sql",json={"query": query,"fetch_size": fetch_size}).json().get('rows',[]) #rows("select s,i from dic where s like 'dobj:VERB_open:NOUN_%'")
si		= lambda pattern, cp='en', sepa='_': [ (row[0].split(sepa)[-1], int(row[1]) )  for row in rows(f"select s,i from {cp} where s like '{pattern}' order by i desc")]
lemlex	= lambda lem, cp='en': [ (s.split(':')[-1],i) for s,i in rows(f"select s,i from {cp} where s like '_{lem}:%'")]
lempos	= lambda lem, cp='en': [ (s.split(':')[0], i) for s,i in rows(f"select s,i from {cp} where s in ('VERB:{lem}','NOUN:{lem}', 'ADJ:{lem}','ADV:{lem}')")]

trpdeps = lambda glem='open', gpos='VERB', dep='dobj', pos='NOUN', cp='dic', limit=10: esrows(f"select lem, count(*) cnt from {cp} where type ='tok' and glem = '{glem}' and gpos='{gpos}' and dep = '{dep}' and pos='{pos}' group by lem order by cnt desc limit {limit}")
trpgovs = lambda lem='door', pos='NOUN', dep='dobj', gpos='VERB', cp='dic', limit=10: esrows(f"select glem, count(*) cnt from {cp} where type ='tok' and lem = '{lem}' and pos='{pos}' and dep = '{dep}' and gpos='{gpos}' group by glem order by cnt desc limit {limit}")

#scheduling	VBG	VERB	planed	advcl	schedule
advcl	= lambda lex='scheduling', dep='advcl', gpos='VERB', cp='dic', limit=10: esrows(f"select glem, count(*) cnt from {cp} where type ='tok' and lex = '{lex}' and dep = '{dep}' and gpos='{gpos}' group by glem order by cnt desc limit {limit}")

terms	= lambda termlist='VERB,vtov,vvbg,VBD,dative', suffix='', sumkey=None, cp='en': rows(f"select s,i from {cp} where s in ('" + "','".join([ v.strip() + suffix for v in termlist.split(',')]) + f"', '{sumkey}')")
silist  = lambda vlist='vtov,vvbg,ccomp,dobj,nsubj', suffix=':VERB_consider', sumkey="VERB:consider", cp='en': rows(f"select s,i from {cp} where s in ('" + "','".join([ v + suffix for v in vlist.split(',')]) + f"', '{sumkey}')")

def keyness(si_src, si_tgt, sumkey:str=None): # keyness(lempos('sound','sino'),lempos('sound','en'))
	''' return (src, tgt, src_sum, tgt_sum, keyness) '''
	df = pd.DataFrame({'src': dict(si_src), 'tgt': dict(si_tgt)}).fillna(0)
	if sumkey is not None : df = df.drop(sumkey) 
	df['src_sum'] = sum([i for s,i in si_src]) if sumkey is None else dict(si_src)[sumkey]
	df['tgt_sum'] = sum([i for s,i in si_tgt]) if sumkey is None else dict(si_tgt)[sumkey]
	df['keyness'] = [ likelihood(row['src'],row['tgt'],row['src_sum'],row['tgt_sum']) for index, row in df.iterrows()] 
	return df.sort_values(df.columns[-1], ascending=True) 

def lemma_phrase_keyness(lemma:str='_force', phrase:list=["_be in force","_come into force","_go into force","_be forced to _VERB",'by force', '_VERB with force'], cps:str='sino', cpt:str='en'): 
	''' return: word  sino    en  sino_sum  en_sum  keyness '''
	sum_src = iphrase(lemma, cps)
	sum_tgt = iphrase(lemma, cpt)
	rows = [ (w, iphrase(w, cps), iphrase(w, cpt) ) for w in phrase]    
	return pd.DataFrame( [ (w, c1, c2, sum_src, sum_tgt, likelihood(c1,c2,sum_src, sum_tgt))  for w, c1,c2 in rows], columns=["word", cps, cpt, f"{cps}_sum", f"{cpt}_sum","keyness"])   

def cands_product(q='one two/ three/'):
	''' {'one three', 'one two', 'one two three'} '''
	if not ' ' in q : return set(q.strip().split('/'))
	arr = [a.strip().split('/') for a in q.split()]
	res = [' '.join([a for a in ar if a]) for ar in itertools.product( * arr)]
	return set( [a.strip() for a in res if ' ' in a]) 

def compare(q="_discuss about/ the issue", given:str=None, index='c4-*'):
	'''  given:str="the early years" '''
	cands = cands_product(q)
	return [ (cand, iphrase(cand, index))  for cand in cands] if given is None else  [{"phrase": phrase, "given":given, "count": requests.post(f"http://{requests.eshost}/{index}/_search/", json={
  "query": {
    "bool": {
      "must": 
        {"match_phrase": {
          "postag": phrase
        }}
      ,
      
       "filter": {
        "match_phrase": {
          "postag": given
        }
      }
      
    }
  } }).json()["hits"]["total"]["value"] }  for phrase in cands ]


def dually_must(q="_idea/_memory", given_A:str="children", given_B:str="the early years", index='c4-*'):
	'''  [('_idea', 33), ('_memory', 8)] '''
	cands = cands_product(q)
	return [ (phrase,  requests.post(f"http://{requests.eshost}/{index}/_search/", json={
		  "query": {
			"bool": {
			  "must": [
				{ "match_phrase": {"postag": phrase}},
				{ "match_phrase": {"postag": given_A}},
				{ "match_phrase": {"postag": given_B}}
			  ] 
			}
		  }
		}).json()["hits"]["total"]["value"] )  for phrase in cands ]

addpat	= lambda s : f"{s}_[^ ]*" if not s.startswith('_') else f"[^ ]*{s}[^ ]*"   # if the last one, add $ 
rehyb   = lambda hyb: ' '.join([ addpat(s) for s in hyb.split()])  #'the_[^ ]* [^ ]*_NNS_[^ ]* of_[^ ]*'
heads   = lambda chunk:  ' '.join([s.split('_')[0].lower() for s in chunk.split()])		#the_the_DT_DET adventures_adventure_NNS_NOUN of_of_IN_ADP
def hybchunk(hyb:str='_in that moment , _NP _VERB', index:str='c4-*', size:int= 1000, topk:int=100, asdic:bool=False):
	''' the _NNS of -> {the books of: 13, the doors of: 7} , added 2021.10.13 '''
	start = time.time()
	sql= { "query": {  "match_phrase": { "postag": hyb  } },  "_source": ["postag"], "size":  size}
	res = requests.post(f"http://{requests.eshost}/{index}/_search/", json=sql).json()
	si = Counter()
	repat = rehyb(hyb)
	for ar in res['hits']['hits']: 
		postag =  ar["_source"]['postag']
		m= re.search(repat,postag) #the_the_DT_DET adventures_adventure_NNS_NOUN of_of_IN_ADP
		if m : si.update({ heads(m.group()):1})
	data  = [{"name":s, "value":i} for s,i in si.most_common(topk)] if asdic else si.most_common(topk)
	return {"hit-total": res["hits"]["total"]["value"],  "timing": round(time.time() - start, 1), "hyb": hyb, "index":index, "topk":topk, "size":size, "data":data}

poslist = lambda arr: [i for i, term in enumerate(arr) if term.startswith("_") and term[1] >= 'A' and term[1] <= 'Z' and term != '_NP' ]
def poscands(hyb:str='pay _JJ attention to', posidx:int=None, index:str='c4-*', size:int= 1000, topk:int=100):
	''' '''
	res = hybchunk(hyb, index, size, topk) 
	arr = hyb.strip().split() 
	if posidx is None: posidx = poslist(arr)[0]
	si = Counter()
	[ si.update({ s.split()[posidx]:i}) for s, i in res['data'] ]
	res['data'] = si.most_common()
	return res 

postag_snt = lambda postag='_^ the_the_DET_DT solution_solution_NOUN_NN is_be_AUX_VBZ':  ' '.join([  ar.split('_')[0] for ar in postag.strip().split()[1:] ])
def phrsnts(q:str="_take _NOUN into account", index:str='c4-*', field:str='postag', size:int=10, keep_first:bool=True):
	''' phrase -> snts '''
	sql= { "query": {  "match_phrase": { field: q  } },  "_source": [field], "size":  size}  #"track_total_hits": true
	res = requests.post(f"http://{requests.eshost}/{index}/_search/", json=sql).json()
	total = res['hits']['total']['value']
	snts  = [ar['_source'][field] for ar in res['hits']['hits'] ]
	return [ postag_snt(snt) for snt in snts ] if keep_first else snts 

def snts(q="_idea", given:str=None, index='c4-*', size:int=10, postag:bool=False):
	'''  given="the early years" '''
	res = requests.post(f"http://{requests.eshost}/{index}/_search/", json={
		  "query": {
			"bool": {
			  "must": [
				{ "match_phrase": {"postag": q}},
				{ "match_phrase": {"postag": q if given is None else given}}
			  ] 
			}
		  }, "size": size 
		}).json()
	return {"total": res['hits']['total']['value'],  "data": [ postag_snt(snt) if not postag else snt for snt in [ar['_source']['postag'] for ar in res['hits']['hits'] ] ] }

def lempos(q="sound", index='c4-*', size:int=1000):
	''' sound -> {'VERB': 17, 'NOUN': 13, ... } '''
	si = Counter()
	postags = snts(f"_{q}", index=index, size=size, postag=True)
	for postag in postags['data'] : 
		lex = [ item.split('_') for item in postag.split() if f"_{q}_" in item]
		if len(lex) <= 0 : continue 
		for t in lex[0]:
			if t.startswith( ('VERB', 'ADJ', 'ADV', 'NOUN') ): 
				si.update( {t:1})
				break 
	return si.most_common() 

def lemlex(q="sound", index='c4-*', size:int=1000):
	''' sound -> {'sound': 17, 'sounds': 13, ... } '''
	si = Counter()
	postags = snts(f"_{q}", index=index, size=size, postag=True)
	for postag in postags['data'] : 
		lex = [ item.split('_')[0].lower() for item in postag.split() if f"_{q}_" in item]
		if len(lex) > 0 : si.update( {lex[0]:1})
	return si.most_common() 

def sidep(docs, headlem:str='save', dep:str="dobj", pos:str="NOUN",  topk:int=20):
	''' sidep( [spacy.sm(snt) for snt in phrsnts("_decide to save", size=1000) ] )   '''
	from collections import Counter
	si =  Counter()
	for doc in docs: 
		for t in doc: 
			if t.head.lemma_ == headlem and t.dep_ == dep and t.pos_ == pos and t.lemma_.isalpha(): 
				si.update({t.lemma_:1})
	return si.most_common(topk) 

def xlist():
	from dic import advlist
	with open('advlist.json','w') as fw:
		fw.write(json.dumps( list(advlist.advlist)))

cursor_sql = lambda query, cursor='': requests.post(f"http://{requests.eshost}/_sql", json={"query":query, "cursor":cursor}).json() 
def rows_iterate(query="select glem, count(*) cnt from dic where type ='tok' and lem = 'door' and pos='NOUN' and dep = 'dobj' and gpos='VERB' group by glem order by cnt desc"):
	cursor=''
	while True : 
		res = cursor_sql(query, cursor)  
		yield res['rows']  
		cursor = res.get('cursor','')         
		if not cursor: break

def cursor_rows(query="select dep, gov, lem, pos, count(*) cnt from gzjc where type='tok' group by dep, gov, lem, pos"):
	rows = []				
	cursor=''
	while True : 
		res = cursor_sql(query, cursor)  
		if 'rows' in res :  rows.extend(res['rows'])
		cursor = res.get('cursor','') 
		if not cursor: break
	return rows

def save(dic, filename):
	with open(filename,'w') as fw:
		fw.write(json.dumps( dic ))

def gov_tags(dep='advcl', gpos='VERB', tag='VBG', cp="dic"):
	si = cursor_rows(f"select glem, count(*) cnt from {cp} where type='tok' and tag='{tag}' and dep='{dep}' and gpos='{gpos}' group by glem order by cnt desc")
	dic = {}
	for s, i in si: 
		if i > 1 : 
			dic[s] = cursor_rows(f"select lex, count(*) cnt from {cp} where type='tok' and tag='{tag}' and glem='{s}' and dep='{dep}' and gpos='{gpos}' group by lex order by cnt desc")
	save(dic, f"{cp}-{dep}-{gpos}-{tag}.json")

def tag_govs(dep='advcl', gpos='VERB', tag='VBG', cp="dic"):
	si = cursor_rows(f"select lex, count(*) cnt from {cp} where type='tok' and tag='{tag}' and dep='{dep}' and gpos='{gpos}' group by lex order by cnt desc")
	dic = {}
	for s, i in si: 
		if i > 1 : 
			dic[s] = cursor_rows(f"select glem, count(*) cnt from {cp} where type='tok' and tag='{tag}' and lex='{s}' and dep='{dep}' and gpos='{gpos}' group by glem order by cnt desc")
	save(dic, f"{cp}~{dep}-{gpos}-{tag}.json")

def gov_deps(dep='dobj', gpos='VERB', pos='NOUN', cp="dic"):
	si = cursor_rows(f"select glem, count(*) cnt from {cp} where type='tok' and pos='{pos}' and dep='{dep}' and gpos='{gpos}' group by glem order by cnt desc")
	dic = {}
	for s, i in si: 
		if i > 1 : 
			dic[s] = cursor_rows(f"select lem, count(*) cnt from {cp} where type='tok' and pos='{pos}' and glem='{s}' and dep='{dep}' and gpos='{gpos}' group by lem order by cnt desc")
	save(dic, f"{cp}-{dep}-{gpos}-{pos}.json")

def dep_govs(dep='dobj', gpos='VERB', pos='NOUN', cp="dic"):
	si = cursor_rows(f"select lem, count(*) cnt from {cp} where type='tok' and pos='{pos}' and dep='{dep}' and gpos='{gpos}' group by lem order by cnt desc")
	dic = {}
	for s, i in si: 
		if i > 1 : 
			dic[s] = cursor_rows(f"select glem, count(*) cnt from {cp} where type='tok' and pos='{pos}' and lem='{s}' and dep='{dep}' and gpos='{gpos}' group by glem order by cnt desc")
	save(dic, f"{cp}~{dep}-{gpos}-{pos}.json")

def pos_rank(pos='VERB', cp="dic"):
	si = cursor_rows(f"select lem, count(*) cnt from {cp} where type='tok' and pos='{pos}' and lem rlike '[a-z]+' group by lem order by cnt desc")
	dic = dict( esrows(f"select type, count(*) cnt from {cp} where type in ('snt','tok') group by type")) 
	res = { 'pos':pos, 'cp': cp, 'num': len(si), 'sum': sum([i for s,i in si]), 'sntnum': dic['snt'], 'lexnum': dic['tok'], 'data': si }
	save(res, f"{cp}-{pos}.json")

def lex_rank(cp="dic"):
	si = cursor_rows(f"select lex, count(*) cnt from {cp} where type='tok' group by lex order by cnt desc")
	dic = dict( esrows(f"select type, count(*) cnt from {cp} where type in ('snt','tok') group by type")) 
	res = { 'pos':'LEX', 'cp': cp, 'num': len(si), 'sum': sum([i for s,i in si]), 'sntnum': dic['snt'], 'lexnum': dic['tok'], 'data': si }
	save(res, f"{cp}-LEX.json")

def lem_pos(cp="dic"):
	rows = cursor_rows(f"select lem, pos, count(*) cnt from {cp} where type='tok' and lem rlike '[a-z]+' and pos not in ('NUM','PUNCT','PROPN') group by lem, pos")
	ssi = defaultdict(dict) 
	for lem,pos, cnt in rows: ssi[lem][pos]  = cnt 
	dic = dict( esrows(f"select type, count(*) cnt from {cp} where type in ('snt','tok') group by type")) 
	res = { 'cate':"lempos", 'cp': cp, 'num': len(rows), 'sum': sum([row[-1] for row in rows]), 'sntnum': dic['snt'], 'lexnum': dic['tok'], 'data': ssi }
	save(res, f"{cp}-lempos.json")

def lem_lex(cp="dic"):
	rows = cursor_rows(f"select lem, lex, count(*) cnt from {cp} where type='tok' and lem rlike '[a-z]+' and pos not in ('NUM','PUNCT','PROPN') group by lem, lex")
	ssi = defaultdict(dict) 
	for lem,lex, cnt in rows: ssi[lem][lex]  = cnt 
	dic = dict( esrows(f"select type, count(*) cnt from {cp} where type in ('snt','tok') group by type")) 
	res = { 'cate':"lemlex", 'cp': cp, 'num': len(rows), 'sum':  sum([row[-1] for row in rows]), 'sntnum': dic['snt'], 'lexnum': dic['tok'], 'data': ssi }
	save(res, f"{cp}-lemlex.json")

def lempos_attr(cp="dic"):
	''' name, attr, count '''
	ssi = defaultdict(Counter) 
	rows = cursor_rows(f"select lem, pos, tag, count(*) cnt from {cp} where type='tok' and lem rlike '[a-z]+' and pos in ('ADJ','ADV','VERB','NOUN') group by lem, pos, tag")
	for lem,pos,tag, cnt in rows: ssi[f"{lem}:{pos}"].update({ tag: cnt })

	rows = cursor_rows(f"select lem, pos, dep, count(*) cnt from {cp} where type='tok' and lem rlike '[a-z]+' and pos in ('ADJ','ADV','VERB','NOUN') group by lem, pos, dep")
	for lem,pos,dep, cnt in rows: ssi[f"{lem}:{pos}"].update({ f"~{dep}": cnt })  # door:NOUN:~dobj

	rows = cursor_rows(f"select glem, gpos, dep, count(*) cnt from {cp} where type='tok' and glem rlike '[a-z]+' and gpos in ('ADJ','ADV','VERB','NOUN') group by glem, gpos, dep")
	for lem,pos,dep, cnt in rows: ssi[f"{lem}:{pos}"].update({ dep: cnt })  # open:VERB:dobj 
	
	save( { k: si.most_common() for k,si in ssi.items()}, f"{cp}-lempos-attr.json")

def dumpcp(cp, rels:list=["dobj_VERB_NOUN","nsubj_VERB_NOUN","amod_NOUN_ADJ", "advmod_VERB_ADV", "advmod_ADJ_ADV", "advmod_ADV_ADV", "prep_VERB_ADP"
			, "conj_VERB_VERB","conj_NOUN_NOUN","conj_ADJ_ADJ","conj_ADV_ADV", "oprd_VERB_ADJ", "oprd_VERB_NOUN", "compound_NOUN_NOUN"
			, "xcomp_VERB_VERB", "acomp_VERB_ADJ"], 
			tags:list=["advcl_VERB_VBG","advcl_VERB_VBN", "advcl_VERB_ADJ","xcomp_VERB_VBG","xcomp_VERB_VB"]):
	''' cp: dic/gzjc , 2023.1.7 '''
	print ("started:", cp , rels, tags, flush=True) 
	lem_pos(cp)
	lem_lex(cp)
	lex_rank(cp) 
	lempos_attr(cp)
	for pos in ("NOUN","VERB","ADJ","ADV"):  
		print ( cp, pos, flush=True) 
		pos_rank(pos, cp)
	for tag in tags : 
		print (cp,  tag, flush=True) 
		arr = tag.strip().split('_') 
		gov_tags(arr[0], arr[1], arr[2], cp)
		tag_govs(arr[0], arr[1], arr[2], cp)

	for rel in rels : 
		print (cp,  rel, flush=True) 
		arr = rel.strip().split('_') 
		gov_deps(arr[0], arr[1], arr[2], cp)
		dep_govs(arr[0], arr[1], arr[2], cp)

	print ("finished:", cp ) 

if __name__ == '__main__': 
	fire.Fire( {"dumpcp":dumpcp} )

'''

GET /c4-*/_search
{
  "query": {
    "bool": {
      "must": [
        { "match_phrase": {"postag": "_idea"}},
        { "match_phrase": {"postag": "children"}},
        { "match_phrase": {"postag": "the early years"}}
      ] 
    }
  }
}


sophrase("doctors _decide to save")
['My doctors decided to save money on scalpels .',
 'The doctors decided to save has much arms and legs has they could for me .',
 'After over a year on life support , the doctors decided to save resources by pulling the plug and letting him die .']

hybchunk("some of _PRON memories _be _ADJ")
hybchunk("some of _PRON memories _be _ADJ")

GET /clec/_search
{
  "query": { "match": {"type": "snt"}   }, 
  "size":0,
  "aggs": {
    "myagg": {
      "terms": {
        "field": "kps",
         "include": "dobj:have_VERB:NOUN_dream"
      },
    "aggs" : {
                "snt" : {
                    "top_hits": { "_source": {"includes":"snt" }, "size":5
                    }
                }
            }

    }
  }
}

GET /dic/_search
{
  "size":0,
  "aggs": {
    "myagg": {
      "terms": {
        "field": "kps",
         "include": "VERB:sound|ADJ:sound|ADV:sound|NOUN:sound"
      }
    }
  }
}

GET /dic/_search
{
  "size":0,
  "aggs": {
    "myagg": {
      "terms": {
        "field": "kps",
         "include": "VERB:.*",
         "size":10000
      }
    }
  }
}

def dobj():
	words = requests.get("http://files.jukuu.com:8000/static/yulk/verblist.json").json() 
	dic = { w: cursor_rows(f"select lem, count(*) cnt from dic where type ='tok' and glem = '{w}' and gpos='VERB' and dep = 'dobj' and pos='NOUN' group by lem order by cnt desc") for w in words }
	with open('dobj-VERB-NOUNs.json','w') as fw:
		fw.write(json.dumps( dic ))

def advcl():
	si = cursor_rows("select glem, count(*) cnt from dic where type='tok' and tag='VBG' and dep='advcl' and gpos='VERB' group by glem order by cnt desc")
	dic = {}
	for s, i in si: 
		if i > 1 : 
			dic[s] = cursor_rows(f"select lex, count(*) cnt from dic where type='tok' and tag='VBG' and glem='{s}' and dep='advcl' and gpos='VERB' group by lex order by cnt desc")
	save(dic, "advcl-VERB-VBG.json")
'''