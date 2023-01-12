from typing import Dict, List, Union

from belvo.resources.base import Resource


class TaxDeclarations(Resource):
    endpoint = "/api/tax-declarations/"

    def create(
        self,
        link: str,
        year_from: str,
        year_to: str,
        *,
        attach_pdf: bool = False,
        save_data: bool = True,
        raise_exception: bool = False,
        **kwargs: Dict,
    ) -> Union[List[Dict], Dict]:
        """Retrieve tax declaration for a link

        Args:
            link (str): The fiscal `link.id` you want specific tax declaration information for.
            year_from (str, optional): The starting year you want to get tax declaration for, in `YYYY` format.
            year_to (str, optional): The year you want to stop geting tax declaration for, in `YYYY` format.
            attach_pdf (bool, optional): When this is set to `True`, you will receive the PDF as a binary string in the response. Defaults to `False`.
            save_data (bool, optional): Indicates whether or not to persist the data in Belvo. Defaults to `True`.
            raise_exception (bool, optional): Indicates whether to raise an exception or return the API error. Defaults to `False`.

        Returns:
            Dict: The details of the object. For more information on the response from the API, see our [Tax declarations API documentation](https://developers.belvo.com/reference/retrievetaxdeclarations).
        """

        data = {
            "link": link,
            "year_from": year_from,
            "year_to": year_to,
            "attach_pdf": attach_pdf,
            "save_data": save_data,
        }

        return self.session.post(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )
