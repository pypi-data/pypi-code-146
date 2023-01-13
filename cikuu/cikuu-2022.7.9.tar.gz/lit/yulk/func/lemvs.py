# 2022.7.23
from lit import yulk 

def rank(lem, cps, cpt): 
	st.header(f"单词 {lem}")
	col1, col2 = st.columns(2)
	cnt = geti(cps, 'LEM:{lem}' )
	col1.metric("Freq", cnt )
	col2.metric("Rank", rows(f"select count(*) from {cps} where s like 'LEM:%' and i > {cnt}" )[0][0])

def show(data, cps, cpt) : 
	col1, col2 = st.columns(2)
	with col1: 	bar_dual([row["index"].split(':')[-1] for row in data], [100 * int(row[cps])/int(row[cps+"_sum"]) for row in data], [100 * int(row[cpt])/int(row[cpt + "_sum"]) for row in data])

	df = pd.DataFrame(data)
	with col2:	grid	= grid_response(df) 
	row = grid['selected_rows'][0] if grid['selected_rows'] else data[0]		
	w = row['index'].split(':')[-1]
	col3, col4 = st.columns(2)
	col3.subheader(df.columns[1] + ":" + w)
	#if row[ df.columns[1] ] > 0 : col3.write( trpsnts(row['index'], df.columns[1], 10) if showsnts else pd.DataFrame(rows(f"select s,i from {df.columns[1]} where s like '{row['index']}:%' order by i desc limit 10"), columns=['term','count']) , unsafe_allow_html=True )
	col4.subheader(df.columns[3] + ":" + w)
	#if row[ df.columns[3] ] > 0 : col4.write( trpsnts(row['index'], df.columns[3], 10) if showsnts else pd.DataFrame(rows(f"select s,i from {df.columns[3]} where s like '{row['index']}:%' order by i desc limit 10"), columns=['term','count']), unsafe_allow_html=True )

def run(app_state={}):
	st.sidebar.title(f"LEMMA vs")
	lem = st.sidebar.text_input("Input a lemma", "sound") 
	cps	= st.sidebar.selectbox('choose a source corpus', cplist, 0) 
	cpt	= st.sidebar.selectbox('choose a target corpus', cplist, 1) 
	topk = st.sidebar.slider('topk', 0, 50, 10)

	tabs = st.tabs([lem, f"词性对比", f"词型对比"])
	with tabs[0]: rank(lem, cps, cpt) 
	with tabs[1]: show( kndata(f"LEM:{lem}", cps, cpt, f"{lem}:POS:%"), cps, cpt  )
	with tabs[2]: show( kndata(f"LEM:{lem}", cps, cpt, f"{lem}:LEX:%"), cps, cpt  )

if __name__ == '__main__': run()