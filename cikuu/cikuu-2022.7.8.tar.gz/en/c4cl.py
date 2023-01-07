# 2022.10.25 updated to:   book:VERB:S.advcl:{cl}
# 2022.10.18
import json, traceback,sys, time,  fileinput, os, en
from collections import Counter

def dump_clause(doc, fw):  # {'S.prep-0': {'type': 'S.prep', 'start': 0, 'end': 2, 'lem': 'consider', 'chunk': 'Considering the possibility'}, 'S.conj-9': {'type': 'S.conj', 'start': 9, 'end': 12, 'lem': 'be', 'chunk': 'she is ok .'}}
	for v in [t for t in doc if t.pos_ == 'VERB' and t.dep_ != 'ROOT' ] : # non-root
		children = list(v.subtree) #end = children[-1].i 	tag = "S." + v.dep_   # S.advcl ,  S.conj 
		start = children[0].i
		end = children[-1].i + 1 #"type":"cl", "kp": "S." + v.dep_, 		#arr.append( (v, v.dep_, start, end, " ".join([c.text for c in v.subtree])) ) #last one is 'chunk'   lempos":v.lemma_ + "_" + v.pos_,"chunk": } #"lem":v.lemma_, NOT confuse with 'tok' 
		chunk = " ".join([c.text for c in v.subtree]).strip()
		if not ' ' in chunk or ':' in chunk  or '\t' in chunk or '\n' in chunk:  continue 
		if not v.lemma_.isalpha() or len(chunk) >= 64 : continue 
		fw.write(f"{v.lemma_}:{v.pos_}:S.{v.dep_}:{chunk}\n")

def run(infile):
	''' c4-train.00604-of-01024.docjsonlg.3.4.1.gz -> c4-train.00604-of-01024.cl.gz | 2022.10.18 '''
	outfile = infile.split('.docjson')[0] + f".cl"
	start = time.time()
	si = Counter()
	print ("started:", infile ,  ' -> ',  outfile, flush=True)
	with open(outfile, 'w') as fw: 
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): 
			try:
				arr = json.loads(line.strip()) 
				tdoc = spacy.from_json(arr) 
				for sp in tdoc.sents:
					dump_clause(sp.as_doc(), fw) 
			except Exception as e:
				print ("ex:", e, sid, line) 
	os.system(f"gzip {outfile}") #-f -9
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

if __name__	== '__main__':
	import fire 
	fire.Fire(run)

'''
				for v, vdep, start, end, chunk in clause(doc): 
					if not ':' in chunk and ' ' in chunk and len(chunk) < 64 :  # change PROPN, _NUM of chunk 
						fw.write(f"{v}:{vdep}:{chunk.strip()}\n")
'''