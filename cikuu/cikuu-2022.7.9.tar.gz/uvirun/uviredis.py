# 2022.8.6 cp from stream/uvirun.py  | rhost=172.18.0.1 uvicorn uviredis:app --host 0.0.0.0 --port 16379 --reload 
import json,requests,hashlib,os,time,redis,fastapi, uvicorn , random,asyncio, platform 
from fastapi.responses import HTMLResponse, StreamingResponse, PlainTextResponse,  RedirectResponse
from fastapi.requests import Request
from typing import Iterator
app	= globals().get('app', fastapi.FastAPI()) #from uvirun import *
if not hasattr(redis,'r'): 
	redis.r		= redis.Redis(host=os.getenv("rhost", "127.0.0.1" if "Windows" in platform.system() else "172.17.0.1"), port=int(os.getenv('rport', 6379)), db=int(os.getenv('rdb', 0)), decode_responses=True) 

from fastapi.staticfiles import StaticFiles #http://localhost/static/index.html
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/redis/info')
def redis_info1(): return redis.r.info()

@app.get('/tcl/xy_change')
def xy_change(x:int="210",y:int="297",page_x:int="210",page_y:int="297",height:int="5600",width:int="7920"): 
	'''腾千里 码点坐标转换为可视化宽高'''
	res = {} 
	res['x'] = round(x * height * 1.524 / page_x)
	res['y'] = round(y * width * 1.524 / page_y)
	print(res)
	return res

@app.get('/redis/rg_pyexecute')
def rg_pyexecute(cmd:str="GB().flatmap(lambda x: execute('hvals', x['key']) ).countby().run('rid-230537:tid-1:uid-*')", name:str = 'rg.eval'):
	''' GB().map(lambda x: x['value']).flatmap(lambda x: x.split()).countby().run('sent:*')	'''
	res = redis.r.execute_command(*["RG.PYEXECUTE",cmd if cmd.startswith("GB().") else f"GB().{cmd}"])
	return [ eval(line) for line in res[0] ] if res and len(res) > 0 else None 

@app.post('/redis/mexec')
def command_execute_mul(cmds:dict={"test1":["get","hello"], "snt-search": "FT.SEARCH ftsnt '@cola:[0.5,0.9]' limit 0 2".split(),}):
	''' execute sql-like-scripts over redis '''
	res = {} 
	for name, args in cmds.items():
		try:
			args = args if isinstance(args, list) else args.split()
			res[name] = mapf.get(name.split(":")[0], lambda x: x)(redis.r.execute_command(*args))
		except Exception as e:
			res[name] = str(e)
	return res 
	
@app.get('/redis/get')
def redis_get(key:str=""):
  return redis.r.get(key)

@app.post('/redis/keylist')
def redis_keylist(keys:list=["ap-ap136:info:page-1713.537.31.107"],names:list=["ctime"]):
	return [{"key": key, "value":redis.r.hmget(key,*names)} for key in keys]

@app.post('/redis/keylistAll')
def redis_keylistAll(keys:list=["ap-ap136:info:page-1713.537.31.107"]):
	return [{"key": key, "value":redis.r.hgetall(key)} for key in keys]

@app.get('/redis/hgetall')
def redis_hgetall(key:str='rid-230537:tid-1', JSONEachRow:bool=False): 
	return redis.r.hgetall(key) if not JSONEachRow else [{"key":k, "value":v} for k,v in redis.r.hgetall(key).items()]

@app.get('/redis/hgetalls')
def redis_hgetalls(pattern:str='rid-*'):
	''' rid-230537:tid-1:uid-* | for JSONEachRow , added 2022.5.17 '''
	return { key: redis.r.hgetall(key) for key in redis.r.keys(pattern) if redis.r.type(key) == 'hash' }

@app.get('/redis/zrangelist')
def redis_zrangelist(pattern:str='stroke:ap-quick:page-1713.537.31.92:pen-BP2-0L3-03I-4V:item-*', withscores:bool=False):
	''' stroke:ap-quick:page-1713.537.31.92:pen-BP2-0L3-03I-4V:item-fill-11  '''
	return { key: list(redis.r.zrange(key,0,-1, withscores=withscores)) for key in redis.r.keys(pattern) if redis.r.type(key) == 'zset' }

@app.get('/redis/keys_hgetall')
def redis_hgetalls_map(pattern:str='rid-230537:tid-0:uid-*'):
	''' added 2022.5.14 '''
	return [] if pattern.startswith("*") else [{"key": key, "value":redis.r.hgetall(key)} for key in redis.r.keys(pattern)]

@app.get('/redis/keys')
def redis_keys(pattern:str='rid-230537:tid-0:uid-*'):	return [] if pattern.startswith("*") else [{"key": key} for key in redis.r.keys(pattern)] 
@app.get('/redis/keys_hget')
def redis_keys_hget(pattern:str='rid-230537:tid-0:uid-*', hkey:str='rid', jsonloads:bool=False):
	''' added 2022.5.15 '''
	if pattern.startswith("*"): return []
	return [{"key": key, "value": ( res:=redis.r.hget(key, hkey), json.loads(res) if res and jsonloads else res)[-1] } for key in redis.r.keys(pattern)]

@app.get('/redis/hget')
def redis_hget(key:str='config:rid-10086:tid-1', hkey:str='rid', jsonloads:bool=False):
	res = redis.r.hget(key, hkey)
	return json.loads(res) if res and jsonloads else res  
@app.post('/redis/execute_command')
def redis_execute_command(cmd:list='zrevrange rid-230537:snt_cola 0 10 withscores'.split()):	return redis.r.execute_command(*cmd)
@app.post('/redis/execute_commands')
def redis_execute_commands(cmds:list=["info"]):	return [redis.r.execute_command(cmd) for cmd in cmds]

@app.post('/redis/xinfo')
def redis_xinfo(keys:list=["rid-230537:xwordidf","xessay"], name:str="last-entry"):	return { key: redis.r.xinfo_stream(key)[name]  for key in keys }
@app.get('/redis/delkeys')
def redis_delkeys(pattern:str="rid-230537:*"): return [redis.r.delete(k) for k in redis.r.keys(pattern)]
@app.post('/redis/delkeys')
def redis_delkeys_list(patterns:list=["rid-230537:*","essay:rid-230537:*"]): return [ redis_delkeys(pattern) for pattern in patterns ]
@app.get('/redis/delete')
def redis_delete(key:str="stroke:ap-{ap}:page-{page}:pen-{pen}:item-{item}"): return redis.r.delete(key)
@app.post('/redis/xadd')
def redis_xadd(name:str="xitem", arr:dict={"rid":"230537", "uid":"1001", "tid":0, "type":"fill", "label":"open the door"}): return redis.r.xadd(name, arr )
@app.get('/redis/xrange')
def redis_xrange(name:str='xitem', min:str='-', max:str="+", count:int=1): return redis.r.xrange(name, min=min, max=max, count=count)
@app.get('/redis/lrange')
def redis_lrange(name:str='stroke:ap-quick:page-1713.537.31.92:pen-BP2-0L3-03I-4V:item-fill-11', start:int=0, end:int=-1): return redis.r.lrange(name, start, end)
@app.get('/redis/xrevrange')
def redis_xrevrange(name:str='xlog', min:str='-', max:str="+", count:int=1): return redis.r.xrevrange(name, min=min, max=max, count=count)
@app.get('/redis/zrevrange')
def redis_zrevrange(name:str='rid-230537:log:tid-4', start:int=0, end:int=-1, withscores:bool=True, JSONEachRow:bool=False): return redis.r.zrevrange(name, start, end, withscores) if not JSONEachRow else [{"member":member, "score":score} for member, score in redis.r.zrevrange(name, start, end, withscores)]
@app.get('/redis/zrange')
def redis_zrange(name:str='rid-230537:log:tid-4', start:int=0, end:int=-1, withscores:bool=True, JSONEachRow:bool=False): return redis.r.zrange(name, start, end, withscores=withscores) if not JSONEachRow else [{"member":member, "score":score} for member, score in redis.r.zrange(name, start, end, withscores=withscores)]
@app.get('/redis/set')
def redis_set(key:str='rid-230537:config',value:str=""): return redis.r.set(key, value) 
@app.post('/redis/hset')
def redis_hset(arr:dict={}, key:str='rid-10086:tid-1:uid-pen-zz', k:str="label", v:str="v"):	return redis.r.hset(key, k, v, arr) 
@app.post('/redis/hmset')
def redis_hmset(arr:dict={}, key:str='rid-10086:tid-1:uid-pen-zz'):	return redis.r.hmset(key,arr) 
@app.post('/redis/hdel')
def redis_hdel(keys:list=[], name:str='one'): return redis.r.hdel(name, *keys) 
@app.get('/redis/hdel')
def redis_hdel_get(key:str='one', hkey:str='k,k1' , sep:str=','): return [redis.r.hdel(key, k) for k in hkey.split(sep)]
@app.post('/redis/zadd')
def redis_zadd(arr:dict={}, key:str='rid-230537:config'): return redis.r.zadd(key, arr) 
@app.get('/redis/xlen')
def redis_xlen(key:str='xsnt',ts:bool=False): return redis.r.xlen(key) if not ts else {"time":time.time(), "Value":redis.r.xlen(key)}
@app.get('/redis/zsum')
def redis_zsum(key='rid-230537:essay_wordnum',ibeg=0, iend=-1): return sum([v for k,v in redis.r.zrevrange(key, ibeg, iend, True)])
@app.get('/redis/zrangebyscore')
def redis_zrangebyscore(key='pen-id', min:float=0, max:float=0, withscores:bool=False):  return redis.r.zrangebyscore(key, min=min, max=max, withscores=withscores) 

@app.post('/redis/join_even_odd')
def redis_even_odd(arr:list=['even line','odd line'], asdic:bool=False): return dict(zip(arr[::2], arr[1::2])) if asdic else list(zip(arr[::2], arr[1::2]))

four_int = lambda four, denom=100: [int( int(a)/denom) for a in four]
xy = lambda four : [f"{a},{b}" for a in range(four[0], four[2]+2) for b in range( four[1], four[3] + 2) ] # xy_to_item
@app.post('/redis/penly/xy_to_item')
def penly_xy_to_items(arr:list=[[620,170,1800,370,"zh_CN-name"],[200,650,1150,880,"select-1:A"],[1300,650,2160,880,"select-1:B"],[2400,650,3520,880,"select-1:C"],[3550,650,4700,880,"select-1:D"],[200,1020,1160,1250,"select-2:A"],[1300,1020,2160,1250,"select-2:B"],[2400,1020,3520,1250,"select-2:C"],[3550,1020,4700,1250,"select-2:D"],[200,1400,1290,1590,"select-3:A"],[1360,1400,2160,1590,"select-3:B"],[2400,1400,3520,1590,"select-3:C"],[3550,1400,4760,1590,"select-3:D"],[200,1750,1160,1950,"select-4:A"],[1300,1750,2160,1950,"select-4:B"],[2400,1750,3520,1950,"select-4:C"],[3550,1750,4700,1950,"select-4:D"],[200,2100,1160,2320,"select-5:A"],[1300,2100,2160,2320,"select-5:B"],[2400,2100,3520,2320,"select-5:C"],[3550,2100,4700,2320,"select-5:D"],[200,2450,1160,2670,"select-6:A"],[1300,2450,2160,2670,"select-6:B"],[2400,2450,3400,2670,"select-6:C"],[3550,2450,4700,2670,"select-6:D"],[200,2800,1160,3040,"select-7:A"],[1300,2800,2260,3040,"select-7:B"],[2400,2800,3420,3040,"select-7:C"],[3550,2800,4700,3040,"select-7:D"],[200,3180,1160,3380,"select-8:A"],[1300,3200,2160,3380,"select-8:B"],[2400,3180,3520,3380,"select-8:C"],[3550,3180,4700,3380,"select-8:D"],[200,3530,1210,3750,"select-9:A"],[1300,3530,2360,3750,"select-9:B"],[2550,3530,3520,3750,"select-9:C"],[3550,3530,4700,3750,"select-9:D"],[200,3900,1160,4120,"select-10:A"],[1300,3900,2200,4120,"select-10:B"],[2400,3900,3520,4120,"select-10:C"],[3550,3900,4700,4120,"select-10:D"],[2580,4260,4380,4500,"fill-11"],[3000,4550,5240,4790,"zh_CN-fill-12"],[460,5050,620,5200,"cross-13:No_1"],[630,5050,950,5200,"cross-13:reliable_2"],[960,5050,1250,5200,"cross-13:figures_3"],[1260,5050,1390,5200,"cross-13:are_4"],[1400,5050,1780,5200,"cross-13:available_5"],[1790,5050,1930,5200,"cross-13:for_6"],[1940,5050,2220,5200,"cross-13:money_7"],[2230,5050,2750,5200,"cross-13:accumulated_8"],[2760,5050,2960,5200,"cross-13:from_9"],[2980,5050,3320,5200,"cross-13:popcorn_10"],[3330,5050,3530,5200,"cross-13:sales_11"],[3590,5050,3720,5200,"cross-13:but_13"],[3740,5050,3900,5200,"cross-13:film_14"],[3930,5050,4100,5200,"cross-13:fans_15"],[4120,5050,4420,5200,"cross-13:usually_16"],[4430,5050,4800,5200,"cross-13:consume_17"],[4820,5050,4870,5200,"cross-13:a_18"],[4880,5050,5000,5200,"cross-13:lot_19"],[5020,5050,5120,5200,"cross-13:of_20"],[5130,5050,5300,5200,"cross-13:this_21"],[310,5300,530,5500,"cross-13:salty_22"],[550,5300,730,5500,"cross-13:food_23"],[770,5300,1170,5500,"cross-13:especially_25"],[1200,5300,1400,5500,"cross-13:when_26"],[1440,5300,1800,5500,"cross-13:watching_27"],[1830,5300,1870,5500,"cross-13:a_28"],[1890,5300,2100,5500,"cross-13:tense_29"],[2110,5300,2390,5500,"cross-13:thriller_30"],[340,5920,1860,6290,"branstorm-14-1"],[2060,5920,3530,6290,"branstorm-14-2"],[3790,5920,5220,6290,"branstorm-14-3"],[480,6670,4880,6950,"essay15-1"],[499,7100,4880,7340,"zh_CN-question-1"],[4990,7140,5280,7390,"submit-1:0"],[310,7400,810,7700,"hands:0"],[3500,7450,3880,7700,"select-25:A"],[3960,7450,4270,7700,"select-25:B"],[4320,7450,4670,7700,"select-25:C"],[4720,7450,5050,7700,"select-25:D"],[5000,6720,5270,6940,"translate:0"],[420,470,610,580,"evidence-1:The_1"],[1020,470,1130,580,"evidence-1:of_2"],[1140,470,1370,580,"evidence-1:blood_3"],[1380,470,1610,580,"evidence-1:made_4"],[1620,470,1760,580,"evidence-1:the_5"],[1770,470,1910,580,"evidence-1:girl_6"],[1920,470,2090,580,"evidence-1:feel_7"],[2100,470,2280,580,"evidence-1:sick_8"],[2290,470,2450,580,"evidence-1:and_9"],[2460,470,2590,580,"evidence-1:she_10"],[2600,470,2860,580,"evidence-1:began_11"],[2870,470,2960,580,"evidence-1:to_12"],[2970,470,3120,580,"evidence-1:cry_13"],[600,500,1000,650,"display-select-1"],[3200,850,3600,1000,"display-select-2"],[760,1220,1160,1370,"display-select-3"],[3510,1570,3910,1720,"display-select-4"],[1080,1940,1480,2090,"display-select-5"],[430,2300,830,2450,"display-select-6"],[1550,2660,1950,2810,"display-select-7"],[1260,3000,1660,3150,"display-select-8"],[3670,3370,4070,3520,"display-select-9"],[480,3720,880,3870,"display-select-10"],[2430,5360,5240,5490,"display-cross-13"]], denom:int=100,key:str="page:1713.537.31.92:xy_to_item"): 
	''' submit data into the permanent store, updated 2021.10.8 '''
	return [redis.r.hset(key, k, tag) for x1,y1,x2,y2,tag in arr for k in xy( ( int(x1/denom), int(y1/denom), int(x2/denom), int(y2/denom)) )]

@app.post('/redis/penly/mock_send_stroke')
def penly_mock_send_stroke(strokes:list=["quick:1713.537.31.92:BP2-0L3-03I-4V:1658389523.028:3752,1389,100,1658389523 3738,1395,428,1658389523 3719,1429,720,1658389523 3731,1602,832,1658389523 3797,1605,848,1658389523 3845,1551,808,1658389523 3876,1375,708,1658389523 3840,1330,748,1658389523 3782,1331,740,1658389523",
"quick:1713.537.31.92:BP2-0L3-03I-4V:1658389718.028:2641,2157,100,1658389718 2623,2160,624,1658389718 2611,2192,700,1658389718 2607,2290,728,1658389718 2639,2315,796,1658389718 2711,2279,760,1658389718 2756,2109,756,1658389718 2688,2078,552,1658389718",
"quick:1713.537.31.92:BP2-0L3-03I-4V:1658389718.48:2604,2446,100,1658389718 2595,2482,700,1658389718 2606,2560,744,1658389718 2757,2442,788,1658389718 2609,2450,100,1658389718 2579,2508,100,1658389718",
"quick:1713.537.31.89:BP2-0L3-03I-4V:1658389981.072:3766,1648,676,1658389981 3755,1680,688,1658389981 3767,1811,772,1658389981 3807,1813,684,1658389981 3851,1790,708,1658389981 3881,1737,696,1658389981 3870,1682,724,1658389981 3836,1637,748,1658389981 3807,1635,748,1658389981 3796,1647,100,1658389981 3798,1643,100,1658389981",
"quick:1713.537.31.92:BP2-0L3-03I-4V:1659688058.044:3781,1060,231,1659688058 3771,1058,477,1659688058 3759,1062,704,1659688058 3752,1097,732,1659688058 3732,1139,736,1659688058 3731,1178,780,1659688058 3747,1200,808,1659688058 3778,1208,824,1659688058 3818,1194,772,1659688058 3864,1146,792,1659688058 3889,1091,772,1659688058 3875,1016,756,1659688058 3844,1006,772,1659688058 3808,1008,792,1659688058 3786,1023,640,1659688058 3777,1030,165,1659688058",
#open
"quick:1713.537.31.92:BP2-0L3-03I-4V:1659688120.028:3747,4355,100,1659688120 3746,4355,141,1659688120 3747,4355,516,1659688120 3745,4364,640,1659688120 3745,4384,724,1659688120 3759,4408,752,1659688120 3768,4412,780,1659688120 3770,4402,744,1659688120 3780,4381,736,1659688120 3785,4366,768,1659688120 3782,4353,784,1659688120 3781,4336,792,1659688120 3776,4327,772,1659688120 3768,4330,764,1659688120 3760,4334,776,1659688120 3759,4337,712,1659688120 3750,4350,188,1659688120 3750,4361,188,1659688120",
"quick:1713.537.31.92:BP2-0L3-03I-4V:1659688121.192:3810,4319,100,1659688121 3816,4315,198,1659688121 3819,4316,668,1659688121 3821,4317,740,1659688121 3822,4321,784,1659688121 3825,4328,812,1659688121 3833,4357,820,1659688121 3817,4492,840,1659688121 3813,4490,453,1659688121 3806,4479,104,1659688121",
"quick:1713.537.31.92:BP2-0L3-03I-4V:1659688121.524:3821,4326,100,1659688121 3823,4324,412,1659688121 3835,4324,648,1659688121 3853,4331,708,1659688121 3868,4353,756,1659688121 3871,4378,760,1659688121 3865,4394,796,1659688121 3843,4406,756,1659688121 3820,4411,236,1659688121",
"quick:1713.537.31.92:BP2-0L3-03I-4V:1659688122.02:3891,4369,100,1659688122 3892,4366,501,1659688122 3898,4367,660,1659688122 3902,4368,736,1659688122 3909,4370,784,1659688122 3921,4368,804,1659688122 3935,4360,792,1659688122 3939,4350,728,1659688122 3945,4339,776,1659688122 3937,4336,796,1659688122 3933,4330,816,1659688122 3924,4328,816,1659688122 3914,4331,840,1659688122 3906,4341,856,1659688122 3901,4359,856,1659688122 3902,4383,852,1659688122 3906,4409,852,1659688122 3922,4418,880,1659688122 3928,4417,868,1659688122 3935,4407,820,1659688122 3942,4390,100,1659688122 3944,4373,100,1659688122",
"quick:1713.537.31.92:BP2-0L3-03I-4V:1659688122.588:3978,4319,100,1659688122 3976,4319,277,1659688122 3980,4325,540,1659688122 3979,4329,728,1659688122 3981,4344,828,1659688122 3980,4368,844,1659688122 3977,4385,844,1659688122 3979,4390,880,1659688122 3978,4389,872,1659688122 3977,4383,816,1659688122 3980,4364,740,1659688122 3984,4340,736,1659688122 3986,4330,764,1659688122 3991,4325,780,1659688122 4003,4318,796,1659688122 4011,4314,816,1659688122 4023,4313,816,1659688122 4029,4315,832,1659688122 4031,4317,816,1659688122 4032,4321,828,1659688122 4031,4323,872,1659688122 4032,4327,876,1659688122 4032,4333,900,1659688123 4033,4358,876,1659688123 4033,4373,868,1659688123 4033,4386,856,1659688123 4029,4405,860,1659688123 4040,4417,888,1659688123 4036,4416,872,1659688123 4034,4411,744,1659688123 4027,4399,252,1659688123 3994,4370,252,1659688123",
], name:str='pen_stroke'):
	''' mock sending strokes to redis:pen_stroke '''
	redis.r.delete("stroke:ap-quick:page-1713.537.31.92:pen-BP2-0L3-03I-4V:item-fill-11") # open stroke
	for s in strokes :  redis.r.publish(name, s ) 
	return 'Finished sending data: ' + time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))  

@app.get('/redis/penly/mock')
def penly_mock(): return penly_mock_send_stroke()
              
@app.get('/redis/penly/svg', response_class=HTMLResponse)
def penly_svg(lkey:str="stroke:ap-quick:page-1713.537.31.105:pen-BP2-1E1-03P-MK:item-zh_CN-fill-7", start:int=0, end:int=-1, color:str='black', width:int=10, full:bool=True): 
	''' <svg viewBox="0 0 5600 7920">
  <polyline points="26,90 23,89 25,89 24,88 24,90 24,92 20,98 17,121 23,144 35,159 48,162 73,142 87,108 89,76 80,56 58,51 31,66 15,99 13,117" style="fill:none;stroke:blue;stroke-width:15" />
  <polyline points="97,54 94,52 97,47 109,44 110,41 111,42 112,43 112,41 116,42 114,44 117,53 124,113 134,167 140,174 153,143 164,109 167,83 170,64 172,62 166,61 155,59" style="fill:none;stroke:black;stroke-width:15" />
  <polyline points="175,108 178,114 188,118 199,121 215,120 242,112 247,102 248,92 247,84 237,75 219,72 211,77 205,95 199,125 200,153 210,171 220,173 247,155 273,116 290,89 297,78 298,71 296,64 294,61 294,63 295,64 296,66 297,68 299,76 302,107 309,145 310,156 310,145 312,118 319,91 325,86 327,89 332,99 340,105" style="fill:none;stroke:black;stroke-width:15" />
  <polyline points="410,81 423,50 399,62 381,85 377,135 384,166 392,173 405,174 424,150 444,134 448,126 449,125 447,125 448,125 447,125 448,128 448,131 450,141 456,157 467,166 482,169 489,149 492,133 490,117 478,102 450,91 445,94 444,99 459,110 481,102" style="fill:none;stroke:black;stroke-width:15" />
  <polyline points="527,89 532,82 532,79 534,81 535,84 534,102 526,134 524,140 526,139 531,132 535,113 546,90 558,75 568,64 569,64 571,67 570,71 577,97 578,114 578,117 579,117 582,114 586,108 594,91 604,74 613,60 614,58 615,59 616,63 618,82 615,111 616,133 614,162 614,156 625,124" style="fill:none;stroke:black;stroke-width:15" />
  <polyline points="655,84 655,87 659,93 668,96 681,95 696,90 710,82 718,70 718,57 715,52 709,48 698,47 670,57 655,96 652,145 681,175 710,174 724,168 728,160 733,128" style="fill:none;stroke:black;stroke-width:15" />
</svg> '''
	def polyline(stroke:str='903,554,100,1656990923 911,559,161,1656990923 917,552,201,1656990923', xmin:int=0, ymin:int=0): 
		res = []
		for s in stroke.split(' '): 
			arr = s.split(',')
			if len(arr) >= 4:  res.append( f"{int(arr[0]) - xmin},{int(arr[1]) - ymin}") 
		plist = " ".join(res)
		return f'<polyline points="{plist}" style="fill:none;stroke:{color};stroke-width:{width}" />'
	strokes = redis.r.lrange(lkey, start, end) if redis.r.type(lkey) == 'list' else redis.r.zrange(lkey, start, end)
	xypts	= [ ar.split(',') for stroke in strokes for ar in stroke.split(':')[-1].split(' ')]
	if not xypts: return ""
	x_min	= min([int(x) for x,y,p,t in xypts ])
	x_max	= max([int(x) for x,y,p,t in xypts ])
	y_min	= min([int(y) for x,y,p,t in xypts ])
	y_max	= max([int(y) for x,y,p,t in xypts ])
	polylines = "\n".join([ polyline(stroke, x_min, y_min) for stroke in strokes ])
	return HTMLResponse(content=f'<svg viewBox="0 0 {5600 if full else x_max - x_min} {7920 if full else y_max - y_min}">{polylines}</svg>')

@app.get('/redis/psub') 
async def redis_psub(request: Request)-> StreamingResponse:
	''' sse version pubsub psubscribe , 2022.8.24 '''
	async def getdata(request: Request) -> Iterator[str]:
		pattern = request.query_params.get('pattern','pen_*')
		span = float(request.query_params.get('span','0.2'))
		p = redis.r.pubsub(ignore_subscribe_messages=True)
		p.psubscribe(pattern) #"my-channel-1", "my-channel-2"
		while True:
			if not await request.is_disconnected()==True:
				message = p.get_message()
				if message: 
					yield f"{time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))}:{message}\n\n"
			await asyncio.sleep(span)
	return StreamingResponse(getdata(request), media_type="text/event-stream", headers={"Cache-Control": "no-cache","X-Accel-Buffering": "no"})

@app.get("/")
def read_root(request: Request): # 1012.penly.cn 
	penid = request.url.hostname.split('.')[0].strip() #client_host = request.client.host
	token = redis.r.hget("penid-folder", penid) #{"client_host":"123.116.137.86","host":"xx.werror.com"}
	return RedirectResponse(f"https://sentbase.feishu.cn/drive/folder/{token}")  if token else RedirectResponse(f"https://www.penly.cn")

@app.post('/feishu/event')
def feishu_event(arr:dict={ "challenge": "ajls384kdjx98XX", "token": "xxxxxx",     "type": "url_verification"   } ):
	''' last update: 2022.9.19 '''
	arr['listener_count'] = redis.r.publish("feishu_event", json.dumps(arr)) 
	return arr

# sudo pip install fastapi-utils
feishu  = "https://open.feishu.cn/open-apis"
datasource_id ='7142465268567015426'
tat		= lambda :requests.post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/", data={"app_id":"cli_a390c187f1f9d00b", "app_secret":"sL6udKjwYarn3y8QKb4nyfO18OFqyp3F"}).json()['tenant_access_token']
headers = lambda : {"content-type":"application/json", "Authorization":"Bearer " + tat()} # redis.tat

from fastapi_utils.tasks import repeat_every #https://fastapi-utils.davidmontague.xyz/user-guide/repeated-tasks/
@app.on_event("startup")
@repeat_every(seconds=7000)  # < 2 hours
def timer_update() -> None:
	redis.tat = tat() 
	print ( "feishu tat is updated:",  time.time(),  redis.tat, flush=True)

@app.get('/feishu/tat')
def feishu_tat():  return redis.tat

@app.get('/feishu/get') 
def feishu_get(url:str="search/v2/data_sources/7142465268567015426/items/pen-HH:20220914"):
	return requests.get(url if url.startswith("https://open.feishu.cn") else f"{feishu}/{url}", headers=headers()).json()

@app.post('/feishu/post') 
def feishu_post(arr:dict={}, url:str="search/v2/data_sources/7142465268567015426/items/pen-HH:20220914"):
	return requests.post(url if url.startswith("https://open.feishu.cn") else f"{feishu}/{url}", headers=headers(),json=arr).json()

@app.get('/feishu/datasource/get') 
def feishu_datasource_get(key:str='pen-HH:20220914', datasource_id:str='7142465268567015426'):
	res = feishu_get(f"search/v2/data_sources/{datasource_id}/items/{key}") # page-1713.537.31.92
	return json.loads( res.get('data',{}).get("item",{}).get("structured_data","{}") ) 

@app.get('/feishu/delete') 
def feishu_delete( url:str="search/v2/data_sources/7142465268567015426/items/pen-123:20220912:file_token"): #  key:str='pen-123:20220912:file_token', datasource_id:str='7142465268567015426'):
	return requests.delete(f"{feishu}/{url}", headers=headers()).json()

@app.post('/feishu/put') 
def feishu_datasource_put(arr:dict={
  "file_token": "shtcnDOEFBSeRzEIHv6r6NVYm1g",
  "cards": {"英语蓝卡": "5387f2"}
}, id:str="pen-HH:20220914", title:str='title', source_url:str='http://www.penly.cn', content_data:str='', datasource_id:str='7142465268567015426'):
	''' id: ap-*, card-*, pen-*,  '''
	return requests.post(f"https://open.feishu.cn/open-apis/search/v2/data_sources/{datasource_id}/items", headers = headers(), json={
  "id": id,
  "acl": [
    {
      "access": "allow",
      "value": "everyone",
      "type": "user"
    }
  ],
  "metadata": {
    "title": title,
    "source_url": source_url
  },
  "structured_data": json.dumps(arr),
  "content": {
    "format": "html",
    "content_data": content_data
  }
}).json()

@app.get('/feishu/put_metadata') 
def put_metadata(id:str="pen-HH:20220914", title:str='title', source_url:str='http://www.penly.cn', content_data:str='', datasource_id:str='7142465268567015426'):
	''' id: ap-*, card-*, pen-*,  '''
	return requests.post(f"https://open.feishu.cn/open-apis/search/v2/data_sources/{datasource_id}/items", headers = headers(), json={
  "id": id,
  "acl": [
    {
      "access": "allow",
      "value": "everyone",
      "type": "user"
    }
  ],
  "metadata": {
    "title": title,
    "source_url": source_url
  },
  "structured_data": "{}",
  "content": {
    "format": "html",
    "content_data": ""
  }
}).json()

@app.get('/feishu/pen2id_fs') 
def pen2id_fs(pen:str='BP2-0L3-03I-4V'):
	''' starts from 1001 '''
	id = requests.get(f"https://open.feishu.cn/open-apis/search/v2/data_sources/{datasource_id}/items/pen2id:{pen}", headers=headers()).json()['data'].get('item',{}).get("metadata",{}).get('title','')
	if id : return int(id)
	maxid = int(requests.get(f"https://open.feishu.cn/open-apis/search/v2/data_sources/{datasource_id}/items/pen2id:_maxid", headers=headers()).json()['data'].get('item',{}).get("metadata",{}).get('title','1001'))
	id = maxid + 1 # change to a random delta later 
	put_metadata("pen2id:_maxid", id ) 
	put_metadata(f"pen2id:{pen}", id ) 
	put_metadata(f"id2pen:{id}", pen ) 
	return id 

@app.get('/feishu/id2pen') 
def id2pen(id:int=1002):
	''' must hit '''
	return requests.get(f"https://open.feishu.cn/open-apis/search/v2/data_sources/{datasource_id}/items/id2pen:{id}", headers=headers()).json()['data'].get('item',{}).get("metadata",{}).get('title','')

@app.get('/feishu/get_xls_sheets') 
def get_xls_sheets(xls_token:str='shtcnDOEFBSeRzEIHv6r6NVYm1g'):
	''' 2022.9.13 '''
	return requests.get(f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/{xls_token}/sheets/query", headers=headers()).json()

@app.get('/feishu/new_xls') 
def new_xls(title:str="title", folder_token:str=""):
	''' '''
	return requests.post(f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheets", headers = headers(), json={
  "title": title,
  "folder_token": folder_token}).json() 

@app.get('/feishu/new_folder', response_class=PlainTextResponse) 
def new_folder(name:str="ap-quick", parent_folder_token:str="fldcn2gxTwkH0j1XQm4XbQbPake", key:str="penid-folder"):
	token = redis.r.hget(key, name)
	if not token: 
		res = requests.post(f"https://open.feishu.cn/open-apis/drive/v1/files/create_folder", headers = headers(), json={"name": name, "folder_token": parent_folder_token}).json()
		token = res.get('data',{}).get('token',json.dumps(res))	 
		redis.r.hset(key, name, token)
	return token

@app.get('/feishu/get_pen_folder') 
def get_pen_folder(pen:str="pen-123", penlist_folder_token:str="fldcnFGUAIg9Is8iUfNbvJPNOrE"):
	''' { "title": "fldcnXLBKs1W8K0aZCoMUFDrvHg" , "source_url": "https://sentbase.feishu.cn/drive/folder/fldcnXLBKs1W8K0aZCoMUFDrvHg" } '''
	meta = requests.get(f"https://open.feishu.cn/open-apis/search/v2/data_sources/{datasource_id}/items/{pen}:folder_token", headers=headers()).json()['data'].get('item',{}).get("metadata",{})
	if meta: return meta  # { "title": folder_token , "source_url": "https://sentbase.feishu.cn/drive/folder/fldcnXLBKs1W8K0aZCoMUFDrvHg" }

	res = requests.post(f"https://open.feishu.cn/open-apis/drive/v1/files/create_folder", headers = headers(), json={"name": pen, "folder_token": penlist_folder_token}).json()
	data = res.get('data',{})	 # "data": {"token": "fldcnXLBKs1W8K0aZCoMUFDrvHg", "url": "https://sentbase.feishu.cn/drive/folder/fldcnXLBKs1W8K0aZCoMUFDrvHg"  },
	put_metadata(f"{pen}:folder_token", title=data.get('token',''), source_url=data.get('url',''))
	return { "title": data.get('token','') , "source_url": data.get('url','') }

@app.get('/feishu/get_penpage_xls') 
def get_penpage_xls(pen:str="pen-123", page:str="1713.537.31.92", date:str="20220912"):
	''' https://sentbase.feishu.cn/sheets/shtcnWC6m4LEJtDUMtojlFZUcKh  {'file_token': 'shtcnWC6m4LEJtDUMtojlFZUcKh', 'sheet_id': 'de2f51'} '''
	id		= f"{pen}:{date}:{page}"
	meta	= requests.get(f"https://open.feishu.cn/open-apis/search/v2/data_sources/{datasource_id}/items/{id}", headers=headers()).json()['data'].get('item',{}).get("metadata",{})
	if meta: return {"file_token": meta["source_url"],  "sheet_id": meta["title"] } # "metadata": {"source_url": "file_token",  "title": "sheet_id" }

	page_name	= requests.get(f"https://open.feishu.cn/open-apis/search/v2/data_sources/{datasource_id}/items/page-{page}", headers=headers()).json()['data'].get('item',{}).get("metadata",{}).get('title',page)
	pen_folder	= get_pen_folder(pen) #{ "title": "fldcnXLBKs1W8K0aZCoMUFDrvHg" , "source_url": "https://sentbase.feishu.cn/drive/folder/fldcnXLBKs1W8K0aZCoMUFDrvHg" }
	res			= requests.post(f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheets", headers = headers(), json={"title": f"{date}-{page_name}-{pen}","folder_token": pen_folder.get('title','')}).json() 
	file_token  = res.get('data',{}).get('spreadsheet',{}).get('spreadsheet_token','')
	sheet_res	= requests.get(f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/{file_token}/sheets/query", headers=headers()).json()
	sheet_id	= sheet_res['data'].get("sheets",[{}])[0].get('sheet_id','')

	put_metadata(id, title=sheet_id, source_url = file_token)
	return {"file_token": file_token,  "sheet_id": sheet_id }

@app.get('/feishu/get_sheet') 
def get_sheet(file_token:str="shtcnxMkvkwo1NdE36h9wtS95Cd", sheet_title:str='Sheet1', index:int=0):
	''' get, create if not exsits  '''
	arr = requests.get(f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/{file_token}/sheets/query",headers = headers()).json()
	for ar in arr['data']['sheets']:
		if ar['title'] == sheet_title: return ar['sheet_id']
	res = requests.post(f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{file_token}/sheets_batch_update", headers = headers(),json={
  "requests": [
    {
      "addSheet": {
        "properties": {
          "title": sheet_title,
          "index": index
        }
      }
    }  ]
} ).json()
	return res['data']['replies'][0]['addSheet']['properties']['sheetId']

@app.get('/feishu/get_pen_xls_token') 
def get_pen_xls_token(pen:str="pen-123", date:str="20220912"):
	''' https://sentbase.feishu.cn/sheets/shtcnWC6m4LEJtDUMtojlFZUcKh  2022.9.15 '''
	id		= f"{pen}:{date}:xls_token"
	meta	= requests.get(f"https://open.feishu.cn/open-apis/search/v2/data_sources/{datasource_id}/items/{id}", headers=headers()).json()['data'].get('item',{}).get("metadata",{})
	if meta: return meta["source_url"] #,  "sheet_id": meta["title"] } # "metadata": {"source_url": "file_token",  "title": "sheet_id" }

	pen_folder	= get_pen_folder(pen) #{ "title": "fldcnXLBKs1W8K0aZCoMUFDrvHg" , "source_url": "https://sentbase.feishu.cn/drive/folder/fldcnXLBKs1W8K0aZCoMUFDrvHg" }
	res			= requests.post(f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheets", headers = headers(), json={"title": f"{date}-{pen}","folder_token": pen_folder.get('title','')}).json() 
	file_token  = res.get('data',{}).get('spreadsheet',{}).get('spreadsheet_token','')
	put_metadata(id, title=date, source_url = file_token)
	return file_token #{"file_token": file_token,  "sheet_id": sheet_id }

@app.get('/feishu/create_pen_xls') 
def create_pen_xls(pen:str="pen-123", date:str="20220912"):
	''' https://sentbase.feishu.cn/sheets/shtcnxMkvkwo1NdE36h9wtS95Cd  '''
	pen_xls = feishu_datasource_get(f"{pen}:{date}:file_token")
	file_token = pen_xls.get('file_token','') #if "file_token" in pen_xls : return pen_xls["file_token"]
	if not file_token:
		pen_folder = feishu_datasource_get(f"{pen}:folder")
		if not pen_folder : pen_folder = create_pen_folder(pen) 
		print ("folder:",  pen_folder) 
		folder_token = pen_folder.get('token','') 
		res = requests.post(f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheets", headers = headers(), json={"title": f"{date}-{pen}","folder_token": folder_token}).json() 
		file_token = res.get('data',{}).get('spreadsheet',{}).get('spreadsheet_token','')
		if file_token: feishu_datasource_put({"file_token":file_token}, f"{pen}:{date}:file_token")
	data = get_xls_sheets(file_token ).get('data',{})
	data['file_token'] = file_token
	return data #{'sheets': [{'grid_properties': {'column_count': 20, 'frozen_column_count': 0, 'frozen_row_count': 0, 'row_count': 200}, 'hidden': False, 'index': 0, 'resource_type': 'sheet', 'sheet_id': '3a7b99', 'title': 'Sheet1'}], 'file_token': 'shtcnxMkvkwo1NdE36h9wtS95Cd'}

@app.post('/feishu/del_sheet') 
def del_sheet(file_token:str="shtcnxMkvkwo1NdE36h9wtS95Cd", sheet_id:str='DQ0Kc'):
	'''  '''
	return requests.post(f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{file_token}/sheets_batch_update", headers = headers(),json={
  "requests": [
    {
      "deleteSheet": {
        "sheetId": sheet_id
      }
    }  ]
} ).json()

@app.get('/feishu/pen2id')
@app.get('/feishu/pen-id') 
def pen_to_id(pen:str="BP2-1A3-03I-HH"):
	''' http://werror.com:16379/feishu/pen-id?pen=xyza | 2022.9.17  '''
	id = redis.r.zscore("pen-id", pen) 
	if not id: 
		id = int(redis.r.zrevrange("pen-id",0,0,True)[0][-1]) + 1
		redis.r.zadd('pen-id', {pen:id})
	return int(id)

@app.get('/feishu/penid-folder') 
def penid_to_folder(penid:str="1023"):
	''' 2022.9.17 '''
	key = 'penid-folder'
	v = redis.r.hget(key, penid)
	if not v is None : return {"folder_token": v}

	penlist_token = redis.r.hget(key, 'penlist')
	res = requests.post(f"https://open.feishu.cn/open-apis/drive/v1/files/create_folder", headers = headers(), json={"name": f"pen-{penid}", "folder_token": penlist_token}).json()
	v = res.get('data',{}).get('token',json.dumps(res))	 # "data": {"token": "fldcnXLBKs1W8K0aZCoMUFDrvHg", "url": "https://sentbase.feishu.cn/drive/folder/fldcnXLBKs1W8K0aZCoMUFDrvHg"  },
	redis.r.hset(key, penid, v) 
	return {"folder_token": v}

@app.get('/feishu/pendate-token') 
def pendate_to_token(penid:str="1023", date:str="20220912"):
	''' 2022.9.17 '''
	key = f"penid-date:{penid}:{date}" #
	vals = redis.r.hgetall(key) 
	if 'xls_token' in vals : return vals['xls_token']

	res	= requests.post(f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheets", headers = headers(), json=dict(penid_to_folder(penid), **{"title": f"{date}-pen-{penid}"})  ).json() 
	xls_token  = res.get('data',{}).get('spreadsheet',{}).get('spreadsheet_token','')
	redis.r.hset(key, 'xls_token', xls_token)
	return xls_token

@app.post('/feishu/update_xls') 
def update_xls(values:list=[["Hellosxxx", 1],["World", 2]], range:str="A1:C20", file_token:str="shtcnxMkvkwo1NdE36h9wtS95Cd", sheet_id:str='3a7b99'):
	'''  '''
	return requests.put(f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{file_token}/values", headers = headers(), json={
"valueRange":{
    "range": f"{sheet_id}!{range}",
    "values": values
    }
}).json() 

@app.post('/feishu/parse-pen-label') 
def feishu_parse_pen_label(arr:dict={"item": "select-5", "label": "C", "ap": "quick", "page": "1713.537.31.92", "pen": "BP2-0L3-03I-4V", "tm": 1658389718.028, "stroke": "2641,2157,100,1658389718 2623,2160,624,1658389718 2611,2192,700,1658389718 2607,2290,728,1658389718 2639,2315,796,1658389718 2711,2279,760,1658389718 2756,2109,756,1658389718 2688,2078,552,1658389718"}): 
	''' parse pen_label, 2022.9.20  ''' 
	try:
		ap,pen,page,item = arr.get('ap',''), arr.get('pen',''), arr.get('page','') , arr.get('item','') 
		date		= time.strftime("%Y%m%d", time.localtime(arr['tm']))
		penid		= pen_to_id(pen)  # "pen-" + str(pen2id(pen)) 

		key			= f"penid-date:pen-{penid}:date-{date}" 
		vals		= redis.r.hgetall(key) 
		xls_token	= vals.get('xls_token','')
		if not xls_token: 
			res	= requests.post(f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheets", headers = headers(), json=dict(penid_to_folder(penid), **{"title": f"{date}-pen-{penid}"})  ).json() 
			xls_token  = res.get('data',{}).get('spreadsheet',{}).get('spreadsheet_token','')
			redis.r.hset(key, 'xls_token', xls_token)
			requests.patch(f"https://open.feishu.cn/open-apis/drive/v1/permissions/{xls_token}/public?type=sheet",headers = headers(),json={"external_access": True, "security_entity": "anyone_can_view", "comment_entity": "anyone_can_view", "share_entity": "anyone",  "link_share_entity": "tenant_readable",  "invite_external": True})

		sheet_id	= vals.get(f"page-{page}:sheet_id", '')
		if not sheet_id: 
			res = requests.post(f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{xls_token}/sheets_batch_update", headers = headers(),json={
  "requests": [
    {
      "addSheet": {
        "properties": {
          "title": redis.r.hgetall(f"page:{page}").get('sheet-title', page),
          "index": 0
        }
      }
    }  ]
} ).json()
			sheet_id =  res['data']['replies'][0]['addSheet']['properties']['sheetId']
			redis.r.hset(key, f"page-{page}:sheet_id", sheet_id)

		pagevals	= redis.r.hgetall(f"page:{page}")
		rowidx 		= int(pagevals.get(f"xlsrow:{item}", arr.get("item", "0").split("-")[-1] ))
		rowname		= pagevals.get(f"name:{item}", item)
		return {"key":key, "penid":penid, "date":date, "xls_token":xls_token, "sheet_id":sheet_id, "rowidx":rowidx, "rowname":rowname, "tat": redis.tat }
	except Exception as ex:
		print (">>feishu_parse_pen_label ex:", ex, "\t|", arr, flush=True)
		return {}

@app.post('/pen-label') 
def feishu_pen_label(arr:dict={"item": "select-5", "label": "C", "ap": "quick", "page": "1713.537.31.92", "pen": "BP2-0L3-03I-4V", "tm": 1658389718.028, "stroke": "2641,2157,100,1658389718 2623,2160,624,1658389718 2611,2192,700,1658389718 2607,2290,728,1658389718 2639,2315,796,1658389718 2711,2279,760,1658389718 2756,2109,756,1658389718 2688,2078,552,1658389718"}): 
	''' pen-label consumer of redis channel ''' 
	try:
		ap,pen,page = arr.get('ap',''), arr.get('pen',''), arr.get('page','') 
		date		= time.strftime("%Y%m%d", time.localtime(arr['tm']))
		hpen		= redis.r.hgetall(f"pen:{pen}") #date-20220919:page-1713.537.31.107:sheetid | date-20220919:xls

		xls_token	= hpen.get(f'date-{date}:xls','')
		if not xls_token: 
			res	= requests.post(f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheets", headers = headers(), json=dict( hpen['folder'], **{"title": f"{date}-pen-{hpen['id']}"})  ).json() 
			xls_token  = res.get('data',{}).get('spreadsheet',{}).get('spreadsheet_token','')
			redis.r.hset(f"pen:{pen}", f'date-{date}:xls', xls_token)
			requests.patch(f"https://open.feishu.cn/open-apis/drive/v1/permissions/{xls_token}/public?type=sheet",headers = headers(),json={"external_access": True, "security_entity": "anyone_can_view", "comment_entity": "anyone_can_view", "share_entity": "anyone",  "link_share_entity": "tenant_readable",  "invite_external": True})

		sheet_id	= hpen.get(f"date-{date}:page-{page}:sheetid", '')
		if not sheet_id: 
			res = requests.post(f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{xls_token}/sheets_batch_update", headers = headers(),json={
  "requests": [
    {
      "addSheet": {
        "properties": {
          "title": redis.r.hgetall(f"page:{page}").get('sheet-title', page),
          "index": 0
        }
      }
    }  ]
} ).json()
			sheet_id =  res['data']['replies'][0]['addSheet']['properties']['sheetId']
			redis.r.hset(f"pen:{pen}", f"date-{date}:page-{page}:sheetid", sheet_id)

		#redis.r.hmset(f"{key}:page-{page}:{arr['item']}", arr) 
		hpage	= redis.r.hgetall(f"page:{page}")
		rowidx 	= int(hpage.get(f"xlsrow:{item}", arr.get("item", "0").split("-")[-1] ))
		rowname	= hpage.get(f"name:{item}", item)

		row			= int(arr.get("item", "0").split("-")[-1])
		values		= [ arr.get('item',''), arr.get('label',''), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(arr.get('tm',''))), '***',arr.get('ap',''),  arr.get('stroke','') ] #%Y-%m-%d %H:%M:%S
		res			= requests.put(f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{xls_token}/values", headers = headers(), json={"valueRange":{"range": f"{sheet_id}!A{row}:Z{row}","values": [values]} }).json()
		print (penid, date, xls_token,sheet_id, row, res, values, flush=True) 
		return res
	except Exception as ex:
		print ( ">>pen_label ex:", ex, "\t|", arr, flush=True)

@app.post('/pen-label-to-essay')
def pen_label_essay(arr:dict={"item": "select-5", "label": "C", "ap": "quick", "page": "1713.537.31.92", "pen": "BP2-0L3-03I-4V", "tm": 1658389718.028, "stroke": "2641,2157,100,1658389718 2623,2160,624,1658389718 2611,2192,700,1658389718 2607,2290,728,1658389718 2639,2315,796,1658389718 2711,2279,760,1658389718 2756,2109,756,1658389718 2688,2078,552,1658389718"}): # one row of the essay is updated 
	''' connect pen_label to this api, 2022.9.21 '''
	try:
		ap,pen,page,item, label,tm = arr.get('ap',''), arr.get('pen',''), arr.get('page',''), arr.get('item',''), arr.get('label',''), arr.get('tm',time.time())
		if item.startswith("composition") or item.startswith("essay"):
			prefix	= item.split("-")[0].strip() #essay, composition, row , fill, select, essay_1 
			rows	= [( int(k.split("-")[-1]), snt) for k, snt in redis.r.hgetall(f"ap-{ap}:page-{page}:pen-{pen}:item-{item}").items() if k.startswith(f"{prefix}-")]  #essay3-2
			rows.sort(key=lambda a: a[0]) # composition-1, composition-2, ... 
			essay	= " ".join( [row[1] for row in rows if row[1] ]) # no para info
			redis.r.xadd('xessay', {'page':page, 'rid': f"{ap}-{page}", 'tid': item, 'uid':pen, 'essay_or_snts': essay , 'tm': tm, 'type': prefix}) #redis.r.publish("pen_essay", json.dumps({'ap':ap, 'pen':pen, 'essay': essay , 'tm': int(tm), 'label': label, 'item': item , 'type': prefix}) ) 
	except Exception as ex:
		print ( ">>pen_essay ex:", ex, "\t|", msg, flush=True) 

def start(port):
	''' python uviredis.py start 16379 '''
	uvicorn.run(app, host='0.0.0.0', port=16379)

if __name__ == '__main__':	
	import fire
	fire.Fire({"start":start}) 

'''
curl --location --request PUT 'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/shtcngNygNfuqhxTBf588jwgWbJ/values' \
--header 'Authorization: Bearer t-e346617a4acfc3a11d4ed24dca0d0c0fc8e0067e' \
--header 'Content-Type: application/json' \
--data-raw '{
"valueRange":{
    "range": "Q7PlXT!A1:B2",
    "values": [
      [
        "Hello", 1
      ],
      [
        "World", 1
      ]
    ]
    }
}'

--https://open.feishu.cn/open-apis/sheets/v3/spreadsheets
{
  "code": 0,
  "msg": "success",
  "data": {
    "spreadsheet": {
      "title": "title",
      "folder_token": "fldcnMsNb*****hIW9IjG1LVswg",
      "url": "https://bytedance.feishu.cn/sheets/shtcnmBA*****yGehy8",
      "spreadsheet_token": "shtcnmBA*****yGehy8"
    }
  }
}

{
  "code": 0,
  "data": {"token": "fldcnXLBKs1W8K0aZCoMUFDrvHg", "url": "https://sentbase.feishu.cn/drive/folder/fldcnXLBKs1W8K0aZCoMUFDrvHg"  },
  "msg": "success"
}

#print(penly_svg("stroke:ap-quick:pen-BP2-0L3-03I-4V:page-1713.537.31.90:item-fill-58")) 

new_xls : return 
{
  "code": 0,
  "data": {
    "spreadsheet": {
      "folder_token": "",
      "spreadsheet_token": "shtcniqBtL3XqNxiVj5S5jFLpoe",
      "title": "title",
      "url": "https://sentbase.feishu.cn/sheets/shtcniqBtL3XqNxiVj5S5jFLpoe"
    }
  },
  "msg": "success"
}

@app.get('/feishu/put_pen_token') 
def put_pen_token(file_token:str="shtcnMD6U26MAIX8KllkO9OQtQe", sheet_token:str="c50291", pen:str='pen-HH', date:str='20220915', datasource_id:str='7142465268567015426'):
	return requests.post(f"https://open.feishu.cn/open-apis/search/v2/data_sources/{datasource_id}/items", headers = {"content-type":"application/json", "Authorization":"Bearer " + str(tat())}, json={
  "id": f"{pen}:{date}",
  "acl": [
    {
      "access": "allow",
      "value": "everyone",
      "type": "user"
    }
  ],
  "metadata": {
    "title": sheet_token,
    "source_url": file_token
  },
  "structured_data": "{}",
  "content": {
    "format": "html",
    "content_data": ""
  }
}).json()

@app.get('/feishu/get_pen_token') 
def get_pen_token(pen:str='pen-HH', date:str='20220914', datasource_id:str='7142465268567015426'):
	return geturl(f"https://open.feishu.cn/open-apis/search/v2/data_sources/{datasource_id}/items/{pen}:{date}")

@app.get('/feishu/datasource')
def feishu_datasource():
	return {"pen":"7142465268567015426"} # pendate, card, ap, 

2) "pen_stroke"
3) "quick:1713.537.31.92:D80BCB700685:1663223820.0:4592,3175,40,1663223820 4626,3167,81,1663223820 4657,3161,77,1663223820 4694,3150,81,1663223820 4726,3144,83,1663223820 4792,3125,84,1663223820 4800,3123,92,1663223820 4802,3121,1,1663223820 4787,3126,1,1663223820 4787,3126,0,1663223820"
1) "message"
2) "pen_stroke"
3) "quick:1713.537.31.92:D80BCB700685:1663223823.029:4645,3307,44,1663223823 4680,3298,49,1663223823 4851,3251,54,1663223823 4874,3246,54,1663223823 4892,3246,55,1663223823 4917,3246,67,1663223823 4914,3246,1,1663223823 4915,3244,1,1663223823 4915,3244,0,1663223823"

apweb
https://blog.csdn.net/weixin_42530658/article/details/123415798
http://101.35.187.248:4070/#/
http://192.168.2.201:3000/setTarget.html
http://192.168.40.1/#/basic
'''