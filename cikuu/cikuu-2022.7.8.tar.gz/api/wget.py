# 2022.9.2 
import time, requests ,json, platform,os,re,builtins
from collections import Counter,defaultdict
apihost	= os.getenv('apihost', 'cpu76.wrask.com:8000')

def cloze(snt:str="The quick fox * over the lazy dog.", model:str='native', topk:int=10):
	''' [{name,word,score}] '''
	#http://cpu76.wrask.com:8000/unmasker?q=The%20goal%20of%20life%20is%20%2A.&model=native&topk=10&verbose=false
	return requests.get(f"http://{apihost}/unmasker", params={"q":snt, "model":model, "topk":topk}).json()

def gramcnt(q:str="overcome difficulty,overcame difficulty,overcame difficulty***", sepa:str=','):
	''' [{name,word,score}] '''
	return requests.get(f"http://{apihost}/gramx/grams", params={"grams":q, "sepa":sepa}).json()
	#http://cpu76.wrask.com:8000/gramx/grams?grams=overcome%20difficulty%2Covercame%20difficulty%2Covercame%20difficulty%2A%2A%2A&sepa=%2C

def cola(snt:str="I love you."):
	''' cola '''
	return requests.get(f"http://{apihost}/cola", params={"snt":snt}).json()[0]['cola'] #http://cpu76.wrask.com:8000/cola?snt=I%20love%20you.&host=172.17.0.1%3A8003

def semdis(cands:str="orange/banana", given:str="apple", sepa:str='/'): 
	''' 2022.1.5 ''' 
	return requests.post(f'http://hw6.jukuu.com:8002/gensim/distance/words?src={given}', json=cands.strip().split(sepa)).json() 

if __name__	== '__main__': 
	print (semdis())