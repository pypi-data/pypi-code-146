import pandas as pd

ceb_corpus = pd.read_csv('CNLTK/Datasets/annotatedtestxt.csv')
print(ceb_corpus)

# GET CORPUS
def cebuano_corpus():
    ceb_corpus = pd.read_csv('CNLTK/Datasets/annotatedtestxt.csv')
    
    return ceb_corpus