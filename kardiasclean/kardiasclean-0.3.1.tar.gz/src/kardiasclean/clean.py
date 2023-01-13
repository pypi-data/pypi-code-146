"""Process and tokenize strings"""
import nltk
from nltk.corpus import stopwords as _stopwords
import phonetics
import pandas as pd


def split_string(column: pd.Series, delimiter: str = "+") -> pd.Series:
    """Split string by delimiter and clear whitespaces.

    Args:
        column (pd.Series): Column to clean.
        delimiter (str, optional): Delimiter without whitespaces. Defaults to "+".

    Returns:
        pd.Series: Clean column.

    Example:

        diagnosis = split_string(df['diagnosis'])
    """
    def clean(x: str):
        return [string.strip() for string in x.split(delimiter)]

    return column.map(clean)


def clean_accents(column: pd.Series) -> pd.Series:
    """Clear accents from a string.

    Args:
        column (pd.Series): Column to clean.

    Returns:
        pd.Series: Clean column.

    Example:

        data['surgery'] = clean_accents(data['surgery'])

    https://stackoverflow.com/questions/65833714/how-to-remove-accents-from-a-string-in-python
    """
    _normalize = str.maketrans(
        {
            "À": "A",
            "Á": "A",
            "Â": "A",
            "Ã": "A",
            "Ä": "A",
            "à": "a",
            "á": "a",
            "â": "a",
            "ã": "a",
            "ä": "a",
            "ª": "A",
            "È": "E",
            "É": "E",
            "Ê": "E",
            "Ë": "E",
            "è": "e",
            "é": "e",
            "ê": "e",
            "ë": "e",
            "Í": "I",
            "Ì": "I",
            "Î": "I",
            "Ï": "I",
            "í": "i",
            "ì": "i",
            "î": "i",
            "ï": "i",
            "Ò": "O",
            "Ó": "O",
            "Ô": "O",
            "Õ": "O",
            "Ö": "O",
            "ò": "o",
            "ó": "o",
            "ô": "o",
            "õ": "o",
            "ö": "o",
            "º": "O",
            "Ù": "U",
            "Ú": "U",
            "Û": "U",
            "Ü": "U",
            "ù": "u",
            "ú": "u",
            "û": "u",
            "ü": "u",
            "Ñ": "N",
            "ñ": "n",
            "Ç": "C",
            "ç": "c",
            "§": "S",
            "³": "3",
            "²": "2",
            "¹": "1",
        }
    )
    return column.str.translate(_normalize)


def clean_symbols(column: pd.Series, pattern: str = r",|\(|\)|\.") -> pd.Series:
    """Remove all symbols on a string using a regex pattern.

    Args:
        column (pd.Series): Column to clean.
        pattern (str): Any raw string with regex pattern.

    Returns:
        pd.Series: Clean column.

    Example:

        surgery = clean_symbols(data['surgery'])
    """
    return column.str.replace(pat=pattern, repl="", regex=True)


def clean_stopwords(
    column: pd.Series, language: str = "spanish", extra: list = None, lower: bool = True
) -> pd.Series:
    """Remove all stopwords from a string and returns a new sorted string.
    This function will also convert all words to lowercase before removing stopwords.

    Args:
        column (pd.Series): Column to clean.
        language (str): Language, see nltk.
        extra (list, optional): Additional stopwords to remove. Defaults to None.

    Returns:
        pd.Series: Clean column.

    Example:

        data['keywords'] = clean_stopwords(data['surgery'])
    """

    try:
        sw = _stopwords.words(language)
    except LookupError:
        nltk.download("stopwords")
        sw = _stopwords.words(language)

    sws = set([*sw, *extra]) if extra is not None else set(sw)

    def clean(x: str) -> str:
        return " ".join(word for word in sorted(set(x.split(" ")) - sws))
    
    return column.str.lower().map(clean) if lower else column.map(clean)


def clean_tokenize(column: pd.Series, algorithm: str = "metaphone") -> pd.Series:
    """Use a fuzzy string match algorithm to tokenize a string.

    Valid algorithms: metaphone, dmetaphone.

    Args:
        column (pd.Series): Column to clean.
        algorithm (str, optional): Algorithm. Defaults to 'metaphone'.

    Raises:
        ValueError: If the algorithm is not valid.

    Returns:
        pd.Series: Clean column.

    Example:
        surgery_map_df['token'] = clean_tokenize(data['keywords'])
    """
    if algorithm == "metaphone":
        return column.map(phonetics.metaphone)
    elif algorithm == "dmetaphone":
        return column.map(phonetics.dmetaphone)
    else:
        raise ValueError("Not a valid algorithm!")
