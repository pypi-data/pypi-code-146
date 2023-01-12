from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class PreferenceManagementService(TcService):

    @classmethod
    def deletePreferenceCategories(cls, categoryNames: List[str]) -> ServiceData:
        """
        Deletes preference category for each provided category name if there are no preferences assigned to the
        category.
        Only Site administrators can delete an existing category.
        
        Use cases:
        Delete an existing preference category:
        Site administrator that wants to delete an existing category "MyCategory" using the deletePreferenceCategories
        operation by providing a name (e.g. " MyCategory ") as the category name. Multiple names can be provided to
        delete multiple categories.
        """
        return cls.execute_soa_method(
            method_name='deletePreferenceCategories',
            library='Internal-Administration',
            service_date='2018_06',
            service_name='PreferenceManagement',
            params={'categoryNames': categoryNames},
            response_cls=ServiceData,
        )
