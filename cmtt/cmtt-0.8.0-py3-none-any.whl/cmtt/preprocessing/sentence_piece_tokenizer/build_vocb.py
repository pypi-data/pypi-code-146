from fastai.text import * 
from pathlib import *

import sentencepiece as spm

# Path to the directory containing the training files
path = pathlib.Path(r'')

p = path.glob('**/*')
files = [x for x in p if x.is_file()]
files = [str(file) for file in files]
flist = ','.join(files)

custom_symbols = [text.transform.FLD, 
                text.transform.TK_MAJ,
                text.transform.TK_UP,
                text.transform.TK_REP,
                text.transform.TK_WREP]

str_specialcases = ",".join(custom_symbols)

# Trained Models uploaded to the CMTT cloud
spm.SentencePieceTrainer.Train(f'--input={flist} --model_prefix=hinDev_engRom --vocab_size=60000 --input_sentence_size=22500000 --unk_id=0 --bos_id=1 --eos_id=2 --pad_id=3 --unk_piece={text.transform.UNK} --bos_piece={text.transform.BOS} --eos_piece={text.transform.EOS} --pad_piece={text.transform.PAD} --user_defined_symbols={str_specialcases}')