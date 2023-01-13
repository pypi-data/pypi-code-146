# 22-11-30
import json, sys, time, fire,traceback, requests,os

class util(object):
	def __init__(self): pass 

	def wps (self, host, port:int=7000, suffix:str='jukuu.com'):
		''' host=hw160 '''
		res = requests.post(f"http://{host}.{suffix}:{port}/wps-gec-dsk?use_gec=true&topk_gec=64&gec_local=false&max_snt_len=2048&with_score=true&score_snts=32&internal_sim_default=0.2&ibeg_byte=true&diffmerge=false&mkfbatch=0&dskhost=172.17.0.1%3A7095&timeout=9").json()
		print ( res) 

	def api (self, host, port:int=7000, suffix:str='jukuu.com'):
		''' host=hw160 '''
		res = requests.post(f"http://{host}.{suffix}:{port}/gecdsk?essay_or_snts=She%20has%20ready.%20It%20are%20ok.%20I%20think%20it%20is%20right.&timeout=9&use_gec=true&topk_gec=64&internal_sim_default=0.2&gechost=gpu120.wrask.com%3A6379&dskhost=gpu120.wrask.com%3A7095&with_dim_score=false").json()
		print ( res) 

if __name__ == '__main__': 
	fire.Fire(util) 