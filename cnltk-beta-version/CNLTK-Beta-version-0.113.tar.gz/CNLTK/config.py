import os
import pickle

data_path = os.path.join(os.path.dirname(__file__), 'models', 'vocab_model2.pkl')

with open(data_path, 'rb') as data_file:
    vocab_model = pickle.load(data_file)
    
print(vocab_model)