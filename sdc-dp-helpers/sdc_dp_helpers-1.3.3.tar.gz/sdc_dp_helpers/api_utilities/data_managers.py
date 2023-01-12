import re


def multiple_regex_replace(text: str, replace_map: dict) -> str:
    """Replace multiple Regex Patterns in one go
    @param: replace_map - dict of key (what to replace) value (replacements)
                            i.e {".": "_dot_", "+": "_plus_", " ":"_space_"}
    @param: text - string to perform the regex substititution on.
    """
    # Create a regular expression  from the dictionaryionary keys
    # regex = re.compile("(%s)" % "|".join(map(re.escape, replace_map.keys())))
    regex = re.compile(f"({'|'.join(map(re.escape, replace_map.keys()))})")

    # For each match, look-up corresponding value in dictionaryionary
    return regex.sub(lambda mo: replace_map[mo.string[mo.start() : mo.end()]], text)
