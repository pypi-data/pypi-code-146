import pandas as pd

# GET CORPUS
def cebuano_corpus():
    ceb_corpus = pd.read_csv('Datasets/annotatedtestxt.csv')
    
    return ceb_corpus