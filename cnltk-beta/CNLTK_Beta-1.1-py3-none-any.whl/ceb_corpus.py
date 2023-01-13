import pandas as pd
import os

# GET CORPUS
# FUNCTION IN ACCESSING THE ANNOTATED CEBUANO CORPUS USED TO TRAIN THE MODEL
def cebuano_corpus():
   
    # ACCESS FILE PATH
    corpus_csv_filepath = os.path.join(os.path.dirname(__file__), 'Datasets', 'annotatedtestxt.csv')

    corpus_csv_filepath = pd.read_csv(corpus_csv_filepath)
    
    return corpus_csv_filepath
