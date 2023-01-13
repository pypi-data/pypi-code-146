# 2022.8.7
from lit import * 

def run(app_state={}):
	st.subheader("Upon given phrase, words distribution") 
	cp = st.sidebar.text_input("Input a corpus", "bnc") 
	context = st.text_input("context given", "not sure")
	word = st.text_input("word expected", "likely")

	if st.button("submit") : 
		res = es_phrase_word(context, word, cp) 
		#st.sidebar.write(res)
		st.metric("Total", res['hits']['total']['value'])
		for i, ar in enumerate(res['hits']['hits']): # add highlight later 
			st.write(f"{i+1}. " + ar['_source']['snt'])

if __name__ == '__main__': run()