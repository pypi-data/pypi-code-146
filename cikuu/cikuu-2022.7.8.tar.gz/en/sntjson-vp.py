# 2022.12.24
import json, traceback,sys, time, fire,os,traceback,fileinput,en

def merge_np(doc):
	with doc.retokenize() as retokenizer:
		for np in doc.noun_chunks:
			attrs = {"tag": np.root.tag, "dep": np.root.dep, "ent_type": "NP", "lemma":doc[np.end-1].lemma} # , "lemma":doc[np.end-1].lemma | added 2022.7.26
			retokenizer.merge(np, attrs=attrs) 
	return doc

def merge_clause(doc): # subtree of a verb is the clause , https://subscription.packtpub.com/book/data/9781838987312/2/ch02lvl1sec13/splitting-sentences-into-clauses
	with doc.retokenize() as retokenizer:
		for v in [t for t in doc if t.pos_ == 'VERB' and t.dep_ != 'ROOT' ] : # non-root
			try:
				children = list(v.subtree)
				start = children[0].i  	
				end = children[-1].i 
				attrs = {"pos": v.pos, "tag": v.tag, "dep": v.dep, "lemma":v.lemma, "ent_type": "S." + v.dep_ } # S.advcl ,  S.conj 
				retokenizer.merge(doc[start : end+1], attrs=attrs)
			except Exception as e:
				print ( "merge_clause ex:", e, v )
	return doc

vp_tok = lambda t:  "NP/" + t.text.replace(' ','_') if t.ent_type_ == 'NP' else t.ent_type_  if t.ent_type_.startswith("S.") else t.tag_ +"/" + t.text
vp_chunk = lambda doc, start, end:  

def run(infile):
	'''  '''
	name = infile.split('.jsonlg')[0] 
	start = time.time()
	with open (f"{name}.vp", "w") as fw: 
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)):  #for rowid, snt, doc in tqdm(Spacybs(dbfile).docs()) :
			try:
				arr = json.loads(line.strip()) 
				doc = spacy.from_json(arr) 	#for sid, sp in enumerate(tdoc.sents):				doc = sp.as_doc()
				doc = merge_np(doc)
				doc = merge_clause(doc)
				for t in doc: 
					if t.pos_ in ("VERB") or t.tag_ in ("MD"): 
												

			except Exception as e: 
				print ("ex:", e, sid,line)
				exc_type, exc_value, exc_traceback_obj = sys.exc_info()
				traceback.print_tb(exc_traceback_obj)
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

if __name__	== '__main__':
	fire.Fire(run)