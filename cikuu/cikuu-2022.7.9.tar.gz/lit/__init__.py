# 2022.7.26 pip install streamlit-aggrid pyecharts streamlit_echarts pandas numpy matplotlib seaborn streamlit-aggrid -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
import time,redis, requests ,json, platform,os,re,builtins
from collections import Counter,defaultdict
import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib #import seaborn as sns
from util import likelihood

st.set_page_config (layout="wide")
st.write('''<style type="text/css">a:link,a:visited{ text-decoration:none; }a:hover{ text-decoration:underline; }</style>''',unsafe_allow_html=True)
app_state = st.experimental_get_query_params()
if not isinstance(app_state, str): 	app_state = {k: v[0] if isinstance(v, list) else v for k, v in app_state.items()} 

eshost		= os.getenv('eshost', 'es.corpusly.com:9200')
apihost		= os.getenv('apihost', 'cpu76.wrask.com:8000')
urlroot		= os.getenv('urlroot', 'http://cpu76.wrask.com:8000')  
@st.cache(allow_output_mutation=True)
def rows(sql): return requests.get(f"{urlroot}/kpsi/rows", params={'sql':sql}).json()
cplist		= [row[0].split('_')[0].strip() for row in rows("show tables") if row[0].endswith("_snt")] #['bnc', 'clec', 'dic', 'fengtai', 'gaokao', 'gblog', 'guten', 'gzjc', 'nju', 'nyt', 'qdu', 'sino', 'twit']
poslist		= ["VERB","NOUN","ADJ","ADV","LEX","LEM"]
rellist		= ["dobj:NOUN", "~dobj:VERB", "amod:ADJ", "~amod:NOUN"]
trplist		= ["VERB:dobj:NOUN, NOUN:~dobj:VERB, NOUN:amod:ADJ, ADJ:~amod:NOUN"]

rels = { 
"VERB": ["dobj:NOUN", "nsubj:NOUN", "advmod:ADV", "oprd:ADJ", "oprd:NOUN"],
"NOUN": ["~dobj:VERB", "~nsubj:VERB", "amod:ADJ"],
"ADJ": [ "~amod:NOUN"],
"ADV": ["~advmod:ADJ","~advmod:VERB"],
}

attrs = {
'VERB':	'ROOT,VB,VBD,VBG,VBN,VBP,VBZ,Vend,acl,acomp,advcl,advmod,agent,amod,appos,attr,aux,auxpass,be_vbn_p,cc,ccomp,compound,conj,csubj,csubjpass,dative,dep,det,dobj,expl,intj,mark,meta,neg,nmod,npadvmod,nsubj,nsubjpass,nummod,oprd,parataxis,pcomp,pobj,poss,preconj,predet,prep,prt,punct,quantmod,relcl,sattr,sbea,sva,svc,svo,svx,v_n_vbn,vap,vdp,vnp,vnpn,vp,vpg,vpn,vpnpn,vppn,vprt,vtov,vvbg,xcomp,~acl,~acomp,~advcl,~advmod,~agent,~amod,~appos,~attr,~case,~cc,~ccomp,~compound,~conj,~csubj,~csubjpass,~dative,~dep,~dobj,~intj,~mark,~nmod,~npadvmod,~nsubj,~nsubjpass,~nummod,~oprd,~parataxis,~pcomp,~pobj,~poss,~predet,~prep,~prt,~punct,~relcl,~sbea,~xcomp'.split(','), #select group_concat(substring_index(s,':',-1))  from dic where s like '*:VERB:%'
'ADJ':	'AFX,JJ,JJR,JJS,acl,acomp,advcl,advmod,agent,amod,ap,appos,aux,auxpass,be_adj_p,cc,ccomp,compound,conj,csubj,csubjpass,dative,dep,det,dobj,intj,mark,neg,nmod,npadvmod,nsubj,nsubjpass,nummod,oprd,parataxis,pcomp,pobj,poss,preconj,predet,prep,prt,punct,quantmod,relcl,sbea,xcomp,~acl,~acomp,~advcl,~advmod,~amod,~appos,~attr,~cc,~ccomp,~compound,~conj,~csubj,~csubjpass,~dative,~dep,~det,~dobj,~intj,~mark,~nmod,~npadvmod,~nsubj,~nsubjpass,~nummod,~oprd,~parataxis,~pcomp,~pobj,~poss,~predet,~prep,~prt,~punct,~quantmod,~relcl,~sbea,~xcomp'.split(','),
'NOUN':	'NN,NNS,acl,acomp,advcl,advmod,agent,amod,appos,aux,auxpass,case,cc,ccomp,compound,conj,csubj,csubjpass,dative,dep,det,dobj,expl,intj,mark,meta,neg,nmod,np,npadvmod,nsubj,nsubjpass,nummod,oprd,parataxis,pcomp,pobj,poss,pp,preconj,predet,prep,prt,punct,quantmod,relcl,sbea,xcomp,~acl,~acomp,~advcl,~advmod,~amod,~appos,~attr,~case,~ccomp,~compound,~conj,~csubj,~dative,~dep,~det,~dobj,~intj,~mark,~meta,~nmod,~npadvmod,~nsubj,~nsubjpass,~nummod,~oprd,~parataxis,~pcomp,~pobj,~poss,~predet,~prep,~prt,~punct,~quantmod,~relcl,~sbea,~xcomp'.split(','),
'ADV':	'RB,RBR,RBS,WRB,acl,acomp,advcl,advmod,agent,amod,appos,aux,auxpass,cc,ccomp,compound,conj,csubj,dative,dep,det,dobj,intj,mark,neg,nmod,npadvmod,nsubj,nsubjpass,nummod,oprd,parataxis,pcomp,pobj,poss,preconj,prep,prt,quantmod,relcl,xcomp,~acl,~acomp,~advcl,~advmod,~agent,~amod,~appos,~attr,~cc,~ccomp,~compound,~conj,~dative,~dep,~det,~dobj,~expl,~intj,~mark,~neg,~nmod,~npadvmod,~nsubj,~nsubjpass,~nummod,~oprd,~pcomp,~pobj,~poss,~preconj,~predet,~prep,~prt,~punct,~quantmod,~relcl,~sbea,~xcomp'.split(','),
}

kn_sumkey = {
"#VERB": ["*:VERB:%", "VERB:%"],  #with src as ( select *, (select i from kpsi.clec where s = '#VERB') sumi from kpsi.clec where s like '*:VERB:%'), tgt as ( select *, (select i from kpsi.dic where s = '#VERB') sumi from kpsi.dic where s like '*:VERB:%') select tgt.s, src.i, src.sumi, tgt.i ti, tgt.sumi tsumi, keyness(src.i, tgt.i, src.sumi, tgt.sumi) kn from src right outer join tgt on src.s= tgt.s  order by kn 
"#NOUN": ["*:NOUN:%", "NOUN:%"],
"LEM:sound": ["sound:POS:%", "sound:LEX:%"],
"knowledge:NOUN:~dobj":  ["knowledge:NOUN:~dobj:VERB:%"], 
"open:VERB:dobj":  ["open:VERB:dobj:NOUN:%"], 
"consider:VERB": ["consider:VERB:be_vbn_p:%","consider:VERB:vtov:%","consider:VERB:VBN:%"],
}

@st.cache
def geti(cp,s):
	res = rows(f"select i from {cp} where s = '{s}' limit 1")
	return res[0][0] if res and len(res) > 0 else 0 

@st.cache
def slike(cp,pattern, topk:int=10):
	return rows(f"select substring_index(s,':',-1) ,i,snt from {cp},{cp}_snt where s like '{pattern}' and t = sid order by i desc limit {topk}")
#print ( slike("dic", "open:VERB:dobj:NOUN:%") )  #[['door', 255, 'A coachman has to drive, a groom has to open the door, a peon has to shout warnings.'], ['eye', 67, 'And even when revolution or military defeat should have opened eyes, distorted versions of reality survive.'], ['window', 66, "And then suddenly I pop back to life, clamber across Jenny's lap and open the window."], ['mouth', 62, "'I'll go,' Travis said quickly before she could open her mouth."], ['fire', 59, 'According to eyewitness accounts, soldiers opened fire on the crowd.'], ['account', 36, 'All you need to open the account is'], ['gate', 27, "And it's five, six, seven, open up the pearly gates."], ['store', 26, 'Argos opened 19 stores last year, with 25 more planned for 1993.'], ['letter', 23, 'A police spokesman said if the man had gone much further in opening the letter, he could have been killed.'], ['box', 22, 'After building your own machine you certainly will not be worried about opening the box!']]

@st.cache(allow_output_mutation=True)
def sisnt(cp="dic",pattern="open:VERB:dobj:NOUN:%", topk:int=10, color:str="#d65f5f"): #https://user-images.githubusercontent.com/27242399/140746511-1205f24a-869f-4b24-9ed7-9153cfeef8e3.png
	df = pd.DataFrame(slike(cp, pattern), columns=["Word", "Count", "Sentence"]).sort_values(by="Count", ascending=False).reset_index(drop=True)
	df.index += 1
	return df.style.bar(subset=['Count'], color=color) 	#st.table(df)

def add_style(df):
	cmGreen = sns.light_palette("green", as_cmap=True)
	cmRed = sns.light_palette("red", as_cmap=True)
	df = df.style.background_gradient(cmap=cmGreen,subset=["Relevancy",],)
	#df = df.format({"Relevancy": "{:.1%}",})
	return df

@st.cache
def attr(pos): 
	if not hasattr(attr, pos): setattr(attr, pos, [row[0] for row in rows(f"select substring_index(s,':',-1) w from bnc where s like '*:VERB:%' and i > 1000")])
	return getattr(attr, pos) 
#print ( attr('VERB'))# ['ROOT', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'Vend', 'acl', 'acomp', 'advcl', 'advmod', 'agent', 'amod', 'appos', 'attr', 'aux', 'auxpass', 'be_vbn_p', 'cc', 'ccomp', 'compound', 'conj', 'csubj', 'csubjpass', 'dative', 'dep', 'det', 'dobj', 'expl', 'intj', 'mark', 'meta', 'neg', 'nmod', 'npadvmod', 'nsubj', 'nsubjpass', 'nummod', 'oprd', 'parataxis', 'pcomp', 'pobj', 'poss', 'preconj', 'prep', 'prt', 'punct', 'relcl', 'sattr', 'sva', 'svc', 'svo', 'svx', 'vap', 'vdp', 'vnp', 'vnpn', 'vp', 'vpg', 'vpn', 'vpnpn', 'vppn', 'vprt', 'vtov', 'vvbg', 'xcomp', '~acl', '~acomp', '~advcl', '~advmod', '~amod', '~appos', '~attr', '~case', '~ccomp', '~compound', '~conj', '~csubj', '~csubjpass', '~dep', '~dobj', '~intj', '~nmod', '~npadvmod', '~nsubj', '~nsubjpass', '~oprd', '~parataxis', '~pcomp', '~pobj', '~prep', '~punct', '~relcl', '~xcomp']
 
@st.cache
def kndata(sumkey='knowledge:NOUN:~dobj', cps:str='clec', cpt:str='dic', slike:str="knowledge:NOUN:~dobj:VERB:%",tail:bool=False, asdf:bool=False): 
	''' return (word, srccnt, tgtcnt, srcsum, tgtsum, keyness) , 2022.7.24 '''
	_rows = requests.get(f"{urlroot}/kpsi/kndata", params={"sumkey":sumkey, "cps":cps, "cpt":cpt, "slike":slike, "tail":tail}).json()
	return pd.DataFrame(_rows) if asdf else _rows 

def df_perc(_rows): #sql:str="select substring_index(s,':',-1),i, (select i from clec where s = '#VERB') sumi from clec where s like '*:VERB:%'"
	''' (index, cnt, sum, perc)  '''
	df = pd.DataFrame(_rows, columns=['index', 'count', 'sum'])
	df["percent(%)"] = round(100 * df["count"]/df["sum"],1)
	return df.sort_values(["percent(%)"], ascending=[False])

mf		= lambda s='VERB:consider', cps='gzjc,clec,dic' :  rows(' union all '.join ( [f"select '{cp}' name, 1000000 * i / (select i from {cp} where s = '#SNT') mf from {cp} where s = '{s}'" for cp in cps.strip().split(',')]) )
trpsnts = lambda s,cp, topk: requests.get(f"{urlroot}/kpsi/snts", params={"s":s, "cp":cp, "topk":topk, "hl_words":f"{s.split(':')[0]},{s.split(':')[-1]}"}).text
def snts(cp, s, topk:int=10): 
	_sidlist= rows(f"select substring_index(t,',',{topk}) from {cp} where s = '{s}' limit 1")[0][0]
	word	= s.split(':')[-1]
	return [ re.sub(rf'\b{word}\b', f'<font color="red">{word}</font>', row[0]) for row in rows (f"select snt from {cp}_snt where sid in ({_sidlist}) ")  ]
#print (snts("clec", 'open:VERB:dobj:NOUN:door')) #st.write(f"{i+1}. {snt}", unsafe_allow_html=True)
#print (mf()) #[['gzjc', 2704.8349], ['clec', 3810.3077], ['dic', 3863.9423]]

def rank(lem:str="LEM:sound", cp:str="dic", cps:str="gzjc,clec,dic"): 
	col1, col2 = st.columns(2)
	cnt = rows(f"select i from {cp} where s = '{lem}' limit 1" )[0][0]
	col1.metric("Freq", cnt )
	col2.metric("Rank", rows(f"select count(*) from {cp} where s like '{lem.split(':')[0]}:%' and i > {cnt}" )[0][0])
	data = mf(f"{lem}", cps)
	bar(data, f= lambda name: (st.subheader(name), st.write(snts(name, lem, topk=3) ) ) )

def snts_html(s:str="open:VERB:dobj:NOUN:door", cp:str='dic', hl_words:str="open,door", topk:int=10, sntsum:bool=True): 
	''' return HTML <ol><li> , 2022.8.1 '''
	from dic import lemma_lex
	sids = rows(f"select i, t from {cp} where s = '{s}' limit 1")
	if sids and len(sids) > 0 :
		cnt = sids[0][0]
		sids = ",".join([str(sid) for sid in sids[0][1].split(',')[0:topk] ])
	else: 
		return f"Found <b>0</b>  sentences in <i>{cp}</i> of <u>{s}</u> "
	snts = rows(f"select snt from {cp}_snt where sid in ({sids})")
	words = '|'.join([ '|'.join(list(lemma_lex.lemma_lex[w])) for w in hl_words.strip().split(',') if w in lemma_lex.lemma_lex])
	arr = [re.sub(rf'\b({words})\b', r'<font color="red">\g<0></font>', snt[0]) if words else snt[0] for snt in snts]
	html = f"<ol> Found <b>{cnt}</b>  sentences in <i>{cp}</i>." if sntsum else "<ol>"
	return html + "\n".join([f"<li>{snt}</li>" for snt in arr]) + "</ol>"

def snts_markdown(s:str="open:VERB:dobj:NOUN:door", cp:str='dic', hl_words:str="open,door", topk:int=10, sntsum:bool=True): 
	st.markdown( snts_html(s, cp, hl_words, topk, sntsum), unsafe_allow_html=True ) 

@st.cache
def vecso_snthtml(snt, name, topk=10): 
	return  requests.get(f"{urlroot}/hnswlib", params={"snt":snt, "topk":topk, "name":name}).text #http://cpu76.wrask.com:8000/hnswlib?snt=I%20am%20too%20tired%20to%20move%20on.&topk=10&name=dic

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
def grid_gb(df, pagesize=10): 
	gb = GridOptionsBuilder.from_dataframe(df)
	#customize gridOptions  pip install streamlit-aggrid
	gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
	gb.configure_side_bar()
	gb.configure_selection("single")
	gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=pagesize)
	gb.configure_grid_options(domLayout='normal')
	return gb

def grid_response(df, height=350):
	gb = grid_gb(df) 
	if not df.empty:
		return AgGrid(
			df, 
			gridOptions=gb.build(),
			height=height, 
			width='100%',
			data_return_mode=DataReturnMode.__members__["FILTERED"], 
			update_mode=GridUpdateMode.__members__["MODEL_CHANGED"],
			fit_columns_on_grid_load=True, # auto fit 
			allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
			)

def grid(df, height=350, pagesize=10,  name:str='grid' ): 
	''' last update: 2022.8.1 '''
	if df.empty: return 
	gb = GridOptionsBuilder.from_dataframe(df) #customize gridOptions  pip install streamlit-aggrid
	gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
	gb.configure_side_bar()
	gb.configure_selection("single")
	gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=pagesize)
	gb.configure_grid_options(domLayout='normal')
	gb = grid_gb(df) 
	g = AgGrid(df, gridOptions=gb.build(),height=height, width='100%',
		data_return_mode=DataReturnMode.__members__["FILTERED"], 
		update_mode=GridUpdateMode.__members__["MODEL_CHANGED"],
		fit_columns_on_grid_load=True, # auto fit 
		allow_unsafe_jscode=True) #Set it to True to allow jsfunction to be injected
	if g['selected_rows']:  st.session_state[name] = g['selected_rows'][0] # dict , row['word']
	return g

#import altair as alt
from streamlit_echarts import st_pyecharts, st_echarts #https://share.streamlit.io/andfanilo/streamlit-echarts-demo/master/app.py
def bar(_rows, height:int=350, name:str='bar'): # [ ['first',1,2,3], ['second',4,5,6] ]
	''' 2022.7.30 '''
	if _rows is None or len(_rows) <=0 or len(_rows[0]) <=0 : return 
	rowlen = len(_rows[0]) 
	options = {"xAxis": {"type": "category","data": [row[0] for row in _rows  ],},
				"yAxis": {"type": "value"},	"series": [{"data": [row[i] for row in _rows ], "type": "bar"} for i in range(1,rowlen)],	}
	events = {"click": "function(params) { return params.name }","dblclick": "function(params) { return [params.type, params.name, params.value] }",} 	#st.markdown("Click on a bar for label + value, **double** click to see type+name+value")
	s = st_echarts(options=options, events=events, height=f"{height}px") #, key="render_basic_bar_events"
	if s is not None: st.session_state[name] = s 
	return s
#bar(rows("select substring_index(s,':',-1) ,i, i+1, i+3 from clec where s like 'open:VERB:dobj:NOUN:%' order by i desc limit 10"), f = lambda s: st.write(s) )

def wordcloud(si, height:int=350, name: str='wordcloud' ): 
	wordcloud_option = {"series": [{"type": "wordCloud", "data": [{"name": name, "value": value} for name, value in si]}]}
	events = {"click": "function(params) { return params.name }","dblclick": "function(params) { return [params.type, params.name, params.value] }",} 	#st.markdown("Click on a bar for label + value, **double** click to see type+name+value")
	s = st_echarts(wordcloud_option, events=events, height=f"{height}px") 
	if s is not None: st.session_state[name] = s 
	return s

def pie(si, height:int=350, name: str='pie' ):
	options = {"tooltip": {"trigger": "item"}, "legend": {"top": "5%", "left": "center"},
	    "series": [ {"name": "", "type": "pie","radius": ["40%", "70%"], "avoidLabelOverlap": False,
            "itemStyle": {"borderRadius": 10, "borderColor": "#fff", "borderWidth": 2,  },
            "label": {"show": False, "position": "center"},
            "emphasis": {"label": {"show": True, "fontSize": "40", "fontWeight": "bold"}},
            "labelLine": {"show": False},
            "data":   [ {"value":i, "name":s} for s,i in si ], } ], }
	events = {"click": "function(params) { return params.name }","dblclick": "function(params) { return [params.type, params.name, params.value] }",} 	#st.markdown("Click on a bar for label + value, **double** click to see type+name+value")
	s = st_echarts(options, events=events, height=f"{height}px") 
	if s is not None: st.session_state[name] = s 
	return s

es_postag = lambda hyb="it _be impossible to _VERB", index='dic' : requests.post(f"http://{eshost}/{index}/_search", json=
{
  "query": {
    "match_phrase": {
      "postag":hyb
    }
  }
}).json()

es_hybcnt = lambda hyb="it _be impossible to _VERB", index='dic' : int(es_postag(hyb, index)['hits']['total']['value'])

es_phrase_word = lambda phrase="not sure", word="likely", index='dic' : requests.post(f"http://{eshost}/{index}/_search", json=
{
  "query": { 
    "bool": { 
      "must": [
        { "match_phrase": { "snt":  phrase}},
		{ "match": { "type":"snt" }},
        { "match": { "snt":word }}
      ]
    }
  }
}).json()


if __name__ == '__main__': 
	print ( es_postag()) 