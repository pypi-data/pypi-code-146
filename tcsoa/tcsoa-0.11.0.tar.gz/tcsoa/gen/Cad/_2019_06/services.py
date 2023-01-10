from __future__ import annotations

from tcsoa.gen.Cad._2007_01.StructureManagement import CreateBOMWindowsResponse
from tcsoa.gen.Cad._2019_06.StructureManagement import CreateWindowsInfo3
from typing import List
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def createOrReConfigureBOMWindows(cls, info: List[CreateWindowsInfo3]) -> CreateBOMWindowsResponse:
        """
        Creates a list of windows and set the respective input ItemRevision as the top line. This operation can be used
        to set, update and reconfigure BOMWindow using multiple saved variant rules or single stored option set to the
        window. This will provide the ability to specify and apply more configuration for the BOMWindow. For setting
        Product Configurator authored variant rule on the window, value of preference "PSM_enable_product_configurator"
        must be true. It can be used to set certain window property, if sent as a part of input. It can be used to
        create the BOMLine for input to Expand Product Structure services. All BOMLine objects under this window are
        unpacked. To use the Teamcenter default unitNo or use your input RevisionRule with no changes, you must set
        unitNo to -1 in RevisionRuleEntryProps::unitNo. If it is not specified, your input rule will function as a
        modified/transient revision rule with a unitNo of 0.
        """
        return cls.execute_soa_method(
            method_name='createOrReConfigureBOMWindows',
            library='Cad',
            service_date='2019_06',
            service_name='StructureManagement',
            params={'info': info},
            response_cls=CreateBOMWindowsResponse,
        )
