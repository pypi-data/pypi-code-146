# 2022.9.12 ,cp from esjson.py , for snt doc lg.3.4.1
import json, traceback,sys, time,  fileinput, os, en

def run(infile, outfile=None,  with_tok:bool=False):
	''' gzjc.jsonlg.3.4.1.gz -> gzjc.snt-esjson | 2022.9.12 '''
	if outfile is None: outfile = infile.split('.json')[0] + f".snt-esjson"
	name = infile.split('/')[-1].split('.')[0] #  ./spok.jsonlg.3.4.1.gz, gzjc, dic 
	if os.path.exists(f"{outfile}.gz"): return print("already exists")
	start = time.time()
	print (f"started: {infile} -> {outfile}, name={name}", flush=True)
	with open(outfile, 'w') as fw: 
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): 
			try:
				doc = Doc(spacy.nlp.vocab).from_json( json.loads(line.strip()) )	
				ar = {'_id': f"{name}-{sid}", '_source': {'type':'snt', "id": f"{name}-{sid}", "src":name,  'snt':doc.text, 'postag': en.es_postag(doc),  'tc': len(doc), 'kps': en.kps(doc) } }
				fw.write(json.dumps(ar) + "\n") 
				if with_tok: 
					for t in doc:
						fw.write(json.dumps({'_id': f"{name}-{sid}-tok-{t.i}", '_source': {"type":"tok", "id": f"{name}-{sid}-tok-{t.i}", "src":name, "src":sid, 'i':t.i, "head":t.head.i, 'lex':t.text, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, "gpos":t.head.pos_, "glem":t.head.lemma_ } }) + "\n") 
			except Exception as e:
				print ("ex:", e, sid, line) 
	os.system(f"gzip -f -9 {outfile}")
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

if __name__	== '__main__':
	import fire 
	fire.Fire(run)