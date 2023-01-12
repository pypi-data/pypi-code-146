from typing import Dict, List, Union

from belvo.resources.base import Resource


class Invoices(Resource):
    endpoint = "/api/invoices/"

    def create(
        self,
        link: str,
        date_from: str,
        date_to: str,
        type_: str,
        *,
        attach_xml: bool = False,
        save_data: bool = True,
        raise_exception: bool = False,
        **kwargs: Dict,
    ) -> Union[List[Dict], Dict]:
        """Retrieve invoices for a link

        You can ask for up to **one** year (365 days) of invoices per request. If you need invoices for more than one year, just make another request.

        Example:
        ```python
        # Fetch invoices for a Link
        invoices = client.Invoices.create(
            "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
            "2019-07-01",
            "2019-07-31",
            "INFLOW"
        )
        ```

        Args:
            link (str): The fiscal `link.id` that you want to get information for (UUID).
            date_from (str): Date from which you want to start receiving invoices for, in `YYYY-MM-DD` format. The value of `date_from` cannot be greater than `date_to`.
            date_to (str, optional): Date that you want to stop receiving invoirces for, in `YYYY-MM-DD` format. The value of `date_to` cannot be greater than today's date (in other words, no future dates).
            type_ (str): The direction of the invoice (from the perspective of the Link owner). Can be either `OUTFLOW` OR `INFLOW`.
            attach_xml (bool, optional): When set to `True`, you will receive the XML invoice in the response. Defaults to False.
             save_data (bool, optional): Indicates whether or not to persist the data in Belvo. Defaults to `True`.
            raise_exception (bool, optional): Indicates whether to raise an exception or return the API error. Defaults to `False`.

        Returns:
            Union[List[Dict], Dict]: For more information on the response from the API, see our [Invoices API documentation](https://developers.belvo.com/reference/retrieveinvoices).
        """

        data = {
            "link": link,
            "date_from": date_from,
            "date_to": date_to,
            "type": type_,
            "attach_xml": attach_xml,
            "save_data": save_data,
        }

        return self.session.post(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )

    def resume(
        self,
        session: str,
        token: str,
        *,
        link: str = None,
        raise_exception: bool = False,
        **kwargs: Dict,
    ) -> Dict:
        raise NotImplementedError()
