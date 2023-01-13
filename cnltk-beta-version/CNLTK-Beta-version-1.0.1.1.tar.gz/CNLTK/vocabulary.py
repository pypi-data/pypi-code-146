import pickle
from importlib import resources
import io


# VOCABULARY OF THE MODEL
def get_VOCAB_model():
    # with open("models/vocab_model2.pkl", "rb") as f:
    #     vocab_model = pickle.load(f)
    
    vocab_model = 'vocab_model2.pkl'

    with resources.open_binary('CNLTK', vocab_model) as vp:
        vocab_model = vp.read()
    
    vocab_model = io.BytesIO(vocab_model)
        
    return vocab_model