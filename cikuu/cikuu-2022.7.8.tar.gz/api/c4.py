# 2023.1.1  sudo ufw allow from 101.35.196.171 to any port 9200
from api.es import * 
requests.c4host	= os.getenv('c4host', 'wrask.com:9200') #wrask.com

@app.get("/c4/igiven", tags=["es"])
def igiven(phraselist:str="_memory|_joke", given:str="the early years", index:str="c4-*"):
	''' phrase freq on the given chunk '''
	return  [{"phrase": phrase, "given":given, "count": requests.post(f"http://{requests.c4host}/{index}/_search/", json={
  "query": {
    "bool": {
      "must": 
        {"match_phrase": {
          "postag": phrase
        }}
      ,
      
       "filter": {
        "match_phrase": {
          "postag": given
        }
      }
      
    }
  } }).json()["hits"]["total"]["value"] }  for phrase in phraselist.strip().split("|") ]


if __name__ == '__main__': 
	print ( igiven()) 

'''

GET /c4-*/_search
{
  "query": {
    "bool": {
      "must": 
        {"match_phrase": {
          "postag": "funny"
        }}
      ,
      
       "filter": {
        "match_phrase": {
          "postag":"the early years"
        }
      }
      
    }
  }
}

GET /c4-1/_search
{ 
    "query": {
        "ids" : {
            "type" : "_doc",
            "values" : ["bc343eab29888c137904ebf8f3ee47cc"]
			}
		}
	}


POST /c4-1/_search
{
  "query": {
    "match_phrase": {
      "postag":"as soon as _ADV possible"
    }
  }
}


GET /clec/_search
{
  "query": { "match": {"type": "snt"}   }, 
  "size":0,
  "aggs": {
    "myagg": {
      "terms": {
        "field": "kps",
         "include": "dobj:have_VERB:NOUN_dream"
      },
    "aggs" : {
                "snt" : {
                    "top_hits": { "_source": {"includes":"snt" }, "size":5
                    }
                }
            }

    }
  }
}

GET /dic/_search
{
  "size":0,
  "aggs": {
    "myagg": {
      "terms": {
        "field": "kps",
         "include": "VERB:sound|ADJ:sound|ADV:sound|NOUN:sound"
      }
    }
  }
}

GET /dic/_search
{
  "size":0,
  "aggs": {
    "myagg": {
      "terms": {
        "field": "kps",
         "include": "VERB:.*",
         "size":10000
      }
    }
  }
}
'''