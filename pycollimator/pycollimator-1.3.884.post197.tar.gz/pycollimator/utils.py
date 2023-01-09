import uuid

PATH_DELIMITER = "."


def is_uuid(s: str) -> bool:
    try:
        uuid.UUID(str(s), version=4)
        return True
    except ValueError:
        return False


# technically a nested path.
def is_path(s: str) -> bool:
    return s and PATH_DELIMITER in s
