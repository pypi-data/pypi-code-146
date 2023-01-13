import pickle
import os

# INDEXED TAG OF POS TRAINED CORPUS
def get_POS_TAGS():
    # ACCESS FILE PATH
    postagsindex_pkl_filepath = os.path.join(os.path.dirname(__file__), 'models', 'tagindex_model.pkl')

    with open(postagsindex_pkl_filepath, "rb") as f:
        postagindex_model = pickle.load(f)
        
    return postagindex_model

# INDEXED TAG OF NER TRAINED CORPUS
def get_NER_TAGS():
    # ACCESS FILE PATH
    nertagsindex_pkl_filepath = os.path.join(os.path.dirname(__file__), 'models', 'ner_tagindex_model.pkl')
    
    with open(nertagsindex_pkl_filepath, "rb") as f:
        nertagindex_model = pickle.load(f)
        
    return nertagindex_model