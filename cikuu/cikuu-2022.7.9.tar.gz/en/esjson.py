# 2022.8.26  add withsi support
# 2022.8.25  _book:booked (lem) 
# 2022.8.19 , cp from docjson 
# 2022.8.14 , depend on spacy3.4.1 lg model 
import json, traceback,sys, time,  fileinput, os, en
from collections import Counter

def _oneself( t ) :
	from dic.oneself import oneself 
	return oneself.get(t.text.lower(), '') 

doc_toks = lambda sid, doc:  [ {'_id': f"{sid}-tok-{t.i}", '_source': {"type":"tok", "src":sid, 'i':t.i, "head":t.head.i, 'lex':t.text, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, "gpos":t.head.pos_, "glem":t.head.lemma_ } } for t in doc ] 
postag	=  lambda doc:  "_^ " + ' '.join([ f"_{t.pos_}_{t.tag_}" if t.pos_ in ('PROPN','NUM','X','SPACE') else f"{t.text if t.text in ('I') else t.text.lower()}_{t.lemma_}_{t.pos_}_{t.tag_}{_oneself(t)}"  for t in doc]) # uniq by ana #,'PUNCT'

def sntdoc_kps(doc): 
	''' doc is of single sent, 2022.9.6 '''
	_kps = []
	[ _kps.append(f"{t.pos_}:{t.lemma_}") for t in doc]  # VERB:book
	[ _kps.append(f"_{t.lemma_}:{t.text.lower()}") for t in doc]  # _book:booked,  added 2022.8.21
	[ _kps.append(f"{t.tag_}:{t.pos_}_{t.lemma_}") for t in doc]  # VBD:VERB_book,  added 2022.8.25
	[ _kps.append(f"{t.dep_}:{t.head.pos_}_{t.head.lemma_}:{t.pos_}_{t.lemma_}") for t in doc if t.pos_ not in ('PUNCT')]  # 
	[ _kps.append(f"~{t.dep_}:{t.pos_}_{t.lemma_}:{t.head.pos_}_{t.head.lemma_}") for t in doc if t.pos_ not in ('PUNCT')]  # 
	[ _kps.append(f"NP:{doc[sp.end-1].pos_}_{doc[sp.end-1].lemma_}:{sp.text.lower()}") for sp in doc.noun_chunks ]
	_kps.append( f"stype:" +  "simple_snt" if en.simple_sent(doc) else "complex_snt" )
	if en.compound_snt(doc) : _kps.append("stype:compound_snt")

	# [('pp', 'on the brink', 2, 5), ('ap', 'very happy', 9, 11)]
	for lem, pos, type, chunk in en.kp_matcher(doc): #brink:NOUN:pp:on the brink
		_kps.append(f"{type}:{pos}_{lem}:{chunk}")
	for trpx, row in en.dep_matcher(doc): #[('svx', [1, 0, 2])] ## consider:VERB:vnpn:**** 
		verbi = row[0] #consider:VERB:be_vbn_p:be considered as
		_kps.append(f"{trpx}:{doc[verbi].pos_}_{doc[verbi].lemma_}")
		if trpx == 'sva' and doc[row[0]].lemma_ == 'be': # fate is sealed, added 2022.7.25   keep sth. stuck
			_kps.append(f"sbea:{doc[row[1]].pos_}_{doc[row[1]].lemma_}:{doc[row[2]].pos_}_{doc[row[2]].lemma_}")
		
	# last to be called, since NP is merged
	for row in en.verbnet_matcher(doc): #[(1, 0, 3, 'NP V S_ING')]
		if len(row) == 4: 
			verbi, ibeg, iend, chunk = row
			if doc[verbi].lemma_.isalpha() : 
				_kps.append(f"verbnet:{doc[verbi].pos_}_{doc[verbi].lemma_}:{chunk}")

	for name,ibeg,iend in en.post_np_matcher(doc): #added 2022.7.25
		if name in ('v_n_vbn','v_n_adj'): 
			_kps.append(f"{name}:{doc[ibeg].pos_}_{doc[ibeg].lemma_}:{doc[ibeg].lemma_} {doc[ibeg+1].lemma_} {doc[ibeg+2].text}")

	return list(set(_kps))

def kps(sid, snt, doc, with_tok:bool=False): 
	''' 2022.8.19 '''
	postag = "_^ " + ' '.join([ f"_{t.pos_}_{t.tag_}" if t.pos_ in ('PROPN','NUM','X','SPACE') else f"{t.text if t.text in ('I') else t.text.lower()}_{t.lemma_}_{t.pos_}_{t.tag_}{_oneself(t)}"  for t in doc]) # uniq by ana #,'PUNCT'
	actions = []
	actions.append( {'_id': sid, '_source': {'type':'snt', 'snt':snt, 'postag':postag,  'src': sid,  'tc': len(doc), 'kps': sntdoc_kps(doc) } } )
	if with_tok: [ actions.append( {'_id': f"{sid}-tok-{t.i}", '_source': {"type":"tok", "src":sid, 'i':t.i, "head":t.head.i, 'lex':t.text, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, "gpos":t.head.pos_, "glem":t.head.lemma_ } }) for t in doc ] 
	return actions

def kps_esjson(infile, outfile=None,  with_tok:bool=False,  withsi:bool=True):
	''' gzjc.jsonlg.3.4.1.gz -> gzjc.esjson | 2022.8.19 '''
	if outfile is None: outfile = infile.split('.json')[0] + f".esjson"
	if os.path.exists(f"{outfile}.gz"):  #os.remove(f"{outfile}.gz")
		print("already exists")
		return 
	start = time.time()
	si = Counter()
	print (f"started: {infile} -> {outfile}, withsi = {withsi}", flush=True)
	with open(outfile, 'w') as fw: 
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): 
			try:
				arr = json.loads(line.strip())
				doc = Doc(spacy.nlp.vocab).from_json(arr)				#res['info'] = {"tm": arr.get("timestamp",""), "url":arr.get('url','')}
				for ar in kps(sid, doc.text, doc, with_tok):
					if withsi: #[ si.update({kp:1}) for kp in ar['_source']['kps'] ]
						for kp in ar['_source']['kps']:
							si.update({kp:1})
							akp = kp.split(':')
							if len(akp) > 1: si.update({akp[0]:1})
							if len(akp) > 2: si.update({f"{akp[0]}:{akp[1]}":1})
					fw.write(json.dumps(ar) + "\n") 
			except Exception as e:
				print ("ex:", e, sid, line) 
		fw.write(json.dumps({'_id': "sntsum", '_source': {'s':"sntsum", 'i':sid+1 } }) + "\n")  # added 2022.9.4
		if withsi and len(si) > 0: 
			for s,i in si.items(): 
				fw.write(json.dumps({'_id': s, '_source': {'s':s, 'i':i	} }) + "\n") 
	os.system(f"gzip -f -9 {outfile}")
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

if __name__	== '__main__':
	import fire 
	fire.Fire(kps_esjson)

'''
dic  with tok :  7705941  2.5gb
without tok :	681563    1.4gb

(spacy341) pigaiwang@dgx-1:~/tmp$ python esjson.py dic.jsonlg.3.4.1.gz 
started: dic.jsonlg.3.4.1.gz  ->  dic.esjson
dic.jsonlg.3.4.1.gz is finished, 	| using:  1040.6460061073303

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