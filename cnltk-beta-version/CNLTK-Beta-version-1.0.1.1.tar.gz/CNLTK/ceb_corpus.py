import pandas as pd
from importlib import resources
import io

corpus_path = 'annotatedtestxt.csv'

with resources.open_binary('CNLTK', corpus_path) as cp:
    corpus = cp.read()

ceb_corpus = pd.read_csv(io.BytesIO(corpus))
print(ceb_corpus)

# GET CORPUS
def cebuano_corpus():
    # ceb_corpus = pd.read_csv(io.BytesIO(corpus))
    corpus_path = 'annotatedtestxt.csv'

    with resources.open_binary('CNLTK', corpus_path) as cp:
        ceb_corpus = cp.read()
        
    ceb_corpus = io.BytesIO(ceb_corpus)
    return ceb_corpus

cebuano_corpus()