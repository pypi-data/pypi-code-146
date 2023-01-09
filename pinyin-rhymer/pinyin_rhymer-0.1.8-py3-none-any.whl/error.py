class NotAPinYinError(Exception):
    def __init__(self, string):
        message = f'"{string}" is not a valid pinyin.'
        super().__init__(message)


class IrregularPinYinError(Exception):
    def __init__(self, string):
        message = f'"{string}" is an irregular pinyin, handle it manually for now.'
        super().__init__(message)


class NotAConsonantError(Exception):
    def __init__(self, string):
        message = f'"{string}" is not a valid consonant.'
        super().__init__(message)


class NotAVowelError(Exception):
    def __init__(self, string):
        message = f'"{string}" is not a valid vowel.'
        super().__init__(message)


class NotARhymeSchemeError(Exception):
    def __init__(self, string, scheme_name):
        message = f'"{string}" is not a valid {scheme_name}.'
        super().__init__(message)
