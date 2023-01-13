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
from attention import attention

import configparser
import h5py

from pathlib import Path

# from config import vocabs_pkl_filepath, pos_h5_filepath

# with open(vocabs_pkl_filepath, "rb") as f:
#         vocab_model = pickle.load(f)

file = Path('config.ini')
config = configparser.ConfigParser()
config.read(file)


# vocabs_pkl_filepath = config['PATHS']['vocabs_pkl_filepath']
vocabs_pkl_filepath = config.get('PATHS', 'vocabs_pkl_filepath')
# pos_h5_filepath = config['PATHS']['pos_h5_filepath']
pos_h5_filepath = config.get('PATHS', 'pos_h5_filepath')

with open(vocabs_pkl_filepath, "rb") as f:
    vocab_model = pickle.load(f)

modelx = h5py.File(pos_h5_filepath, 'r')



def POS_TAGGER_MODEL(test_samples):
    # Register the custom layer
    custom_objects = {'attention': attention}

    model2 = keras.models.load_model(modelx, custom_objects={'attention': attention, "CRF": CRF, 'crf_loss': crf_loss,'crf_viterbi_accuracy': crf_viterbi_accuracy}, compile=True)
    model2.compile(optimizer=tf.optimizers.Adam(lr=0.008), loss=losses.crf_loss, metrics=[tf.keras.metrics.Recall(),tf.keras.metrics.AUC(),tf.keras.metrics.Precision(),'accuracy'])
    # model2.summary()

    test_samples_X = []
    for s in test_samples:
        s_int = []
        for w in s:
            try:
                s_int.append(vocab_model[w.lower()])
            except KeyError:
                s_int.append(vocab_model['<_UNK_>'])
        test_samples_X.append(s_int)
    
    test_samples_X = pad_sequences(test_samples_X, maxlen=70, padding='post')

    predictions = model2.predict(test_samples_X)
    
    return predictions
    
    
def logits_to_tokens(sequences, index):
    token_sequences = []
    for categorical_sequence in sequences:
        token_sequence = []
        for categorical in categorical_sequence:
            token_sequence.append(index[np.argmax(categorical)])
 
        token_sequences.append(token_sequence)
 
    return token_sequences