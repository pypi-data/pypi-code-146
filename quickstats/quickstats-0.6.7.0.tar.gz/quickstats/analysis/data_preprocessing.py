from typing import Optional, Union, List, Dict

import numpy as np

from quickstats import DescriptiveEnum

class NegativeWeightMode(DescriptiveEnum):
    DONOTHING = (0, "do not apply any correction to negative weight")
    SETZERO   = (1, "set negative weight to 0")
    SETABS    = (2, "set negative weight to its absolute value")

def fix_negative_weights(df, mode:Union[int, NegativeWeightMode, str]=0,
                         weight_col:str="weight"):
    mode = NegativeWeightMode.parse(mode)
    if mode == NegativeWeightMode.DONOTHING:
        return None
    mask = df[weight_col] < 0
    if mode == NegativeWeightMode.SETZERO:
        df[weight_col][mask] = 0
    elif mode == NegativeWeightMode.SETABS:
        df[weight_col][mask] = abs(df[weight_col][mask])
        
def shuffle_arrays(*arrays, random_state:Optional[int]=None):
    if random_state < 0:
        return arrays
    from sklearn.utils import shuffle
    return shuffle(*arrays, random_state=random_state)

def get_class_label_encodings(class_labels:Union[List, np.ndarray]):
    from sklearn import preprocessing
    encodings = {}
    labelencoder = preprocessing.LabelEncoder()
    labelencoder.fit_transform(class_labels)
    encodings = dict(zip(labelencoder.classes_, np.arange(len(class_labels))))
    return encodings