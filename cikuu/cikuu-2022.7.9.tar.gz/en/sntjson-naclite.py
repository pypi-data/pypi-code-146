# 2022.11.17, cp from sntjson-mysql.py
# 2022.10.26 cp from sntjson-zset   # 2022.10.25  zset-like:  (key, name, value)  |markdown highlight : ==highlighted text==
import json, traceback,sys, time,  fileinput, os, en,fire, sqlite3
from collections import Counter,defaultdict
from dic.wordlist import wordlist 
add = lambda *names: [fire.ssi[ name.split('|')[0] ].update({ name.split('|')[-1] : 1}) for name in names if  not '\t' in name and len(name) <= 80 ]
reg = lambda kp, snt : fire.mapsnt.update({kp: snt})  if not kp in fire.mapsnt else None # use mysql later, to low down memory requirement

def walk(doc): 
	add( "#|sntnum")  
	[add( f"{t.lemma_}|{t.pos_}", f"{t.lemma_}:LEX|{t.text.lower()}", f"LEM|{t.lemma_.lower()}", f"LEX|{t.text.lower()}", f"{t.pos_}|{t.lemma_.lower()}"
		,f"{t.lemma_.lower()}:{t.pos_}|{t.tag_}",f"*:{t.pos_}|{t.tag_}") for t in doc if not t.pos_ in ('PROPN','X', 'PUNCT') and t.is_alpha  and t.lemma_.lower() in wordlist]
	for t in doc:
		add( "#|LEX", f"#|{t.pos_}", f"#|{t.tag_}",f"{t.pos_}|{t.tag_}",f"#|{t.dep_}",f"{t.pos_}|{t.dep_}") 
		reg(f"{t.lemma_}:{t.pos_}:{t.tag_}", doc.text)
		if t.pos_ not in ("PROPN","PUNCT","SPACE") and t.is_alpha and t.head.is_alpha and t.lemma_.lower() in wordlist and t.head.lemma_.lower() in wordlist: #*:VERB:~punct:VERB:wink
			add(f"{t.head.lemma_}:{t.head.pos_}:{t.dep_}:{t.pos_}|{t.lemma_}", f"{t.head.lemma_}:{t.head.pos_}:{t.dep_}|{t.pos_}",f"{t.head.lemma_}:{t.head.pos_}|{t.dep_}", f"*:{t.head.pos_}|{t.dep_}")
			reg(f"{t.head.lemma_}:{t.head.pos_}:{t.dep_}:{t.pos_}:{t.lemma_}", doc.text) 
			if t.dep_ not in ('ROOT'): 
				add(f"{t.lemma_}:{t.pos_}:~{t.dep_}:{t.head.pos_}|{t.head.lemma_}", f"{t.lemma_}:{t.pos_}:~{t.dep_}|{t.head.pos_}", f"{t.lemma_}:{t.pos_}|~{t.dep_}", f"*:{t.pos_}|~{t.dep_}")
				reg(f"{t.lemma_}:{t.pos_}:~{t.dep_}:{t.head.pos_}:{t.head.lemma_}", doc.text)
			
	for sp in doc.noun_chunks: #book:NOUN:np:a book
		add(f"{sp.root.lemma_.lower()}:{sp.root.pos_}:np|{sp.text.lower()}", f"{sp.root.lemma_.lower()}:{sp.root.pos_}|np", f"*:{sp.root.pos_}|np", f"#|np",)
		reg(f"{sp.root.lemma_.lower()}:{sp.root.pos_}:np:{sp.text.lower()}", doc.text.replace(sp.text, f"<b>{sp.text}</b>") )

	# [('pp', 'on the brink', 2, 5), ('ap', 'very happy', 9, 11)]
	for lem, pos, type, chunk in en.kp_matcher(doc): #brink:NOUN:pp:on the brink
		add(f"{lem}:{pos}:{type}|{chunk}", f"{lem}:{pos}|{type}", f"*:{pos}|{type}", f"#|{type}")
	for trpx, row in en.dep_matcher(doc): #[('svx', [1, 0, 2])] ## consider:VERB:vnpn:**** 
		verbi = row[0] #consider:VERB:be_vbn_p:be considered as
		add(f"{doc[verbi].lemma_}:{doc[verbi].pos_}|{trpx}", f"*:{doc[verbi].pos_}|{trpx}", f"#|{trpx}") #consider:VERB:svx
		if trpx == 'sva' and doc[row[0]].lemma_ == 'be': # fate is sealed, added 2022.7.25
			add(f"{doc[row[1]].lemma_}:{doc[row[1]].pos_}:sbea:{doc[row[2]].pos_}|{doc[row[2]].lemma_}", f"{doc[row[1]].lemma_}:{doc[row[1]].pos_}|sbea", f"*:{doc[row[1]].pos_}|sbea")
			add(f"{doc[row[2]].lemma_}:{doc[row[2]].pos_}:~sbea:{doc[row[1]].pos_}|{doc[row[1]].lemma_}", f"{doc[row[2]].lemma_}:{doc[row[2]].pos_}|~sbea", f"*:{doc[row[2]].pos_}|~sbea")

	# last to be called, since NP is merged
	for row in en.verbnet_matcher(doc): #[(1, 0, 3, 'NP V S_ING')]
		if len(row) == 4: 
			verbi, ibeg, iend, chunk = row
			if doc[verbi].lemma_.isalpha() : 
				add(f"{doc[verbi].lemma_}:{doc[verbi].pos_}:verbnet|{chunk}") #consider:VERB:verbnet:NP V S_ING

	for name,ibeg,iend in en.post_np_matcher(doc): #added 2022.7.25
		if name in ('v_n_vbn','v_n_adj'): 
			add(f"{doc[ibeg].lemma_}:{doc[ibeg].pos_}:{name}|{doc[ibeg].lemma_} {doc[ibeg+1].lemma_} {doc[ibeg+2].text}", f"{doc[ibeg].lemma_}:{doc[ibeg].pos_}|{name}", f"*:{doc[ibeg].pos_}|{name}")

def run(infile, sqlite:str='corpus.naclite'):
	''' saveto: mysql/file '''
	name = infile.split('/')[-1].split('.')[0] # ./
	start = time.time()
	fire.ssi = defaultdict(Counter)
	fire.mapsnt = {}
	print ("started:", infile , ",name=", name, flush=True)

	conn =	sqlite3.connect(sqlite, check_same_thread=False) 
	conn.execute(f"create table if not exists corpuslist( name varchar(100) not null primary key, en varchar(100), zh varchar(100), sntnum int not null default 0, lexnum int not null default 0) without rowid")
	conn.execute(f'DROP TABLE if exists {name}')
	conn.execute(f"create table {name}( name varchar(100) not null, attr varchar(100) not null, count int not null default 0, primary key(name, attr) ) without rowid")
	conn.execute(f'DROP TABLE if exists {name}_snt')
	conn.execute(f'''CREATE VIRTUAL TABLE if not exists {name}_snt USING fts5(sid, snt, terms, columnsize=0, detail=full,tokenize = "unicode61 remove_diacritics 0 tokenchars '-_'")''') #self.conn.execute('''CREATE VIRTUAL TABLE if not exists fts USING fts5(snt, terms, columnsize=0, detail=none,tokenize = "unicode61 remove_diacritics 0 tokenchars '-_'")''')
	conn.execute('PRAGMA synchronous=OFF')
	conn.execute('PRAGMA case_sensitive_like = 1')
	conn.commit()

	for did, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): 
		try:
			arr = json.loads(line.strip()) 
			doc = spacy.from_json(arr) 
			terms = " ".join([ f"{t.lemma_}_{t.pos_}" for t in doc  if t.pos_ not in ('PUNCT')] 
				+ [ f"{t.lemma_}_{t.pos_}_{t.tag_}_{t.text.lower()}" for t in doc  if t.pos_ not in ('PUNCT')] # consider:VERB:VBG:considering
				+ [ f"{t.head.lemma_}_{t.head.pos_}_{t.dep_}_{t.pos_}_{t.lemma_}" for t in doc if t.pos_ not in ('PRON','PUNCT') and t.dep_ in ('dobj','nsubj','advmod','acomp','amod','compound','xcomp','ccomp','oprd')])
			conn.execute(f"insert or ignore into {name}_snt(sid, snt,terms) values(?,?,?)", (did, doc.text.strip(), terms))
			walk(doc)
		except Exception as e:
			print ("ex:", e, did, line) 

	for k,si in fire.ssi.items(): 
		for s,i in si.items(): 
			try:
				conn.execute(f"insert or ignore into {name}(name, attr, count) values(?,?,?)", (k,s,i))
				if f"{k}:{s}" in fire.mapsnt:
					conn.execute(f"insert or ignore into {name}(name, attr, count) values(?,?,?)", (f"{k}:{s}",fire.mapsnt[f"{k}:{s}"],i) )
			except Exception as e: 
				print ("ex:", e, k,s,i)
	conn.execute(f"insert or ignore into corpuslist(name, sntnum, lexnum) values(?,?,?)", (name,fire.ssi['#']['sntnum'],fire.ssi['#']['LEX']))
	conn.commit()
	print(f"{infile} is finished, \t| using: ", time.time() - start)

if __name__	== '__main__':
	fire.Fire(run)

'''
select * from dic_snt where snt match  'niche';
select * from dic_snt where terms match  'niche_NOUN';
select * from dic_snt where terms match  'open_VERB_dobj_NOUN_door';

select * from dic where name= 'consider:VERB' and attr in ('dobj','vtov', 'vvbg', 'ccomp')

	outfile = name +".nac"
	with open( outfile, 'w') as fw:
		for k,si in fire.ssi.items(): 
			for s,i in si.items(): 
				fw.write(f"{k}\t{s}\t{i}\n")		
	os.system(f"gzip {outfile}") #-f -9
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

'''