import keras
import re
import string
import tensorflow
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

from keras.layers import *
from keras.models import *
from keras import backend as K

from keras_contrib.layers.crf import CRF, crf_loss, crf_viterbi_accuracy
from keras_contrib import losses

import pickle

from POS_MODEL import POS_TAGGER_MODEL, logits_to_tokens

import configparser
from pathlib import Path

ceb_stopwords = [
    "ako",
    "amua",
    "ato",
    "busa",
    "ikaw",
    "ila",
    "ilang",
    "imo",
    "imong",
    "iya",
    "iyang",
    "kaayo",
    "kana",
    "kaniya",
    "kaugalingon",
    "kay",
    "kini",
    "kinsa",
    "kita",
    "lamang",
    "mahimong",
    "mga",
    "mismo",
    "nahimo",
    "nga",
    "pareho",
    "pud",
    "sila",
    "siya",
    "unsa"
]


def remove_stopwords(text):
    return " ".join([word for word in text.split() if word.lower() not in ceb_stopwords])


# Load the pickle file
# with open("models/tagindex_model.pkl", "rb") as f:
#     tagindex_model = pickle.load(f)


file = Path('config.ini')
config = configparser.ConfigParser()
config.read(file)

# postagsindex_pkl_filepath = config['PATHS']['postagsindex_pkl_filepath']
postagsindex_pkl_filepath = config.get('PATHS', 'postagsindex_pkl_filepath')

with open(postagsindex_pkl_filepath, "rb") as f:
    tagindex_model = pickle.load(f)



def predict_POS_model():
    test_samples = []

    test_sample = input('INPUT YOUR TEST SENTENCE: ')
    
    # decide = input('DO YOU WANT TO PREPROCESS TEXT? Y/N: ').lower()
    
    # if decide == 'Y'.lower():
        
    #     test_sample = test_sample.lower()
    
    #     test_sample = remove_stopwords(test_sample)
        
    #     test_samples.append(test_sample.split())
    
    # else:

    test_samples.append(test_sample.split())

    max_len = len(test_samples[0])

    predictions = POS_TAGGER_MODEL(test_samples)

    predix = logits_to_tokens(predictions, {i: t for t, i in tagindex_model.items()})

    # print('\n')
    # print(test_samples[0])
    # print(predix[0][:max_len])
    sentence = test_samples[0]
    tagged = predix[0][:max_len]
    return sentence, tagged

# sentz, tagz = predict_model()
# print(sentz)
# print(tagz)

predict_POS_model()
