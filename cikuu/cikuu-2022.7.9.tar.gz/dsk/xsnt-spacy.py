# 2022.11.16 python xsnt-spacy.py xsnt --host 172.17.0.1 --port 6626 --debug true
import json,os,time,redis, socket, traceback,sys,fire, spacy
now	= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
if not hasattr(spacy, 'nlp'): spacy.nlp	= spacy.load( os.getenv('spacy_model','en_core_web_sm')) # 3.4.1, lg

def consume(name:str, func:str='spacy341',  waitms=3600000,  precount=1,debug=False): #ttl=47200,
	''' python xsnt-spacy.py xsnt '''
	rhost	= os.getenv('rhost', "172.17.0.1" if 'linux' in sys.platform else 'hw160.jukuu.com' )
	redis.r	= redis.Redis(host=rhost, port=int( os.getenv('rport', 6626 ) ), decode_responses=True) 
	ttl		= int( os.getenv("ttl", 47200) )
	try:
		redis.r.xgroup_create(name, func,  mkstream=True)
	except Exception as e:
		print(e)

	def process(xid, arr): #[['xsnt', [('1583928357124-0', {'snt': 'hello worlds'})]]]
		''' '''
		try:
			snt		= arr.get('snt','') 
			if not redis.r.exists(f"snt:{snt}"):
				doc = spacy.nlp(snt) 
				redis.r.setex(f"snt:{snt}", ttl, json.dumps(doc.to_json())  )
			
		except Exception as e:
			print ("xsnt-spacy err:", e, arr) 
			exc_type, exc_value, exc_traceback_obj = sys.exc_info()
			traceback.print_tb(exc_traceback_obj)

	consumer_name = f'consumer_{socket.gethostname()}_{os.getpid()}'
	print(f"Started: {consumer_name}|{name}|{func}| ", redis.r, now(), flush=True)
	while True:
		item = redis.r.xreadgroup(func, consumer_name, {name: '>'}, count=precount, noack=True, block= waitms )
		if not item: break
		if debug: print(f"{name}:\t", item, "\t", now(), flush=True)  #redis.func(item)  #[['_new_snt', [('1583928357124-0', {'snt': 'hello worlds'})]]]
		for stm_arr in item : #[['xsnt', [('1583928357124-0', {'snt': 'hello worlds'})]]]
			for id,arr in stm_arr[1]: 
				try:
					process(id, arr) 
				except Exception as e:
					print(">>[stream]", e, "\t|", id, arr)
					exc_type, exc_value, exc_traceback_obj = sys.exc_info()
					traceback.print_tb(exc_traceback_obj)

	redis.r.xgroup_delconsumer(name, func, consumer_name)
	redis.r.close()
	print ("Quitted:", consumer_name, "\t",now())

if __name__ == '__main__':
	fire.Fire(consume)