__version__ = '0.1.8'

from pinyin_rhymer.data.pinyin_list import PINYIN_LIST, PINYIN_ZI_DICT
from pinyin_rhymer.pinyin import PinYin


def rhyme_with(source, consonants, vowels, tones):
    pinyin = PinYin(source)
    return pinyin.generate_rhymes(consonants, vowels, tones)
