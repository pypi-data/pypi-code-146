# 2022.7.23
from lit import *

def run(app_state={}):
	st.title(f"Corpus List")
	dims	= '#LEX,#VERB,#ADJ,#ADV,#ADJ,#NOUN,#SNT,#vtov,#VBG,#vvbg,#dobj,#amod,#advmod'
	dimlist = dims.replace(',', "','")
	ssi		= defaultdict(Counter) 
	for name in cplist: 	#ssi[name] = Counter(dict(rows(f"select s,i from {name} where s in ('{dimlist}')")))
		for s, i in rows(f"select s,i from {name} where s in ('{dimlist}')"):
			ssi[s].update ({name: i})

	df		= pd.DataFrame(ssi).reset_index() #(inplace = True)#df	= df.fillna(0).transpose()
	grid	= grid_response(df) 
	if grid['selected_rows']: 
		row = grid['selected_rows'][0] 
		st.write(row)

if __name__ == '__main__': 
	pass 