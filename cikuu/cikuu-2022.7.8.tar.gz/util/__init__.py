# 2022.3.10
import requests,re,time
from collections import	Counter, defaultdict
now	= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))

import hashlib
sntmd5	= lambda sntarr: " ".join([hashlib.md5(snt.strip().lower().encode("utf-8")).hexdigest() for snt in sntarr if len(snt) > 1])
md5text	= lambda text: hashlib.md5(text.strip().encode("utf-8")).hexdigest()

from math import log as ln
def likelihood(a,b,c,d, minus=None):  #from: http://ucrel.lancs.ac.uk/llwizard.html
	try:
		if a is None or a <= 0 : a = 0.000001
		if b is None or b <= 0 : b = 0.000001
		if c is None or c <= 0 : c = 0.000001
		if d is None or d <= 0 : d = 0.000001
		E1 = c * (a + b) / (c + d)
		E2 = d * (a + b) / (c + d)
		G2 = round(2 * ((a * ln(a / E1)) + (b * ln(b / E2))), 2)
		if minus or  (minus is None and a * d < b * c): G2 = 0 - G2 #if minus or  (minus is None and a/c < b/d): G2 = 0 - G2
		return round(G2,1)
	except Exception as e:
		print ("likelihood ex:",e, a,b,c,d)
		return 0

def logdice(xy, x, y): # https://www.fi.muni.cz/usr/sojka/download/raslan2008/13.pdf
	return round(14  + ln ( 2 * xy/ (x+y), 2),1)
#print (logdice( 1, 23, 56) )

def lexlist( lemma='open', sepa="|"):
	from dic import lemma_lex
	return sepa.join(list(lemma_lex.lemma_lex.get(lemma, [lemma]))) #opens|openest|opened|opener|opening|open
highlight	= lambda snt='I open the door.', words='open|opened|door': re.sub(rf'\b({words})\b', r'<b>\g<0></b>', snt) if words else snt

def  si_to_es(si, index, batch=10000, eshost='127.0.0.1',esport=9200): 
	''' ie: spellerr, added 2022.9.6 '''
	print (len(si), index,  flush=True) 
	actions=[]
	for s,i in si.items() if isinstance(si, dict) else si: 
		try:
			requests.post(f"http://{eshost}:{esport}/{index}/{s}", json={"s": s, "i":i})
		except Exception as e:
			print("ex:", e)	
	print(">>load finished:" , index )

def xblpop(r, name, arr, timeout=10, suc_prefix='suc:', err_prefix="err:"):
	''' name:xsnt/xsnts, arr: {"snt": "hello"}  added 2022.4.4 '''
	id  = r.xadd(name, arr)
	return r.blpop([f"{suc_prefix}{id}",f"{err_prefix}{id}"], timeout=timeout)

def getlog(logfile='daily.log'):
	import logging
	from logging.handlers import TimedRotatingFileHandler
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	handler = TimedRotatingFileHandler(logfile, when="midnight", interval=1)
	handler.suffix = "%Y%m%d"
	logger.addHandler(handler)
	handler.setLevel(logging.INFO) 
	handler.setFormatter(logging.Formatter("%(message)s"))
	logger.addHandler(handler)
	return logger

def readline(infile, sepa=None): #for line in fileinput.input(infile):
	with open(infile, 'r', encoding='utf-8') as fp:
		while True:
			line = fp.readline()
			if not line: break
			yield line.strip().split(sepa) if sepa else line.strip()

def process(infile, outfile, asjson=True, func = lambda x: x):
	''' line processor, added 2022.3.20  '''
	print ("process started:", infile, outfile, flush=True)
	with open(outfile, 'w') as fw: 
		for line in readline(infile):
			try:
				fw.write( func( json.loads(line.strip(), strict=False) if asjson else line.strip())  + "\n")
			except Exception as ex:
				print ("process ex:", ex, line) 
	print ('process finished:', infile) 

def hset_if_greater(r, key, eid, ver ): 
	res = r.hget(key, eid)
	try: 
		if not res :
			r.hset(key, eid, ver)
		else: 
			if int(ver) > int(res) : r.hset(key, eid, ver)
	except Exception as e:
		print("ex:", e, eid)

# nltk
def traverse(t, label='NP', f = lambda t:  print(t.pos()) ):
  try:
      t.label()
  except AttributeError:
      return
  else:
      if t.label() == label: f(t)  # or do something else
      else:
          for child in t: 
              traverse(child, label, f)

if __name__ == '__main__': 
	pass 
	#logger = getlog()
	#print (logger) 

'''
def  si_to_es(si, index, batch=10000, eshost='127.0.0.1',esport=9200): 
	from elasticsearch import Elasticsearch,helpers
	es = Elasticsearch([ f"http://{eshost}:{esport}" ])  
	print (index, es, flush=True) 
	actions=[]
	for s,i in si.items() if isinstance(si, dict) else si: 
		try:
			actions.append( {'_op_type':'index', '_index':index, "_id": s, "_source":{"s": s, "i":i} })
			if len(actions) >= batch: 
				helpers.bulk(client=es,actions=actions, raise_on_error=False)
				print ( actions[-1], flush=True)
				actions = []
		except Exception as e:
			print("ex:", e)	
	if actions : helpers.bulk(client=es,actions=actions, raise_on_error=False)
	print(">>load finished:" , index )
'''