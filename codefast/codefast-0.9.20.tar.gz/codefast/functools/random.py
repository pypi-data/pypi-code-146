import random
import string


def random_string(length: int = 10) -> str:
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))

def sample_one(l: list) -> str:
    return random.choice(l)

def sample(l: list, number: int) -> list:
    return random.sample(l, number)

def shuffle(l: list) -> list:
    random.shuffle(l)
    return l

def hex(length: int = 10) -> str:
    return ''.join(random.choice(string.hexdigits) for i in range(length))
