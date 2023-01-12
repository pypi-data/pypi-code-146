import pandas as pd

ceb_corpus = pd.read_csv('Datasets/annotatedtestxt.csv')
print(ceb_corpus)

# GET CORPUS
def cebuano_corpus():
    ceb_corpus = pd.read_csv('Datasets/annotatedtestxt.csv')
    
    return ceb_corpus