# 2022.7.23
from lit import * 

def run(app_state={}):
	st.sidebar.title(f"POSvs")
	lem = app_state['lem'] if 'lem' in app_state else st.sidebar.text_input("Input a lemma", "sound") 
	cps	= app_state['cps'] if 'cps' in app_state else st.sidebar.selectbox('choose a source corpus', cplist, 0)
	cpt	= app_state['cpt'] if 'cpt' in app_state else st.sidebar.selectbox('choose a target corpus', cplist, 1)
	topk = st.sidebar.slider('topk', 0, 50, 10)

	st.title(lem) 
	df = kndata(f"LEM:{lem}", cps, cpt, slike = f'{lem}:POS:%', tail=True, asdf=True)
	bar([ ( row['index'],  row[cps]/row[cps+"_sum"], row[cpt]/row[cpt+"_sum"])  for index,row in df.iterrows()], name=f"posvs-bar-{lem}-{cps}-{cpt}")
	grid(df, name=f"posvs-grid-{lem}-{cps}-{cpt}")
	#pos = pie(data) 

if __name__ == '__main__': run()