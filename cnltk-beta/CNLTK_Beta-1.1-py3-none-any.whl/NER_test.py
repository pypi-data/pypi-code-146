import keras
import re
import string
import tensorflow
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

from keras.layers import *
from keras.models import *
from keras import backend as K
import os
from keras_contrib.layers.crf import CRF, crf_loss, crf_viterbi_accuracy
from keras_contrib import losses
import h5py
import pickle

class attention(Layer):
      def __init__(self, name=None, return_sequences=True, **kwargs):
        super(attention, self).__init__(name=name, **kwargs)
        self.return_sequences = return_sequences

        super(attention,self).__init__()

      def build(self, input_shape):
        self.W=self.add_weight(name="att_weight", shape=(input_shape[-1],1),
                               initializer="normal")
        self.b=self.add_weight(name="att_bias", shape=(input_shape[1],1),
                               initializer="zeros")
        
        super(attention,self).build(input_shape)


      def call(self, x):
        e = K.tanh(K.dot(x,self.W)+self.b)
        a = K.softmax(e, axis=1)
        output = x*a
        if self.return_sequences:

            return output
        return K.sum(output, axis=1)


vocabs_pkl_filepath = os.path.join(os.path.dirname(__file__), 'models', 'vocab_model2.pkl')

pos_h5_filepath = os.path.join(os.path.dirname(__file__), 'models', 'POS_TAG_WORD(1).h5')

with open(vocabs_pkl_filepath, "rb") as f:
    vocab_model = pickle.load(f)

modelx = h5py.File(pos_h5_filepath, 'r')



def POS_TAGGER_MODEL(test_samples):

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


nertagsindex_pkl_filepath = os.path.join(os.path.dirname(__file__), 'models', 'ner_tagindex_model.pkl')

with open(nertagsindex_pkl_filepath, "rb") as f:
    tagindex_model = pickle.load(f)



def predict_NER_model():
    test_samples = []

    test_sample = input('INPUT YOUR TEST SENTENCE: ')

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