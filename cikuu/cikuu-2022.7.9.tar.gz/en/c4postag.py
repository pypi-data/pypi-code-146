# 2022.8.30   | https://blog.csdn.net/weixin_44993313/article/details/106883827  | parent-child relations
import json, traceback,sys, time,  fileinput, os, en,hashlib

def _oneself( t ) :
	from dic.oneself import oneself 
	return oneself.get(t.text.lower(), '') 

def postag_token( t ): # uniq by ana 
	if t.pos_ in ('PROPN','NUM','X','SPACE','PUNCT'): return  f"{t.text}_{t.pos_}_{t.tag_}"
	if t.text.lower() in (t.lemma_, t.text): return  f"{t.text}_{t.lemma_}_{t.pos_}_{t.tag_}{_oneself(t)}"  # has_has_have
	return f"{t.text}_{t.text.lower()}_{t.lemma_}_{t.pos_}_{t.tag_}{_oneself(t)}"

def postag_doc( doc ):
	arr = [ postag_token(t) for t in doc]
	for np in doc.noun_chunks:
		nplen = np.end - np.start
		arr[ np.start] =  arr[ np.start] + f"_NP{nplen}"  # _NP3
	res =  "_^ " + ' '.join(arr)
	return res.replace('\n_SPACE__SP','').strip()

def run(infile):
	''' c4-train.00604-of-01024.docjsonlg.3.4.1.gz -> c4-train.00604-of-01024.postag.gz | 2022.8.22 '''
	outfile = infile.split('.docjson')[0] + f".postag"
	start = time.time()
	print ("started:", infile ,  ' -> ',  outfile, flush=True)
	with open(outfile, 'w') as fw: 
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): 
			try:
				arr = json.loads(line.strip()) #				Doc(spacy.nlp.vocab).from_json(arr)				#res['info'] = {"tm": arr.get("timestamp",""), "url":arr.get('url','')}
				url = arr.get('info',{}).get('url','')
				if not url: continue 
				did = hashlib.md5(url.encode("utf8")).hexdigest()
				fw.write(json.dumps({'_id': did, '_source': {'url':url, 'tm': arr.get('info',{}).get('tm','')} }) + "\n") # type:doc 
				tdoc = spacy.from_json(arr) 
				for i,snt in enumerate(tdoc.sents):
					doc = snt.as_doc() 
					smd5 = hashlib.md5(snt.text.strip().encode("utf8")).hexdigest() # overwrite the duplicated snt
					#postag = "_^ " + ' '.join([ postag_token(t) for t in doc]) # uniq by ana #,'PUNCT'
					fw.write(json.dumps({'_id': smd5, '_source': {"did": did, "postag":postag_doc(doc) } }) + "\n") 
			except Exception as e:
				print ("ex:", e, sid, line) 
	os.system(f"gzip -f -9 {outfile}")
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

if __name__	== '__main__':
	import fire 
	fire.Fire(run)

'''
ubuntu@cpu76:/ftp/c4/10$ nohup find . -name "*.gz" -exec python3 c4postag.py {} \; & 
[1] 2097770

(spacy341) pigaiwang@dgx-1:~/tmp/c4data/6x$ python c4postag.py c4-train.00604-of-01024.docjsonlg.3.4.1.gz 
started: c4-train.00604-of-01024.docjsonlg.3.4.1.gz  ->  c4-train.00604-of-01024.postag
c4-train.00604-of-01024.docjsonlg.3.4.1.gz is finished, 	| using:  5043.917199850082

=> 7314660 (docs)  3gb

6799957
2.7gb

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