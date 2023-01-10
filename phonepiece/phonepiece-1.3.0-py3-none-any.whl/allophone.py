from phonepiece.config import *
import json


def read_allophone(lang_id):

    assert len(lang_id) == 3, "lang_id should be an ISO lang_id"

    allophone_json = allospeech_config.data_path / 'language' / lang_id / 'allophone.json'
    phoneme_file = allospeech_config.data_path / 'language' / lang_id / 'phoneme.txt'
    phone_file = allospeech_config.data_path / 'language' / lang_id / 'phone.txt'

    phone2phoneme = dict()

    if allophone_json.exists():
        # use allophone file if allovera supports it

        allo_json = json.load(open(allospeech_config.data_path / 'language' / lang_id / 'allophone.json', encoding='utf-8'))
        allo_map = allo_json['mappings']

        phone2phoneme = dict()

        for allo in allo_map:
            phone = allo['phone']
            phoneme = allo['phoneme']

            if phone == '' or phoneme == '':
                continue

            if phone in phone2phoneme:
                phone2phoneme[phone].append(phoneme)
            else:
                phone2phoneme[phone] = [phoneme]


    elif phoneme_file.exists():
        # use phoneme file, we assume each phoneme is a phone

        for line in open(phoneme_file, encoding='utf-8'):
            phoneme = line.strip().split()[0]
            phone2phoneme[phoneme] = [phoneme]

    elif phone_file.exists():
        # use phone file, we assume each phone is a phoneme

        for line in open(phone_file, encoding='utf-8'):
            phone = line.strip().split()[0]
            phone2phoneme[phone] = [phone]

    #elif temp_file.exists():
    #    print("loading from temporary data")
    #    for line in open(temp_file, encoding='utf-8'):
    #        phoneme = line.strip().split()[0]
    #        phone2phoneme[phoneme] = [phoneme]

    else:
        raise FileNotFoundError

    return Allophone(lang_id, phone2phoneme)

class Allophone:

    def __init__(self, lang_id, phone2phoneme_dict):

        self.lang_id = lang_id

        self.phone2phoneme_dict = phone2phoneme_dict

        self.phoneme2phone_dict = dict()

        self.phone_set = set()
        self.phoneme_set = set()

        for phone, phonemes in phone2phoneme_dict.items():

            for phoneme in phonemes:

                self.phone_set.add(phone)
                self.phoneme_set.add(phoneme)

                if phoneme in self.phoneme2phone_dict:
                    self.phoneme2phone_dict[phoneme].append(phone)
                else:
                    self.phoneme2phone_dict[phoneme] = [phone]

    def __repr__(self):
        return "<Allophone lang_id: "+self.lang_id+" phones: "+str(len(self.phone_set))+" phonemes: "+str(len(self.phoneme_set))+">"

    def __str__(self):
        return self.__repr__()


    def phones(self):
        return list(sorted(self.phone_set))

    def phonemes(self):
        return list(sorted(self.phoneme_set))

    def phone2phoneme(self, phone):
        assert phone in self.phone2phoneme_dict
        return self.phone2phoneme_dict[phone]

    def phoneme2phone(self, phoneme):
        assert phoneme in self.phoneme_set
        return self.phoneme2phone_dict[phoneme]