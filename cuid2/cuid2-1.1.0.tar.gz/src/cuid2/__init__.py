# DO NOT CHANGE MANUALLY THIS IS CHANGED IN THE PIPELINES
__version__ = '1.1.0'

from datetime import datetime
from math import floor
from secrets import SystemRandom
from time import mktime

from cuid2.generator import (generate_entropy, generate_fingerprint,
                             generate_hash)
from cuid2.utils import base36_encode, random_letter


def cuid(length: int = 24) -> str:
    generator: SystemRandom = SystemRandom()
    fingerprint: str = generate_fingerprint()
    entropy: str = generate_entropy(length)
    counter: str = base36_encode(int(generator.random() * 2057) + 1)
    letter: str = random_letter()

    time: datetime = datetime.now()
    timestamp: str = base36_encode(floor(mktime(time.timetuple()) * 1000 + (time.microsecond/1000)))

    return letter + generate_hash(timestamp + entropy + counter + fingerprint, length)[1:length]
