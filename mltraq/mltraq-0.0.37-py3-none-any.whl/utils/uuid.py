from mltraq.utils.wordlist import words

n_words = len(words)


def uuid3words(uuid):
    idx0 = (uuid.int + 0) % n_words
    idx1 = (uuid.int + 1) % n_words
    idx2 = (uuid.int + 2) % n_words
    return f"{words[idx0]}.{words[idx1]}.{words[idx2]}"
