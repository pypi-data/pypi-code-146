# 2022.12.31
import json, traceback,sys, time, fire,os,traceback,fileinput,en, pymysql
from spacy.matcher import Matcher,DependencyMatcher
matcher = DependencyMatcher(spacy.nlp.vocab)
pattern = {
# be thrilled , worried, 
"advcl-acomp": [ {"RIGHT_ID": "v", "RIGHT_ATTRS": {"POS": "VERB"}},  { "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "advcl", "RIGHT_ATTRS": {"DEP": "advcl"} }, { "LEFT_ID": "advcl", "REL_OP": ">","RIGHT_ID": "object", "RIGHT_ATTRS": {"DEP": "acomp"} }] , 
"nsubj-acomp": [ { "RIGHT_ID": "v",   "RIGHT_ATTRS": {"POS": "VERB"}},{ "LEFT_ID": "v", "REL_OP":">", "RIGHT_ID": "subject", "RIGHT_ATTRS": {"DEP": "nsubj"} }, {  "LEFT_ID": "v", "REL_OP": ">",  "RIGHT_ID": "object",    "RIGHT_ATTRS": {"DEP": "acomp"}}], 
#She is  a girl.
"nsubj-attr": [  {"RIGHT_ID": "v", "RIGHT_ATTRS": {"LEMMA": "be"}}, { "LEFT_ID": "v", "REL_OP": ">","RIGHT_ID": "subject", "RIGHT_ATTRS": {"DEP": "nsubj"} }, {    "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "object", "RIGHT_ATTRS": {"DEP": "attr"} }],
# plan to go , enjoy swimming 
"nsubj-xcomp": [  {"RIGHT_ID": "v", "RIGHT_ATTRS": {"POS": "VERB"}},{"LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "subject", "RIGHT_ATTRS": {"DEP": "nsubj"} }, { "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "object",  "RIGHT_ATTRS": {"DEP": "xcomp"} }],
"xcomp-to": [  {"RIGHT_ID": "v", "RIGHT_ATTRS": {"POS": "VERB"}}, { "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "object",  "RIGHT_ATTRS": {"DEP": "xcomp"} }, {"LEFT_ID": "object", "REL_OP": ";", "RIGHT_ID": "to", "RIGHT_ATTRS": {"LEMMA": "to"} },],
# turn off the light
"prt-dobj": [  {"RIGHT_ID": "v","RIGHT_ATTRS": {"POS": "VERB"}},  { "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "subject", "RIGHT_ATTRS": {"DEP": "prt"} }, { "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "object", "RIGHT_ATTRS": {"DEP": "dobj"} }],
# be happy with
"acomp-prep":[ {"RIGHT_ID": "v","RIGHT_ATTRS": {"POS": "VERB"}}, { "LEFT_ID": "v","REL_OP": ">","RIGHT_ID": "acomp","RIGHT_ATTRS": {"DEP": "acomp"}},{  "LEFT_ID": "acomp", "REL_OP": ">", "RIGHT_ID": "prep", "RIGHT_ATTRS": {"DEP": "prep"}}],
# be based on
"be-vbn-prep":[ {"RIGHT_ID": "v", "RIGHT_ATTRS": {"TAG": "VBN"}}, {"LEFT_ID": "v", "REL_OP": ">","RIGHT_ID": "be","RIGHT_ATTRS": {"LEMMA": "be"} }, { "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "prep", "RIGHT_ATTRS": {"DEP": "prep"}  }],
}

for name,pat in pattern.items(): matcher.add(name, [pat])

def test():
	doc = spacy.nlp("While I was thrilled that he was an animal lover, I worried that three dogs were perhaps too many.")
	for name, ar in matcher(doc) : 
		print(spacy.nlp.vocab[name].text, doc[ar[0]].lemma_, doc[ar[1]].lemma_, doc[ar[2]]) # worry be thrilled

def run(infile):
	'''  '''
	name = infile.split('.jsonlg')[0] 
	print ("started :" ,infile, flush=True)
	with open (f"{name}.trpx", "w") as fw: 
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)):  #for rowid, snt, doc in tqdm(Spacybs(dbfile).docs()) :
			try:
				arr = json.loads(line.strip()) 
				doc = spacy.from_json(arr)  #for sid, sp in enumerate(tdoc.sents):				doc = sp.as_doc()
				for name, ar in matcher(doc) : 
					fw.write(spacy.nlp.vocab[name].text +":" + doc[ar[0]].lemma_ +":" + doc[ar[1]].lemma_ + ":" + doc[ar[2]].lemma_ + "\n")
			except Exception as e: 
				print ("ex:", e, sid,line)
				exc_type, exc_value, exc_traceback_obj = sys.exc_info()
				traceback.print_tb(exc_traceback_obj)
	print ("finished :" ,infile, flush=True)

if __name__	== '__main__':
	fire.Fire(run)

'''
dep = new_depmatcher([ 
  {
    "RIGHT_ID": "v",
    "RIGHT_ATTRS": {"POS": "VERB"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "advcl",
    "RIGHT_ATTRS": {"DEP": "advcl"}
  },
  {
    "LEFT_ID": "advcl",
    "REL_OP": ">",
    "RIGHT_ID": "object",
    "RIGHT_ATTRS": {"DEP": "acomp"}
  }
])

def new_depmatcher(pattern, name='advcl:acomp'):
	matcher.add(name, [pattern])
	return matcher
'''