# 2022.10.22
import json, traceback,sys, time,  fileinput, os,en
from collections import Counter
from pathlib import Path

doctoks = lambda doc: ['<s>'] + [ f"_{t.pos_}" if t.pos_ in ('PROPN','NUM','CD','X','SPACE') else "_NP" if t.ent_type_ == 'NP' else t.text.lower()  for t in doc ]

def count(toks, ts, n): # ts: set 
	tlen =  len(toks)
	for i in range( tlen ): 
		for j in range(n): 
			if i+j < tlen: 
				ts.add( " ".join(toks[i:i+j]) )

def run(infile, n:int=7, batch:int=3000, remove:bool=True):
	''' c4-train.00604-of-01024.docjsonlg.3.4.1.gz -> c4-train.00604-of-01024.6.gz | 2022.10.22 '''
	outfile = infile.split('.docjson')[0] + f".{n}"
	if Path(f"{outfile}.gz").exists(): return f"{outfile} exists"
	start = time.time()
	ts = set() 
	print ("started:", infile ,  ' -> ',  outfile, flush=True)
	with open(outfile, 'w') as fw: 
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): #356317 docs of each doc file
			try:
				if (sid+1) % batch == 0 : 
					print (f"sid = {sid}, reset spacy, to release memory ", flush=True)
					spacy.nlp	= spacy.load('en_core_web_lg')

				arr = json.loads(line.strip()) 
				tdoc = spacy.from_json(arr) 
				for sp in tdoc.sents:
					ts.clear() 	
					doc = sp.as_doc()
					count( doctoks(doc), ts, n) 
					en.merge_np(doc) 
					count( doctoks(doc), ts, n) 
					for s in ts:  
						if s: fw.write( f"{s.strip()}\n") 
			except Exception as e:
				print ("ex:", e, sid, line) 
	os.system(f"gzip {outfile}") #-f -9
	if remove: 
		os.remove(infile) # delete , added 2022.10.22
		os.system("rm *.7") # added 2022.11.20 
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

if __name__	== '__main__':
	import fire 
	fire.Fire(run)