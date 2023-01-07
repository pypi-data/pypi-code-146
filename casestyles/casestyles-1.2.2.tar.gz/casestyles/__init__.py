from typing import Callable

__all__ = ["Word", "Name"]

class Word:
    class EmptyValueError(Exception):
        def __init__(self) -> None:
            super().__init__("the value can't be empty")

    class NotLowerValueError(Exception):
        def __init__(self) -> None:
            super().__init__("the value must be lower")

    class NotEnglishValueError(Exception):
        def __init__(self) -> None:
            super().__init__("the value must contain only english letters")

    _value: str
    
    def get(self):
        return self._value

    def set(self, value: str):
        if not value:
            raise self.EmptyValueError

        if not value.islower():
            raise self.NotLowerValueError

        if not value.isalnum():
            raise self.NotEnglishValueError
        
        self._value = value


    def __init__(self, value: str):
        self.set(value)

    def __str__(self):
        return self.get()

class Name:
    class EmptyWordError(Exception):
        def __init__(self) -> None:
            super().__init__("each word in name must not be empty")

    class NotLowerWordError(Exception):
        def __init__(self) -> None:
            super().__init__("each word in name must not be lower")

    class NotEnglishWordError(Exception):
        def __init__(self) -> None:
            super().__init__("each word in name must be alphabet-numeric")

    class NotLowerWordInSnakeCaseError(Exception):
        def __init__(self) -> None:
            super().__init__("each word in snake case name must not be lower")

    class InnerError(Exception):
        def __init__(self) -> None:
            super().__init__("inner error")

    class UnderscoreError(Exception):
        def __init__(self) -> None:
            super().__init__("double underscore and underscores at the and at start in name are not allowed")

    _words: list[Word]
    _cache: dict[Callable[[], str], str]

    def __init__(self, words: list[Word]):
        self._words = words
        self._cache = {}

    @classmethod
    def _create_name(cls, words: list[Word]):
        return Name(words)

    @classmethod
    def _create_word(cls, value: str) -> Word:
        return Word(value)

    @classmethod
    def from_words_str_list(cls, words: list[str]):
        try:
            return cls._create_name(list(map(cls._create_word, words)))
        
        except Word.EmptyValueError:
            raise cls.EmptyWordError

        except Word.NotLowerValueError:
            raise cls.NotLowerWordError

        except Word.NotEnglishValueError:
            raise cls.NotEnglishWordError

    @classmethod
    def from_snake_case(cls, value: str) -> "Name":
        try:
            result = cls.from_words_str_list(value.split("_"))
            result._cache[result._to_snake_case] = value
            return result

        except cls.NotLowerWordError:
            raise cls.NotLowerWordInSnakeCaseError

        except cls.EmptyWordError:
            raise cls.UnderscoreError

    @classmethod
    def from_camel_case(cls, value: str) -> "Name":
        words_str: list[str] = []
        word_str = ""
        for symbol in value:
            if symbol.isupper():
                words_str.append(word_str)
                word_str = ""
            word_str += symbol.lower()
        words_str.append(word_str)
        try:
            result = cls.from_words_str_list(words_str)
            result._cache[result._to_camel_case] = value
            return result
        
        except (cls.EmptyWordError, cls.NotLowerWordError):
            raise cls.InnerError
    
    @classmethod
    def from_pascal_case(cls, value: str) -> "Name":
        result = cls.from_camel_case(value[:1].lower()+value[1:])
        result._cache[result._to_pascal_case] = value
        return result

    def _to_snake_case(self):
        return "_".join(map(str, self._words))

    def _to_camel_case(self):
        pascal_case = self.pascal_case
        return pascal_case[:1].lower() + pascal_case[1:]

    def _to_pascal_case(self) -> str:
        return "".join(map(lambda word: str(word).capitalize(), self._words))

    def _cached(self, getter: Callable[[], str]):
        if not (result := self._cache.get(getter)):
            result = getter()
            self._cache[getter] = result
        return result

    @property
    def snake_case(self) -> str:
        return self._cached(self._to_snake_case)

    @property
    def camel_case(self) -> str:
        return self._cached(self._to_camel_case)

    @property
    def pascal_case(self) -> str:
        return self._cached(self._to_pascal_case)

    @property
    def words_str_list(self) -> list[str]:
        return list(map(lambda word: word.get(), self._words))

    def __hash__(self):
        return hash(self.snake_case)

    def __eq__(self, other: object):
        if not isinstance(other, Name):
            return False
        return self.camel_case == other.camel_case