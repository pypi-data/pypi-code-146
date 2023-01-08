"""Utilities for dealing with filenames and Excel sheet names."""

import re


def sanitize_filename(filename: str) -> str:
    """
    Ensure valid filenames.

    Given a filename, remove all characters that are
    potentially hazardous in a filename.
    The only chars allowed are

    - Word characters ([a-zA-Z0-9_])
    - Dashes
    - Periods
    - Spaces
    - Parenthesis

    Parameters
    ----------
    filename : str
        The filename to clean.

    Returns
    -------
    str
        The cleaned up filename.

    See Also
    --------
    sanitize_xl_sheetname : Ensure valid Excel sheetnames.

    Examples
    --------
    >>> sanitize_filename('python is fun 🐍.py')
    'python is fun _.py'
    """
    return re.sub(r"[^\w\-_. ()]", "_", filename)


def sanitize_xl_sheetname(sheetname: str) -> str:
    """
    Ensure valid Excel sheetnames.

    This function replaces most invalid characters with underscores and
    truncates the sheetname to an appropriate size.

    Parameters
    ----------
    sheetname : str
        Name of Excel sheet.

    Returns
    -------
    str
        The Excel sheet name which will definitely be valid.

    See Also
    --------
    sanitize_filename : Ensure valid filenames.

    Examples
    --------
    >>> sanitize_xl_sheetname("9:00 AM")
    '9_00 AM'
    >>> sanitize_xl_sheetname("'single quoted'")
    '_single quoted_'
    """
    # A worksheet cannot be named history, regardless of case
    # A worksheet name cannot be left blank
    if sheetname == "" or sheetname.lower() == "history":
        raise ValueError(f'Invalid sheet name "{sheetname}"')

    # A sheetname cannot start or end with an apostrophe
    sheetname = re.sub(r"^'|'$", "_", sheetname)

    # Only certain chars are allowed
    allowed = r"`~!@#$%^&()\-_=+{}|;,<.> '"
    sheetname = re.sub(rf"[^{allowed}\w]", "_", sheetname)
    return sheetname[-31:]
