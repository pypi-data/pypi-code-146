# 2022.8.30 , pure load _source | {"_index": "gzjc", "_type": "_doc", "_id": "2897-stype", "_source": {"src": 2897, "tag": "simple_snt", "type": "stype"}}
import json,fire,sys, os, time ,  fileinput, so
from elasticsearch import Elasticsearch,helpers

def run(infile, index:str=None, batch=200000, refresh:bool=False, eshost='127.0.0.1',esport=9200): 
	''' python3 -m so.load gzjc.esjson.gz '''
	es	  = Elasticsearch([ f"http://{eshost}:{esport}" ])  
	if index is None : index = infile.split('.')[0]
	print(">>load started: " , infile, index, flush=True )
	if refresh or not es.indices.exists(index=index): 
		if es.indices.exists(index=index):es.indices.delete(index=index)
		es.indices.create(index=index, body=so.config) #, body=snt_mapping

	actions=[]
	for line in fileinput.input(infile,openhook=fileinput.hook_compressed): 
		try:
			arr = json.loads(line.strip())
			#if '_source' in arr and 'postag' in arr['_source']:  # added 2023.1.1
			#	arr['_source']['postag'] = arr['_source']['postag'].replace("_PRP$", '_PRPS')  # snts("_suggest _PRP$ house")
			arr.update({'_op_type':'index', '_index':index})
			actions.append( arr )

			if len(actions) >= batch: 
				helpers.bulk(client=es,actions=actions, raise_on_error=False)
				print ( actions[-1], flush=True)
				actions = []
		except Exception as e:
			print("ex:", e)	
	if actions : helpers.bulk(client=es,actions=actions, raise_on_error=False)
	print(">>load finished:" , infile, index )

if __name__ == '__main__':
	fire.Fire(run)

'''
GET /index_*/_search
GET /index_01,index_02/_search
'''