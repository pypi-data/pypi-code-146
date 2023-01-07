from typing import List

from rhino_health.lib.dataclass import RhinoBaseModel
from rhino_health.lib.endpoints.endpoint import RESULT_DATACLASS_EXTRA

# TODO


class Workgroup(RhinoBaseModel, extra=RESULT_DATACLASS_EXTRA):
    """
    @autoapi False
    """

    uid: str
    """@autoapi True The unique ID of the Workgroup"""
    name: str
    """@autoapi True The name of the Workgroup"""
    org_name: str
    """@autoapi True The organization name of the Workgroup"""
    users: "List[User]"
    """@autoapi True A list of Users in the Workgroup"""
    admins: "List[User]"
    """@autoapi True A list of Admins in the Workgroup"""


class FutureWorkgroup(Workgroup):
    """
    @objname Workgroup
    """

    users: "List[FutureUser]"
    admins: "List[FutureUser]"


from rhino_health.lib.endpoints.user.user_dataclass import FutureUser, User

Workgroup.update_forward_refs()
FutureWorkgroup.update_forward_refs()
