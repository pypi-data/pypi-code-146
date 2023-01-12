import pickle

with open("CNLTK/models/tagindex_model.pkl", "rb") as f:
        tagindex_model = pickle.load(f)
        
print(tagindex_model)

# INDEXED TAG OF TRAINED CORPUS
def get_POS_TAGS_index():
    # Load the pickle file
    with open("CNLTK/models/tagindex_model.pkl", "rb") as f:
        tagindex_model = pickle.load(f)
        
    return tagindex_model
