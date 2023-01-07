# 2022.9.10, doc version of snt/esjson.py 
import json, traceback,sys, time,  fileinput, os, en
from collections import Counter

def run(infile, outfile=None,  with_tok:bool=False,  withsi:bool=True):
	''' spider-ag.docjsonlg.3.4.1.gz -> spider-ag.esjson | 2022.9.10 '''
	if outfile is None: outfile = infile.split('.docjson')[0] + f".esjson"
	if os.path.exists(f"{outfile}.gz"):  return  print("already exists")
	start = time.time()
	si = Counter()
	print (f"started: {infile} -> {outfile}, withsi = {withsi}", flush=True)
	with open(outfile, 'w') as fw: 
		for line in fileinput.input(infile,openhook=fileinput.hook_compressed): 
			try:
				arr = json.loads(line.strip())
				info = arr.get('info',{})
				did = info.get("id",0)
				info.update({"type":"doc"}) 
				fw.write(json.dumps({"_id": did,"_source":info}) + "\n") 

				text = arr.get("text","")
				for sid, ar in enumerate(arr["sents"]): #"sents": [{"start": 0, "end": 150}, {"start": 150, "end": 276}, 
					doc = spacy.nlp(text[ ar["start"]: ar["end"] ])
					_kps = en.kps(doc)
					asnt ={'_id': f"{did}-{sid}", '_source': {'type':'snt', 'snt':doc.text.strip(), 'postag':en.es_postag(doc),  'src': f"{did}-{sid}", 'tc': len(doc), 'kps': _kps }}
					fw.write(json.dumps(asnt) + "\n") 
					if withsi: #[ si.update({kp:1}) for kp in ar['_source']['kps'] ]
						for kp in _kps:
							si.update({kp:1})
							akp = kp.split(':')
							if len(akp) > 1: si.update({akp[0]:1})
							if len(akp) > 2: si.update({f"{akp[0]}:{akp[1]}":1})
			except Exception as e:
				print ("ex:", e, did, line) 
		if withsi and len(si) > 0: 
			for s,i in si.items(): 
				fw.write(json.dumps({'_id': s, '_source': {'s':s, 'i':i	} }) + "\n") 
	os.system(f"gzip -f -9 {outfile}")
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

if __name__	== '__main__':
	import fire 
	fire.Fire(run)
'''
"sents": [{"start": 0, "end": 150}, {"start": 150, "end": 276}, 
"info": {"id": 3000001, "did": 
302539, "domain": "www.newsday.com", "description": "A new hunting season Will Attorney General William Barr be the instrument of Donald Trump's revenge against
 the \"witch hunt?\" The president would be terribly disappointed if Barr said he wouldn't be.", "title": "AG Barr goes snoop dogging, probes Trump probers", "u
rl": "https://www.newsday.com/long-island/politics/trump-barr-mueller-russia-fbi-1.29655697", "doc_txt": "A new hunting season\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t "chanel": "Politics", "tag": "world,newsday,campaigns,political issues,government,education,campaign con
tributions,local,politics,military affairs,elections,health care policy,nation and world,source,nation,us government,donald trump,applenews", "pub_date": "Thu, 
11 Apr 2019 08:37:00 -0400"}}
'''