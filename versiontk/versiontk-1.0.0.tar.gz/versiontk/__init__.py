from . import grade as __grade


def upgrade(__version: str, limit: int = 99):
    return __grade.upgrade(__version, limit=limit)


def downgrade(__version: str, limit: int = 99):
    return __grade.downgrade(__version, limit=limit)
