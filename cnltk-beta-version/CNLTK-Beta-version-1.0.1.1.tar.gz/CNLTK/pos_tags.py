import pickle
from importlib import resources
import io


# INDEXED TAG OF TRAINED CORPUS
def get_POS_TAGS_index():
    # Load the pickle file
    # with open("models/tagindex_model.pkl", "rb") as f:
    #     tagindex_model = pickle.load(f)
        
    pos_tags = 'tagindex_model.pkl'

    with resources.open_binary('CNLTK', pos_tags) as ptp:
        pos_tags = ptp.read()
    
    pos_tags = io.BytesIO(pos_tags)
    return pos_tags

get_POS_TAGS_index()