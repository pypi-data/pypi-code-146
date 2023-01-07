# 2022.8.7
from lit import * 

def run(app_state={}):
	st.sidebar.title(f"Single parsing")
	body = st.sidebar.text_input("Input a body", "Parents * much importance to education.") 
	options = st.sidebar.text_input("options", "attach,pay,link,apply").strip().split(',')
	cp = st.sidebar.text_input("Choose a corpus", "bnc") 
	topk = st.sidebar.slider('topk', 0, 50, 10)
	st.sidebar.button('submit')

	st.subheader(body) 
	cols = st.columns(len(options))
	for i in range(len(options)): cols[i].metric("", options[i])

	xrange = st.slider('chunk range', 0, 50, (1,5)) # to get the snt len 
	if st.button('gramx'): 
		rows = requests.get(f"http://{apihost}/gramx/single", params={"body":body, 'options':','.join(options), "start":xrange[0], "end":xrange[1]}).json()
		rows = [ (s,i) for s,i in rows.items()]
		bar(rows)
		st.write(pd.DataFrame(rows, columns=["chunk", "freq"])) 

if __name__ == '__main__': run()