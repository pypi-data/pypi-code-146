# prefill func, 2022.11.23 | python xsnt-gec.py  xsnt --gpuhost gpu120.wrask.com:6379
import json,os,time,redis, socket, traceback,sys,fire, gecv1
now	= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))

def xgecsnts(redis_gec, snts:str=["She has ready.","It are ok."], timeout:int=9,): #gechost:str='gpu120.wrask.com', gecport:int=6379
	''' {'She has ready.': 'She is ready.', 'It are ok.': 'It is ok.'}  2022.11.21 '''
	if redis_gec is None: return {}
	id	= redis_gec.xadd("xsnts", {'snts':json.dumps(snts)})
	res = redis_gec.blpop([f"suc:{id}",f"err:{id}"], timeout=timeout)
	redis_gec.xdel("xsnts", id)
	return {} if res is None else json.loads(res[1])

def consume(name:str, func:str='gec', gpuhost:str=None,timeout:int=9, waitms=3600000,  precount=1, debug=False): #ttl=47200,
	''' python xsnt-gec.py xsnt | gpuhost="gpu120.wrask.com:6379" '''
	rhost		= os.getenv('rhost', "172.17.0.1" if 'linux' in sys.platform else 'hw160.jukuu.com' )
	redis.r		= redis.Redis(host=rhost, port=int( os.getenv('rport', 6626 ) ), decode_responses=True) 
	redis.gpu	= None if gpuhost is None else redis.Redis(host=gpuhost.split(':')[0], port=int( gpuhost.split(':')[-1] ), decode_responses=True) 
	ttl			= int( os.getenv("ttl", 47200) )
	try:
		redis.r.xgroup_create(name, func,  mkstream=True)
	except Exception as e:
		print(e)

	def process(xid, arr): #[['xsnt', [('1583928357124-0', {'snt': 'hello worlds'})]]]
		''' '''
		try:
			snt		= arr.get('snt','') 
			if not redis.r.exists(f"gec:{snt}"):
				sntdic = xgecsnts(redis.gpu, [snt]) if redis.gpu is not None else gecv1.gecsnts([snt])
				[redis.r.setex(f"gec:{s}", ttl, gec) for s,gec in sntdic.items() if s ]
			
		except Exception as e:
			print ("xsnt-gec err:", e, arr) 
			exc_type, exc_value, exc_traceback_obj = sys.exc_info()
			traceback.print_tb(exc_traceback_obj)

	consumer_name = f'consumer_{socket.gethostname()}_{os.getpid()}'
	print(f"Started: {consumer_name}|{name}|{func}| ", redis.r, redis.gpu, now(), flush=True)
	print ( gecv1.gecsnts(["She has ready.","It are ok."]) , flush=True)
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