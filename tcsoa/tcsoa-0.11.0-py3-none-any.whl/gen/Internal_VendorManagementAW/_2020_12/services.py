from __future__ import annotations

from tcsoa.gen.Internal.VendorManagementAW._2020_12.VendorManagement import OrderedViewModelInput
from tcsoa.base import TcService
from tcsoa.gen.Internal.VendorManagementAW._2019_12.VendorManagement import ViewModelRowsResponse


class VendorManagementService(TcService):

    @classmethod
    def sortAndFilterViewModelRows(cls, input: OrderedViewModelInput) -> ViewModelRowsResponse:
        """
        This operation returns the filtered and sorted logical rows for a given row&rsquo;s, filter and sort criteria.
        """
        return cls.execute_soa_method(
            method_name='sortAndFilterViewModelRows',
            library='Internal-VendorManagementAW',
            service_date='2020_12',
            service_name='VendorManagement',
            params={'input': input},
            response_cls=ViewModelRowsResponse,
        )
