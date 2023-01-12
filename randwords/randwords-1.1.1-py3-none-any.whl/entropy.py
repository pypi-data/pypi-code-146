import math
import string

def calculate_corpus(corpus_size, selection_size):
    return math.log2(corpus_size) * selection_size

def calculate_chars(value):
    charset_remaining = set(value)
    char_entropy = len(string.ascii_lowercase) if len(charset_remaining.intersection(string.ascii_lowercase)) > 0 else 0
    charset_remaining.difference_update(string.ascii_lowercase)

    char_entropy += len(string.ascii_uppercase) if len(charset_remaining.intersection(string.ascii_uppercase)) > 0 else 0
    charset_remaining.difference_update(string.ascii_uppercase)

    char_entropy += len(string.digits) if len(charset_remaining.intersection(string.digits)) > 0 else 0
    charset_remaining.difference_update(string.digits)

    char_entropy += len(charset_remaining)
    return math.log2(char_entropy) * len(value)
