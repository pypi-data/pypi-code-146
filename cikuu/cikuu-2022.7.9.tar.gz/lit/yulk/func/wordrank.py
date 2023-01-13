# 2022.7.25
from lit import yulk

def show(data) : 
	st.metric("Count", len(data) )
	if not data : return
	col1, col2 = st.columns(2)
	with col1: 
		labels = ",".join([row['index'].split(':')[-1] for row in data[0:100]])
		values = ",".join([str( abs(row.get('keyness',0)) ) for row in data[0:100]])
		components.iframe(f"{urlroot}/echart/wordcloud?height=500&width=600&labels={labels}&values={values}",height=500)
	df = pd.DataFrame(data)
	with col2:	grid	= grid_response(df) 
	row = grid['selected_rows'][0] if grid['selected_rows'] else data[0]		
	w = row['index'].split(':')[-1]
	col3, col4 = st.columns(2)
	col3.metric(df.columns[1] + ":" + w, geti(df.columns[1], row['index']) )
	col4.metric(df.columns[3] + ":" + w, geti(df.columns[3], row['index']) )
	
def run(app_state={}):
	#st.sidebar.title(f"Word rank in dual corpus")
	pos = st.sidebar.selectbox("词性", poslist) 
	cps	= st.sidebar.selectbox('源语料库', cplist, 0) 
	cpt	= st.sidebar.selectbox('参考语料库', cplist, 1) 
	knv  = st.sidebar.slider('显著度范围',-20, 20, (-6, 6)) 
	topk = st.sidebar.slider('例句条数', 0, 50, 10) #st.sidebar.button('submit')

	knrows = kndata(f"#{pos}", cps, cpt, f"{pos}:%") 
	tabs = st.tabs([pos,"待学", "疑似误用","超用"]) 
	with tabs[0] :  show( knrows )
	with tabs[1]:	show( [ row for row in knrows if row.get('keyness', 0) < knv[0] ] )
	with tabs[2]:	show( [ row for row in knrows if row[cpt] <= 0 ] )
	with tabs[3]:	show( [ row for row in knrows if row.get('keyness', 0) > knv[1] ] )

if __name__ == '__main__': run()