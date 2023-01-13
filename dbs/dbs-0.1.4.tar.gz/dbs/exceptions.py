from pydantic import StrictStr


class DBSException(Exception):
    """
    Base class for all the DBS exceptions.
    Contains one field for description (hopefully actionable)
    """

    def __init__(self, detail: StrictStr) -> None:
        self.detail = detail

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(detail={self.detail!r})"
