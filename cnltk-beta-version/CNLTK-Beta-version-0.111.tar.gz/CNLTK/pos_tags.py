import pickle
import configparser
from pathlib import Path

# INDEXED TAG OF TRAINED CORPUS
def get_POS_TAGS_index():
    # Load the pickle file
    # with open(postags_pkl_filepath, "rb") as f:
    #     tagindex_model = pickle.load(f)
    
    file = Path('config.ini')
    config = configparser.ConfigParser()
    config.read(file)

    # postagsindex_pkl_filepath = config['PATHS']['postagsindex_pkl_filepath']
    # postagsindex_pkl_filepath = config.get('postagsindex_pkl_filepath')
    postagsindex_pkl_filepath = Path('models/tagindex_model.pkl')

    with open(postagsindex_pkl_filepath, "rb") as f:
        tagindex_model = pickle.load(f)
        
    return tagindex_model

get_POS_TAGS_index()