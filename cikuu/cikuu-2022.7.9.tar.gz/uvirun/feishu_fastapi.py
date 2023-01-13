#2022.11.5
from uvirun import *
import json,requests,hashlib,os,time,redis,fastapi, uvicorn , random,asyncio, platform ,sys, traceback
from fastapi.responses import HTMLResponse, StreamingResponse, PlainTextResponse,  RedirectResponse
from collections import Counter, defaultdict

feishu_host		= os.getenv('feishu_redis_host', '172.17.0.1:6665' if 'linux' in sys.platform else 'data.penly.cn:6665') 
redis.feishu 	= redis.Redis(host=feishu_host.split(':')[0], port=int(feishu_host.split(':')[-1]), decode_responses=True) 
hgetall		= lambda key='ap:CC1BE0E29824:sub-folder': redis.feishu.hgetall(key)	 # ap:* , page:*, pen:* , config:* , app:* 
tat			= lambda app='penclass': requests.post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/", data={"app_id": hgetall(f"app:{app}")['app_id'] , "app_secret": hgetall(f"app:{app}")['app_secret'] }).json()['tenant_access_token'] 
headers		= lambda app='penclass': {"content-type":"application/json", "Authorization":"Bearer " + tat(app)}
now			= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
page_title	= lambda page:	hgetall(f"page:{page}").get("title", page)
pagebit_key	= lambda app, ap, date, page, prefix='token': f"{prefix}:{app}:ap-{ap}:date-{date}:page-{page}"
mid			= lambda s, left, right=':':  s.split(left)[-1].split(right)[0]

@app.get('/feishu/app-sub-folder', tags=["feishu"])
def feishu_app_sub_folder(app:str="penclass",sub:str='en', refresh:bool=False): 
	''' 在应用根目录上 创建 sub-en- 子目录  '''
	v = redis.feishu.hget(f"app:{app}", f"sub-{sub}")
	if v: return v 
	res = requests.get("https://open.feishu.cn/open-apis/drive/v1/files", headers=headers(app)).json()
	tokens = [ file['token'] for file in res['data']['files'] if file['name'].startswith(f"sub-{sub}-") ]
	if tokens: 
		redis.feishu.hset(f"app:{app}", f"sub-{sub}", tokens[0])
		return tokens[0]
	else: 
		res = requests.post(f"https://open.feishu.cn/open-apis/drive/v1/files/create_folder", headers=headers(app), json={
			  "name": f"sub-{sub}-",
			  "folder_token": ""}).json()
		token = res['data']['token'] #https://open.feishu.cn/open-apis/drive/v1/permissions/fldcnhVndMAmQ8VK5oYLGiJpsfb/members?need_notification=false&type=folder
		redis.feishu.hset(f"app:{app}", f"sub-{sub}", token)
		return token
#print ( feishu_app_sub_folder (sub='ma')) 

@app.get('/feishu/app-sub-ap-folder', tags=["feishu"])
def feishu_app_sub_ap_folder(app:str="penclass",ap:str="CC1BE0E29824", sub:str='en', refresh:bool=False): 
	''' 在 sub-en- 下面 创建 ap-CC1BE0E29824- 子目录  '''
	v = redis.feishu.hget(f"app:{app}", f"sub-{sub}:ap-{ap}")
	if v: return v 
	sub_folder = feishu_app_sub_folder(app, sub) 
	assert sub_folder is not None, f"sub_folder is None, check app:{app}  sub-{sub}"

	res = requests.get(f"https://open.feishu.cn/open-apis/drive/v1/files?folder_token={sub_folder}&page_size=100", headers=headers(app)).json()
	tokens = [ file['token'] for file in res['data']['files'] if file['name'].startswith(f"ap-{ap}-") ]
	if tokens: 
		redis.feishu.hset(f"app:{app}", f"sub-{sub}:ap-{ap}", tokens[0])
		return tokens[0]
	else: 
		res = requests.post(f"https://open.feishu.cn/open-apis/drive/v1/files/create_folder", headers=headers(app), json={
			  "name": f"ap-{ap}-",
			  "folder_token": sub_folder}).json()
		token = res['data']['token'] #https://open.feishu.cn/open-apis/drive/v1/permissions/fldcnhVndMAmQ8VK5oYLGiJpsfb/members?need_notification=false&type=folder
		redis.feishu.hset(f"app:{app}", f"sub-{sub}:ap-{ap}", token)
		return token
#print ( feishu_app_sub_ap_folder (sub='ma')) 

@app.get('/feishu/app-sub-ap-date-folder', tags=["feishu"])
def feishu_app_sub_ap_date_folder(app:str="penclass",ap:str="CC1BE0E29824", sub:str='en', date:str="20220929", refresh:bool=False): 
	''' 在 ap-CC1BE0E29824- 下面 创建 20220929 子目录  '''
	folder = feishu_app_sub_ap_folder(app,ap, sub) 
	assert folder is not None, f"folder is None"
	res = requests.get(f"https://open.feishu.cn/open-apis/drive/v1/files?folder_token={folder}&page_size=200", headers=headers(app)).json()
	tokens = [ file['token'] for file in res['data']['files'] if file['name'].startswith(f"{date}") ]
	if tokens: 
		return tokens[0]
	else: 
		res = requests.post(f"https://open.feishu.cn/open-apis/drive/v1/files/create_folder", headers=headers(app), json={"name": date, "folder_token": folder}).json()
		token = res['data']['token'] #https://open.feishu.cn/open-apis/drive/v1/permissions/fldcnhVndMAmQ8VK5oYLGiJpsfb/members?need_notification=false&type=folder
		return token

def clone_bitable( app, template_token, title, parent_folder:str=""):
	''' for internal use only '''
	try:
		assert template_token 
		res	= requests.post(f"https://open.feishu.cn/open-apis/drive/v1/files/{template_token}/copy", headers = headers(app), json={"name":title,	"type": "bitable","folder_token":parent_folder }).json()
		print ("[cloned:]", res ) 
		token = res.get('data',{}).get('file',{}).get('token','') 
		if not token or token is None: return print (">> Failed to clone:", res, template_token, title, parent_folder, flush=True) 
		requests.patch(f"https://open.feishu.cn/open-apis/drive/v1/permissions/{token}/public?type=bitable",headers = headers(app),json={"external_access": True, "security_entity": "anyone_can_view", "comment_entity": "anyone_can_view", "share_entity": "anyone",  "link_share_entity": "tenant_readable",  "invite_external": True})
		requests.post(f"https://open.feishu.cn/open-apis/drive/v1/files/{token}/subscribe?file_type=bitable", headers = headers(app)).json()
		return token 
	except Exception as ex:
		print ( ">>clone ex:", ex, "\t|", template_token, title, parent_folder,  flush=True)
		traceback.print_exc()

@app.get('/feishu/pagebit-token', tags=["feishu"])
def feishu_pagebit_token( app:str="penclass", ap:str="CC1BE0E29824", date:str="20220929", page:str="0.0.0",prefix:str="token", refresh:bool=False): 
	''' 不需要设置 目标文件夹， 带有日期目录， 2022.11.2 '''
	key		= pagebit_key(app, ap, date, page,prefix=prefix) 
	if refresh: redis.feishu.delete(key) # added 2022.10.26
	token	= redis.feishu.hget(key, "token")
	if token: return token 

	sub		= redis.feishu.hgetall(f"page:{page}").get('sub','en')
	sub_folder = feishu_app_sub_folder(app, sub) 
	res		= requests.get(f"https://open.feishu.cn/open-apis/drive/v1/files?folder_token={sub_folder}&page_size=200", headers=headers(app)).json() # in random order
	temps	= [ file['token'] for file in res['data']['files'] if file['name'].startswith(f"page-{page}-") ]
	if not temps: return f"** page-{page}-desc , is missed at the expected folder={sub_folder}, app={app}, sub={sub}, failed to new pagebit token."
	folder	= feishu_app_sub_ap_date_folder(app,ap, sub, date)
	if folder is  None: return f"** Failed to find target folder, app:{app}, ap={ap}, sub={sub}, tp={tp}, page={page}, date={date}"

	res		= requests.get(f"https://open.feishu.cn/open-apis/drive/v1/files?folder_token={folder}&page_size=200", headers=headers(app)).json() # in random order
	tokens	= [ file['token'] for file in res['data']['files'] if file['name'].startswith(f"{date}-{page}-") ]
	token	=  tokens[0]  if tokens else clone_bitable( app, temps[0], f"{date}-{page}-{page_title(page)}", folder)
	redis.feishu.hset(key, "token", token)
	return token

@app.get('/feishu/pagebit-token-table', tags=["feishu"])
def feishu_pagebit_token_table(app:str='penclass', ap:str="CC1BE0E29824",date:str="20220929", page:str="0.0.3", prefix:str="token", idx:int=0, retry:int=4 ): 
	'''	{"token":token, "table":table , "msg": f"Extract the #{idx} table"} , 2022.11.2 '''
	key	= pagebit_key(app, ap, date, page,prefix=prefix) 
	for i in range( retry ) : 
		token = feishu_pagebit_token( app, ap, date, page,prefix=prefix) #token	= feishu_pagebit_token_with_cache(app, ap, date,page, prefix=prefix)
		if token.startswith("*") : return {"token":None, "table":None, "msg": token} 
		table	= redis.feishu.hget(key, "table")
		if token and table : return {"token":token, "table":table , "msg": f"cached in {key}"}

		res	= requests.get(f"https://open.feishu.cn/open-apis/bitable/v1/apps/{token}/tables",headers = headers(app)).json() # 第一次调用常常失败	#print ("get table:", token, res )  #get table: wikcnEGzujMBKAKInlV5tDPUUlf {'code': 91402, 'msg': 'NOTEXIST', 'data': {}}
		print (res) 
		code = res.get('code','')
		if code == 0: 
			table   = res['data']['items'][idx]['table_id']
			redis.feishu.hset(key, 'table', table) 
			return {"token":token, "table":table , "msg": f"Extract the #{idx} table"}
		elif code == 1254036: 	time.sleep(retry) #  {'code': 1254036, 'msg': 'Bitable is copying, please try again later.',
		elif code == 1002 or code == 91402: # { "code": 1002, "msg": "note has been deleted",  "data": {}} | {'code': 91402, 'msg': 'NOTEXIST', 'data': {}}
			key = redis.feishu.get(f"token-key:{token}")
			redis.feishu.delete(key if key else '', f"token-key:{token}") 
			continue # discard the old one 
		print ( f"No. {i}:", res, token) #No. 0: {'code': 91402, 'msg': 'NOTEXIST', 'data': {}}
		time.sleep( max(1,  int (retry * random.random()) )	  ) 
	return {"token":None, "table":None, "msg": f"failed for {retry} times"} 

@app.get('/feishu/pagebit-recid', tags=["feishu"])
def feishu_pagebit_recid(app:str='penclass', ap:str="CC1BE0E29824",date:str="20220929", page:str="0.0.3", prefix:str="token"): 
	'''	{"token":, "table": , pen:item: recid} '''
	key	= pagebit_key(app, ap, date, page,prefix=prefix) 
	arr = redis.feishu.hgetall(key) 
	if not 'token' in arr or not 'table' in arr: return feishu_pagebit_token_table(app, ap,date, page, prefix=prefix)  
	return arr

@app.post('/feishu/pagebit-upsert', tags=["feishu"])
def feishu_pagebit_upsert(data:dict={"ap": "CC1BE0E29824", "page": "0.0.0", "date" : "20220929", "label":"hello"}, app:str='penclass', ap:str="CC1BE0E29824",date:str="20220929", page:str="0.0.3", prefix:str="token"): 
	''' upsert one record, 2022.11.4 '''
	key	= pagebit_key(app, ap, date, page,prefix=prefix)
	dic = feishu_pagebit_recid(app, ap, date, page, prefix=prefix) 
	token, table = dic.get('token',''), dic.get('table','')
	if not token or not table: return {"code":404, "msg": f"token/table is None, app={app}, ap={ap}, date={date}, page={page}"}
	pk		= data.get('pen','') + ":" + data.get('item','')
	recid	= dic.get(pk, '')

	if recid :  # update 
		res  =   requests.put(f"https://open.feishu.cn/open-apis/bitable/v1/apps/{token}/tables/{table}/records/{recid}",json={"fields":  data }, headers = headers(app)).json()
		if res['code'] == 0 : return dict(res, **{"recid": recid, "func": "update", "token":token, "table":table})
		#if res['code'] == 1254043 : # #update: rec6iql5nP bascnjh9ezHaaXrLcvNzhNo77Yc {'code': 1254043, 'msg': 'RecordIdNotFound', 'error': {'log_id': '20221104215325010150211230051BD2CE'}}

	redis.feishu.hdel(key, pk) # not a valid recid, 
	res = requests.post(f"https://open.feishu.cn/open-apis/bitable/v1/apps/{token}/tables/{table}/records", json={"fields": data}, headers = headers(app)).json() # add new
	recid = res.get('data',{}).get('record',{}).get("record_id", "")
	if recid: redis.feishu.hset(key, pk, recid) 
	return dict(res, **{"recid": recid, "func": "addnew", "token":token, "table":table})

@app.post('/feishu/pagebit-upsert-batch', tags=["feishu"])
def feishu_pagebit_upsert_batch(items:list=[{"ap": "CC1BE0E29824", "page": "0.0.0", "date" : "20220929", "pen":"D80BCB7002AE","item":"fill-2", "label":"hello"}], app:str='penclass', ap:str="CC1BE0E29824",date:str="20220929", page:str="0.0.3", prefix:str="token"): 
	''' upsert batch records, clean data , adapt to feishu bitable, no extra fields, 2022.11.5 '''
	appage_labels = defaultdict(list) # 	
	[ appage_labels[ (arr['ap'],arr['date'], arr['page']) ].append( arr ) for arr in items if 'label' in arr] 	
	resp = {"appage-len": len(appage_labels), "itemcnt": len(items), 'xrec':{} }
	for appage, labels in appage_labels.items():  
		try:
			ap,date, page	= appage
			key	= pagebit_key(app, ap, date, page,prefix=prefix)
			dic = feishu_pagebit_recid(app, ap, date, page, prefix=prefix) 
			token, table = dic.get('token',''), dic.get('table','')
			if not token or not table: 
				resp['xrec'][f"error:{ap},{date},{page}"] =  f"token/table is None, app={app}, ap={ap}, date={date}, page={page}"
				continue 

			update_data, create_data = [], []
			for label in labels:
				pk = label['pen'] + ":" + label['item']
				update_data.append({"record_id": dic[pk], "fields": label })  if pk in dic else create_data.append({ "fields": label} )
				if pk in dic: resp['xrec'][ dic[pk] ] = dict(label, **{"recid":dic[pk], "token":token, "table":table, 'app':app }) 

			if create_data: #[{'fields': {'ap': 'CC1BE0E29824', 'page': '0.0.3', 'date': '20220929', 'pen': 'D80BCB7002AE', '姓名': '王强', 'item': 'branstorm-14-3', 'sub': 'en', 'label': 'possibility', 'ip': '', '耗时': 0, '笔划': 0}}]
				res = requests.post(f"https://open.feishu.cn/open-apis/bitable/v1/apps/{token}/tables/{table}/records/batch_create", json= {"records":create_data},headers = headers(app) ).json()
				pdic = { rec['fields']['pen'] + ":" + rec['fields']['item']:rec["record_id"] for rec in res.get('data',{}).get('records',[]) }
				redis.feishu.hset(key, mapping=pdic)
				for label in create_data: 
					recid = pdic[label['fields']['pen'] + ":" + label['fields']['item']]
					resp['xrec'][recid ] = 	dict(label['fields'], **{"recid":recid, "token":token, "table":table, 'app':app })
				resp[f'batch_create:{token}']  = res 
			if update_data: 
				res  = requests.post(f"https://open.feishu.cn/open-apis/bitable/v1/apps/{token}/tables/{table}/records/batch_update",json={"records":  update_data }, headers = headers(app)).json()
				resp[f'batch_update:{token}']  = res 
		except Exception as e:
				print(">>[Ex]", e, "\t|", labels, appage )
				traceback.print_exc()
	return resp

@app.post('/feishu/pagebit-recid-update', tags=["feishu"])
def feishu_pagebit_recid_update(arr:dict={}, app:str='penclass', ap:str="CC1BE0E29824",date:str="20220929", page:str="0.0.0", prefix:str="token"): 
	''' {pen}:{item}  -> {recid} ''' 
	key	= pagebit_key(app, ap, date, page,prefix=prefix) 
	return redis.feishu.hset(key, mapping=arr) 

@app.get('/pagebit/clear-bitable', tags=["feishu"])
def feishu_clear_bitable(app:str, token:str, table:str, page_size:int=500):
	''' '''
	res		= requests.get(f"https://open.feishu.cn/open-apis/bitable/v1/apps/{token}/tables/{table}/records?page_size={page_size}", headers=headers(app) ).json()
	recs	= [ item.get('record_id','') for item in res.get('data',{}).get('items',[])]
	res		= requests.post(f"https://open.feishu.cn/open-apis/bitable/v1/apps/{token}/tables/{table}/records/batch_delete", headers=headers(app),json={"records": [ rec    for rec in recs if rec   ]} ).json()
	print ( res) 
	return res 

@app.get('/pagebit/build-in-batch', tags=["feishu"])
def feishu_build_in_batch(app:str="penclass", ap:str="CC1BE0E29824",date:str="20220929", page:str="0.0.0", refresh:bool=False): 
	''' 根据存量label 数据一次生成 对应的 bitable , 2022.10.26'''
	res =  feishu_pagebit_token_table(app, ap,date, page)
	token = res['token']
	table = res['table'] 
	assert token is not None and table is not None , f"failed to get token/table" 
	if refresh: feishu_clear_bitable(app, token,table) 

	for k in redis.feishu.keys(f"label:ap-{ap}:date-{date}:page-{page}:pen-*"): #label:ap-CC1BE0E29824:date-20221025:page-177.0.2:pen-D80BCB7000A6:item-fill-16
		pen = mid(k,"pen-", ":")
		item = k.split(":item-")[-1]
	
		seconds	= set()
		rows	= redis.feishu.zrevrange(f"stroke:ap-{ap}:date-{date}:page-{page}:pen-{pen}:item-{item}", 0, -1, True)
		for stroke, tm in rows: seconds.add( int(tm))

		arr		= redis.feishu.hgetall(k)
		data	= {"fields": {"ap":  arr.get('ap',''), "page": arr.get('page',''), "date" : arr.get('date',''), "pen":arr.get('pen',''), "姓名": redis.feishu.hgetall(f"ap:{ap}:pen-name").get(pen, pen[-2:]), "item":arr.get('item','') , "sub": redis.feishu.hgetall(f"page:{page}").get('sub','en'), 'label':arr.get('label', ''), "耗时":len(seconds),  "笔划":len(rows)} }
		requests.post(f"https://open.feishu.cn/open-apis/bitable/v1/apps/{token}/tables/{table}/records",headers = headers(app),json=data).json() 
	return token 

@app.get('/snt/editdistance', tags=["feishu"])
def feishu_snt_editdistance(snt:str="how are you :", refer:str='how are you?'):
	''' called by bitable automation 2022.10.11'''
	import editdistance # pip install editdistance  https://pypi.org/project/editdistance/
	from nltk.tokenize import wordpunct_tokenize # pip install nltk  https://www.nltk.org/api/nltk.tokenize.html
	arr_snt = wordpunct_tokenize(snt.lower())
	arr_ref = wordpunct_tokenize(refer.lower())
	ed		= editdistance.eval(arr_ref, arr_snt )
	wc		= len(arr_ref)
	score	= round( abs(wc - ed) / float(wc), 2)
	return {"StatusMessage":"success","Extra":snt,"StatusCode":score}

@app.get('/feishu/sntlen', tags=["feishu"])
def feishu_sntlen(snt:str="how are you :"):
	return {"StatusMessage":"success","Extra":snt,"StatusCode":len(snt)}

@app.post('/feishu/event', tags=["feishu"])
def feishu_event(arr:dict={ "challenge": "ajls384kdjx98XX", "token": "xxxxxx",     "type": "url_verification"   } ):
	''' last update: 2022.9.19 '''
	arr['listener_count'] = redis.feishu.publish("pen-feishu-event", json.dumps(arr)) 
	event_type = arr.get('header',{}).get('event_type','')
	if event_type == 'drive.file.trashed_v1': 
		token	= arr.get('event',{}).get('file_token','')
		key		= redis.feishu.get(f"token-key:{token}") 
		redis.feishu.delete(f"token-key:{token}",  key if key is not None else "") #f"token-table:{token}",
	elif event_type == 'drive.file.bitable_record_changed_v1':  # added 2022.11.3
		token	= arr.get('event',{}).get('file_token','')
		key		= redis.feishu.get(f"token-key:{token}") 
		for act in arr.get('event',{}).get('action_list',[]):
			if act.get('action','') == 'record_deleted': 
				recid = act.get('record_id','') 
				pks = [pk for pk, rid in redis.feishu.hgetall(key).items() if rid == recid]
				if pks: redis.feishu.hdel(key, pks[0]) 
	return arr

@app.get('/feishu', tags=["feishu"])
def feishu_apdatepage(app:str='penclass', ap:str="CC1BE0E29824",date:str="20220929", page:str="0.0.0"): 
	''' 日卡每天一个文件bitable， 只建不删 ''' 
	token = feishu_pagebit_token(app, ap, date, page) 
	return RedirectResponse(f"https://{app}.feishu.cn/base/{token}")

if __name__ == '__main__':	
	print ( feishu_pagebit_upsert_batch()) 
	#uvicorn.run(app, host='0.0.0.0', port=80)