# 2022.10.3
import json, traceback,sys, time,  fileinput, os, en
from collections import Counter
from pathlib import Path

def run(infile):
	''' c4-train.00604-of-01024.docjsonlg.3.4.1.gz -> c4-train.00604-of-01024.postag.gz | 2022.8.22 '''
	outfile = infile.split('.docjson')[0] + f".trp"
	if Path(f"{outfile}.gz").exists(): return f"{outfile} exists"
	start = time.time()
	si = Counter()
	print ("started:", infile ,  ' -> ',  outfile, flush=True)
	with open(outfile, 'w') as fw: 
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): 
			try:
				arr = json.loads(line.strip()) 
				doc = spacy.from_json(arr) 
				for t in doc:
					if not t.lemma_.replace('-','').isalpha() or not t.head.lemma_.replace('-','').isalpha(): continue # added 2022.1.6 
					if t.pos_ not in ('SP','PUNCT','PROPN') and t.tag_ not in ('NUM','CD') and not ':' in t.text :
						trp = f"{t.dep_}:{t.head.pos_}:{t.pos_}:{t.head.tag_}:{t.tag_}:{t.head.lemma_}:{t.lemma_}"  
						fw.write(f"{trp}\n")
			except Exception as e:
				print ("ex:", e, sid, line) 
	os.system(f"gzip -f -9 {outfile}")
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

if __name__	== '__main__':
	import fire 
	fire.Fire(run)