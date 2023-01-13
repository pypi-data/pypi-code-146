#2022.11.19  pip install scipy==1.7.0 -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
import gensim,json,math
import gensim.downloader as api
import numpy as np
from collections import Counter
from scipy import spatial
from dic import word_idf

model = api.load('glove-wiki-gigaword-300')
vec = lambda w, inner_sim_r: json.loads(inner_sim_r.get(f'word2vec:{w}')) #json.loads(r.get('word2vec:consider'))

def kw_similarity(kw0:dict={"apple":12, "orange":13}, kw1:dict={"table":1.4, "desk":1.5}): 
	''' { "kw0": {"apple":12, "orange":13}, "kw1": {"table":1.4, "desk":1.5} } , added 2021.12.11 '''
	ws0 = [w for w in kw0.keys()]
	ws1 = [w for w in kw1.keys()]
	sim0 = [  f * model.n_similarity([w], ws1).tolist()  for w,f in kw0.items()]
	sim1 = [  f * model.n_similarity([w], ws0).tolist()  for w,f in kw1.items()]
	return 0.5 * sum(sim0) / len(sim0) + 0.5 * sum(sim1) / len(sim1)

def sent_sim(): #https://www.tutorialexample.com/python-calculate-the-similarity-of-two-sentences-with-gensim-gensim-tutorial/
	sen_1_words = [w for w in sen_1.split() if w in model.vocab]
	sen_2_words = [w for w in sen_2.split() if w in model.vocab]
	sim = model.n_similarity(sen_1_words, sen_2_words)
	print(sim)

INNER_SIM_THRESHOLD = 0.7	# 分段计算的域值
INNER_SIM_FACTOR_GE = 0.4	# 最高关键词权重大于等于域值时的权重因子
INNER_SIM_FACTOR_LT = 1.5	# 最高关键词权重小于域值时的权重因子
INNER_SIM_SUM_MAX =1.2		# 相关度加权和的最大值，超过此值按此值计算

def norm_l1(items):
	s = sum([v for k,v in items])
	return [ (k,v/s) for k,v in items] if s > 0 else items

def norm_l2(items):
	s = math.sqrt(sum([(v * v) for k,v in items]))
	return [ (k,v/s) for k,v in items] if s > 0 else items

# 算法说明：
# 当最大关键词权重大于0.7时，直接认为相关，取0.4倍计算得分，最高0.4为100分，最低0.28对应88分
# 当最大关键词权重小于0.7时，考虑各关键词之间的相关性，若高相关则认为主题相关
# 计算时取各词与最高权重词相关度加权和为结果，计算得分
# 计算公式为：maxweight * sum(weight[i] * sim[i]) * factor
# 要求关键词权重为0.7时计算结果为0.7，即各相关度加权和为1，乘以最高权重0.7=0.7
# 理想情况下，各词与最高权重词相关度为1，各词权重平均为sqrt((1-0.7*0.7)/31)=0.12826
# 最大计算结果为31*1*0.12826=3.9762
# 以此算要求加权和除4为最终结果。
# 考虑到各词相关度很难为1，加之试验结果，w2v的相关度加权和最大值不超过2，因此取经验值1，factor=1/1=1
# 对于一些w2v里没有的词如e-book，可以通过数据库表word_sim加以维护
def innersim(skw, inner_sim_r): #[(key, weight)]形式的列表 	#skw = sorted(keyswords.items(), key=lambda kw: kw[1], reverse = True)
	#skw = kw(ess)
	if skw[0][1] >= INNER_SIM_THRESHOLD:
		return skw[0][1] * INNER_SIM_FACTOR_GE
	sim = internal_sim_w2v(skw, inner_sim_r)
	return sim * INNER_SIM_FACTOR_LT

# 使用word2vec，计算列表中的第idx个元素和后面3个权重最大的元素的相似度之和
def internal_sim_w2v(keywords, inner_sim_r):
	for i in range(len(keywords)):
		if not inner_sim_r.exists(f'word2vec:{keywords[i][0]}'): #keywords[i][0] not in word2vec:
			#print("skip %s for not exists\n" % (keywords[i][0]))
			continue
		sum = 0
		num = 0
		for j in range(i+1, len(keywords)):
			if not inner_sim_r.exists(f'word2vec:{keywords[j][0]}'): #keywords[j][0] not in word2vec:
				continue

			sim = 1 - abs(spatial.distance.cosine(vec(keywords[i][0],inner_sim_r), vec(keywords[j][0],inner_sim_r)))
			if sim > 1e-4:
				sum = sum + keywords[j][1] * sim
				#print("sim of %s and %s is %.4f, sum=%.4f" %(keywords[i][0], keywords[j][0], sim, sum))
				num = num+1
				if num > 3:
					break
		if num > 0:
			if sum > INNER_SIM_SUM_MAX:
				sum = INNER_SIM_SUM_MAX
			return sum * keywords[i][1]
	return 0

def docs_kw(docs, topn=32): 
	''' input: spacy docs '''
	si = Counter()
	[si.update({t.lemma_:1}) for doc in docs for t in doc if t.pos_ in ('VERB', 'NONE', 'PROPN', 'NUM', 'ADJ', 'ADV') and not t.is_stop]
	tfidf = Counter({ w: c * word_idf[w] for w,c in si.items() if w in word_idf}) #i = IDF_UNHITTED # 如果没有其它办法，可以用是否被idf收录判断是否是拼写错误
	skw = norm_l2( tfidf.most_common(topn))
	return skw 	

def get_kw(snts, key=None, topn=32): #topn = essay.get('topkw', 32)

	if key: 
		kw = redis.dsk.zrevrange(f"{key}:kw",0,-1,True)
		if kw: return kw

	si = Counter()
	[si.update({t.lemma_:1}) for snt in snts for t in spacy.getdoc(snt) if t.pos_ in ('VERB', 'NONE', 'PROPN', 'NUM', 'ADJ', 'ADV') and not t.is_stop]
	tfidf = Counter({ w: c * word_idf[w] for w,c in si.items() if w in word_idf}) #i = IDF_UNHITTED # 如果没有其它办法，可以用是否被idf收录判断是否是拼写错误
	#tfidf_sort = sorted(tfidf.items(), key=lambda x:x[1], reverse=True)[0:topn]
	skw = norm_l2( tfidf.most_common(topn))
	if key: redis.dsk.zadd(f"{key}:kw", dict(skw))
	return skw 	

def get_sim(sorted_kw, key=None) : # 

	if key: 
		sim = redis.dsk.zscore(f"{key}:dim", "sim")
		if sim: return sim 

	sim = innersim(sorted_kw, redis.dic)
	if key: redis.dsk.zadd(f"{key}:dim", {"sim":sim})
	return sim 

if __name__ == '__main__':
	kw1 = {"niche":0.23, "apple":0.25}
	kw2 = {"orange":0.22, "film":0.15, "close":0.07}
	print ( kw_similarity()) 

'''
	tf = {}
	for snt in snts: #for doc in ess['docs']:
		doc = spacy.getdoc(snt)
		for token in doc:
			if token.pos_ in ('VERB', 'NONE', 'PROPN', 'NUM', 'ADJ', 'ADV') and not token.is_stop:
				w = token.lemma_.lower() # 要过滤掉拼写错误的单词
				if w in tf:
					tf[w] += 1
				else:
					tf[w] = 1

	skw = redis.dsk.zrevrange(f"{key}:kw",0,-1,True)
	if not kw: 
		skw = kw(snts) 
		redis.dsk.zadd(f"{key}:kw", dict(skw))

>>> import gensim
>>> import gensim.downloader as api
>>> model = api.load('glove-wiki-gigaword-300')
model['niche'].tolist() 
model.similarity(w1, w2)  , -0.12
'''