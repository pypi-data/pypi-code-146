# 2022.8.7
from lit import * 

def run(app_state={}):
	st.title(f"Style")
	query = st.sidebar.text_input("Input a query", "LEX:consider") 
	cps = st.sidebar.text_input("Input cplist", "gzjc,clec,dic") 
	if st.button("submit"): 
		res = mf(query, cps)
		bar(res) 
		st.write(res) 

if __name__ == '__main__': run()