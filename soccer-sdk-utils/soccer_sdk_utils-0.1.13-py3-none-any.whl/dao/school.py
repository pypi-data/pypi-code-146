from soccer_sdk_utils.dao.base import DataAccessObject


class SchoolDAO(DataAccessObject):
    def __init__(self, **kwargs):
        super().__init__("school", "/id", **kwargs)
