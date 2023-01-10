import epitran
from epitran.xsampa import XSampa
import panphon
from allospeech.lm.unit import *
from allospeech.lm.phone.allophone import *
from allospeech.lm.phone.articulatory import *


def read_phoneme(lang_id):

    allophone = read_allophone(lang_id)
    phonemes = allophone.phonemes()

    phoneme_dict = dict()

    phoneme_dict['<blk>'] = 0

    for i, phoneme in enumerate(phonemes):
        phoneme_dict[phoneme]=i+1

    # temporarily allocate <eos> here
    phoneme_dict['<eos>'] = len(phoneme_dict)

    return Phoneme(lang_id, phoneme_dict, allophone)


class Phoneme(Unit):

    def __init__(self, lang_id, phoneme_dict, allophone):
        super().__init__(phoneme_dict)

        self.lang_id = lang_id
        self.allophone = allophone

        self.articulatory = Articulatory()
        self.nearest_mapping = dict()


    def get_nearest_phoneme(self, phoneme):

        # special handling for :
        if phoneme.endswith('ː') and phoneme[:-1] in self.unit_to_id:
            self.nearest_mapping[phoneme] = phoneme[:-1]
            return phoneme[:-1]

        if phoneme in self.nearest_mapping:
            nearest_phoneme = self.nearest_mapping[phoneme]

        else:

            target_phonemes = list(self.unit_to_id.keys())[1:]
            nearest_phoneme = self.articulatory.most_similar(phoneme, target_phonemes)
            self.nearest_mapping[phoneme] = nearest_phoneme

        return nearest_phoneme