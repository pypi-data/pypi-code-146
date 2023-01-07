# 2022.8.21 
import json,fire,sys, os, hashlib ,time ,  fileinput
from elasticsearch import Elasticsearch,helpers
import so 

def run(infile, idxname=None, batch=100000, eshost='127.0.0.1',esport=9200): 
	''' python3 -m so.loadc4 c4-train.00099-of-01024.json.gz '''
	es	  = Elasticsearch([ f"http://{eshost}:{esport}" ])  
	if not idxname : idxname = infile.split('.')[0]  # c4-train
	print(">>started: " , infile, idxname, flush=True )
	if not es.indices.exists(index=idxname): es.indices.create(index=idxname, body=so.config) #, body=snt_mapping

	actions=[]
	for line in fileinput.input(infile,openhook=fileinput.hook_compressed): 
		try:
			arr = json.loads(line.strip())
			url = arr.get('url','')
			if not url: continue
			did = hashlib.md5(url.encode("utf8")).hexdigest()

			actions.append( {'_op_type':'index', '_index':idxname, '_id': did, '_source': arr } )
			if len(actions) >= batch: 
				helpers.bulk(client=es,actions=actions, raise_on_error=False)
				print ( actions[-1], flush=True)
				actions = []
		except Exception as e:
			print("ex:", e)	
	if actions : helpers.bulk(client=es,actions=actions, raise_on_error=False)
	print(">>finished " , infile, idxname )

if __name__ == '__main__':
	fire.Fire(run)
'''
{"_index": "gzjc", "_type": "_doc", "_id": "2897-stype", "_source": {"src": 2897, "tag": "simple_snt", "type": "stype"}}
import warnings
warnings.filterwarnings("ignore")
'''