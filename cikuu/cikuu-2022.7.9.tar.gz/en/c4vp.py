# 2022.10.16
import json, traceback,sys, time,  fileinput, os, en
from collections import Counter
from pathlib import Path

def run(infile):
	''' c4-train.00604-of-01024.docjsonlg.3.4.1.gz -> c4-train.00604-of-01024.vp.gz | 2022.10.16 '''
	outfile = infile.split('.docjson')[0] + f".vp"
	if Path(f"{outfile}.gz").exists(): return f"{outfile} exists"
	start = time.time()
	si = Counter()
	print ("started:", infile ,  ' -> ',  outfile, flush=True)
	with open(outfile, 'w') as fw: 
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): 
			try:
				arr = json.loads(line.strip()) 
				doc = spacy.from_json(arr) 
				for lem, pos, type, chunk in kp_matcher(doc): #base:VERB:be_vbn_p:be based on   | lem, pos, type, chunk 
					fw.write(f"{lem}:{pos}:{type}:{chunk}\n")
			except Exception as e:
				print ("ex:", e, sid, line) 
	os.system(f"gzip {outfile}") #-f -9
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

if __name__	== '__main__':
	import fire 
	fire.Fire(run)