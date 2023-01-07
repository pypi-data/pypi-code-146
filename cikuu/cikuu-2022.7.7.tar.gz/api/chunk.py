
def chunks(snt="The quick fox jumped over the lazy dog."):
	''' return spans: [The quick fox, jumped over the lazy dog, .] '''
	import benepar, spacy
	if not hasattr(chunks, 'nlp'):
		chunks.nlp = spacy.load('en_core_web_sm')
		chunks.nlp.add_pipe("benepar", config={"model": "benepar_en3"})
	doc = chunks.nlp(snt)
	sent = list(doc.sents)[0]
	return list(sent._.children)

def parse(snt="The quick fox jumped over the lazy dog.", merge_np= False):
	''' used in the notebook, for debug '''
	import pandas as pd
	import spacy
	if not hasattr(parse, 'sm'): parse.sm = spacy.load('en_core_web_sm')
	doc = parse.sm(snt) 
	return pd.DataFrame({'word': [t.text for t in doc], 'tag': [t.tag_ for t in doc],'pos': [t.pos_ for t in doc],'head': [t.head.orth_ for t in doc],'dep': [t.dep_ for t in doc], 'lemma': [t.text.lower() if t.lemma_ == '-PRON-' else t.lemma_ for t in doc],
	'n_lefts': [ t.n_lefts for t in doc], 'left_edge': [ t.left_edge.text for t in doc], 
	'n_rights': [ t.n_rights for t in doc], 'right_edge': [ t.right_edge.text for t in doc],
	'subtree': str([ list(t.subtree) for t in doc]),'children': str([ list(t.children) for t in doc]),
	'morph': [ t.morph for t in doc],
	}) 
		
if __name__	== '__main__': 
	print (parse())