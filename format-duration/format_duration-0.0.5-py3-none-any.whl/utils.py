from typing import Optional, List


def contains_word(string: str, word: str) -> bool:
    return f' {word} ' in f' {string} '


def find_words(string: str, words: List[str]) -> Optional[str]:
    return next((w for w in words if contains_word(string, w)), None)
