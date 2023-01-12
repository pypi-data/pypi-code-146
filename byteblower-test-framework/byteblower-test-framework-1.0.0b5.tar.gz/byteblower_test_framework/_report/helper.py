"""Helper functions related to reporting."""


def snake_to_title(word: str) -> str:
    """Convert ``snake_case`` format to ``Title Case``.

    :param word: Word to convert
    :type word: str
    :return: Title-case formatted word.
    :rtype: str
    """
    return ' '.join(x.capitalize() or '_' for x in word.split('_'))
