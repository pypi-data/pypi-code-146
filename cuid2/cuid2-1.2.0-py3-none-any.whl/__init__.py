# DO NOT CHANGE MANUALLY THIS IS CHANGED IN THE PIPELINES
__version__ = '1.2.0'

from datetime import datetime
from math import floor
from time import mktime

from cuid2.generator import (generate_entropy, generate_fingerprint,
                             generate_hash, inc_counter)
from cuid2.utils import base36_encode, random_letter


class CUID:
    def __init__(self) -> None:
        self.session_counter: int = -1

    def generate(self, length: int = 24) -> str:
        fingerprint: str = generate_fingerprint()
        entropy: str = generate_entropy(length)
        counter: str = base36_encode(inc_counter(self.session_counter))
        letter: str = random_letter()

        time: datetime = datetime.now()
        timestamp: str = base36_encode(floor(mktime(time.timetuple()) * 1000 + (time.microsecond/1000)))

        return letter + generate_hash(timestamp + entropy + counter + fingerprint, length)[1:length]
