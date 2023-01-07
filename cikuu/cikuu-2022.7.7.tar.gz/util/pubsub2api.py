# 2022.9.19
import redis, time, requests,json,sys,os, fire, traceback

def run(name, host='172.17.0.1', port=6379, db=0, apihost:str='werror.com:16379', func:str='pen-label', debug:bool=False): 
	''' python pubsub2api.py pen_label '''
	redis.r  = redis.Redis(host=host, port=port, db=db,   decode_responses=True) 
	print ("started:", redis.r, flush=True)
	ps = redis.r.pubsub()
	ps.subscribe(name)
	for item in ps.listen():
		if item['type'] == 'message':
			if debug: print ( item['data'], flush=True) 
			try:
				arr = json.loads(item['data'])
				res = requests.post(f"http://{apihost}/{func}", json=arr).text
				print(res) 
			except Exception as ex:
				print ( ">>pubsub2api ex:", ex, "\t|", item, flush=True)
				exc_type, exc_value, exc_tb = sys.exc_info()
				tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
				print(''.join(tb.format_exception_only()))

if __name__ == '__main__': 
	fire.Fire(run)
	#process('{"item": "select-2", "label": "C", "ap": "quick", "page": "1713.537.31.92", "pen": "BP2-0L3-03I-4V", "tm": 1658389523.028, "stroke": "3752,1389,100,1658389523 3738,1395,428,1658389523 3719,1429,720,1658389523 3731,1602,832,1658389523 3797,1605,848,1658389523 3845,1551,808,1658389523 3876,1375,708,1658389523 3840,1330,748,1658389523 3782,1331,740,1658389523"}')
	#{"item": "select-1", "label": "B", "ap": "quick", "page": "1713.537.31.92", "pen": "D80BCB700693", "tm": 1663550364.042, "stroke": "1651,882,44,1663550364 1680,888,36,1663550364 1707,876,55,1663550364 1736,848,97,1663550364 1736,710,205,1663550364 1682,682,1,1663550364 1682,682,0,1663550364"}

'''
sudo uvicorn uvipenly:app --host 0.0.0.0 --port 80 --reload
'''
