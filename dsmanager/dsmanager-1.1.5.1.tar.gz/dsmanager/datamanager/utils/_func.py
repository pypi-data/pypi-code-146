"""@Author: Rayane AMROUCHE

Utils functions for the DataManager.
"""


def find_type(path: str) -> str:
    """Extract file's type form path.

    Args:
        path (str): Path of a file.

    Returns:
        str: Type of file.
    """
    file_type = path.split(".")[-1]
    if file_type.startswith("xls"):
        return "excel"
    return file_type
