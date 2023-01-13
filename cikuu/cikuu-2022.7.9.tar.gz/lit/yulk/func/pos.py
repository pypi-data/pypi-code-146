# 2022.7.23
from lit import * 

def run(app_state={}):

	lem = app_state['lem'] if 'lem' in app_state else st.sidebar.text_input("Input a lemma", "sound") 
	cp	= app_state['cp'] if 'cp' in app_state else st.sidebar.selectbox('choose a source corpus', cplist, 0)

	st.subheader(f"[{cp}]{lem}")
	data = rows(f"select substring_index(s,':',-1), i from {cp} where s like '{lem}:POS:%'")
	st.markdown( " ".join([f"{s}:{i}" for s,i in data]) )
	#cols = st.columns(len(data) + 1)
	#cols[0].metric(cp, lem)
	#for i in range(len(data)): cols[i+1].metric(data[i][0], data[i][1])

	pos = pie(data, name=f"pos-{lem}-{cp}") 
	if pos :    #col1, col2 = st.columns(2)
		freq = geti(cp, f'{pos}:{lem}' ) #	col1.metric("Freq", cnt )
		rank = int(rows(f"select count(*) from {cp} where s like '{pos}:%' and i > {freq}" )[0][0]) #col2.metric("Rank", rank)
		st.subheader(f"{pos} 频次是 {freq}, 排名是 {rank} ")
		st.slider('', 1, rows(f"select count(*) from {cp} where s like '{pos}:%'" )[0][0] , rank)

if __name__ == '__main__': run()