import hashlib
import random
import string
from time import time

from django.conf import settings


def create_random_str(length: int):
    seed = f"{random.getstate()}{time()}{settings.SECRET_KEY}"
    random.seed(hashlib.sha256(seed.encode()).digest())
    return "".join(random.choice(string.printable) for _ in range(length))


__all__ = ['create_random_str']
