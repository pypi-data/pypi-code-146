from allospeech.lm.tokenizer import Tokenizer
from allospeech.lm.phone.transliterator import Transliterator
import torch

class PhoneTokenizer(Tokenizer):

    def __init__(self, config):
        self.config = config
        self.default_lang_id = self.config.default_lang_id
        self.trans = {}


    def __repr__(self):
        return f"<PhoneTokenizer />"

    def tokenize(self, sent, lang_id=None):

        if lang_id is None:
            lang_id = self.default_lang_id

        if lang_id not in self.trans:
            trans = Transliterator(lang_id)
            self.trans[lang_id] = trans

        trans = self.trans[lang_id]

        words = sent.split()

        ipa_lst = []
        for word in words:
            ipa_lst.extend(trans.get_ipa(word))

        return torch.LongTensor(ipa_lst)

    def compute(self, sent, lang_id=None):

        if lang_id is None:
            lang_id = self.default_lang_id

        if lang_id not in self.trans:
            trans = Transliterator(lang_id)
            self.trans[lang_id] = trans

        trans = self.trans[lang_id]

        words = sent.split()

        id_lst = []
        for word in words:
            id_lst.extend(trans.get_id(word))

        return torch.LongTensor(id_lst)