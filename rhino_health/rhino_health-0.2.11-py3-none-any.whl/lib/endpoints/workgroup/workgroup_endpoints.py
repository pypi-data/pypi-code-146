from typing import List
from warnings import warn

from rhino_health.lib.endpoints.endpoint import Endpoint, NameFilterMode, VersionMode
from rhino_health.lib.endpoints.workgroup.workgroup_dataclass import FutureWorkgroup, Workgroup
from rhino_health.lib.utils import rhino_error_wrapper


class WorkgroupEndpoints(Endpoint):
    """
    @autoapi False
    """

    @property
    def workgroup_data_class(self):
        """
        @autoapi False
        """
        return Workgroup

    @rhino_error_wrapper
    def get_workgroups(self, workgroup_uids: List[str] = None) -> List[Workgroup]:
        """
        Returns the specified workgroup_uids

        .. warning:: This feature is under development and the interface may change

        :param workgroup_uids: List of strings of workgroup uids to get
        """
        warn("The Workgroup dataclass is not fully functional and will be changed in the future")
        if not workgroup_uids:
            return []
        else:
            return [
                self.session.get(f"/workgroups/{workgroup_uid}/").to_dataclass(
                    self.workgroup_data_class
                )
                for workgroup_uid in workgroup_uids
            ]


class WorkgroupFutureEndpoints(WorkgroupEndpoints):
    """
    @autoapi True
    @objname WorkgroupEndpoints
    Endpoints available to interact with Workgroups on the Rhino Platform

    Notes
    -----
    You should access these endpoints from the RhinoSession object
    """

    @property
    def workgroup_data_class(self):
        """
        @autoapi False
        """
        return FutureWorkgroup
