import pickle
import configparser

# INDEXED TAG OF TRAINED CORPUS
def get_POS_TAGS_index():
    # Load the pickle file
    # with open("models/tagindex_model.pkl", "rb") as f:
    #     tagindex_model = pickle.load(f)
    
    file = 'config.ini'
    config = configparser.ConfigParser()
    config.read(file)

    postagsindex_pkl_filepath = config['PATHS']['postagsindex_pkl_filepath']

    with open(postagsindex_pkl_filepath, "rb") as f:
        tagindex_model = pickle.load(f)
        
    return tagindex_model

print(get_POS_TAGS_index())