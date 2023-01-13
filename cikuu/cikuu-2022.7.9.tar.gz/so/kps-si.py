# 2022.9.12 cp from esjson.py 
import json, traceback,sys, time,  fileinput, os, en
from collections import Counter

def run(infile, outfile=None, cutoff:int=0, zip:bool=True):
	''' gzjc.snt-esjson.gz -> gzjc.kps-si | 1. cat *.kps-si >> all.si  2. ** all.si , need a large memory | 2022.9.12 '''
	if outfile is None: outfile = infile.split('.')[0] + f".kps-si"
	start = time.time()
	si = Counter()
	print (f"started: {infile} -> {outfile}, zip={zip}", flush=True)
	with open(outfile, 'w') as fw: 
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): 
			try:
				ar = json.loads(line.strip())
				for kp in ar['_source']['kps']:
					si.update({kp:1})
					akp = kp.split(':')
					if len(akp) > 1: si.update({akp[0]:1})
					if len(akp) > 2: si.update({f"{akp[0]}:{akp[1]}":1})
			except Exception as e:
				print ("ex:", e, sid, line) 
		fw.write(json.dumps({'_id': "sntsum", '_source': {'s':"sntsum", 'i':sid+1 } }) + "\n")  # added 2022.9.4
		for s,i in si.items(): 
			if i > cutoff : 
				fw.write(json.dumps({'_id': s, '_source': {'s':s, 'i':i	} }) + "\n") 
	if zip: os.system(f"gzip -f -9 {outfile}")
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

if __name__	== '__main__': #python kps-si.py gzjc.snt-esjson --zip False
	import fire 
	fire.Fire(run)
