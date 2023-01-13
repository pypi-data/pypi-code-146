# 2022.8.20 , cp from esjson 
import json, traceback,sys, time,  fileinput, os, en,hashlib

def run(infile):
	''' gzjc.docjsonlg.3.4.1.gz -> gzjc.c4skenp | 2022.8.20 '''
	outfile = infile.split('.docjson')[0] + f".skenp"
	start = time.time()
	print ("started:", infile ,  ' -> ',  outfile, flush=True)
	with open(outfile, 'w') as fw: 
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): 
			try:
				arr = json.loads(line.strip()) 
				url = arr.get('info',{}).get('url','')
				did = hashlib.md5(url.encode("utf8")).hexdigest()
				tdoc = spacy.from_json(arr) 
				for i,snt in enumerate(tdoc.sents):
					doc = snt.as_doc() 
					merge_nps(doc) # merge adv + verb/adj 
					skenp = "_^ " + " ".join([ "_{t.lemma_}_NP" if t.ent_type_ == 'NP' else f"{t.text}_{t.lemma_}_{t.pos_}_{t.tag_}" for t in doc]) + " _$"
					fw.write(json.dumps({'_id': f"{did}-{i}-skenp", '_source': {"skenp":skenp, "url":url, 'tm': arr.get('info',{}).get('tm','')} }) + "\n") 
			except Exception as e:
				print ("ex:", e, sid, line) 
	os.system(f"gzip -f -9 {outfile}")
	print(f"{infile} is finished, \t| using: ", time.time() - start) 


if __name__	== '__main__':
	import fire 
	fire.Fire(run)

'''
>>> doc.to_json()
{'text': 'I am a boy.', 'ents': [], 'sents': [{'start': 0, 'end': 11}], 'tokens': [{'id': 0, 'start': 0, 'end': 1, 'tag': 'PRP', 'pos': 'PRON', 'morph': 'Case=Nom|Number=Sing|Person=1|PronType=Prs', 'lemma': 'I', 'dep': 'nsubj', 'head': 1}, {'id': 1, 'start': 2, 'end': 4, 'tag': 'VBP', 'pos': 'AUX', 'morph': 'Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin', 'lemma': 'be', 'dep': 'ROOT', 'head': 1}, {'id': 2, 'start': 5, 'end': 6, 'tag': 'DT', 'pos': 'DET', 'morph': 'Definite=Ind|PronType=Art', 'lemma': 'a', 'dep': 'det', 'head': 3}, {'id': 3, 'start': 7, 'end': 10, 'tag': 'NN', 'pos': 'NOUN', 'morph': 'Number=Sing', 'lemma': 'boy', 'dep': 'attr', 'head': 1}, {'id': 4, 'start': 10, 'end': 11, 'tag': '.', 'pos': 'PUNCT', 'morph': 'PunctType=Peri', 'lemma': '.', 'dep': 'punct', 'head': 1}]}

 [{'id': 0,
   'start': 0,
   'end': 3,
   'tag': 'PRP',
   'pos': 'PRON',
   'morph': 'Case=Nom|Gender=Fem|Number=Sing|Person=3|PronType=Prs',
   'lemma': 'she',
   'dep': 'nsubj',
   'head': 1},
'''