import pickle
import configparser

from pathlib import Path

# VOCABULARY OF THE MODEL
def get_VOCAB_model():
    # with open(vocabs_pkl_filepath, "rb") as f:
    #     vocab_model = pickle.load(f)
    
    file = Path('config.ini')
    config = configparser.ConfigParser()
    config.read(file)

    # vocabs_pkl_filepath = config['PATHS']['vocabs_pkl_filepath']
    vocabs_pkl_filepath = config.get('PATHS', 'vocabs_pkl_filepath')

    with open(vocabs_pkl_filepath, "rb") as f:
        vocab_model = pickle.load(f)
    
    return vocab_model

print(get_VOCAB_model())