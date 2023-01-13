import pandas as pd
import configparser
from pathlib import Path


# GET CORPUS
def cebuano_corpus():
    # ceb_corpus = pd.read_csv(corpus_csv_filepath)
    
    file = Path('config.ini')
    config = configparser.ConfigParser()
    config.read(file)

    # corpus_csv_filepath = config['PATHS']['corpus_csv_filepath']
    # corpus_csv_filepath = config.get('PATHS', 'corpus_csv_filepath')
    corpus_csv_filepath = Path('Datasets/annotatedtestxt.csv')

    corpus_csv_filepath = pd.read_csv(corpus_csv_filepath)
    
    return corpus_csv_filepath

cebuano_corpus()