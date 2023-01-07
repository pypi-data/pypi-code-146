# 2022.8.7
from lit import * 
from .common import * 

def run(app_state={}):
	st.subheader("The Corpus of Linguistic Acceptability (CoLA)") 
	st.markdown(f"[refer](https://nyu-mll.github.io/CoLA/)") 
	essay = st.text_area( "Input an essay or sntlist", '''She has ready.
She is ready.
I believe we can doing it.
The quick fox jumped over the lazy dog.''', height=300)
	if st.button("submit") : 
		rows = requests.post(f"http://{apihost}/cola/snts", json=essay.strip().split('\n')).json()
		st.write(pd.DataFrame(rows, columns=["sentence", "score"])) 

if __name__ == '__main__': run()