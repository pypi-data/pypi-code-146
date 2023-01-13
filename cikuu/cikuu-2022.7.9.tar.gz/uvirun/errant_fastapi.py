#coding:utf-8 2022.3.10  pip install Levenshtein -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
from uvirun import *
import sys,traceback

errant_filter = {"R:SPELL":"t.tag_ not in ('NNP','NNPS')"} #R:SPELL=NNP -> t.tag_ not in ('NNP','NNPS') |   A and B , in one unit
errant_type = {
"M:DET":"{ 'error': '冠词缺失', 'short_msg':f'建议添加冠词<b>{edit.c_str}</b>'}",
"R:ADV":"{ 'error': '副词误用', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"M:NOUN:POSS":"{ 'error': '名词所有格缺失', 'short_msg':f'建议添加名词所有格<b>{edit.c_str}</b>'}",
"M:PREP":"{ 'error': '介词缺失', 'short_msg':f'建议添加介词<b>{edit.c_str}</b>'}",
"R:PRON":"{ 'error': '代词误用', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"UNK":"{ 'error': '未知错误', 'short_msg':f'检测到但未修正错误'}",
"R:VERB:SVA":"{ 'error': '主谓不一致', 'short_msg':f'请检查动词<b>{edit.o_str}</b>形态'}",
"R:ADJ":"{ 'error': '形容词误用', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"M:CONTR":"{ 'error': '缩略形式缺失', 'short_msg':f'建议添加缩略形式<b>{edit.c_str}</b>'}",
"R:ADJ:FORM":"{ 'error': '形容词形式错误', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"M:VERB:TENSE":"{ 'error': '动词时态缺失', 'short_msg':f'建议添加动词时态<b>{edit.c_str}</b>'}",
"R:DET":"{ 'error': '冠词误用', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"U:VERB:TENSE":"{ 'error': '动词时态多余', 'short_msg':f'动词时态<b>{edit.o_str}</b>疑似多余'}",
"R:NOUN":"{ 'error': '名词误用', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"R:NOUN:POSS":"{ 'error': '名词所有格误用', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"R:VERB:TENSE":"{ 'error': '动词时态误用', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"U:VERB:FORM":"{ 'error': '动词形式多余', 'short_msg':f'动词形式<b>{edit.o_str}</b>疑似多余'}",
"U:PUNCT":"{ 'error': '标点符号多余', 'short_msg':f'标点符号<b>{edit.o_str}</b>疑似多余'}",
"U:NOUN":"{ 'error': '名词多余', 'short_msg':f'名词<b>{edit.o_str}</b>疑似多余'}",
"R:ORTH":"{ 'error': '大小写/或空格错误', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"R:NOUN:INFL":"{ 'error': '名词词形变化错误', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"R:NOUN:NUM":"{ 'error': '名词单复数错误', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"M:CONJ":"{ 'error': '连词缺失', 'short_msg':f'建议添加连词<b>{edit.c_str}</b>'}",
"R:VERB":"{ 'error': '动词误用', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"M:PRON":"{ 'error': '代词缺失', 'short_msg':f'建议添加代词<b>{edit.c_str}</b>'}",
"M:NOUN":"{ 'error': '名词缺失', 'short_msg':f'建议添加名词<b>{edit.c_str}</b>'}",
"M:ADV":"{ 'error': '副词缺失', 'short_msg':f'建议添加副词<b>{edit.c_str}</b>'}",
"U:CONJ":"{ 'error': '连词多余', 'short_msg':f'连词<b>{edit.o_str}</b>疑似多余'}",
"R:PUNCT":"{ 'error': '标点符号误用', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"U:ADV":"{ 'error': '副词多余', 'short_msg':f'副词<b>{edit.o_str}</b>疑似多余'}",
"R:CONTR":"{ 'error': '缩略形式错误', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"U:PREP":"{ 'error': '介词多余', 'short_msg':f'介词<b>{edit.o_str}</b>疑似多余'}",
"U:DET":"{ 'error': '冠词多余', 'short_msg':f'冠词<b>{edit.o_str}</b>疑似多余'}",
"M:VERB:FORM":"{ 'error': '动词形式缺失', 'short_msg':f'建议添加动词形式<b>{edit.c_str}</b>'}",
"M:ADJ":"{ 'error': '形容词缺失', 'short_msg':f'建议添加形容词<b>{edit.c_str}</b>'}",
"M:VERB":"{ 'error': '动词缺失', 'short_msg':f'建议添加动词<b>{edit.c_str}</b>'}",
"U:CONTR":"{ 'error': '缩略形式多余', 'short_msg':f'缩略形式<b>{edit.o_str}</b>疑似多余'}",
"U:VERB":"{ 'error': '动词多余', 'short_msg':f'动词<b>{edit.o_str}</b>疑似多余'}",
"U:PART":"{ 'error': '与动词构成短语动词的副词或介词多余', 'short_msg':f'与动词构成短语动词的副词或介词<b>{edit.o_str}</b>疑似多余'}",
"R:OTHER":"{ 'error': '单词误用', 'short_msg':f'建议修改为<b>{edit.c_str}</b>'}",
"U:NOUN:POSS":"{ 'error': '名词所有格多余', 'short_msg':f'名词所有格<b>{edit.o_str}</b>疑似多余'}",
"R:WO":"{ 'error': '语序错误', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"R:PREP":"{ 'error': '介词误用', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"R:VERB:INFL":"{ 'error': '动词词形变化错误', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"U:PRON":"{ 'error': '代词多余', 'short_msg':f'代词<b>{edit.o_str}</b>疑似多余'}",
"R:CONJ":"{ 'error': '连词误用', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"R:SPELL":"{ 'error': '拼写错误', 'short_msg':f'请检查<b>{edit.o_str}</b>拼写'}",
"R:PART":"{ 'error': '与动词构成短语动词的副词或介词误用', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"U:SPACE":"{ 'error': '空格多余', 'short_msg':f'建议删除空格'}",
"U:OTHER":"{ 'error': '单词冗余', 'short_msg':f'建议删除<b>{edit.o_str} </b>'}",
"R:MORPH":"{ 'error': '词性误用', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"R:VERB:FORM":"{ 'error': '动词形式误用', 'short_msg':f'建议<b>{edit.o_str}</b>修改为<b>{edit.c_str}</b>'}",
"M:OTHER":"{ 'error': '单词缺失', 'short_msg':f'建议添加<b>{edit.c_str}</b>'}",
"U:ADJ":"{ 'error': '形容词多余', 'short_msg':f'形容词<b>{edit.o_str}</b>疑似多余'}",
"M:PART":"{ 'error': '与动词构成短语动词的副词或介词缺失', 'short_msg':f'建议添加与动词构成短语动词的副词或介词<b>{edit.c_str}</b>'}",
"M:PUNCT":"{ 'error': '标点符号缺失', 'short_msg':f'建议添加标点符号<b>{edit.c_str}</b>'}",
}

def pass_filter(doc, edit): # R:SPELL=NNP -> t.tag_ not in ('NNP','NNPS')
	try:
		code =  errant_filter.get(edit.type, "True" ) 
		return eval ( code, {'doc': doc, 't': doc[edit.o_start]} )
	except Exception as e:
		print("pass_filter ex:", e, edit)
	return False # ?

def doc_edit(doc, edit):
	op = 's' if edit.type.startswith("R:") else 'i' if edit.type.startswith("M:") else 'd' if edit.type.startswith("U:") else 'x' #missed, unnecessay
	hit =  {'op': op, 'offset': doc[edit.o_start].idx, 'ibeg':edit.o_start,'word_list':edit.o_str, 'kp':edit.o_str, 'correct':edit.c_str, 'cate': edit.type, 'error': edit.type, 'short_msg':f'Please check <b>{edit.o_str}</b>',}
	try:
		cate_msg = errant_type.get(edit.type,'{}') 
		hit.update( eval( cate_msg, {'doc':doc, 'hit':hit, 'edit':edit})   )
	except Exception as e:
		print("from_edit ex:", e, hit)
	return hit

doc_edits = lambda doc, tdoc: [ doc_edit(doc, edit) for edit in gec_errant.annotator.annotate(doc, tdoc) if edit.o_start >= 0 and pass_filter(doc, edit)] 

@app.post('/gec/errant', tags=["gec"])
def gec_errant(pairs:dict={"She has ready.":"She is ready.", "It are ok.":"It is ok."}): 
	''' [{'snt': 'She has ready.', 'tgt': 'She is ready.', 'edits': [{'op': 's', 'position': 4, 'ibeg': 1, 'word_list': 'has', 'kp': 'has', 'correct': 'is', 'cate': 'R:VERB', 'error': '动词误用', 'short_msg': '建议<b>has</b>修改为<b>is</b>'}]}, {'snt': 'It are ok.', 'tgt': 'It is ok', 'edits': [{'op': 's', 'position': 3, 'ibeg': 1, 'word_list': 'are', 'kp': 'are', 'correct': 'is', 'cate': 'R:VERB:SVA', 'error': '主谓不一致', 'short_msg': '请检查动词<b>are</b>形态'}, {'op': 'd', 'position': 9, 'ibeg': 3, 'word_list': '.', 'kp': '.', 'correct': '', 'cate': 'U:PUNCT', 'error': '标点符号多余', 'short_msg': '标点符号<b>.</b>疑似多余'}]}] '''
	import spacy, errant # 2020-9-10 #https://github.com/chrisjbryant/errant
	if not hasattr(gec_errant, 'nlp'): 
		gec_errant.nlp = spacy.load('en_core_web_sm')
		gec_errant.annotator = errant.load('en', gec_errant.nlp)
	return [ {"snt": snt, "tgt": tgt,  "edits": doc_edits(gec_errant.nlp(snt), gec_errant.nlp(tgt))} for snt, tgt in pairs.items() ]

#from maperrs import doc_edits
@app.get('/errant', tags=["gec"])
def xgec_errant(essay:str="English is a internationaly language which becomes importantly for modern world. \nIn China, English is took to be a foreigh language which many student choosed to learn. They begin to studying English at a early age. They use at least one hour to learn English knowledges a day. Even kids in kindergarten have begun learning simple words. That's a good phenomenan, for English is essential nowadays.\nIn addition to, some people think English is superior than Chinese. In me opinion, though English is for great significance, but English is after all a foreign language. it is hard for people to see eye to eye. English do help us read English original works, but Chinese helps us learn a true China. Only by characters Chinese literature can send off its brilliance. Learning a country's culture, especial its classic culture, the first thing is learn its language. Because of we are Chinese, why do we give up our mother tongue and learn our owne culture through a foreign language?"): 
	''' 2022.11.15 [ {"snt": snt, "edits": doc_edits(doc, tdoc) } ] '''
	from gec_fastapi import xgec
	import spacy, errant # 2020-9-10 #https://github.com/chrisjbryant/errant
	if not hasattr(xgec_errant, 'nlp'): 
		xgec_errant.nlp = spacy.load('en_core_web_sm')
		xgec_errant.annotator = errant.load('en', xgec_errant.nlp)

	_doc_edits = lambda doc, tdoc: [ doc_edit(doc, edit) for edit in xgec_errant.annotator.annotate(doc, tdoc) if edit.o_start >= 0 and pass_filter(doc, edit)] 
	try:
		doc		= xgec_errant.nlp(essay)
		snts	= [ snt.text for snt in doc.sents ] 
		mapgec	= xgec(snts)  # pipeline_snts(snts)
		return [ {"snt": snt.text, "offset": snt[0].idx,  "edits": _doc_edits(snt.as_doc(), xgec_errant.nlp(mapgec[snt.text]))}  for snt in doc.sents ]
	except Exception as ex:
		print(">>callback Ex:", ex, essay)
		exc_type, exc_value, exc_traceback_obj = sys.exc_info()
		traceback.print_tb(exc_traceback_obj)
		return str(ex)
		
if __name__ == '__main__':
	print (gec_errant() )
	#[{'op': 's', 'position': 4, 'ibeg': 1, 'word_list': 'has', 'kp': 'has', 'correct': 'is', 'cate': 'R:VERB', 'error': '动词误用', 'short_msg': '建议<b>has</b>修改为<b>is</b>'}, 
	# {'op': 's', 'position': 8, 'ibeg': 2, 'word_list': 'readies', 'kp': 'readies', 'correct': 'ready', 'cate': 'R:MORPH', 'error': '词性误用', 'short_msg': '建议<b>readies</b>修改为<b>ready</b>'}]