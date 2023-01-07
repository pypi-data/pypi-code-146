# 2022.8.29  rebuild cache
import json,fire,sys, os, hashlib ,time , requests, fileinput
from elasticsearch import Elasticsearch,helpers
from collections import Counter

def run(index, batch=10000, eshost='127.0.0.1',esport=9200): 
	''' python3 sikps.py gzjc --eshost es.corpusly.com '''
	es	  = Elasticsearch([ f"http://{eshost}:{esport}" ])  
	print(">>started: ",  index, flush=True )
	print (requests.post(f"http://{eshost}:{esport}/{index}/_delete_by_query", json={"query": {"exists": {"field":"s"} }}).text , flush=True)

	si = Counter()
	for doc in helpers.scan(es,query={"query": {"match": {"type":"snt"}}}, index=index):
		for kp in doc['_source'].get('kps',[]):
			si.update({kp:1})
			akp = kp.split(':')
			if len(akp) > 1: si.update({akp[0]:1})
			if len(akp) > 2: si.update({f"{akp[0]}:{akp[1]}":1})
	print(">>count of kp : ",  len(si), flush=True )

	actions=[]
	for s,i in si.items(): 
		actions.append( {'_op_type':'index', '_index':index, '_id': s, '_source': {"s":s, "i": i} } )
		if len(actions) >= batch: 
			helpers.bulk(client=es,actions=actions, raise_on_error=False)
			print ( actions[-1], flush=True)
			actions = []
	if actions : helpers.bulk(client=es,actions=actions, raise_on_error=False)
	print(">>finished ",  index )

if __name__ == '__main__':
	fire.Fire(run)