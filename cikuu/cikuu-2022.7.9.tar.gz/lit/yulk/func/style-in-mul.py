# 2022.8.15
from lit import *

@st.cache
def data(pos:str='VERB', lem='consider'): 
	return rows(f'''select 'sino' label, 1000000 * i / (select i from kpsi.sino where s = '#SNT') mf from kpsi.sino where s = '{pos}:{lem}'
union all 
select 'dic' label, 1000000 * i / (select i from kpsi.dic where s = '#SNT') mf   from kpsi.dic where s = '{pos}:{lem}'
union all 
select 'bnc' label, 1000000 * i / (select i from kpsi.bnc where s = '#SNT') mf   from kpsi.bnc where s = '{pos}:{lem}'
union all 
select 'twit' label, 1000000 * i / (select i from kpsi.twit where s = '#SNT') mf   from kpsi.twit where s = '{pos}:{lem}'
union all 
select 'nyt' label, 1000000 * i / (select i from kpsi.nyt where s = '#SNT') mf from kpsi.nyt where s = '{pos}:{lem}'
''')

def run(app_state={}):	#cps = st.sidebar.multiselect('Choose corpus',corpuslist,corpuslist[0:5] ) 
	pos	= st.sidebar.selectbox('Part of speech (pos)',poslist)
	lem = st.sidebar.text_input("Input a word", "consider") 
	st.sidebar.button('submit')

	dic = dict(data(pos, lem))
	options = {
		"xAxis": {
			"type": "category",
			"data": [k for k,v in dic.items()], 
		},
		"yAxis": {"type": "value"},
		"series": [{"data": [{"value": v, "itemStyle": {"color": "#a90000"}} if k =='学生' else v for k,v in dic.items()], "type": "bar"}],
	}
	events = {
		"click": "function(params) { console.log(params.name); return params.name }",
		"dblclick": "function(params) { return [params.type, params.name, params.value] }",
	}

	st.markdown("Collocation frequency per million sentences")
	cp = st_echarts(options=options, events=events, height="500px", key="render_basic_bar_events")
	with st.expander("Source data"):
		st.write(dic) 
	if cp is not None: #SELECT snt FROM fts WHERE terms MATCH 'dobj_VERB_NOUN_open_door' limit 3
		res = snts(cp, f"{pos}:{lem}")
		st.write(res)
		st.sidebar.subheader(cp) 

if __name__ == '__main__': 
	res = snts('bnc', 'book:VERB:VBD')
	print (res) 
