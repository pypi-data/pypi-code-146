from typing import Dict, List, Union

from belvo.enums import TaxRetentionType
from belvo.exceptions import BelvoAPIException
from belvo.resources.base import Resource


class TaxRetentions(Resource):
    endpoint = "/api/tax-retentions/"

    def create(
        self,
        link: str,
        date_from: str,
        date_to: str,
        _type: TaxRetentionType,
        attach_xml: bool = False,
        save_data: bool = True,
        raise_exception: bool = False,
        **kwargs: Dict,
    ) -> Union[List, Dict]:
        """Retrieve tax retentions for a link

        Retrieve (inflow or outflow) tax retentions for a fiscal link

        Args:
            link (str): The fiscal 'link.id' you want specific tax retention information for
            date_from (str, optional): The starting date you want to get tax retentions for, in `YYYY-MM-DD` format. The value of `date_from` cannot be greater than `date_to`. Defaults to None.
            date_to (str, optional): The date you want to stop getting tax retentions for, in `YYYY-MM-DD` format. The value of `date_to` cannot be greater than today's date (in other words, no future dates). Defaults to None.
            _type (TaxRetentionType): The type of tax retention in relation to the invoice (from the perspective of the Link owner). `OUTFLOW` relates to a tax retention for a sent invoice. `INFLOW` related to a tax retention for a received invoice.
            attach_xml (bool, optional): When set to`True`, you will receive the XML tax retention in the response.
            save_data (bool, optional): Indicates whether or not to persist the data in Belvo. Defaults to `True`.

        Returns:
            Dict: The details of the object. For more information on the response from the API, see our [Tax retentions API documentation](https://developers.belvo.com/reference/retrievetaxretentions).
        """

        data = {
            "link": link,
            "attach_xml": attach_xml,
            "save_data": save_data,
            "type": _type.value,
            "date_from": date_from,
            "date_to": date_to,
        }

        return self.session.post(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )

    def resume(self, **_):
        raise BelvoAPIException("Method not supported for tax retentions")
