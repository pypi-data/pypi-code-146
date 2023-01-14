class Tokenizer:
    sample = ['영상미 대사 임수정 외모 모두 최고',
             '약간 동심 가지 충분히 재미나 매력적 영화 박사 정말 너무 좋 ㅋㅋ ㅋ',
             '재밌 ㅎㅎ 또 보 영화',
             '필름 정말 정말 미안',
             '연기 도연 기 스토리 졸라 이상 얼마나 편집',
             '오늘 과학 날 행사 있 이 영화 보 재미 좀 그렇', ]
    word_index = None

    def __init__(self, num_words=None):
        self.num_words = num_words


    def fit_on_texts(self, texts):
        import numpy as np
        from nltk import FreqDist

        # 단어별 분리
        texts_splitted = []
        for sentence in texts:
            texts_splitted.append(sentence.split())

        self.word_index = dict(FreqDist(np.hstack(texts_splitted)))
