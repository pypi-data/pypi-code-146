# 2022.7.27
import json, traceback,sys, time,  fileinput, os #https://docs.python.org/3/library/fileinput.html

def walk(infile): 
	''' gzjc.json340.gz '''
	for line in fileinput.input(infile,openhook=fileinput.hook_compressed): 
		print (line) 

def tosnt(infile): 
	''' gzjc.json341.gz => gzjc.snt '''
	for line in fileinput.input(infile,openhook=fileinput.hook_compressed): 
		print (json.loads(line).get('text',''))

def todsk(infile): 
	''' gzjc.json341.gz => gzjc.dsk '''
	import requests
	for line in fileinput.input(infile,openhook=fileinput.hook_compressed): 
		arr = json.loads(line)
		text = arr.get('text','')
		if not text: continue
		arr['dsk'] = requests.post("http://gpu120.wrask.com:8180/gecdsk", json={"essay_or_snts":text}).json() 
		print (json.dumps(arr)) 

def tojson(infile, outfile=None, model:str="lg"):
	''' gzjc.snt => gzjc.jsonlg.3.4.1 '''
	import spacy 
	nlp =spacy.load(f'en_core_web_{model}')
	if outfile is None: outfile = infile.split('.')[0] + f".json{model}." + spacy.__version__
	print ("started:", infile ,  ' -> ',  outfile, flush=True)
	with open(outfile, 'w') as fw: 
		for line in fileinput.input(infile):
			doc = nlp(line.strip().split('\t')[-1].strip()) 
			res = doc.to_json() 
			fw.write( json.dumps(res) + "\n")
	os.system(f"gzip -f -9 {outfile}")
	print ("finished:", infile, outfile ) 

def todocjson(infile, outfile=None, model:str="lg", key:str="doc_txt"):
	''' spider.docjson => spider.jsonlg.3.4.1 , 2022.8.2'''
	import spacy 
	nlp =spacy.load(f'en_core_web_{model}')
	if outfile is None: outfile = infile.split('.')[0] + f".docjson{model}." + spacy.__version__
	print ("started:", infile ,  ' -> ',  outfile, flush=True)
	with open(outfile, 'w') as fw: 
		for line in fileinput.input(infile,openhook=fileinput.hook_compressed): #for line in fileinput.input(infile):
			try:
				arr = json.loads(line.strip())
				essay = arr.get(key, '')
				if not essay: continue 
				doc = nlp(essay) 
				res = doc.to_json() 
				res['info'] = arr 
				fw.write( json.dumps(res) + "\n")
			except Exception as e:
				print ("ex:", e, line) 
	os.system(f"gzip -f -9 {outfile}")
	print ("finished:", infile, outfile ) 

def c4data(infile, model:str="lg"):
	''' train c4data | {"text":"Click here to find out how far it is to Cobram Victoria AUSTRALIA.\nhow far is it to Cobram Victoria AUSTRALIA?\nTell me about travel to Cobram Victoria AUSTRALIA. I could probably use a hotel or a local tour of Cobram.\nIs ther
e anywhere to hire a car in Cobram?\nI would also be interested in places to eat in Cobram Victoria AUSTRALIA.","timestamp":"2019-04-22T07:58:03Z","url":"https://www.how-far-is-it.com/how-far-is/australia/how-far-is-it-to-cobram-victoria
-australia.htm"}'''
	import spacy 
	nlp =spacy.load(f'en_core_web_{model}')
	outfile = infile.split('.json')[0] + f".docjson{model}." + spacy.__version__
	if os.path.exists( outfile + f".gz") : return 
	print ("started:", infile ,  ' -> ',  outfile, flush=True)
	with open(outfile, 'w') as fw: 
		for line in fileinput.input(infile,openhook=fileinput.hook_compressed): 
			try:
				arr = json.loads(line.strip())
				essay = arr.get("text", '')
				if not essay: continue 
				doc = nlp(essay) 
				res = doc.to_json() 
				res['info'] = {"tm": arr.get("timestamp",""), "url":arr.get('url','')}
				fw.write( json.dumps(res) + "\n")
			except Exception as e:
				print ("ex:", e, line) 
	os.system(f"gzip -f -9 {outfile}")
	print ("finished:", infile, outfile ) 

def c4postag(infile, model:str="lg"):
	''' docjson -> postag (es foramt), 2022.8.7 '''
	import spacy 
	nlp =spacy.load(f'en_core_web_{model}')
	outfile = infile.split('.docjson')[0] + f".postag"
	print ("started:", infile ,  ' -> ',  outfile, flush=True)
	with open(outfile, 'w') as fw: 
		for line in fileinput.input(infile,openhook=fileinput.hook_compressed): 
			try:
				arr = json.loads(line.strip())
				doc = from_json(arr) # word = .text[start:end)
				#res['info'] = {"tm": arr.get("timestamp",""), "url":arr.get('url','')}
				postag = "^ " + ' '.join([f"{t.text}_{t.lemma_}_{t.pos_}_{t.tag_}" if t.text == t.text.lower() else f"{t.text}_{t.text.lower()}_{t.lemma_}_{t.pos_}_{t.tag_}" for t in doc]) 
				res = {'postag': postag, 'tms': arr['info']['tm'], 'url': arr['info']['url']}
				fw.write( json.dumps(res) + "\n")
			except Exception as e:
				print ("ex:", e, line) 
	os.system(f"gzip -f -9 {outfile}")
	print ("finished:", infile, outfile ) 


if __name__	== '__main__':
	import fire 
	fire.Fire()

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