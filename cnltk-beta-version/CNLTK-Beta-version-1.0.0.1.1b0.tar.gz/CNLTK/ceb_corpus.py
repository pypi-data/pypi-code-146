import pandas as pd
import configparser
import config


# GET CORPUS
def cebuano_corpus():
    ceb_corpus = pd.read_csv(config.corpus_csv_filepath)
    
    # file = 'config.ini'
    # config = configparser.ConfigParser()
    # config.read(file)

    # corpus_csv_filepath = config['PATHS']['corpus_csv_filepath']

    # corpus_csv_filepath = pd.read_csv(corpus_csv_filepath)
    
    return ceb_corpus

cebuano_corpus()