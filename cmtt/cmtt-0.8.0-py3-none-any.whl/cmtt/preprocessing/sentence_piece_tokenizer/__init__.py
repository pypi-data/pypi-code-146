from readline import set_startup_hook
from fastai.text import *
from cmtt.preprocessing.sentence_piece_tokenizer.config import LanguageCodes
from cmtt.preprocessing.sentence_piece_tokenizer.download_assets import setup_language, verify_tokenizer_model
import sentencepiece as spm
from pathlib import Path
from typing import List

all_language_codes = LanguageCodes().get_all_language_codes()

def check_input_language(language_code: str):
    try:
        if language_code not in all_language_codes:
            raise ValueError()
    except ValueError as err:
        print("Error: Language Not Supported")
        # return -1

    if not verify_tokenizer_model(language_code):
        return -1

    return 1


path = Path(__file__).parent

class Sentencepiece_tokenizer():
    def __init__(self, lang: str):
        self.lang = lang
        if (check_input_language(self.lang)==-1):
            print("Tokenizer model not downloaded. Starting Download...")
            setup_language(self.lang)
        self.sp = spm.SentencePieceProcessor()
        model_path = path/f'models/{lang}/tokenizer.model'
        self.sp.Load(str(model_path))

    def tokenize(self, t: str) -> List[str]:
        return self.sp.EncodeAsPieces(t)

    def numericalize(self, t: str) -> List[int]:
        return self.sp.EncodeAsIds(t)

    def textify(self, ids: List[int]) -> str:
        return (''.join([self.sp.IdToPiece(id).replace('▁', ' ') for id in ids])).strip()

    def remove_foreign_tokens(self, t: str):
        local_pieces = []
        for i in self.sp.EncodeAsIds(t):
            local_pieces.append(self.sp.IdToPiece(i))
        return local_pieces

    def detokenize(self, tokens):
        if type(tokens) is list:
            text = ""
            for i in tokens:
                if "▁" in i:
                    text += " " + i[1:]
                else:
                    text += i
            return text.strip()    
        else:
            raise TypeError('Tokens needs to be of type list. Expected type list but got type ' + str(type(tokens)))

