#2022.8.18  https://segmentfault.com/a/1190000017825534 # 2022.2.9 https://github.com/flairNLP/flair/blob/master/resources/docs/TUTORIAL_2_TAGGING.md
from uvirun import *

@app.get('/flair/frame/snt')
def frame_snt(snt:str="He had a look at different hats."):    
	''' He had <have.LV> a look <look.01> at different hats .   https://github.com/flairNLP/flair/blob/master/resources/docs/TUTORIAL_2_TAGGING.md '''
	from flair.data import Sentence
	from flair.models import SequenceTagger
	if not hasattr(frame_snt, 'tagger'):  frame_snt.tagger = SequenceTagger.load('frame-fast')  # 115M 
	sentence_1 = Sentence(snt)
	frame_snt.tagger.predict(sentence_1)
	#return sentence_1.to_tagged_string()
	return sentence_1.to_dict() #{'text': 'He had a look at different hats.', 'all labels': [{'value': 'have.03', 'confidence': 0.8889056444168091}, {'value': 'look.01', 'confidence': 0.9819096326828003}]}

@app.post('/flair/frame/snts')
def frame_snts(snts:list=["George returned to Berlin to return his hat.","He had a look at different hats."]):  
	''' ["George returned to Berlin to return his hat.","He had a look at different hats."]	'''
	return { snt: frame_snt(snt) for snt in snts }

def walk(index, type:str='snt', eshost:str='es.corpusly.com:9200'):
	''' 2022.8.22 '''
	import requests 
	print ('start to walk:', index, flush=True)
	cursor=''
	while True : 
		res = requests.post(f"http://{eshost}/_sql", json={"query":f"select src, snt from {index} where type='{type}'", "cursor":cursor}).json() 
		for src, snt in  res.get('rows',[]):
			frames  = [ ar['value'] for ar in frame_snt(snt).get('all labels',[]) ] 
			if not frames: continue
			requests.put(f"http://{eshost}/{index}/_doc/{src}-frame", json={"frame": frames, "type":"frame", "src":src}).text
		cursor = res.get('cursor','') 
		if not cursor: break
	print ('finished walking:', index, flush=True)

if __name__ == '__main__': # read 'snt' from es,  parse , and submit back to ES, with type='frame' 
	import fire
	fire.Fire({"walk":walk, "hello": frame_snt})

@app.get('/flair/sentiment')
def classify_sentiment(snt:str="He had a look at different hats."): 
	''' 2022.2.18 '''
	from flair.models import TextClassifier
	from flair.data import Sentence
	if not hasattr(classify_sentiment, 'sentiment'): 
		classify_sentiment.sentiment = TextClassifier.load("sentiment-fast") 
	sentence = Sentence(snt)
	classify_sentiment.sentiment.predict(sentence)
	return sentence.labels[0] 

@app.post('/flair/sentiment/snts')
def classify_sentiment_snts(snts:list=["He had a look at different hats.","I am too tired to move on."]): 
	''' ["He had a look at different hats.","I am too tired to move on."] '''
	return { snt: classify_sentiment(snt) for snt in snts}

'''
https://www.geeksforgeeks.org/flair-a-framework-for-nlp/#:~:text=The%20Flair%20Embedding%20is%20based%20on%20the%20concept,better%20results.%20Flair%20supports%20a%20number%20of%20languages.
[
  {
    "_value": "sci",
    "_score": 0.9978132247924805
  }
]
2022-02-19 20:14:21,967 loading file /models/flair-sci-twit.pt
2022-02-19 20:14:28,579 loading file /home/ubuntu/.flair/models/sentiment-en-mix-ft-rnn_v8.pt

>>> s.get_spans()
[<have.03-span (2): "had">, <look.01-span (4): "look">]

# iterate and print
for entity in s.get_spans('ner'):
    print(entity)

>>> spans[0].text
'had'
>>> spans[0].tag
'have.03'
>>> spans[0].to_dict()
{'text': 'had', 'start_pos': 3, 'end_pos': 6, 'labels': [have.03 (0.8889)]}

>>> spans[0].labels[0].to_dict()
{'value': 'have.03', 'confidence': 0.8889056444168091}
>>> spans[0].labels[0].value
'have.03'
'''