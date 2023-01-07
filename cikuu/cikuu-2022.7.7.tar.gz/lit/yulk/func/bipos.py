# 2022.7.23
from lit import * 
st.set_page_config (layout="wide")

def run(app_state={}):

	lem = app_state['lem'] if 'lem' in app_state else st.sidebar.text_input("Input a lemma", "sound") 
	cps	= app_state['cps'] if 'cps' in app_state else st.sidebar.selectbox('choose a source corpus', cplist, 0)
	cpt	= app_state['cpt'] if 'cpt' in app_state else st.sidebar.selectbox('choose a target corpus', cplist, 1)

	col0, col1 = st.columns(2)
	with col0: __import__(f"lit.yulk.func.pos", fromlist=['run']).run({'cp':cps, 'lem':lem})
	with col1: __import__(f"lit.yulk.func.pos", fromlist=['run']).run({'cp':cpt, 'lem':lem})
	
	col3, col4  = st.columns(2) 
	data	= kndata(f"LEM:{lem}", cps, cpt, f"{lem}:POS:%")
	df		= pd.DataFrame(data).sort_values(["keyness"], ascending=[False]) 
	with col3: 	bar([ (row['index'].split(':')[-1], 100 * row[cps] / row[f"{cps}_sum"], 100 * row[cpt] / row[f"{cpt}_sum"])  for index,row in df.iterrows()] )
	with col4: 	
		grid(df) 
		if 'grid' in st.session_state : 
			st.write( st.session_state.grid) 

if __name__ == '__main__': run()