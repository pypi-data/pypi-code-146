# 2022.8.7
from lit import * 

def run(app_state={}):
	st.title(f"Elastic Query")
	cp = st.sidebar.text_input("Choose an index", "bnc") 
	sql = st.text_area( "", '''{
  "query": { 
    "bool": { 
      "must": [
        { "match_phrase": { "snt":  "not sure"}},
        { "match": { "snt":"likely" }},
        { "match": { "type":"snt" }}
      ]
    }
  }
}''', height=300)

	if st.button("submit"): 
		res = requests.post(f"http://es.corpusly.com:9200/{cp}/_search", json= json.loads(sql)).json()
		st.write(res) 

if __name__ == '__main__': run()