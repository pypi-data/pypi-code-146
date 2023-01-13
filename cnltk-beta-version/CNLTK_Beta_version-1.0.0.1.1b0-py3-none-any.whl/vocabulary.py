import pickle
import configparser
import config

# VOCABULARY OF THE MODEL
def get_VOCAB_model():
    with open(config.vocabs_pkl_filepath, "rb") as f:
        vocab_model = pickle.load(f)
    
    # file = 'config.ini'
    # config = configparser.ConfigParser()
    # config.read(file)

    # vocabs_pkl_filepath = config['PATHS']['vocabs_pkl_filepath']

    # with open(vocabs_pkl_filepath, "rb") as f:
    #     vocab_model = pickle.load(f)
    
    return vocab_model

get_VOCAB_model()