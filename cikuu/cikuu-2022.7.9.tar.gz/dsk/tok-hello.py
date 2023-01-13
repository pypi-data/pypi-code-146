# 22-8-22
import requests

arr = requests.get("http://cpu76.wrask.com:8000/spacy/to_json", params={"text":"It is made in China. She has left."}).json()
# {'text': 'It is made in China.', 'ents': [{'start': 14, 'end': 19, 'label': 'GPE'}], 'sents': [{'start': 0, 'end': 20}], 'tokens': [
# {'id': 0, 'start': 0, 'end': 2, 'tag': 'PRP', 'pos': 'PRON', 'morph': 'Gender=Neut|Number=Sing|Person=3|PronType=Prs', 'lemma': 'it', 'dep': 'nsubjpass', 'head': 2}, 
# {'id': 1, 'start': 3, 'end': 5, 'tag': 'VBZ', 'pos': 'AUX', 'morph': 'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin', 'lemma': 'be', 'dep': 'auxpass', 'head': 2}, {'id': 2, 'start': 6, 'end': 10, 'tag': 'VBN', 'pos': 'VERB', 'morph': 'Aspect=Perf|Tense=Past|VerbForm=Part', 'lemma': 'make', 'dep': 'ROOT', 'head': 2}, {'id': 3, 'start': 11, 'end': 13, 'tag': 'IN', 'pos': 'ADP', 'morph': '', 'lemma': 'in', 'dep': 'prep', 'head': 2}, {'id': 4, 'start': 14, 'end': 19, 'tag': 'NNP', 'pos': 'PROPN', 'morph': 'Number=Sing', 'lemma': 'China', 'dep': 'pobj', 'head': 3}, {'id': 5, 'start': 19, 'end': 20, 'tag': '.', 'pos': 'PUNCT', 'morph': 'PunctType=Peri', 'lemma': '.', 'dep': 'punct', 'head': 2}]}

for tok in arr['tokens']: 
	if tok['tag'] == 'VBN': 
		print( {"type":"ctag", "ctag": "VBN", "start": tok['start'], "end": tok['end'], "text": arr['text'][tok['start']:tok['end']]} ) 

#simple_sent	= lambda doc:  len([t for t in doc if t.pos_ == 'VERB' and t.dep_ != 'ROOT']) <= 0 # else is complex sent 
#compound_snt	= lambda doc:  len([t for t in doc if t.dep_ == 'conj' and t.head.dep_ == 'ROOT']) > 0

def sents(arr): 
	''' '''
	text = arr['text'] 
	toks = arr['tokens'] 
	start_id = {}
	end_id = {}
	for i,ar in enumerate(toks):
		start_id [ ar['start']  ]  = i 
		end_id [ ar['end'] ] = i 
	
	return [ toks[ start_id[ snt['start']] : end_id[ snt['end']] + 1 ] for snt in arr['sents'] ]

def simple_snt( toks, start, end ):
	for i in range(start, end):
		if toks[i]['pos'] == 'VERB' and toks[i]['dep'] != 'ROOT' : return False 
	return True

def compound_snt(toks, start, end): 
	for i in range(start, end):
		if toks[i]['dep'] == 'conj' and toks[ toks[i]['head']  ]['dep'] == 'ROOT' : return True
	return False
