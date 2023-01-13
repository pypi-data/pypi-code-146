# 2022.11.18  | 2022.9.6
import json, traceback,sys, time,  fileinput, os, en
from collections import Counter

def run(infile):
	''' c4-train.00604-of-01024.docjsonlg.3.4.1.gz -> c4-train.00604-of-01024.postag.gz | 2022.8.22 '''
	outfile = infile.split('.docjson')[0] + f".np"
	if os.path.exists(f"{outfile}.gz"): return print (f"{outfile}.gz already exists")

	start = time.time()
	si = Counter()
	print ("started:", infile ,  ' -> ',  outfile, flush=True)
	with open(outfile, 'w') as fw: 
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): 
			try:
				arr = json.loads(line.strip()) 
				doc = spacy.from_json(arr) 
				for np in doc.noun_chunks:
					if np.end - np.start <= 100 : 	#fw.write(" ".join([ f"{t.text}_{t.tag_}_{t.pos_}" for t in np]) +"\n")
						lemma = doc[np.end-1].lemma_ 
						pos = doc[np.end-1].pos_ 
						poslist = " ".join([ t.pos_ for t in np])
						taglist = " ".join([ t.tag_ for t in np])
						fw.write(f"{lemma}:{pos}:np:{np.text.lower()}:{poslist}:{taglist}\n")
						#si.update({" ".join([ f"{t.text.lower()}_{t.tag_}_{t.pos_}" for t in np]) : 1 }) 
			except Exception as e:
				print ("ex:", e, sid, line) 
		#for s, i in si.items(): 
		#	fw.write(f"{s}\t{i}\n")
	os.system(f"gzip -f -9 {outfile}")
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

if __name__	== '__main__':
	import fire 
	fire.Fire(run)