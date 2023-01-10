from uuid import UUID


def is_valid_uuid(uuid: str) -> bool:
    try:
        _ = UUID(uuid, version=4)
        return True
    except ValueError:
        return False
