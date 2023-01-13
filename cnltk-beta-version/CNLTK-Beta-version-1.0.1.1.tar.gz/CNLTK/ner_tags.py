import pickle
from importlib import resources
import io


# INDEXED TAG OF TRAINED CORPUS
def get_NER_TAGS_index():
    # Load the pickle file
    # with open("models/ner_tagindex_model.pkl", "rb") as f:
    #     tagindex_model = pickle.load(f)
    
    ner_tags_path = 'ner_tagindex_model.pkl'
    
    with resources.open_binary('CNLTK', ner_tags_path) as ntp:
        ner_tags = ntp.read()
        
    ner_tags = io.BytesIO(ner_tags)
        
    return ner_tags



get_NER_TAGS_index()
