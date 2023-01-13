import keras
import re
import string
import h5py
import os
import tensorflow
import numpy as np

from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.layers import *
from keras.models import *
from keras import backend as K

from keras_contrib.layers.crf import CRF, crf_loss, crf_viterbi_accuracy
from keras_contrib import losses



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


# LOAD NER TAGGER MODEL
def get_NER_TAGGER_model():
    # ACCESS FILE PATH
    ner_h5_filepath = os.path.join(os.path.dirname(__file__), 'models', 'NER_WORD(1).h5')
    
    modelx = h5py.File(ner_h5_filepath, 'r')
    model2 = keras.models.load_model(modelx, custom_objects={'attention': attention, "CRF": CRF, 'crf_loss': crf_loss,'crf_viterbi_accuracy': crf_viterbi_accuracy}, compile=True)
    model2.compile(optimizer=tf.optimizers.Adam(lr=0.008), loss=losses.crf_loss, metrics=[tf.keras.metrics.Recall(),tf.keras.metrics.AUC(),tf.keras.metrics.Precision(),'accuracy'])
    model2.summary()
    
    return model2