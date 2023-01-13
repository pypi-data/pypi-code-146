import pickle
import configparser
from pathlib import Path
import os

# INDEXED TAG OF TRAINED CORPUS
def get_POS_TAGS_index():
    
    postagsindex_pkl_filepath = os.path.join(os.path.dirname(__file__), 'models', 'tagindex_model.pkl')

    with open(postagsindex_pkl_filepath, "rb") as f:
        tagindex_model = pickle.load(f)
        
    return tagindex_model

get_POS_TAGS_index()