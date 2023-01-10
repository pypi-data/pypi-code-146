"""Utils for modifying MCLI Configs"""
import random
import string


def uuid_generator(length: int = 10) -> str:
    allowed_characters = string.ascii_lowercase + string.digits
    items = random.choices(population=allowed_characters, k=length)
    return ''.join(items)
