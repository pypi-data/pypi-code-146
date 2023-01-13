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

from NER_MODEL import NER_TAGGER_MODEL, logits_to_tokens



# Load the pickle file
with open("models/ner_tagindex_model.pkl", "rb") as f:
    tagindex_model = pickle.load(f)

def predict_NER_model():
    test_samples = []

    test_sample = input('INPUT YOUR TEST SENTENCE: ')
    
    test_samples.append(test_sample.split())

    max_len = len(test_samples[0])

    predictions = NER_TAGGER_MODEL(test_samples)

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