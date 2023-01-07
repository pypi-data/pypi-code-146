# 2022.8.7
from lit import * 

def run(app_state={}):
	st.subheader("ES hybrid search on postag") 
	cp = st.sidebar.text_input("Input a corpus", "bnc") 
	hyb = st.text_input("Input a hybrid query", "it _be possible to _VERB")

	if st.button("submit") : 
		res = es_postag(hyb, cp) 
		#st.sidebar.write(res)
		st.metric("Total", res['hits']['total']['value'])
		for i, ar in enumerate(res['hits']['hits']):
			st.write(f"{i+1}. " + ar['_source']['snt'])

if __name__ == '__main__': run()