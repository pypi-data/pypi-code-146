from soccer_sdk_utils.dao.base import DataAccessObject


class OrganizationDAO(DataAccessObject):
    def __init__(self, **kwargs):
        super().__init__("organization", "/id", **kwargs)
