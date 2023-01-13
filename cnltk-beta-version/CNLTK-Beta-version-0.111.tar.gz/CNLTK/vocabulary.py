import pickle
import configparser
import os
from pathlib import Path

# VOCABULARY OF THE MODEL
def get_VOCAB_model():
    # with open(vocabs_pkl_filepath, "rb") as f:
    #     vocab_model = pickle.load(f)
    
    # file = Path('config.ini')
    # config = configparser.ConfigParser()
    # config.read(file)
    
    # vocabs_pkl_filepath = Path('models/vocab_model2.pkl')
    # vocabs_pkl_filepath = config['PATHS']['vocabs_pkl_filepath']
    # vocabs_pkl_filepath = config.get('PATHS', 'vocabs_pkl_filepath')

    # with open(vocabs_pkl_filepath, "rb") as f:
    #     vocab_model = pickle.load(f)
    
    data_path = os.path.join(os.path.dirname(__file__), 'models', 'vocab_model2.pkl')

    with open(data_path, 'rb') as data_file:
        vocab_model = pickle.load(data_file)
    
    return vocab_model

get_VOCAB_model()