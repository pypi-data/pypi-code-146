# 2022.12.21
import json, traceback,sys, time,  fileinput, os, en
import benepar # run at 136
parser = benepar.Parser("benepar_en3")

def run(infile):
	''' c4-train.00604-of-01024.docjsonlg.3.4.1.gz -> c4-train.00604-of-01024.postag.gz | 2022.8.22 '''
	outfile = infile.split('.docjson')[0] + f".tree"
	if os.path.exists(f"{outfile}.gz"): return print (f"{outfile}.gz already exists")

	start = time.time()
	print ("started:", infile ,  ' -> ',  outfile, flush=True)
	with open(outfile, 'w') as fw: 
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): 
			try:
				arr = json.loads(line.strip()) 
				tdoc = spacy.from_json(arr) 
				for i,sp in enumerate(tdoc.sents):
					snt = sp.text.strip()
					if not snt: continue 
					t = parser.parse(snt)
					line = " ".join([s.strip() for s in str(t).split("\n")])
					fw.write(line + "\n")
			except Exception as e:
				print ("ex:", e, sid, line) 
	os.system(f"gzip -f -9 {outfile}")
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

if __name__	== '__main__':
	import fire 
	fire.Fire(run)