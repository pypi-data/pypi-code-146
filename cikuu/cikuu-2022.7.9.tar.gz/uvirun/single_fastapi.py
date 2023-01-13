# 2022.8.29  
from uvirun import *

@app.post('/single', tags=["single"])
def single(options:list=["attach","link","pay","apply"], body:str='Parents * much importance to education.'): 
	''' 2022.8.29 '''
	import spacy
	from collections import Counter
	if not hasattr(single, 'nlp'):	single.nlp = spacy.load('en_core_web_sm')
	si = Counter()

if __name__ == "__main__":  
	print (single())