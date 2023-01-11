import os
import numpy as np
import shutil
from musiclang.predict.tokenizers import ChordTokenizer

data_path = 'examples/data/training_data'
test_data = 'examples/data/test_data'
train_data = 'examples/data/train_data'
os.makedirs(test_data, exist_ok=True)
os.makedirs(train_data, exist_ok=True)
train_size = 0.80

tokenizer = ChordTokenizer()
data = os.listdir(data_path)

is_tests = np.random.random(len(data)) > train_size

for is_test, filepath in zip(is_tests, data):
    if is_test:
        shutil.copy(os.path.join(data_path, filepath), test_data)
    else:
        shutil.copy(os.path.join(data_path, filepath), train_data)
# Shuffle



