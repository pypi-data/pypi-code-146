from POS_TAGGER_MODEL import get_POS_TAGGER_model
from NER_TAGGER_MODEL import get_NER_TAGGER_model
from POS_MODEL import POS_TAGGER_MODEL, logits_to_tokens
from NER_MODEL import NER_TAGGER_MODEL, logits_to_tokens
from POS_test import predict_POS_model
from NER_test import predict_NER_model
from pos_tags import get_POS_TAGS_index
from ner_tags import get_NER_TAGS_index
from attention import attention
from ceb_corpus import cebuano_corpus
from vocabulary import get_VOCAB_model


def get_POS_TAGGER_model():
    return get_POS_TAGGER_model

def get_NER_TAGGER_model():
    return get_NER_TAGGER_model

def POS_TAGGER_MODEL():
    return POS_TAGGER_MODEL

def NER_TAGGER_MODEL():
    return NER_TAGGER_MODEL

def predict_POS_model():
    return predict_POS_model

def predict_NER_model():
    return predict_NER_model

def get_POS_TAGS_index():
    return get_POS_TAGS_index

def get_NER_TAGS_index():
    return get_NER_TAGS_index

def attention():
    return attention

def cebuano_corpus():
    return cebuano_corpus

def get_VOCAB_model():
    return get_VOCAB_model