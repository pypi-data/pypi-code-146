# 2022.6.30  pip install https://github.com/kpu/kenlm/archive/master.zip
from uvirun import *
import math

def _model(name:str="nyt5"): 
	import kenlm
	if not hasattr(_model, name):  
		c = kenlm.Config() 
		c.load_method = kenlm.LoadMethod.LAZY
		setattr(_model, name, kenlm.Model( f"/data/model/kenlm/{name}.bin", c) )
	return getattr(_model, name)

kenlm_flue	= lambda snt, model : 1.0/(1.0+ math.log10(model.perplexity(snt))) #getao
sntadd		= lambda snt,idx,w : " ".join([lex if i != idx else f"{w} {lex}" for lex, i in zip(snt.split(), range( snt.count(' ') + 1))])
sntrep		= lambda snt,idx,w : " ".join([lex if i != idx else w for lex, i in zip(snt.split(), range( snt.count(' ') + 1))])
sntdel		= lambda snt,idx : " ".join([lex for lex, i in zip(snt.split(), range( snt.count(' ') + 1)) if i != idx])
flue_add	= lambda snt,widx,w, model : round(kenlm_flue(sntadd(snt,widx, w), model) / kenlm_flue(snt,model), 4)
flue_rep	= lambda snt,widx,w, model : round(kenlm_flue(sntrep(snt,widx, w), model) / kenlm_flue(snt,model), 4)
flue_del	= lambda snt,widx, model : round(kenlm_flue(sntdel(snt,widx), model) / kenlm_flue(snt,model), 4)

@app.get('/kenlm/flue', tags=["kenlm"])
def get_kenlm_flue(snt:str="I love you|I like you",name:str="nyt5", sepa:str="|"): 
	model = _model(name)
	return [ {"snt": s, "flue": round(kenlm_flue(s, model), 4)} for s in snt.strip().split(sepa)]

@app.get('/kenlm/flue/single', tags=["kenlm"])
def kenlm_flue_single(body:str="Parents * much importance to education.", star:str='*', options:str="attach,pay,link,apply", sepa:str=",", name:str='nyt5', asrows:bool=False): 
	'''  2022.8.6 '''
	model = _model(name)
	rows  = [   (option, round(kenlm_flue(body.replace(star, option), model), 4) )  for option in options.strip().split(sepa) ] 
	return rows if asrows else [  {"word":row[0], "flue": row[1] }  for row in rows ]

@app.get('/kenlm/score', tags=["kenlm"])
def kenlm_snt_score(snt:str="I love you|I like you", name:str="nyt5", sepa:str="|", fullscore:bool=False): 
	''' name: zkenlm/nyt5 '''
	model = _model(name) 
	return [ {"snt": s, "score": round(model.score(s), 4)} for s in snt.strip().split(sepa)] if not fullscore else [ {"snt": s, "score": model.full_scores(s)} for s in snt.strip().split(sepa)]

@app.get('/kenlm/ppl', tags=["kenlm"])
def get_kenlm_ppl(snt:str="I love you|I like you", name:str="nyt5", sepa:str="|"): 
	model = _model(name)
	return [ {"snt": s, "ppl": round(model.perplexity(s), 4)} for s in snt.strip().split(sepa)]

@app.get('/kenlm/flueadd', tags=["kenlm"]) 
def flueadd(snt:str="I love you", wordidx:int=0, word:str='',name:str="nyt5"): 
	return flue_add(snt, wordidx, word, _model(name)) 

@app.get('/kenlm/fluerep', tags=["kenlm"])
def fluerep(snt:str="I love you", wordidx:int=0, word:str='',name:str="nyt5"):
	return flue_rep(snt, wordidx, word, _model(name)) 

@app.get('/kenlm/fluedel', tags=["kenlm"])
def fluedel(snt:str="I love you", wordidx:int=0, name:str="nyt5"): 
	return flue_del(snt, wordidx, _model(name))

if __name__ == '__main__':
	print ( kenlm_flue_single(asrows=True)) 
	#uvicorn.run(app, host='0.0.0.0', port=80)

'''
files = [file for file in os.listdir(f"/model") if file.endswith(".trie") or file.endswith(".klm") or file.endswith(".bin") or file.endswith(".kenlm")]
# 2020-2-21 | docker run -it -e VIRTUAL_HOST=cclm.werror.com --rm --name cclm -p 8889:80 -v /home/cikuu/model/cclm:/model wrask/kenlm
'''