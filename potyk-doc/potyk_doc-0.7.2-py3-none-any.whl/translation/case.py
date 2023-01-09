from enum import Enum


class Case(str, Enum):
    Nominative = "именительный"
    Genitive = "родительный"
    Prepositional = "предложный"
    Dative = "дательный"
