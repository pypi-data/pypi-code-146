# 2022.9.22
import redis, time, json,sys,os, fire, traceback

def run(src_name, tgt_name=None, src_host='172.17.0.1', src_port=6379, src_db=0, tgt_host='172.17.0.1', tgt_port=6665, tgt_db=0, debug:bool=False):  
	''' python pubsub-sync.py pen_stroke '''
	redis.src  = redis.Redis(host=src_host, port=src_port, db=src_db,   decode_responses=True) 
	redis.tgt  = redis.Redis(host=tgt_host, port=tgt_port, db=tgt_db,   decode_responses=True) 
	if tgt_name is None: tgt_name = src_name
	print (f"started: {src_name} -> {tgt_name}", redis.src, redis.tgt, flush=True)
	ps = redis.src.pubsub()
	ps.subscribe(src_name)
	for item in ps.listen():
		if item['type'] == 'message':
			if debug: print ( item['data'] ) 
			redis.tgt.publish(tgt_name, item['data'])


if __name__ == '__main__': 
	fire.Fire(run)