def match_iterator_pattern(pattern, iterator, default=None):
    """
    Iterates through the iterator and attempts to match each item with the given pattern. If a match is found, it returns
    the first group of the match. If no match is found in the iterator, it returns the default value.
    """
    for item in iterator:
        match = pattern.match(item)
        if match:
            return match.group(1)
    return default
