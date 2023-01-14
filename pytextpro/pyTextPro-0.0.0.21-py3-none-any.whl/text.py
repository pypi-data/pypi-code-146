class Tokenizer:
    sample = ['영상미 대사 임수정 외모 모두 최고',
             '약간 동심 가지 충분히 재미나 매력적 영화 박사 정말 너무 좋 ㅋㅋ ㅋ',
             '재밌 ㅎㅎ 또 보 영화',
             '필름 정말 정말 미안',
             '연기 도연 기 스토리 졸라 이상 얼마나 편집',
             '오늘 과학 날 행사 있 이 영화 보 재미 좀 그렇', ]
    word_index = None
    word_freq = None

    def __init__(self, num_words=None):
        self.num_words = num_words

    def split_texts(self, texts):
        """split texts by space"""
        texts_splitted = []
        for sentence in texts:
            texts_splitted.append(sentence.split(' '))
        return texts_splitted

    def word_index_of_freq(self, texts_splitted):
        """make self.word_index by frequency"""
        import numpy as np
        from collections import Counter

        stacked = Counter(np.hstack(texts_splitted))
        keys = sorted(stacked, reverse=False)                  # sort by name
        keys = sorted(keys, key=stacked.get, reverse=True)     # sort by value
        values = sorted(stacked.values(), reverse=True)
        word_idx = {}
        for key in keys:
            for value in values:
                word_idx[key] = value
                values.remove(value)
                break
        self.word_freq = word_idx

    def word_index_of_order(self, texts_splitted):
        """make self.word_index by frequency order"""
        import numpy as np
        from collections import Counter

        stacked = Counter(np.hstack(texts_splitted))
        keys = sorted(stacked, reverse=False)               # sort by name
        keys = sorted(keys, key=stacked.get, reverse=True)  # sort by value
        word_idx = {}
        cnt = 0
        for key in keys:
            cnt += 1
            word_idx[key] = cnt
        self.word_index = word_idx

    def words_freq(self, texts):
        """
        Make word-index dictionary of frequency
        :param texts:
        :return: return word-index dictionary of frequency through object's attributes (tokenizer.word_index)
        """
        # split texts by space
        texts_splitted = self.split_texts(texts)

        # make self.word_index
        self.word_index_of_freq(texts_splitted)

    def fit_on_texts(self, texts):
        """
        Make word-index dictionary of frequency order
        :param texts: word sentences list
        :return: return word-index dictionary through object's attributes (tokenizer.word_index)
        """
        import numpy as np
        from collections import Counter

        # split texts by space
        texts_splitted = self.split_texts(texts)

        # make self.word_index
        self.word_index_of_order(texts_splitted)

    def texts_to_sequences(self, texts):
        """
        Replace words with index sequences
        :param texts: word sentences list
        :return: index sequences list
        """
        # split texts by space
        texts_splitted = self.split_texts(texts)

        sequences = []
        for text in texts_splitted:
            sequence = []
            for word in text:
                try:
                    sequence.append(self.word_index[word])
                except KeyError:
                    pass
            sequences.append(sequence)

        return sequences
