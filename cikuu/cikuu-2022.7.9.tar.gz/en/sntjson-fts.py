# 2022.12.12,  add map, frames
# 2022.10.25 , add spacy json into dic_snt later 
import json, traceback,sys, time, fire,os,traceback,fileinput,en, pymysql

#brink:NOUN:pp:on the brink
get_pp	= lambda doc: [ f"{type}_" + chunk.replace(' ','_') for lem, pos, type, chunk in en.kp_matcher(doc) if type in ('pp')]

def get_kps(doc): 
	kps = [ f"{t.lemma_}_{t.pos_}" for t in doc  if t.pos_ not in ('PUNCT')] + [ f"{t.lemma_}_{t.pos_}_{t.tag_}" for t in doc  if t.pos_ not in ('PUNCT')] + get_pp(doc) + [ f"{t.head.lemma_}_{t.head.pos_}_{t.dep_}_{t.pos_}_{t.lemma_}" for t in doc if t.pos_ not in ('PRON','PUNCT') and t.dep_ in ('dobj','nsubj','advmod','acomp','amod','compound','xcomp','ccomp','oprd')]
			
	for sp in doc.noun_chunks: 
		kps.append (f"{sp.root.lemma_.lower()}_{sp.root.pos_}_np") 

	# [('pp', 'on the brink', 2, 5), ('ap', 'very happy', 9, 11)]
	for lem, pos, type, chunk in en.kp_matcher(doc): #brink:NOUN:pp:on the brink
		kps.append (f"{lem}_{pos}_{type}_{chunk.replace(' ','_')}")
	for trpx, row in en.dep_matcher(doc): #[('svx', [1, 0, 2])] ## consider:VERB:vnpn:**** 
		verbi = row[0] #consider:VERB:be_vbn_p:be considered as
		kps.append (f"{doc[verbi].lemma_}_{doc[verbi].pos_}_{trpx}") #consider_VERB_svx
		if trpx == 'sva' and doc[row[0]].lemma_ == 'be': # fate is sealed, added 2022.7.25
			kps.append (f"{doc[row[1]].lemma_}_{doc[row[1]].pos_}_sbea")

	# last to be called, since NP is merged
	for row in en.verbnet_matcher(doc): #[(1, 0, 3, 'NP V S_ING')]
		if len(row) == 4: 
			verbi, ibeg, iend, chunk = row
			if doc[verbi].lemma_.isalpha() : 
				kps.append (f"{doc[verbi].lemma_}_{doc[verbi].pos_}_{chunk.replace(' ','_')}") #consider:VERB:verbnet:NP V S_ING

	for name,ibeg,iend in en.post_np_matcher(doc): #added 2022.7.25
		if name in ('v_n_vbn','v_n_adj'): 
			kps.append (f"{doc[ibeg].lemma_}_{doc[ibeg].pos_}_{name}")
	return list(set(kps))

def run(infile, host:str='172.17.0.1', port:int=3309, db:str='nac'):
	'''  '''
	name = infile.split('.jsonlg')[0] 
	start = time.time()
	my_conn = pymysql.connect(host=host,port=port,user='root',password='cikuutest!',db=db)
	print ("started:", infile , my_conn,  flush=True)
	with my_conn.cursor() as cursor: 
		cursor.execute(f"drop TABLE if exists {name}_snt")
		cursor.execute(f"CREATE TABLE if not exists {name}_snt(sid int primary key, snt text not null, kps text not null, map JSON, frames text,  fulltext key `snt`(`snt`), fulltext key `kps`(`kps`), fulltext key `frames`(`frames`) ) engine=myisam  DEFAULT CHARSET=latin1 COLLATE=latin1_bin")
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)):  #for rowid, snt, doc in tqdm(Spacybs(dbfile).docs()) :
			try:
				arr = json.loads(line.strip()) 
				doc = spacy.from_json(arr)  #for sid, sp in enumerate(tdoc.sents):				doc = sp.as_doc()
				dic = {"tc": len(doc), "vc": len([t for t in doc if t.pos_.startswith("V")])}
				cursor.execute(f"insert ignore into {name}_snt(sid, snt, map, kps) values(%s, %s, %s, %s)", (sid, doc.text.strip(), 
					json.dumps(dic), 
					" ".join(get_kps(doc) ) ) )

			except Exception as e: 
				print ("ex:", e, sid,line)
				exc_type, exc_value, exc_traceback_obj = sys.exc_info()
				traceback.print_tb(exc_traceback_obj)
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

if __name__	== '__main__':
	fire.Fire(run)