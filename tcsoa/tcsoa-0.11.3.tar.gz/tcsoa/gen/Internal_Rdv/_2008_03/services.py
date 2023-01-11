from __future__ import annotations

from tcsoa.gen.Internal.Rdv._2008_03.VariantManagement import BomlinesInfoForValidoverlay, GetValidoverlayBomlineResponse
from typing import List
from tcsoa.base import TcService


class VariantManagementService(TcService):

    @classmethod
    def getValidoverlayBomlinesInfo(cls, input: List[BomlinesInfoForValidoverlay]) -> GetValidoverlayBomlineResponse:
        """
        This method performs Valid Overlays Only analysis on the background BOMLine objects provided to it, based on
        the set of VariantRule objects provided by the caller. It matches all the BOMLine objects against each of the
        VariantRule provided and returns them classified as configured and uncofigured BOMLine objects. It also
        performs further filtering based on the effectivity date, based on the caller provided boolean flag. The caller
        can either invoke both the filters or choose to invoke any one of them, by appropriately setting the input flag
        as true.
        The method does not accept any context information and assumes that the BOMLine objects and the VariantRule
        objects are from the same context.
        
        
        Use cases:
        Use case 1: Applying Valid Overlays Only (VOO) filter on the result of a search
        If the user wishes to filter any particular set of BOMLine objects using VOO filter, then this operation can be
        invoked. This operation allows the caller to independantly process any set of BOMLine objects against any set
        of VariantRule object(s). To skip the date filter, user would have to set the 'showUnconfiguredBydate' flag to
        true.
        
        Use case 2: Applying Effectivity Date filter on the result of a search
        If the user wishes to filter a set of BOMLine objects based on their effectivity dates, then this operation can
        be invoked by setting the showUnconfiguredVariant flag to true.
        """
        return cls.execute_soa_method(
            method_name='getValidoverlayBomlinesInfo',
            library='Internal-Rdv',
            service_date='2008_03',
            service_name='VariantManagement',
            params={'input': input},
            response_cls=GetValidoverlayBomlineResponse,
        )
