'''
Provide the basic vocabular instance.
'''

class Vocab(object):
    def __init__(self):
        self.idx2word = {}
        self.word2idx = {}
    
    def __len__(self):
        return len(self.idx2word.keys())
    
    @property
    def words(self):
        return list(self.word2idx.keys())
    
    @property
    def vocab(self):
        return self.idx2word

    def add_sentence(self, sentence):
        if isinstance(sentence, list):
            if len(sentence) == 0:
                return    
            for word in sentence:
                self._add_word(word)
        else:
            self._add_word(sentence)
    
    def _add_word(self, word):
        if word not in self.word2idx:
            self.idx2word[len(self.word2idx)] = word
            self.word2idx[word] = len(self.word2idx)