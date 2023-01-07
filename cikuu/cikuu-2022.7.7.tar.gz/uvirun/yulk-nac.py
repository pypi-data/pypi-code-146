# 2022.11.25 rhost=172.17.0.1 uvicorn yulk-nac:app --host 0.0.0.0 --reload 
import json,requests,hashlib,os,time,pymysql,fastapi, uvicorn , random,asyncio, platform, re 
from collections import defaultdict, Counter 
from functools import lru_cache
from dic import lemma_lex
from util import likelihood
from fastapi import Request
from typing import Optional
from fastapi import FastAPI, Header
from fastapi.responses import HTMLResponse, StreamingResponse, PlainTextResponse,  RedirectResponse

app		= globals().get('app', fastapi.FastAPI()) 
from fastapi.middleware.cors import CORSMiddleware  #https://fastapi.tiangolo.com/zh/tutorial/cors/
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

from fastapi.staticfiles import StaticFiles
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

myhost	= os.getenv("myhost", "172.17.0.1" if not "Windows" in platform.system() else "lab.jukuu.com")
myport  = int(os.getenv("myport", 3309))
mydb	= os.getenv("mydb", "nac")
conn	= pymysql.connect(host=myhost,port=myport,user='root',password='cikuutest!',db=mydb)

def get_cursor(ssdict:bool=False):
	try:
		conn.ping()
	except:
		conn = pymysql.connect(host=myhost,port=myport,user='root',password='cikuutest!',db=mydb)
	return conn.cursor(pymysql.cursors.SSDictCursor) if ssdict else conn.cursor()

@app.get('/yulk/fetchall')
def fetchall(sql:str="select attr, count from dic where name = 'open:VERB:dobj:NOUN' order by count desc limit 10", ssdict:bool=False, columns:str=None): # asdic:bool=False,
	''' ssdict: True to return [{k:v}] else [row], columns=name,value '''
	cursor = get_cursor(ssdict)
	cursor.execute(sql)
	rows =  [row for row in cursor.fetchall() ] 
	if columns: 
		columns = [s.strip() for s in columns.strip().split(',')]
		return [dict(zip(columns, row)) for row in rows]
	return rows

@app.get('/yulk/fetchone')
def fetchone(sql:str="select count(*) from corpuslist", ssdict:bool=False):
	cursor = get_cursor(ssdict)
	cursor.execute(sql)
	return cursor.fetchone() 

@app.get('/yulk/geti')
@lru_cache(maxsize=8192)
def geti(sql): return (row := fetchone(sql), int(row[0]) if row else 0)[-1]

@app.get('/yulk/query')
def query(sql:str="select attr, count from dic where name = 'open:VERB:dobj:NOUN' order by count desc limit 10"): 
	return fetchall(sql,True)

@app.get('/select')
def select_data(sql:str="select attr name, count value from dic where name = 'open:VERB:dobj:NOUN' order by count desc limit 10", dim:bool=False): 
	''' specially for goview | {"dimensions":["product","data1","data2"],"source":[{"product":"Mon","data1":120,"data2":130}, ''' 
	rows = fetchall(sql,True)
	if dim and rows:  rows = {"dimensions":[k for k in rows[0].keys()],"source": rows }
	return {"sql": sql, "data": rows }

# requests.get("http://minio.penly.cn/yulk/logdice:dic:VERB:dobj:NOUN").json()  ['overcome']
##
## goview-special functions
##
def _attach_header(request: Request, dic):
	''' query?sql=select '$varadv0' data '''
	sql = request.query_params.get('sql','')
	for k,v in dic.items():  # varcp=dic
		if k.startswith("var"):
			sql = sql.replace(f"${k}", v.strip() ) 
	return sql 

@app.get('/query')
def query_data(req: Request): 
	''' query?sql=select attr, count from dic where name = 'sound'  | 2022.12.22 ''' 
	sql		= _attach_header(req, req.headers)
	rows	= fetchall(sql,'asrow' not in req.query_params) 
	if 'dim' in req.query_params or len(rows[0]) > 2 :  rows = {"dimensions":[k for k in rows[0].keys()],"source": rows }
	if len(rows) == 1 and 'data' in rows[0]: rows = rows[0]['data']  # select 'good' data , added 2022.12.22
	return {"request": req.query_params, "headers": [(k,v) for k,v in req.headers.items() if k.startswith("var")],  "data": rows}

defaults = {"lemma":"sound", "q":"beautiful", "adj":"beautiful", "noun":"brink", "verb":"consider", "cp":"dic", "limit":"0,10"}
def make_sql(request: Request):
	''' # req?sql=select attr name, count value from $cp where name = '$verb:VERB:dobj:NOUN' order by count desc limit $limit '''
	sql = request.query_params.get('sql','')#if not sql: return "Failed to get 'sql'"  # where name = '$verb:VERB' 
	dic = dict(defaults, **request.query_params)
	for k,v in dic.items():  # verb=consider 
		if k not in ("sql") : 
			sql = sql.replace(f"${k}", v.strip() ) 
	return sql 

@app.get('/wordcloud')
async def goview_wordcloud(req: Request):
	''' wordcloud?sql=select attr, count from dic where name = 'sound'  '''
	sql		= _attach_header(req, req.headers) #make_sql(req) 
	color	= req.query_params.get('color','')
	rows	= fetchall(sql,False) #"textStyle":{"color":"78fbb2"},"emphasis":{"textStyle":{"color":"red"}}
	return {"sql": sql, "request": req.query_params, "data": [{"name":row[0], "value":row[1]} if not color else {"name":row[0], "value":row[1], "textStyle":{"color":f"#{color}"},"emphasis":{"textStyle":{"color":"red"}}} for row in rows]}

@app.get('/rows')
async def goview_rows(req: Request): return fetchall(make_sql(req))

@app.get('/bar')
async def goview_bar(req: Request):
	''' specially for goview | {"dimensions":["product","data1","data2"],"source":[{"product":"Mon","data1":120,"data2":130}, ''' 
	sql		= make_sql(req)
	rows	= fetchall(sql,True)
	return {"sql": sql, "data": {"dimensions":[k for k in rows[0].keys()],"source": rows } }

@app.get('/req')
async def query_request(request: Request):
	''' # req?sql=select attr name, count value from $cp where name = '$verb:VERB:dobj:NOUN' order by count desc limit $limit '''
	sql = request.query_params.get('sql','')
	if not sql: return "Failed to get 'sql'"  # where name = '$verb:VERB' 
	for k,v in request.query_params.items():  # verb=consider 
		if k not in ("sql") : 
			sql = sql.replace(f"${k}", v.strip() ) 
	rows = fetchall(sql,True)
	if rows:
		if 'dim' in request.query_params or len(rows[0]) > 2 :  rows = {"dimensions":[k for k in rows[0].keys()],"source": rows }
	return {"sql": sql, "request": request.query_params, "data": [v for v in rows[0].values()][0] if len(rows) == 1 and len(rows[0]) ==1 else rows } # [{"count(*)":10144423}]

@app.post('/yulk/querys')
def querys(sqls:dict={"wordlist": "select attr, count from dic where name = 'open:VERB:dobj:NOUN' order by count desc limit 10"}): 
	''' 几个query 的执行结果，  geti_* , '''
	return { name: geti(sql) if name.startswith('geti_') else fetchall(sql, True) for name, sql in sqls.items()}

sntnum	 = lambda cp='dic': geti(f"select sntnum from corpuslist where name ='{cp}'")
lexnum	 = lambda cp='dic': geti(f"select lexnum from corpuslist where name ='{cp}'")
lexcnt	 = lambda lex='considered', cp='dic': geti(f"select count(*) from {cp}_snt where match(snt) against ('{lex}')")
uppersum = lambda name='knowledge:NOUN:~dobj:VERB', cp='dic': (arr:=name.split(':'), geti(f"select count from {cp} where name ='{':'.join(arr[0:-1])}' and attr ='{arr[-1]}'"))[-1]
mf		 = lambda cnt, cp='dic': round( 1000000 * cnt / (sntnum(cp) + 0.01), 1)

@app.get('/')
def home(request: Request): 
	if len(request.query_params) > 0 : return request.query_params
	return HTMLResponse(content=f"<h2> mysql-nac (name, attr, count) api </h2><a href='/docs'> docs </a> | <a href='/redoc'> redoc </a><br>")

@app.get('/data')
def home(request: Request): 
	return request.query_params

@app.get('/wordmap')
def yulk_wordmap_name_value(kp:str="sound", match:str='snt', cp:str='dic', limit:int=1000, suffix:str='_VERB,_ADJ,_ADV,_NOUN', topk:int=30): 
	''' #[{'name': 'consider', 'value': 443}, '''
	ssi = defaultdict(Counter) 
	rows = fetchall(f'''select kps from {cp}_snt where match({match}) against ('"{kp}" in boolean mode') limit {limit}''')
	suffix = tuple(suffix.strip().split(','))
	for row in rows: #it_PRON could_AUX be_AUX consider_VERB a_DET waste_NOUN of_ADP prime_ADJ
		for term in row[0].split(' '):
			if term.endswith(suffix) and not term == kp: 
				arr = term.split('_') 
				if arr[0].isalpha() and not arr[0] == kp and len(arr) == 2 : ssi[arr[-1]].update({arr[0]:1})
	arr  = [ {"name":s, "value":i} for pos, si in ssi.items() for s,i in si.items() ] 
	arr.sort(key=lambda a:a['value'], reverse=True)
	return {"kp":kp, "topk": topk, "data": arr[0:topk]}
#print ( yulk_wordmap_name_value(), flush=True) 

lexlist		= lambda lemma='open', sepa="|": sepa.join(list(lemma_lex.lemma_lex.get(lemma, [lemma]))) #opens|openest|opened|opener|opening|open
highlight	= lambda snt='I open the door.', words='open|opened|door': re.sub(rf'\b({words})\b', r'<b>\g<0></b>', snt) if words else snt

@app.get('/trp-perc-snt')
def yulk_trpstar_snt(name:str="open:VERB:dobj", pos:str='NOUN', cp:str='dic', start:int=0, num:int=10): 
	''' 搭配分布，（词，百分比，例句）
	# {'wordtotal': 301, 'freqsum': 1452, 'rows': [{'word': 'door', 'perc': 17.4, 'snt': 'A coachman has to drive, '''
	total	= geti( f"select count(*) from {cp} where name = '{name}:{pos}'")
	isum	= geti( f"select count from {cp} where name = '{name}' and attr = '{pos}'")
	govlist = lexlist( name.split(':')[0] )
	#rows	= [{"word": word, "perc": round(100 * cnt/(isum + 0.01), 1), "snt": highlight(snt, f"{govlist}|" + lexlist(word))} for word, snt, cnt in fetchall(f"select substring_index(name, ':', -1), attr, count from {cp} where name like '{name}:{pos}:%' order by count desc limit {start},{num}")]
	rows	= [ (word, round(100 * cnt/(isum + 0.01), 1), highlight(snt, f"{govlist}|" + lexlist(word)) ) for word, snt, cnt in fetchall(f"select substring_index(name, ':', -1), attr, count from {cp} where name like '{name}:{pos}:%' order by count desc limit {start},{num}")]
	return {"wordtotal":total, "freqsum": isum,  "data": rows} 

@app.get('/yulk/style')
def yulk_style(lex:str="considered", match:str='snt', cps:str='sino,dic,guten,sprg,twit'): 
	''' '''
	return [{"cp":cp, "mf": round(1000000 * lexcnt(lex, cp)/sntnum(cp),1)} for cp in cps.strip().split(',')]

@app.get('/yulk/rank')
def yulk_rank(name:str='LEX', attr:str="considered", cp:str='dic'): 
	''' name: LEX/LEM/VERB/ADJ/ADV/NOUN/LEM '''
	freq = geti( f"select count from {cp} where name = '{name}' and attr = '{attr}'")
	rank = geti(f"select count(*) from {cp} where name = '{name}' and count > {freq}")
	sum  = geti( f"select count(*) from {cp} where name = '{name}'")
	return {"name":name, "attr":attr, "freq":freq, "rank": rank,  "sum":sum, "top_perc": round(100 * rank/sum, 1)	}

@app.get('/yulk/lempos-keyness')
def lempos_keyness(lems:str='age,book,table', cp0:str='sino', cp1:str='dic'): 
	'''  '''
	# select attr,count from sino where name = 'LEM' and attr in ('age','book');
	lemlist = lems.strip().replace(",","','")
	sum0 = dict(fetchall(f"select attr,count from {cp0} where name = 'LEM' and attr in ('{lemlist}')"))
	sum1 = dict(fetchall(f"select attr,count from {cp1} where name = 'LEM' and attr in ('{lemlist}')"))
	row0 = fetchall(f"select * from {cp0} where name in ('{lemlist}')") # name, attr, count 
	row1 = fetchall(f"select * from {cp1} where name in ('{lemlist}')")
	ssi  = defaultdict(Counter)
	for name, attr, count in row1:
		ssi[name][attr] = count 
	return [{"word":name, "pos":attr, "src": count, "tgt": ssi[name][attr], "src_perc": round(100 * count/sum0.get(name,0.1),1), "tgt_perc": round(100 * ssi[name][attr]/sum1.get(name,0.1),1),"keyness": likelihood(count,ssi[name][attr], sum0.get(name,0.1), sum1.get(name,0.1) ) } for name, attr, count in row0]
#print ( lempos_keyness()) 

@app.get('/yulk/wordlist')
def yulk_wordlist(pos:str='VERB', cp0:str='sino', cp1:str='dic', limit:str="0,20"): 
	''' VERB wordlist, 2022.11.27  '''
	rows = fetchall(f"select attr,count from {cp0} where name = '{pos}' order by count desc limit {limit}")
	lems = "','".join([s for s,i in rows])
	dic  = dict(fetchall(f"select attr,count from {cp1} where name = '{pos}' and attr in ('{lems}')"))
	return [{"word": word, cp0: mf(cnt,cp0), cp1: mf(dic.get(word,0), cp1),  "keyness": likelihood(cnt, dic.get(word,0), sntnum(cp0), sntnum(cp1)) } for word, cnt in rows]


import pyecharts.options as opts
from pyecharts.globals import SymbolType
from pyecharts.commons.utils import JsCode
from pyecharts.components import Table
from pyecharts.charts import *

@app.get('/yulk/wordcloud')
def yulk_wordcloud(name:str='knowledge:NOUN:~dobj:VERB', cp:str='dic', topk:int=50,): 
	''' '''
	data = fetchall(f"select attr, count from {cp} where name ='{name}' order by count desc limit {topk}")
	#res =	WordCloud().add(series_name=name, data_pair=data, word_size_range=[6, 66]).set_global_opts(title_opts=opts.TitleOpts(title=name, title_textstyle_opts=opts.TextStyleOpts(font_size=23)),tooltip_opts=opts.TooltipOpts(is_show=True),).render_embed()
	res =  WordCloud().add("", data, word_size_range=[20, 100], shape=SymbolType.DIAMOND).set_global_opts(title_opts=opts.TitleOpts(title="WordCloud-shape-diamond")).render_embed()
	return HTMLResponse(content=res )

@app.get('/wordcloud-viewdata')
def yulk_view_wordcloud(name:str='knowledge:NOUN:~dobj:VERB', cp:str='sino', refer:str='dic', color:str='#78fbb2', topk:int=50,): 
	''' '''
	data = fetchall(f"select attr, count from {cp} where name ='{name}' order by count desc limit {topk}")
	dic  = dict(fetchall(f"select attr, count from {refer} where name ='{name}'"))
	rows =   [ {"name":s, "value":i} for s,i in data if s in dic] +  [ {"name":s, "value":i,"textStyle":{"color": color},"emphasis":{"textStyle":{"color":"red"}}} for s,i in data if not s in dic]
	return {"data": rows}
#print ( yulk_view_wordcloud()) 

@app.get('/yulk/dual')
def yulk_dual(name:str='knowledge:NOUN:~dobj:VERB', attrs:str=None, cp0:str='sino', cp1:str='dic', topk:int=10, 
		html:bool=False, width:int=600, height:int=600,title="", subtitle=""): 
	''' attrs="vtov,dobj,vvbg,ccomp", the 'attr' of the given 'name' in dual corpus,  ie:  VERBs knowledge '''
	sql  = f"select attr, count from {cp0} where name ='{name}'"
	if attrs is not None: sql = sql + " and attr in ('" + attrs.replace(",", "','") + " ')"
	row0 = fetchall(sql) 
	dic1 = dict(fetchall(sql.replace(cp0, cp1)))
	sum0 = sum([i for s,i in row0]) + 0.01 if not ':' in name else uppersum(name, cp0)
	sum1 = sum([i for s,i in dic1.items()]) + 0.01 if not ':' in name else uppersum(name, cp1)
	arr	 = [{"word":attr, cp0: count, cp1: dic1.get(attr,0), 
		f"{cp0}_perc": round(100 * count/sum0,1), 
		f"{cp1}_perc": round(100 * dic1.get(attr,0)/sum1,1),
		"keyness": likelihood(count,dic1.get(attr,0), sum0, sum1 ) } for attr, count in row0]
	arr.sort(key=lambda a:a[cp0], reverse=True)
	if not html: return arr[0:topk] #[{'word': 'learn', 'count': 4595, 'refer': 1, 'src_perc': 17.2, 'tgt_perc': 0.3, 'keyness': 112.0}, {'word': 'have', 'count': 2514, 'refer': 84, 'src_perc': 9.4, 'tgt_perc': 23.5, 'keyness': -52.0}, {'word': 'acquire', 'count': 2367, 'refer': 17, 'src_perc': 8.8, 'tgt_perc': 4.7, 'keyness': 8.1}, {'word': 'get', 'count': 2191, 'refer': 2, 'src_perc': 8.2, 'tgt_perc': 0.6, 'keyness': 43.6}, {'word': 'gain', 'count': 1335, 'refer': 12, 'src_perc': 5.0, 'tgt_perc': 3.4, 'keyness': 2.2}, {'word': 'enrich', 'count': 884, 'refer': 0, 'src_perc': 3.3, 'tgt_perc': 0.0, 'keyness': 23.5}, {'word': 'teach', 'count': 813, 'refer': 2, 'src_perc': 3.0, 'tgt_perc': 0.6, 'keyness': 10.9}, {'word': 'use', 'count': 712, 'refer': 18, 'src_perc': 2.7, 'tgt_perc': 5.0, 'keyness': -5.8}, {'word': 'study', 'count': 614, 'refer': 0, 'src_perc': 2.3, 'tgt_perc': 0.0, 'keyness': 16.3}, {'word': 'increase', 'count': 596, 'refer': 4, 'src_perc': 2.2, 'tgt_perc': 1.1, 'keyness': 2.4}, {'word': 'obtain', 'count': 531, 'refer': 1, 'src_perc': 2.0, 'tgt_perc': 0.3, 'keyness': 8.2}, {'word': 'know', 'count': 530, 'refer': 0, 'src_perc': 2.0, 'tgt_perc': 0.0, 'keyness': 14.1}, {'word': 'master', 'count': 474, 'refer': 0, 'src_perc': 1.8, 'tgt_perc': 0.0, 'keyness': 12.6}, {'word': 'need', 'count': 320, 'refer': 3, 'src_perc': 1.2, 'tgt_perc': 0.8, 'keyness': 0.4}, {'word': 'improve', 'count': 315, 'refer': 10, 'src_perc': 1.2, 'tgt_perc': 2.8, 'keyness': -5.6}, {'word': 'apply', 'count': 312, 'refer': 6, 'src_perc': 1.2, 'tgt_perc': 1.7, 'keyness': -0.7}, {'word': 'incorporate', 'count': 309, 'refer': 1, 'src_perc': 1.2, 'tgt_perc': 0.3, 'keyness': 3.4}, {'word': 'absorb', 'count': 308, 'refer': 0, 'src_perc': 1.2, 'tgt_perc': 0.0, 'keyness': 8.2}, {'word': 'give', 'count': 298, 'refer': 7, 'src_perc': 1.1, 'tgt_perc': 2.0, 'keyness': -1.8}, {'word': 'expand', 'count': 250, 'refer': 3, 'src_perc': 0.9, 'tgt_perc': 0.8, 'keyness': 0.0}, {'word': 'enlarge', 'count': 249, 'refer': 0, 'src_perc': 0.9, 'tgt_perc': 0.0, 'keyness': 6.6}, {'word': 'understand', 'count': 231, 'refer': 0, 'src_perc': 0.9, 'tgt_perc': 0.0, 'keyness': 6.1}, {'word': 'achieve', 'count': 197, 'refer': 0, 'src_perc': 0.7, 'tgt_perc': 0.0, 'keyness': 5.2}, {'word': 'take', 'count': 193, 'refer': 2, 'src_perc': 0.7, 'tgt_perc': 0.6, 'keyness': 0.1}, {'word': 'grasp', 'count': 185, 'refer': 0, 'src_perc': 0.7, 'tgt_perc': 0.0, 'keyness': 4.9}, {'word': 'put', 'count': 181, 'refer': 2, 'src_perc': 0.7, 'tgt_perc': 0.6, 'keyness': 0.1}, {'word': 'broaden', 'count': 179, 'refer': 9, 'src_perc': 0.7, 'tgt_perc': 2.5, 'keyness': -10.4}, {'word': 'bring', 'count': 178, 'refer': 2, 'src_perc': 0.7, 'tgt_perc': 0.6, 'keyness': 0.1}, {'word': 'accumulate', 'count': 164, 'refer': 2, 'src_perc': 0.6, 'tgt_perc': 0.6, 'keyness': 0.0}, {'word': 'impart', 'count': 160, 'refer': 3, 'src_perc': 0.6, 'tgt_perc': 0.8, 'keyness': -0.3}, {'word': 'receive', 'count': 138, 'refer': 0, 'src_perc': 0.5, 'tgt_perc': 0.0, 'keyness': 3.7}, {'word': 'spread', 'count': 128, 'refer': 0, 'src_perc': 0.5, 'tgt_perc': 0.0, 'keyness': 3.4}, {'word': 'widen', 'count': 123, 'refer': 0, 'src_perc': 0.5, 'tgt_perc': 0.0, 'keyness': 3.3}, {'word': 'require', 'count': 100, 'refer': 21, 'src_perc': 0.4, 'tgt_perc': 5.9, 'keyness': -72.7}, {'word': 'soar', 'count': 98, 'refer': 0, 'src_perc': 0.4, 'tgt_perc': 0.0, 'keyness': 2.6}, {'word': 'share', 'count': 89, 'refer': 11, 'src_perc': 0.3, 'tgt_perc': 3.1, 'keyness': -28.3}, {'word': 'provide', 'count': 86, 'refer': 6, 'src_perc': 0.3, 'tgt_perc': 1.7, 'keyness': -9.8}, {'word': 'enhance', 'count': 81, 'refer': 3, 'src_perc': 0.3, 'tgt_perc': 0.8, 'keyness': -2.2}, {'word': 'accept', 'count': 80, 'refer': 0, 'src_perc': 0.3, 'tgt_perc': 0.0, 'keyness': 2.1}, {'word': 'show', 'count': 79, 'refer': 2, 'src_perc': 0.3, 'tgt_perc': 0.6, 'keyness': -0.7}, {'word': 'translate', 'count': 76, 'refer': 0, 'src_perc': 0.3, 'tgt_perc': 0.0, 'keyness': 2.0}, {'word': 'strengthen', 'count': 75, 'refer': 0, 'src_perc': 0.3, 'tgt_perc': 0.0, 'keyness': 2.0}, {'word': 'update', 'count': 71, 're

	bar = Bar(init_opts=opts.InitOpts(width=f"{width}px", height=f"{height}px")) #theme=ThemeType.LIGHT
	bar.add_xaxis([row['word'] for row in arr[0:topk]])
	bar.add_yaxis(cp0, [row[f"{cp0}_perc"] for row in arr[0:topk]] )
	bar.add_yaxis(cp1, [row[f"{cp1}_perc"] for row in arr[0:topk]] )
	bar.set_global_opts(title_opts=opts.TitleOpts(title=title, subtitle=subtitle))
	return HTMLResponse(content=bar.render_embed() ) #bar.render()

@app.get('/yulk/lex-to-snt')
def yulk_lex_to_snt(lex:str='considered', cp:str='dic', limit:str='0,10', html:bool=False):
	''' '''
	rows = fetchall(f"select snt from {cp}_snt where match(snt) against ('{lex}') limit {limit}")
	if not html: return rows
	content =  "<ol>" +	''.join([ "<li>" + re.sub(rf"\b({lex})\b", f"<b>{lex}</b>", row[0]) + "</li>" for row in rows]) 	+ "</ol>"
	return HTMLResponse(content=content )

@app.get('/phrase-so', tags=["yulk.net"])
def phrase_so(chunk:str='as soon as possible', cp:str='dic', limit:str='0,20'):
	'''{'total': 1184, 'mf': 1729.9, 'data': ["Butler, Newman and Blougram might be <b>considered</b> agnostics according to Ayer's definition, or they might be <b>considered</b> theists.", ]} '''
	rows = fetchall(f'''select snt from {cp}_snt where match(snt) against ( '"{chunk}"' in boolean mode) limit {limit}''')
	total = geti(f'''select count(*) from {cp}_snt where match(snt) against ( '"{chunk}"' in boolean mode) ''')
	return {"total": total, "mf": round(1000000 * total/sntnum(cp), 1), "data": [ re.sub(rf"\b({chunk})\b", f"<b>{chunk}</b>", row[0]) for row in rows]}

@app.get('/phrase-context', tags=["yulk.net"])
def phrase_context(chunk:str='very happy', cp:str='dic', limit:str='0,1000', topk:int=20):
	''''''
	rows = fetchall(f'''select snt from {cp}_snt where match(snt) against ( '"{chunk}"' in boolean mode) limit {limit}''')
	next = Counter()
	prev = Counter() 
	for row in rows:
		snt = "<s> " + row[0] + " </s>"
		arr = snt.split(chunk) 
		next.update({arr[1].strip().split(' ')[0]:1})
		prev.update({arr[0].strip().split(' ')[-1]:1})
	return { "next": next.most_common(topk), "prev": prev.most_common(topk)} 
#print ( phrase_context() ) 

@app.get('/lex-to-snt', tags=["yulk.net"])
def lex_to_snt(lex:str='considered', cp:str='dic', limit:str='0,20'):
	'''{'total': 1184, 'mf': 1729.9, 'data': ["Butler, Newman and Blougram might be <b>considered</b> agnostics according to Ayer's definition, or they might be <b>considered</b> theists.", ]} '''
	rows = fetchall(f"select snt from {cp}_snt where match(snt) against ('{lex}') limit {limit}")
	total = geti(f"select count(*) from {cp}_snt where match(snt) against ('{lex}')")
	return {"total": total, "mf": round(1000000 * total/sntnum(cp), 1), 
		"data": [ re.sub(rf"\b({lex})\b", f"<b>{lex}</b>", row[0]) for row in rows]}

@app.get("/fts-snt", response_class=HTMLResponse)
async def fts_snt(request: Request):
	''' 2022.12.9 '''
	word	= request.query_params.get('word','sound')
	cp		= request.query_params.get('cp','dic')
	limit	= request.query_params.get('limit','0,20')
	res		= lex_to_snt(word, cp, limit) 
	return templates.TemplateResponse("fts-snt.html", {"request": request, "word": word, "mf": res['mf'], "data": res['data']})

@app.get('/lexpair-to-snt', tags=["yulk.net"])
def lexpair_to_snt(lex:str='sound', pair:str='hear', cp:str='dic', limit:str='0,20'):
	''' search snt with a lex and a pair, clicked from the wordmap '''
	rows = fetchall(f"select snt from {cp}_snt where match(snt) against ('{lex}') and match(kps) against ('{pair}_NOUN {pair}_VERB {pair}_ADJ {pair}_ADV') limit {limit}")
	return [ re.sub(rf"\b({lex}|{pair})\b", r'<b>\g<0></b>', row[0]) for row in rows]

@app.post('/lempos-to-trp', tags=["yulk.net"])
def lempos_to_trp(dic:dict={"VERB": ["dobj:NOUN","nsubj:NOUN","conj:VERB","~conj:VERB","advmod:ADV","oprd:ADJ","~xcomp:VERB","prep:ADP"], 
		"NOUN": ["~dobj:VERB","~nsubj:VERB","amod:ADJ"]}, 
		lem:str='consider', pos:str='VERB', cp:str='dic', topk:int=10):
	''' '''
	rows = { trp: fetchall(f"select attr, count from {cp} where name = '{lem}:{pos}:{trp}' order by count desc limit {topk}", True) for trp in dic[pos]}
	return {"lem":lem, "pos":pos, "cp":cp, "topk":topk, "data": rows } 
#print (lempos_to_trp()) 

@app.get('/yulk/trp-to-snt')
def yulk_trp_to_snt(trp:str='open_VERB_dobj_NOUN_door', cp:str='dic', limit:str='0,10', html:bool=False):
	''' '''
	from dic import lemma_lex
	trp = trp.replace(":", "_")
	rows = fetchall(f"select snt from {cp}_snt where match(kps) against ('{trp}') limit {limit}")
	if not html: return rows
	arr = trp.split('_')
	lex = "|".join( list(lemma_lex.lemma_lex.get(arr[0], [arr[0]])) + list(lemma_lex.lemma_lex.get(arr[-1], [arr[-1]])) )
	content =  "<ol style='text-align:left;'>" +	''.join([ "<li>" + re.sub(rf"\b({lex})\b", f"<b>\g<1></b>", row[0]) + "</li>" for row in rows]) 	+ "</ol>"
	return HTMLResponse(content=content )

@app.get('/yulk/synonym')
def yulk_synonym(name:str='%:VERB', attrs:str="vtov,dobj,vvbg,ccomp", w0:str='increase', w1:str='raise', cp:str='dic'): 
	''' attrs="vtov,dobj,vvbg,ccomp", refer='*', means avg verb '''
	sql  = f"select attr, count from {cp} where name ='{name.replace('%',w0)}'"
	if attrs is not None: sql = sql + " and attr in ('" + attrs.replace(",", "','") + " ')"
	row0 = fetchall(sql) 
	dic1 = fetchall(sql.replace(w0, w1), True)
	sum0 = sum([i for s,i in row0]) + 0.01 if not ':' in name else uppersum(name.replace('%',w0), cp)
	sum1 = sum([i for s,i in dic1.items()]) + 0.01 if not ':' in name else uppersum(name.replace('%',w1), cp)
	arr	 = [{"attr":attr, w0: count, w1: dic1.get(attr,0), 
		f"{w0}_perc": round(100 * count/sum0,1), 
		f"{w1}_perc": round(100 * dic1.get(attr,0)/sum1,1),
		"keyness": likelihood(count,dic1.get(attr,0), sum0, sum1 ) } for attr, count in row0]
	arr.sort(key=lambda a:a[w0], reverse=True)
	return arr

@app.get('/heatmap/verbattr')
def heatmap_verbattr(limit:str='100,30', cp:str='dic'): 
	''' '''
	attrs = { row[0]:i for i, row in enumerate(fetchall(f"select attr from dic where name = '*:VERB' and count > 50000"))}
	verbs = { row[0]:i for i, row in enumerate(fetchall(f"select attr from dic where name = 'VERB' order by count desc limit 100,30"))}
	vlist = "','".join([ f"{v}:VERB" for v, i in verbs.items()])
	rows  = [(verbs[verb], attrs[attr], i) for verb, attr, i in fetchall(f"select substring_index(name,':',1), attr, count  from dic where name in ( '{vlist}')") if verb in verbs and attr in attrs]
	#{"xAxis":["12a","7p","8p","9p","10p","11p"],"yAxis":[,"Sunday"],"seriesData":[[0,0,5],
	return {"xAxis": [a for a in attrs.keys()], "yAxis":[v for v in verbs.keys()], "seriesData": rows}

@app.get('/echo')
def echo_data(data:str="http://minio.penly.cn/yulk/sosnt.html"): 
	return {"data":data}

if __name__ == '__main__':	 
	uvicorn.run(app, host='0.0.0.0', port=80)

'''
print( yulk_dual("sound:LEX") )
docker run -d --restart=always --name nac.jukuu.com -p 8000:8000 -e pip=pyecharts -v /data/cikuu/pypi/uvirun/yulk-nac.py:/main.py wrask/uvirun uvicorn main:app --host 0.0.0.0 --reload 

root@172.17.0.1|nac>select * from sino where name in ('age','book');
+------+------+-------+
| name | attr | count |
+------+------+-------+
| age  | ADJ  |    14 |
| age  | NOUN | 11324 |
| age  | VERB |   983 |
| book | ADJ  |    85 |
| book | NOUN | 45516 |
| book | VERB |   328 |
+------+------+-------+
6 rows in set (0.00 sec)

lemma:  1. pos yulk_dual("sound"),  2. lex yulk_dual("sound:LEX") 3. style   4. wordmap  5. rank  (high, mid, low ) 
lempos: 
sent:
essay: 
triple:
chunk: 

root@172.17.0.1|nac>select * from dic where name = 'LEX' and attr = 'considered';
+------+------------+-------+
| name | attr       | count |
+------+------------+-------+
| LEX  | considered |  1190 |
+------+------------+-------+
1 row in set (0.00 sec)

root@172.17.0.1|nac>select count(*) from dic where name = 'LEX' and count > 1190;
+----------+
| count(*) |
+----------+
|      760 |
+----------+
1 row in set (0.08 sec)

[mysqld]
interactive_timeout=360000
wait_timeout=360000

@app.post('/test-sql')
async def goview_execute_post(req:dict={"sql":"select * from dic where name = 'sound'"}, data: Optional[str] = Header(None), cp: Optional[str] = Header(None) ):
	sql		= req.get('sql','')
	if data :  
		sql	= sql.replace(f"$data", data )
	if cp:  
		sql	= sql.replace(f"$cp", cp )
	rows	= fetchall(sql,'asrow' not in req) 
	if 'dim' in req or len(rows[0]) > 2 :  rows = {"dimensions":[k for k in rows[0].keys()],"source": rows }
	return {"sql": sql, "request": req, "data": rows}

@app.get('/yulk/subobj')
def yulk_subobj(verb:str='consider', cp:str='dic', topk:int=50,): 
	page = Page(layout=Page.SimplePageLayout)
	page.add(
        WordCloud().add("", fetchall(f"select attr, count from {cp} where name ='{verb}:VERB:nsubj:NOUN' order by count desc limit {topk}"), word_size_range=[20, 100], shape=SymbolType.DIAMOND).set_global_opts(title_opts=opts.TitleOpts(title=f"NOUNs + {verb}")), 
		WordCloud().add("", fetchall(f"select attr, count from {cp} where name ='{verb}:VERB:dobj:NOUN' order by count desc limit {topk}"), word_size_range=[20, 100], shape=SymbolType.DIAMOND).set_global_opts(title_opts=opts.TitleOpts(title=f"{verb} + NOUNs")),
    )
	return HTMLResponse(content=page.render_embed() )
'''