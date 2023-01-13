# 2022.7.23
from lit import * 

def run(app_state={}):
	sql = app_state['sql'] if 'sql' in app_state else st.sidebar.text_input("Input a query", "select substring_index(s,':',-1),i from dic where s like 'open:VERB:dobj:NOUN:%' order by i desc limit 10") 
	s = wordcloud( rows(sql) ) 
	if s is not None:  
		st.write(s) 

if __name__ == '__main__': run()