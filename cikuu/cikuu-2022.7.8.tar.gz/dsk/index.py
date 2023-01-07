''' python gecdsk.py uvirun 7001 '''
from common import * 
import fastapi,uvicorn
app	= fastapi.FastAPI()

@app.get('/')
def home(): return fastapi.responses.HTMLResponse(content=f"<h2>dsk basic api</h2> <a href='/docs'> docs </a> | <a href='/redoc'> redoc </a> <br> last update: 2022-11-21 <hr>")

@app.post('/gecdsk')
def gec_dsk(formula:dict={ "ast":[9.9, 11.99, 15.3, 18.51, 25.32,				2,0.0882, 0.3241],
			"awl":[3.5, 4.1, 4.56, 5.1, 6.0,					3,0.0882, 0.5],
			"b3":[0, 0.03, 0.08, 0.12, 0.15 ,					1, 0.0956, 0.2096],
			"cl_sum":[1, 6.68, 12, 16, 26,						2,0.0441, 0.1621],
			"grammar_correct_ri":[0.6, 0.85, 0.92, 0.97,1.0,	2,0.0368, 0.1352],
			"internal_sim":[0.0, 0.08, 0.4, 0.6, 0.8,			4, 0.0735, 0.7688], #"internal_sim":[0.0, 0.08, 0.2, 0.3, 0.4,			4, 0.0735, 0.7688],
			"kp_correct_ri":[0.7, 0.9, 0.95, 0.97, 1,			1, 0.0368, 0.0807],
			"mwe_pv":[0.01,8.03, 12, 20.21, 25,					4, 0.0221, 0.2312],
			"pred_diff_max3":[3.84, 5.11, 6.51, 7.9, 10.09 ,	1, 0.0368, 0.0807],
			"prmods_ratio":[0.06, 0.21, 0.3, 0.4, 0.5,			2, 0.0294, 0.108],
			"prmods_tc":[1.1, 2.76, 4.75, 6.76, 10.0,			2, 0.0368, 0.1352],
			"simple_sent_ri":[0.4, 0.65, 0.9, 0.95, 1,			2, 0.0368, 0.1352],
			"snt_correct_ratio":[0.1, 0.6, 0.8, 0.9, 1,		1, 0.0368, 0.0807], #"snt_correct_ratio":[0.01, 0.2, 0.45, 0.75, 1,		1, 0.0368, 0.0807],
			"spell_correct_ratio":[0.8, 0.9, 0.97, 0.99, 1,		1, 0.1471, 0.3226],
			"ttr1":[3.43, 4.28, 5.2, 6, 6.8,					3, 0.0882, 0.5],
			"word_diff_avg":[4.47, 4.73, 5.25,5.8, 6.6,			1, 0.0441, 0.0967],
			"word_gt7":[0.11, 0.19, 0.3, 0.42, 0.49,			1, 0.0588, 0.1289]} , 
			essay_or_snts:str="She has ready. It are ok. I think it is right.",timeout:int=9, use_gec:bool=True, topk_gec:int=64,  internal_sim_default:float=0.2, #rescore:bool=False, 
			rhost:str=None, gechost:str='gpu120.wrask.com:6379', dskhost:str='gpu120.wrask.com:7095', with_dim_score:bool=False):
	''' rhost:str="hw6.jukuu.com:6626", dskhost:str='gpu120.wrask.com:7095', 2022.11.22 '''
	dsk = gecdsk(essay_or_snts,timeout=timeout, 
		redis_cache = rconn(rhost)	 if rhost is not None else None,  
		redis_gec	= rconn(gechost) if gechost else None, 
		use_gec=use_gec, topk_gec=topk_gec, dskhost=dskhost)
	
	dims = dsk.get('doc',{})
	if not 'internal_sim' in dims : dims['internal_sim'] = internal_sim_default
	if dims: 
		dsk['info'].update(dims_score(dims, formula, with_dim_score=with_dim_score))
		dsk['info'].update({"pingyu": dims_pingyu(dims)})
	return dsk 

@app.get("/spacy-sntbr")
def spacy_sntbr(text:str="The quick fox jumped over the lazy dog. The justice delayed is justice denied.", trim:bool=False, with_pid:bool=False):return sntbr(text, trim, with_pid)

@app.post('/test-xgec')
def test_xgec(arr:list=["She has ready.","It are ok."], timeout:int=9, gechost:str='gpu120.wrask.com:6379'):
	''' a tesing func '''
	rgec = rconn(gechost)
	id	= rgec.xadd("xsnts", {'snts':json.dumps(arr)})
	return rgec.blpop([f"suc:{id}",f"err:{id}"], timeout=timeout)

@app.post('/wps-gec-dsk')
def wps_xgec_dsk(arr:dict={"essay":"English is a internationaly language which becomes importantly for modern world. 中文In China, English is took to be a foreigh language which many student choosed to learn. They begin to studying English at a early age. They use at least one hour to learn English knowledges a day. Even kids in kindergarten have begun learning simple words. That's a good phenomenan, for English is essential nowadays. In addition to, some people think English is superior than Chinese. In me opinion, though English is for great significance, but English is after all a foreign language. it is hard for people to see eye to eye. English do help us read English original works, but Chinese helps us learn a true China. Only by characters Chinese literature can send off its brilliance. Learning a country's culture, especial its classic culture, the first thing is learn its language. Because of we are Chinese, why do we give up our mother tongue and learn our owne culture through a foreign language?"}
		, use_gec:bool=True, topk_gec:int=64, gec_local:bool=False, max_snt_len:int=2048, with_score:bool=True, score_snts:int=32, internal_sim_default:float=0.2, ibeg_byte:bool=True, diffmerge:bool=False, mkfbatch:int=0, rhost:str='172.17.0.1:6626', gechost:str='gpu120.wrask.com:6379', dskhost:str="172.17.0.1:7095",timeout:int=9, ttl:int=47200):  
	''' This api is specially customized for wps ONLY!!! 6626-xgec based version 
	# arr = {"essay":"Hello world"}, 用essay存放输入的作文
	# use_gec:bool    为True 时启动gpu的gec翻译
	# topk_gec:int = 64 , 只翻译文中 前64 个句子
	# max_snt_len:int=2048, 超过这个长度的句子不分析
	# with_score:bool=True,  为False时 不打分
	# score_snts:int=32,  取文中前32个句子进行打分
	# internal_sim_default:float=0.2 , 缺省内相关度，这个维度计算很重，wps不需要，直接取缺省值
	# ibeg_byte:bool=True： 返回偏移， wps前端定位需求
	# diffmerge:bool=False：GEC的合并策略
	# mkfbatch:int=0： 在调用mkf时的并发数
	# dskhost:str="172.17.0.1:7095"  提供dsk-java分析的api
	# timeout:int=9	：  调用gec时的blpop等待时间
	'''
	import mkf, score, gecv1 # added gecv1 2022.11.21
	from en.dims import docs_to_dims
	if not hasattr(redis, 'r'):
		redis.r = rconn(rhost)
		redis.gec = rconn(gechost) 

	try:
		start	= time.time()
		essay	= arr.get("essay", arr.get('doc','')) #.strip()
		if not essay: return {"failed":"empty essay"}

		sntpids = spacy.sntpid(essay)  # [(snt,pid) ]
		snts	= [snt for snt,pid in sntpids ] 	
		ratios  = [ valid_ratio(snt) for snt in snts ]
		valids  = [ snt for snt, ratio in zip(snts, ratios) if ratio >= float(arr.get('ratio',0.6)) and len(snt) < max_snt_len ] # at least 60% is English
		if redis.r: [redis.r.xadd('xsnt', {'snt':snt}, maxlen=30000) for snt in valids]  # notify:  spacy/gec , added maxlen 2022.10.15

		sntdic = {} if not use_gec else xgecsnts(redis.gec, snts[0:topk_gec],timeout=timeout) if redis.gec else gec_local(snts[0:topk_gec], redis.r)
		if redis.r is not None: [redis.r.setex(f"gec:{snt}", ttl, gec) for snt, gec in sntdic.items()]
		docs   = getdocs(snts, redis.r) #[parse(snt) for snt in snts ] 
		sntmkf = mkf.snt_mkf(valids, docs, sntdic, ibeg_byte=ibeg_byte, diffmerge =diffmerge , batch=mkfbatch, dskhost=dskhost) 
		
		if valids and with_score: #not 'noscore' in arr: 
			dims = docs_to_dims(valids[0:score_snts], docs[0:score_snts]) # only top [0:score_snts] considered for scoring 
			if not 'internal_sim' in dims: dims['internal_sim'] = internal_sim_default
			arr.update(score.dims_score(dims))
			arr['pingyu'] = get_pingyu(dims)

		fds = [ sntmkf.get(snt, {'feedback':{}, 'meta':{'snt':snt}}) for snt in snts ] 
		[ fd['meta'].update({"sid":i}) for i, fd in enumerate(fds) ]
		[ fd['meta'].update({"pid":sntpid[1], "snt_ori": sntpid[0]}) for sntpid, fd in zip(sntpids,fds) ]
		arr["timing"] = time.time() - start

		res = {'snt': fds, "info": arr}
		if 'dims' in dir() and dims: res.update({'doc': dims})
		return res

	except Exception as ex:
		print(">>gecv1_dsk Ex:", ex, "\t|", arr)
		exc_type, exc_value, exc_traceback_obj = sys.exc_info()
		traceback.print_tb(exc_traceback_obj)

def uvirun(port, reload:bool=False):
	''' '''
	uvicorn.run(app, host='0.0.0.0', port=port) #, reload=reload

def test(infile): 
	essay = open(infile,'r', encoding='UTF-8').read()
	print(essay) 

if __name__ == "__main__":  #python gec-dsk.py uvirun 7001
	import fire
	#uvicorn.run(app, host='0.0.0.0', port=7001)
	fire.Fire({"uvirun":uvirun, "test":test})	

# docker run -it --rm --name tt -p 7001:7000 -v /data/cikuu/pypi/dsk:/dsk wrask/gecv1 python /dsk/index.py
# docker run -d --restart=always --name gecdsk -p 7000:7000 -v /data/cikuu/pypi/dsk:/dsk wrask/gecv1 python /dsk/index.py