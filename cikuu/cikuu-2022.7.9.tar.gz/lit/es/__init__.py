from lit import * 

eshost		= os.getenv('eshost', 'es.corpusly.com:9200')

@st.cache
def typesum(type:str='snt', cp:str='clec'):
	return requests.post(f"http://{eshost}/_sql", json={"query":f"select count(*) from {cp} where type='{type}'"}).json()['rows'][0][0]

@st.cache
def kpsum(kp:str="dobj:open_VERB:NOUN_door", cp:str='clec'):
	arr = requests.post(f"http://{eshost}/{cp}/_search", json={
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

@st.cache
def kp_cnt(kps:str="ccomp:consider_VERB|dobj:consider_VERB|vtov:consider_VERB|vvbg:consider_VERB", cp:str='clec'):
	arr =  requests.post(f"http://{eshost}/{cp}/_search", json={
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

@st.cache
def kp_snt(kp:str="dobj:open_VERB:NOUN_door", cp:str='clec', topk:int=5):
	arr =  requests.post(f"http://{eshost}/{cp}/_search", json={
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

@st.cache
def kp_cnt_snt(kp:str="dobj:open_VERB:NOUN_door", cp:str='clec', topk:int=5):
	return requests.post(f"http://{eshost}/{cp}/_search", json={
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

@st.cache
def trp_cnt_snt(trp:str="dobj:open_VERB:NOUN_.*", cp:str='clec', term_size:int=1000, topk:int=1):
	arr = requests.post(f"http://{eshost}/{cp}/_search", json={
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

@st.cache
def phrase_count(hyb:str="_be in force", cp:str='sino', field:str='postag'):
	arr = requests.post(f"http://{eshost}/{cp}/_search", json={   "query": {  "match_phrase": { field: hyb    }   } } ).json()
	return arr['hits']['total']['value']

@st.cache
def term_count(term:str="NOUN:force", cp:str='sino', field:str='kps'):
	arr = requests.post(f"http://{eshost}/{cp}/_search", json={   "query": {  "term": { field: term    }   } } ).json()
	return arr['hits']['total']['value']

if __name__ == '__main__': 
	print (term_count()) 

def hello():
	return requests.post(f"http://{eshost}/clec/_search", json={
	  "query": { "match": {"type": "snt"}   }, 
	  "size":0,
	  "aggs": {
		"myagg": {
		  "terms": {
			"field": "kps",
			 "include": "ccomp:consider_VERB|dobj:consider_VERB|vtov:consider_VERB|vvbg:consider_VERB"
		  },
		  "aggs" : {
					"snt" : {
						"top_hits": { "_source": {"includes":"snt" }, "size":5
						}
					}
				}

		}
	  }
	}).json()