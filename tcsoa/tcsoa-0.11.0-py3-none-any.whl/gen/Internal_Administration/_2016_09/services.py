from __future__ import annotations

from tcsoa.gen.BusinessObjects import User, Group
from tcsoa.base import TcService
from tcsoa.gen.Internal.Administration._2016_09.VolumeManagement import VolumeInfoResponse


class VolumeManagementService(TcService):

    @classmethod
    def getAccessibleVolumes(cls, user: User, group: Group) -> VolumeInfoResponse:
        """
        This operation returns the  list of accessible volumes, default volume and default local volume  for the given 
        user and group. If the preference TC_allow_inherited_group_volume_access is set to a non-zero value, the
        operation considers access granted to volumes on all parent level groups up the chain and uses this information
        for computing the accessibleVolumes, defaultVolume and defaultLocalVolume.
        """
        return cls.execute_soa_method(
            method_name='getAccessibleVolumes',
            library='Internal-Administration',
            service_date='2016_09',
            service_name='VolumeManagement',
            params={'user': user, 'group': group},
            response_cls=VolumeInfoResponse,
        )
