# 2022.6.29  
from uvirun import *
import spacy
from spacy.matcher import Matcher
if not hasattr(spacy, 'nlp'): spacy.nlp  = spacy.load('en_core_web_lg')  #He who laughs last laughs best.

@app.get('/spacy/info', tags=["spacy"])
def spacy_info(): return spacy.nlp.meta

@app.get('/spacy/make-single', tags=["spacy"])
def make_single(snt="Parents attach much importance to education."): 
	''' add idf later, 2022.12.21  '''
	from dic.verbtag import taglist  #options = "attach,pay,link,apply".split(',')
	doc			= spacy.nlp(snt) 
	pred_tag	= [t.tag_ for t in doc if t.dep_ == 'ROOT' and t.pos_.startswith("V") ][0] # VBP 
	body		= " ".join([ '*' if t.dep_ == 'ROOT' else t.text for t in doc ]) 
	rows		= requests.get(f"http://cpu76.wrask.com:8000/unmasker", params={"q":body,"topk":1000}).json()
	tags		= taglist(pred_tag)
	words		= [ {"word":row['word'], "score": row['score']} for row in rows if row['word'] in tags  and row['score']> 0.001 ]
	return {"snt":snt, "pred_tag":pred_tag, "body": body, "data": words }

@app.post('/spacy/snthas', tags=["spacy"])
def sent_has(chunks:list=["by the time", "recognize"], snt:str="By the time when he arrived, he recognized it."): 
	''' 输入译文中是否包括了指定的单词或者词组， 江阴 2022.10.16 '''
	import re
	doc = spacy.nlp(snt) 
	lemmas = " ".join([ t.lemma_.lower() for t in doc])
	return [{"chunk":chunk, "hit": re.search(rf'\b{chunk}\b',lemmas) is not None } for chunk in chunks]

@app.post('/spacy/sent_is_emphatic', tags=["spacy"])
def spacy_emphatic_sentence(rules:dict = {"it_be":  [[{"LEMMA": "it"}, {"LEMMA": 'be'}], [{"LEMMA": "be"}, {"LEMMA": 'it'}] ], 
		"do_verb":  [[ {"LEMMA": "do"}, {"TAG": 'VB'}] ],}
	, snt:str="It is I who am responsible for this project.", missed:str="no_emphatic_sentence"): 
	''' 判断输入的句子是否是强调句 He did write to you last week.  Tom does study hard now.'''
	matcher = Matcher(spacy.nlp.vocab)
	[ matcher.add(name, patterns,  greedy ='LONGEST') for name, patterns in rules.items() ]

	doc = spacy.nlp(snt)
	hits =  [ spacy.nlp.vocab[name].text for name, ibeg,iend in matcher(doc) ]
	if not hits : return missed
	hit = hits[0]
	if hit == 'do_verb' : return hit 
	if hit == 'it_be': return hit if re.search(r'\b(that|who)\b',snt.lower()) is not None else missed
	return missed

@app.get('/spacy/to_json', tags=["spacy"])
def doc_to_json(text:str='The quick fox jumped over the lazy dog.', add_gov:bool=False): 
	''' {'text': 'The quick fox jumped over the lazy dog.', 'ents': [], 'sents': [{'start': 0, 'end': 39}], 'tokens': [{'id': 0, 'start': 0, 'end': 3, 'tag': 'DT', 'pos': 'DET', 'morph': 'Definite=Def|PronType=Art', 'lemma': 'the', 'dep': 'det', 'head': 2}, {'id': 1, 'start': 4, 'end': 9, 'tag': 'JJ', 'pos': 'ADJ', 'morph': 'Degree=Pos', 'lemma': 'quick', 'dep': 'amod', 'head': 2}, {'id': 2, 'start': 10, 'end': 13, 'tag': 'NN', 'pos': 'NOUN', 'morph': 'Number=Sing', 'lemma': 'fox', 'dep': 'nsubj', 'head': 3}, {'id': 3, 'start': 14, 'end': 20, 'tag': 'VBD', 'pos': 'VERB', 'morph': 'Tense=Past|VerbForm=Fin', 'lemma': 'jump', 'dep': 'ROOT', 'head': 3}, {'id': 4, 'start': 21, 'end': 25, 'tag': 'IN', 'pos': 'ADP', 'morph': '', 'lemma': 'over', 'dep': 'prep', 'head': 3}, {'id': 5, 'start': 26, 'end': 29, 'tag': 'DT', 'pos': 'DET', 'morph': 'Definite=Def|PronType=Art', 'lemma': 'the', 'dep': 'det', 'head': 7}, {'id': 6, 'start': 30, 'end': 34, 'tag': 'JJ', 'pos': 'ADJ', 'morph': 'Degree=Pos', 'lemma': 'lazy', 'dep': 'amod', 'head': 7}, {'id': 7, 'start': 35, 'end': 38, 'tag': 'NN', 'pos': 'NOUN', 'morph': 'Number=Sing', 'lemma': 'dog', 'dep': 'pobj', 'head': 4}, {'id': 8, 'start': 38, 'end': 39, 'tag': '.', 'pos': 'PUNCT', 'morph': 'PunctType=Peri', 'lemma': '.', 'dep': 'punct', 'head': 3}]} '''
	doc = spacy.nlp(text)
	res = doc.to_json()
	if add_gov: [ res['tokens'][t.i].update({"glem": t.head.lemma_, "gpos":t.head.pos_}) for t in doc]
	return res 

@app.post('/spacy/matcher', tags=["spacy"])
def spacy_matcher(rules:dict = {
"Vend":[[{"POS": {"IN": ["AUX","VERB"]}},{"POS": {"IN": ["ADV"]}, "OP": "*"}, {"POS": {"IN": ["ADJ","VERB"]}, "OP": "*"},{"POS": {"IN": ["PART","ADP","TO"]}, "OP": "*"},{"POS": 'VERB'}]], # could hardly wait to meet
"vp":  [[{'POS': 'VERB'},{"POS": {"IN": ["DET","ADP","ADJ"]}, "OP": "*"},{"POS": 'NOUN'}, {"POS": {"IN": ["ADP","TO"]}, "OP": "*"}], [{'POS': 'VERB'},{"POS": {"IN": ["DET","ADP","ADJ","TO","PART"]}, "OP": "*"},{"POS": 'VERB'}]], # wait to meet
"pp":  [[{'POS': 'ADP'},{"POS": {"IN": ["DET","NUM","ADJ",'PUNCT','CONJ']}, "OP": "*"},{"POS": {"IN": ["NOUN","PART"]}, "OP": "+"}]],    
"ap":  [[{"POS": {"IN": ["ADV"]}, "OP": "+"}, {"POS": 'ADJ'}]],  
"vprt":	[[{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"POS": {"IN": ["PREP", "ADP",'TO']}, "OP": "+"}]],   # look up /look up from,  computed twice
"vtov":	[[{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"TAG": 'TO'},{"TAG": 'VB'}]],   # plan to go
"vvbg":	[[{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"TAG": 'VBG'}]],   # consider going
"vpg":	[[{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"POS": {"IN": ["PREP", "ADP",'PART']}, "OP": "+"},{"TAG": 'VBG'}]],   # insisted on going
"be_vbn_p": [[{'LEMMA': 'be'},{"TAG": {"IN": ["VBN"]}}, {"POS": {"IN": ["PREP", "ADP",'PART']}}]],   # base:VERB:be_vbn_p:be based on   
"be_adj_p": [[{'LEMMA': 'be'},{"POS": {"IN": ["ADJ"]}}, {"POS": {"IN": ["PREP", "ADP",'PART']}}]],   # be angry with
} , text:str='The quick fox jumped over the lazy dog.'): 
	''' for name, ibeg,iend in matcher(doc) : print(spacy.nlp.vocab[name].text, doc[ibeg:iend].text) 
	#[('vend', 'consider going', 1, 3), ('vp', 'consider going', 1, 3), ('vvbg', 'consider going', 1, 3), ('vprt', 'going to', 2, 4)] , added 2022.8.22 '''
	from spacy.matcher import Matcher
	matcher = Matcher(spacy.nlp.vocab)
	[ matcher.add(name, patterns,  greedy ='LONGEST') for name, patterns in rules.items() ]

	doc = spacy.nlp(text)
	return [ {"name":spacy.nlp.vocab[name].text, "ibeg":ibeg,"iend":iend, "chunk":doc[ibeg:iend].text, "offset": doc[ibeg].idx}  for name, ibeg,iend in matcher(doc)] 

@app.get('/spacy/stype', tags=["spacy"])
def spacy_stype(text:str='The quick fox jumped over the lazy dog. It are ok.'): 
	''' stype , 2022.8.23 '''
	tdoc	= spacy.nlp(text)
	res		= []
	for snt in tdoc.sents: 
		doc = snt.as_doc() 
		stype = [ "simple_sent" if len([t for t in doc if t.pos_ == 'VERB' and t.dep_ != 'ROOT']) <= 0  else "complex_sent"]
		if len([t for t in doc if t.dep_ == 'conj' and t.head.dep_ == 'ROOT']) > 0 : stype.append("compound_sent")
		res.append( {"start":snt.start, "end": snt.end, "text": snt.text, "stype": stype} )
	return res

@app.get('/spacy/annotate', tags=["spacy"])
def spacy_annotate(text:str='The quick fox jumped over the lazy dog.',poslist:str='VERB,NOUN,ADV,ADJ,CCONJ'): 
	''' '''
	doc		= spacy.nlp(text)
	poslist = poslist.strip().split(',') 
	tokens	= [ {'text': t.text} if not t.pos_ in poslist else {'text': t.text, "labels":[t.pos_]} for t in doc ]
	return {"tokens": tokens,"labels": [ {"text": pos} for pos in poslist] }

@app.get('/spacy/tok', tags=["spacy"])
def spacy_tok(text:str='The quick fox jumped over the lazy dog.',chunks:bool=False, morph:bool=False): 
	''' select * from url('http://cpu76.wrask.com:8000/spacy/tok', JSONEachRow, 'i UInt32, head UInt32, off UInt32, lex String, text_with_ws String,lem String, pos String, tag String, dep String, gov String') ''' 
	doc = spacy.nlp(text) 
	dic = { t.i: {'i':t.i, "head":t.head.i, 'off':t.idx, 'lex':t.text, 'text_with_ws':t.text_with_ws, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, "gov":t.head.lemma_ + "_" + t.head.pos_ }  for t in doc }
	if morph: [v.update({"morph":json.dumps(doc[i].morph.to_dict())}) for i,v in dic.items()]
	if chunks: 
		[v.update({"chunks":[]}) for k,v in dic.items()]
		[ dic[ sp.end - 1 ]['chunks'].append( {'lempos': doc[sp.end - 1].lemma_ + "_NOUN", "type":"NP", "chunk":sp.text.lower() } ) for sp in doc.noun_chunks]   ## start/end ? 
	return [ v for v in dic.values()]  # colored VERB html

@app.get('/spacy/chunks', tags=["spacy"])
def spacy_chunks(text:str='The quick fox jumped over the lazy dog.'): 
	''' add vp_matcher,  the fox:NP-DET NOUN ''' 
	doc = spacy.nlp(text) 
	return [{"chunk":sp.text.lower() +":NP-" + " ".join([ doc[i].pos_ for i in range(sp.start, sp.end)])} for sp in doc.noun_chunks if sp.end - sp.start > 1] 

@app.get('/spacy/NP', tags=["spacy"])
def spacy_NP(text:str='The quick fox jumped over the lazy dog.', minlen:int=1): 
	''' 2022.8.23 ''' 
	doc = spacy.nlp(text) 
	return [{"chunk":sp.text, 'start': sp.start, 'end': sp.end, 'offset': doc[sp.start].idx, 'type':"NP" } for sp in doc.noun_chunks if sp.end - sp.start > minlen] 

@app.get('/spacy/clause', tags=["spacy"])
def spacy_clause(text:str='What I read is what I see.',):  
	''' {'S.prep-0': {'type': 'S.prep', 'start': 0, 'end': 2, 'lem': 'consider', 'chunk': 'Considering the possibility'}, 'S.conj-9': {'type': 'S.conj', 'start': 9, 'end': 12, 'lem': 'be', 'chunk': 'she is ok .'}} '''
	doc = spacy.nlp(text) 
	res = []
	for v in [t for t in doc if t.pos_ == 'VERB' and t.dep_ != 'ROOT' ] : # non-root
		children = list(v.subtree) #end = children[-1].i 	tag = "S." + v.dep_   # S.advcl ,  S.conj 
		start = children[0].i
		chunk = " ".join([c.text for c in v.subtree])
		res.append({"type": v.dep_, "start":start, "end":children[-1].i + 1, "offset": doc[start].idx, "lemma": v.lemma_, "pos":v.pos_, "chunk": chunk }) 
	return res

@app.get('/spacy/trp', tags=["spacy"])
def spacy_trp(text:str='The boy is happy. The quick fox jumped over the lazy dog.'): 
	''' select * from url('http://cpu76.wrask.com:8000/spacy/trp', JSONEachRow, 'rel String, gov String, dep String') ''' 
	return [{'rel':f"{t.dep_}_{t.head.pos_}_{t.pos_}", "gov":t.head.lemma_, 'dep':t.lemma_}  for t in spacy.nlp(text)  ]

@app.get('/spacy/snt', tags=["spacy"])
def spacy_snt(text:str='I think I plan to go swimming.', funcs:str="vp,verbnet,clause"): 
	''' select * from url('http://cpu76.wrask.com:8000/spacy/snt?text=I%20think%20I%20plan%20to%20go%20swimming.&func=vp%2Cverbnet%2Cclause', LineAsString )  ''' 
	import en 
	mapf = { 
	"clause":	lambda doc	: [ {"verb":v.lemma_, "type":type, "start":start, "end":end, "chunk":chunk } for v,type, start, end, chunk in en.clause(doc)],
	"verbnet":	lambda doc	: [ {"verb":doc[verb_i].lemma_,  "start":start, "end":end, "chunk":chunk } for verb_i, start, end, chunk in en.verbnet_matcher(doc)],
	"vp":	lambda doc		: [ {"verb":doc[start].lemma_,  "start":start, "end":end, "chunk":chunk } for vp, chunk, start, end in en.vp_matcher(doc)],
	}
	doc = spacy.nlp(text)
	return { f: mapf.get(f, lambda doc: [])(doc)  for f in funcs.strip().split(',') }

@app.get('/spacy/meta', tags=["spacy"])
def doc_meta(text:str='She is happy.'): 
	''' {"pred":"jumped", "sub": "fox", "obj":"dog" } ''' 
	try:
		doc		= spacy.nlp(text) 
		predi	= [ t.i for t in doc if t.dep_ == 'ROOT'][0]
		meta	= {	t.dep_: t.text	for t in doc if t.dep_ not in ('punct') and t.head.i == predi } #if t.dep_ in ('nsubj','dobj','acomp') and t.head.i == predi:  meta[t.dep_] = t.text 
		return meta
	except Exception as e:
		print("ex:", e) 

@app.post('/spacy/desc', tags=["spacy"])
def doc_desc(dic:dict = { "Person=1": "第一人称",
  "Person=3": "第三人称",
  "Person=2": "第二人称",
  "Number=Sing": "单数",
  "Gender=Fem": "阴性",
  "Gender=Masc": "阳性",
  #"auxpass":"被动",
  "AUX": "助动词",
  "VERB": "动词",
  "NOUN": "名词",
  "ADJ": "形容词",
  "JJR": "比较级",
  "JJS": "最高级", 
  "ADV": "副词",
  "RBR": "比较级",
  "RBS": "最高级", 
  "PRON": "代词",
  "dobj": "宾语",
  "nsubj": "主语",
  "ROOT": "谓语",
  "acomp": "表语",
  #"Tense=Pres": "现在时",
  #"Tense=Past": "过去时"
  }
			, text:str='She is happy.', debug:bool=True): 
	''' 句子成分描述, 2022.7.10 '''
	doc		= spacy.nlp(text) #t.morph.to_json():  'Case=Nom|Number=Sing|Person=1|PronType=Prs'
	predi	= [ t.i for t in doc if t.dep_ == 'ROOT'][0]
	lat = { t.i: [ f"单词<span class='{t.pos_} {t.tag_}'>{t.text}</span>是 {dic[t.pos_]}"] if t.pos_ in dic else []  for t in doc  } 
	[ lat[t.i].append( dic[t.dep_] if t.dep_  in ('ROOT','auxpass') else f"单词<span class='{t.head.pos_} {t.head.tag_}'>{t.head.text}</span>的{dic[t.dep_]}" )  for t in doc if t.dep_ in dic and t.head.i == predi ] # only show the first level, the direct child of pred 
	[ lat[t.i].append( dic[t.tag_]) for t in doc if t.tag_ in dic ] # JJR
	[ lat[t.i].append( dic[pair])  for t in doc for pair in t.morph if pair in dic ] # Person=1
	res =  {"result": ["，".join(v) for v in lat.values() if v]}
	res['kp'] = { f"{t.head.dep_}:{t.dep_}" for t in doc if t.head.dep_ == 'ROOT'} # ROOT:auxpass 
	if debug: res['tok'] = { t.i: (t.text, t.pos_, t.tag_, t.dep_, t.head.i, t.morph.to_json()) for t in doc}
	return res

trantab	= str.maketrans("，　。！“”‘’；：？％＄＠＆＊（）［］＋－ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ１２３４５６７８９０ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ", ", .!\"\"'';:?%$@&*()[]+-ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz") #snt.translate(trantab)
@app.post('/nlp/color', tags=["nlp"])
def nlp_color(dic:dict = { "Person=1": "第一人称", "Person=3": "第三人称", "Person=2": "第二人称", "Number=Sing": "单数",  #"Gender=Fem": "阴性",  "Gender=Masc": "阳性",
  "auxpass":"被动", "ROOT:auxpass":"被动语态",  "AUX": "助动词",  "VERB": "动词",  "NOUN": "名词",  "ADJ": "形容词",  "JJR": "比较级",  "JJS": "最高级",   "ADV": "副词",  "RBR": "比较级",  "RBS": "最高级",   "PRON": "代词",
  "dobj": "宾语",  "nsubj": "主语",  "ROOT": "谓语",  "acomp": "表语" ,"NP":"名词短语" #,  "Tense=Pres": "现在时", "Aspect=Perf":"完成时", "Tense=Past": "过去时"
  , "cl:be:ccomp":"表语从句" , "cl:ccomp":"宾语从句", "cl:csubj":"主语从句","cl:acl":"同位语","cl:advcl":"状语从句", "cl:relcl":"定语从句","cl:pcomp":"宾语从句(介宾)"} #关系从句(定语从句)  | 形容词性从句(同位语)
  , text:str='He said he was happy where he was.'):  # ccomp
	''' toks starts from 0 , alike of nldp_synsem '''
	snt		= text.strip().translate(trantab)
	doc		= spacy.nlp(snt) 
	predi	= (t:=[ t.i for t in doc if t.dep_ == 'ROOT'], t[0] if t else -1)[-1]
	toks	= [{"i":t.i,"head":t.head.i,  "text":t.text, "pos":t.pos_, "tag":t.tag_, "dep":t.dep_, "morph":t.morph.to_json(), "label": dic.get(t.pos_,"")} for t in doc] 
	# only show the first level, the direct child of pred 
	[ toks[t.i].update({f"label:dep:{t.dep_}": (t.head.i, dic[t.dep_])}) for t in doc if t.dep_ in dic and t.head.i == predi ] 
	[ toks[t.i].update({f"label:dep:{t.tag_}": dic[t.dep_]})  for t in doc if t.dep_ in dic and t.head.i == predi and t.dep_ in ('ROOT','auxpass') ]
	[ toks[t.i].update({f"label:tag:{t.tag_}": dic[t.tag_]})  for t in doc if t.tag_ in dic ] # JJR
	[ toks[t.i].update({f"label:morph:{pair}": dic[pair]})   for t in doc for pair in t.morph if pair in dic ] # Person=1

	chunks	= [{"chunk":sp.text, "start":sp.start, "end": sp.end, "type":"NP", "dep": doc[sp.end-1].dep_, "head": doc[sp.end-1].head.i, "label":dic.get("NP","") } for sp in doc.noun_chunks if sp.end - sp.start > 1] 
	for v in [t for t in doc if (t.pos_ == 'VERB' or t.lemma_ in ('be') ) and t.dep_ != 'ROOT' ] : # non-root
		children = list(v.subtree) #end = children[-1].i 	tag = "S." + v.dep_   # S.advcl ,  S.conj 
		start,end  = children[0].i, children[-1].i + 1
		if end > start + 1 and doc[start].lemma_ not in ('to'): #In the final part of The Call of the Wild, the local wolves and other animals awake his desire to return to the wild.
			chunks.append({"chunk": " ".join([c.text for c in v.subtree]), "start":start, "end":end, "type":"cl", "dep": v.dep_ , "head": v.head.i
			, "label": dic.get(f"cl:{v.head.lemma_}:{v.dep_}",  dic.get(f"cl:{v.dep_}",'') ) })	# cl:be:ccomp => 表语从句

	res		= {'predi': predi, 'toks':toks, "chunks":chunks} 
	[res.update({ f"label:{t.head.dep_}:{t.dep_}" : dic[f"{t.head.dep_}:{t.dep_}"] }) for t in doc if t.head.dep_ == 'ROOT' and f"{t.head.dep_}:{t.dep_}" in dic] # ROOT:auxpass 
	return res

@app.get('/spacy-colored', tags=["nlp"])
def spacy_colored(snt:str='The sign of maturity is not when you start speaking big things, but, actually it is, when you start understanding small things.'): 
	''' [2022.12.13] 长难句分析， 1. 谓语高亮， 2. 同步gov主词  3. 收起np  4. 划出从句  5. 副词变灰 6， 连词高亮 7， 标上难度值idf 8， add scale '''
	from dic.word_idf import word_idf
	doc		= spacy.nlp(snt) 
	predi	= (t:=[ t.i for t in doc if t.dep_ == 'ROOT'], t[0] if t else -1)[-1]
	toks	= [ {"i":t.i,"head":t.head.i,  "text":t.text, "text_with_ws":t.text_with_ws, "pos":t.pos_, "tag":t.tag_, "dep":t.dep_, "morph":t.morph.to_json(), "glem":t.head.lemma_, "gpos":t.head.pos_, "idf": word_idf.get(t.text.lower(), 0) } for t in doc ]
	nps	= [{"chunk":sp.text, "start":sp.start, "end": sp.end, "type":"NP", "dep": doc[sp.end-1].dep_, "head": doc[sp.end-1].head.i , "headword":doc[sp.end-1].text } for sp in doc.noun_chunks if sp.end - sp.start > 1] 
	cls = []
	for v in [t for t in doc if (t.pos_ == 'VERB' or t.lemma_ in ('be') ) and t.dep_ != 'ROOT' ] : # non-root
		children = list(v.subtree) #end = children[-1].i 	tag = "S." + v.dep_   # S.advcl ,  S.conj 
		start,end  = children[0].i, children[-1].i + 1
		if end > start + 1 and doc[start].lemma_ not in ('to'): #In the final part of The Call of the Wild, the local wolves and other animals awake his desire to return to the wild.
			cls.append({"chunk": " ".join([c.text for c in v.subtree]), "start":start, "end":end, "type":"cl", "dep": v.dep_ , "head": v.head.i })	# cl:be:ccomp => 表语从句
	return {'snt': snt, 'predi': predi, 'toks':toks, "nps":nps, "cls": cls} 

@app.get('/spacy/highlight', tags=["spacy"])
def doc_highlight(text:str='And the quick fox hit the lazy dog.', as_html:bool=False): #, pos:str='ADJ'
	''' return html, with pos highlighted ''' 
	doc = spacy.nlp(text) 
	color = {'ROOT': 'red', 'dobj': 'gray', 'nsubj':'darkgray', 'cc':'orange'}
	dic = { t.i:  f"<span class='{t.pos_}' style='color:{color.get(t.dep_, 'black')}'>{t.text_with_ws}</span>" for t in doc }
	for sp in doc.noun_chunks :
		if sp.end - sp.start > 1 : 
			dic[sp.start] = "<u>" + dic[sp.start]
			dic[sp.end-1] = dic[sp.end-1] + "</u>"
	html = "<h1>"  + "".join([ v for v in dic.values()]) + "</h1>"
	return HTMLResponse(content=html) if as_html else [{"html": html }]

@app.get('/spacy/toks', tags=["spacy"])
def spacy_toks(text:str='The boy is happy. The quick fox jumped over the lazy dog.',chunks:bool=False, sino:str='sino', native:str='dic'): 
	''' [{'i': 0, 'head': 1, 'lex': 'The', 'lem': 'the', 'pos': 'DET', 'tag': 'DT', 'dep': 'det', 'gov': 'boy_NOUN', 'chunks': []}, {'i': 1, 'head': 2, 'lex': 'boy', 'lem': 'boy', 'pos': 'NOUN', 'tag': 'NN', 'dep': 'nsubj', 'gov': 'be_AUX', 'chunks': [{'lempos': 'boy_NOUN', 'type': 'NP', 'chunk': 'the boy'}]}, {'i': 2, 'head': 2, 'lex': 'is', 'lem': 'be', 'pos': 'AUX', 'tag': 'VBZ', 'dep': 'ROOT', 'gov': 'be_AUX', 'chunks': []}, {'i': 3, 'head': 2, 'lex': 'happy', 'lem': 'happy', 'pos': 'ADJ', 'tag': 'JJ', 'dep': 'acomp', 'gov': 'be_AUX', 'chunks': []}, {'i': 4, 'head': 2, 'lex': '.', 'lem': '.', 'pos': 'PUNCT', 'tag': '.', 'dep': 'punct', 'gov': 'be_AUX', 'chunks': []}] JSONEachRow format , added 2022.6.25 ''' 
	from dic.word_idf import word_idf 
	from dic.word_awl import word_awl
	from cos_fastapi  import cos_lemma_keyness
	doc = spacy.nlp(text) 
	dic = { t.i: {'i':t.i, "head":t.head.i, 'off':t.idx, 'idf': word_idf.get(t.text.lower(), 0),'awl': 1 if t.text.lower() in word_awl else 0, 
		'keyness': cos_lemma_keyness(t.pos_, t.lemma_, sino, native) if t.pos_ in ('NOUN','VERB','ADJ','ADV') else 0 , 
		'lex':t.text, 'text_with_ws':t.text_with_ws, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, "gov":t.head.lemma_ + "_" + t.head.pos_ }  for t in doc}
	if chunks: 
		[v.update({"chunks":[]}) for k,v in dic.items()]
		[ dic[ sp.end - 1 ]['chunks'].append( {'lempos': doc[sp.end - 1].lemma_ + "_NOUN", "type":"NP", "chunk":sp.text.lower() } ) for sp in doc.noun_chunks]   ## start/end ? 
	return [ v for v in dic.values()]  # colored VERB html

@app.get("/nlp/terms", tags=["spacy"])
def nlp_terms(text:str="The quick fox jumped over the lazy dog. The justice delayed is justice denied."):
	''' for sqlite indexing, 2022.3.4 '''
	tdoc = spacy.nlp(text)
	arr = []
	for sent in tdoc.sents: 
		doc = sent.as_doc()
		arr.append( { "snt": sent.text, 
		"tokens": [ {"id": t.i,"offset":t.idx, "word": t.text, "lemma":t.lemma_, "is_stop":t.is_stop, "parent": -1, "np_root": False, "pos": t.pos_, "tag": t.tag_, "dep":
 t.dep_,"text_with_ws": t.text_with_ws, "head": t.head.i , "sent_start": t.is_sent_start, "sent_end":t.is_sent_end}  for t in doc], 
		"triples": [ {"id":t.i,"offset":t.idx, "rel": t.dep_, "govlem":t.head.lemma_, "govpos": t.head.pos_, "deplem": t.lemma_, "deppos": t.pos_} for t in doc], 
		"chunk": [ {"id": np.start, "offset": doc[np.start].idx, "lem": doc[np.end-1].lemma_, "chunk":np.text, "end":np.end} for np in doc.noun_chunks], 
		} )
	return arr 

@app.get("/nlp/sntbr", tags=["spacy"])
def nlp_sntbr(text:str="The quick fox jumped over the lazy dog. The justice delayed is justice denied.", trim:bool=True):
	'''  '''
	return spacy.snts(text, trim)

@app.get("/spacy/sntbr", tags=["spacy"])
def sntbr(text:str="The quick fox jumped over the lazy dog. The justice delayed is justice denied.", trim:bool=True, with_pid:bool=False):
	''' 2022.8.10 '''
	from spacy.lang import en
	if not hasattr(sntbr, 'inst'): 
		sntbr.inst = en.English()
		sntbr.inst.add_pipe("sentencizer")

	doc = sntbr.inst(text)
	if not with_pid: return [ snt.text.strip() if trim else snt.text for snt in  doc.sents]

	pid = 0 #spacy.sntpidoff	= lambda essay: (pid:=0, doc:=spacy.sntbr(essay), [ ( pid := pid + 1 if "\n" in snt.text else pid,  (snt.text, pid, doc[snt.start].idx))[-1] for snt in  doc.sents] )[-1]
	arr = []
	for snt in  doc.sents:
		if "\n" in snt.text: pid = pid + 1 
		arr.append( (snt.text, pid) ) 
	return arr 

@app.get("/spacy/wordidf", tags=["spacy"])
def nlp_wordidf(snt:str="The quick fox jumped over the lazy dog.", topk:int=3):
	'''  '''
	from dic.word_idf import word_idf 
	from collections import Counter
	doc = spacy.nlp(snt)
	si  = Counter()
	[  si.update({t.text.lower() : word_idf.get(t.text.lower(), 0)}) for t in doc ]
	return [{"word":w, "idf":idf} for w , idf in si.most_common(topk) if idf > 0  ]

@app.get("/spacy/lemma-idf", tags=["spacy"])
def nlp_lemma_idf(snt:str="The quick fox jumped over the lazy dog.", cutoff:float=1.5, topk:int=10):
	from dic.word_idf import word_idf 
	doc = spacy.nlp(snt)
	dic = {t.lemma_ : {"lemma":t.lemma_, "word":t.text, "idf": word_idf[t.lemma_], "pos":t.pos_, "tag":t.tag_ }   for t in doc if word_idf.get(t.lemma_,0) > cutoff }
	arr = [v for k, v in dic.items()]
	arr.sort(key=lambda a: a['idf'], reverse=True)
	return arr[0:topk]

@app.get("/spacy/ecdic", tags=["spacy"])
def nlp_ecdic(snt:str="The quick fox jumped over the lazy dog."):
	'''  '''
	from dic.ecdic import ecdic
	doc = spacy.nlp(snt)
	return [  { "word": t.lemma_, "trans": ecdic[t.lemma_]} for t in doc if not t.is_stop and t.lemma_ in ecdic ]

@app.get('/yulk/keyness', tags=["spacy"])  
def text_keyness(text="I think that I am going to go to the cinema. The quick fox jumped over the lazy dog.", topk:int=20):  
	''' 单词超用显著性 ''' 
	from dic.bnc_wordlist import bnc_keyness 
	doc = spacy.nlp(text) 
	si = Counter()
	[ si.update({t.lemma_:1}) for t in doc if not t.pos_ in ('PROPN','PUNCT') and not t.is_stop]
	res = bnc_keyness(dict(si), len(doc))
	res.sort(key=lambda x:x[-1], reverse=True)
	return res[0:topk]

@app.get('/yulk/vs/wordidf', tags=["spacy"]) 
def vs_wordidf(text0="I think that I am going to go to the cinema. The quick fox jumped over the lazy dog.", text1="The reality that has blocked my path to become the typical successful student is that engineering and the liberal arts simply don't mix as easily as I assured in hight school.",):  
	''' 单词难度对比 ''' 
	from dic.word_idf import word_idf
	wordidf = lambda txt:  (si := Counter(), [ si.update({word_idf[t.text.lower()]: 1}) for t in spacy.nlp(txt) if t.text.lower() in word_idf] )[0]
	si0 = wordidf(text0)
	si1 = wordidf(text1)
	return (si0, si1)

@app.post('/yulk/wordmap', tags=["spacy"]) 
def wordmap(snts:list=["I think that I am going to go to the cinema.","The quick fox jumped over the lazy dog."], poslist:str="VERB,NOUN,ADV,ADJ"):  
	''' 语义邻居 ''' 
	ssi = defaultdict(Counter)
	pos = poslist.strip().split(',')
	for snt in snts:
		doc = spacy.nlp(snt) 
		[ ssi[t.pos_].update({t.lemma_:1})  for t in doc if t.pos_ in pos]
	return ssi 

@app.get('/benepar/parse', tags=["spacy"]) 
def benepar_parse(snt:str="The quick fox jumped over the lazy dog."):
	''' '''
	import benepar
	if not hasattr(benepar_parse, 'parser'): 
		benepar_parse.parser = benepar.Parser("benepar_en3")
	tree = benepar_parse.parser.parse(snt)
	return HTMLResponse(content=str(tree))

if __name__ == "__main__":  
	#print (spacy_tok(morph=True))	
	#print ( doc_to_json(add_gov=True), flush=True) 
	print (nlp_lemma_idf())
	#uvicorn.run(app, host='0.0.0.0', port=80)

'''
@app.get("/spacy/ngram", tags=["spacy"])
def nlp_ngram( #dic:dict={ "pos_stop":{"PROPN","NUM"}, "tag_stop":{"NNP","CD"} }, 
			text:str="5 fox jumped over the lazy dog. The justice delayed is justice denied.",n:int=3, posstop:str="PROPN,NUM", tagstop:str="NNP,CD"):
	tdoc = spacy.nlp(text)
	res = []
	pos_stop = posstop.strip().split(',')
	tag_stop = tagstop.strip().split(',')
	for sent in tdoc.sents: 
		doc = sent.as_doc()
		for i in range(len(doc) - n + 1): 
			if [j for j in range(n) if doc[i+j].pos_ in pos_stop] or [j for j in range(n) if doc[i+j].tag_ in tag_stop]: 
				continue
			res.append({"text": " ".join([ doc[i+j].text for j in range(n)]).lower()
			, "pos": ",".join([ doc[i+j].pos_ for j in range(n)])
			, "tag": ",".join([ doc[i+j].tag_ for j in range(n)])
			, "morph": ",".join([ doc[i+j].morph.to_json() for j in range(n)])
			}) 
	return res 

spacy subjunctive mood
'''