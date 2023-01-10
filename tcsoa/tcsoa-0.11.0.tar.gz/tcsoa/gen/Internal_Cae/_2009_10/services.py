from __future__ import annotations

from tcsoa.base import TcService


class SimulationProcessManagementService(TcService):

    @classmethod
    def notifyUser(cls, message: str, users: str, groups: str) -> bool:
        """
        This internal operation will send email notification to all the configured users after the completion of a
        simulation process launch. This notification will contain the details of the launch relative to its success or
        failure and also contain information about newly created objects (Item, ItemRevision, Dataset) if any.
        To use this operation, the user should have either a simulation_author or rtt_author license.
        """
        return cls.execute_soa_method(
            method_name='notifyUser',
            library='Internal-Cae',
            service_date='2009_10',
            service_name='SimulationProcessManagement',
            params={'message': message, 'users': users, 'groups': groups},
            response_cls=bool,
        )
