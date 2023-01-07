from typing import Any, List

from rhino_health.lib.dataclass import RhinoBaseModel
from rhino_health.lib.endpoints.endpoint import RESULT_DATACLASS_EXTRA


class User(RhinoBaseModel, extra=RESULT_DATACLASS_EXTRA):
    """
    @autoapi False
    """

    uid: str
    """@autoapi True Unique ID of the user"""
    full_name: str
    """@autoapi True The full name of the user"""
    primary_workgroup_uid: str
    """@autoapi True The Unique ID of the Primary Workgroup of the user"""
    workgroups_uids: List[str]
    """@autoapi True Additional workgroup unique IDs the user belongs to"""


class FutureUser(User):
    """
    @objname User
    DataClass representing a User on the Rhino platform.
    """

    _primary_workgroup: Any
    _workgroups: Any

    def primary_workgroup(self):
        """
        Get the primary workgroup of this user

        .. warning:: Be careful when calling this for newly created objects.
            The workgroup associated with the PRIMARY_WORKGROUP_UID must already exist on the platform.

        .. warning:: The result of this function is cached.
            Be careful calling this function after making changes to the primary workgroup

        Returns
        -------
        primary_workgroup: Workgroup
            A DataClass representing the Workgroup of the user's primary workgroup

        See Also
        --------
        rhino_health.lib.endpoints.workgroup.workgroup_dataclass : Workgroup Dataclass
        """
        if not self._primary_workgroup:
            raise NotImplementedError
        return self._primary_workgroup

    def workgroups(self):
        """
        Get the non primary workgroups of this user

        .. warning:: Be careful when calling this for newly created objects.
            The workgroups associated with the WORKGROUP_UIDS must already exist on the platform.

        .. warning:: The result of this function is cached.
            Be careful calling this function after making changes to the workgroups

        Returns
        -------
        workgroups: List[Workgroup]
            An array of DataClasses representing the additional workgroups the user is a member of

        See Also
        --------
        rhino_health.lib.endpoints.workgroup.workgroup_dataclass : Workgroup Dataclass
        """
        if not self._workgroups:
            raise NotImplementedError
        return self._workgroups
