from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMWindow
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ResourceManagementService(TcService):

    @classmethod
    def showCoordinateSystems(cls, bomWindow: BOMWindow, showCoordinateSystems: bool) -> ServiceData:
        """
        In the Resource Manager application, coordinate systems are used for automatic positioning of components during
        the assembly process. Those coordinate systems are displayed in the BOM tree table in the Resource view in the
        Teamcenter rich client. In some cases the user wants to focus on the main components and hide the coordinate
        systems. This operation changes the configuration to show or hide the coordinate system of BOMLine objects in a
        specific BOMWindow.
        """
        return cls.execute_soa_method(
            method_name='showCoordinateSystems',
            library='Internal-Manufacturing',
            service_date='2013_12',
            service_name='ResourceManagement',
            params={'bomWindow': bomWindow, 'showCoordinateSystems': showCoordinateSystems},
            response_cls=ServiceData,
        )

    @classmethod
    def showGCSConnectionPoints(cls, bomWindow: BOMWindow, showGCSConnectionPointsOption: int) -> ServiceData:
        """
        In the Resource Manager application, connection points are used for the guided component search (GCS) of
        components during the assembly process. Those connection points are displayed in the BOM tree table in the
        Resource view in the Teamcenter rich client. In some cases, the user wants to focus on the main components and
        hide the connection points. This operation can be used to show or hide the connection point BOMLine objects in
        a specific BOMWindow.
        In addition to hide (0) and show (1), a third option "only unconnected" (2) can be used. If this option is used
        only those connection points are displayed that can be used for assembling and that are not yet connected to
        another component.
        """
        return cls.execute_soa_method(
            method_name='showGCSConnectionPoints',
            library='Internal-Manufacturing',
            service_date='2013_12',
            service_name='ResourceManagement',
            params={'bomWindow': bomWindow, 'showGCSConnectionPointsOption': showGCSConnectionPointsOption},
            response_cls=ServiceData,
        )
