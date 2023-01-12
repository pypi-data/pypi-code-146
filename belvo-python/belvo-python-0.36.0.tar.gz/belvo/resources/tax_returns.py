from datetime import date
from typing import Dict, List, Optional, Union

from belvo.enums import TaxReturnType
from belvo.resources.base import Resource


class TaxReturns(Resource):
    endpoint = "/api/tax-returns/"

    def create(
        self,
        link: str,
        year_from: str = None,
        year_to: str = None,
        *,
        attach_pdf: bool = False,
        save_data: bool = True,
        raise_exception: bool = False,
        type_: Optional[TaxReturnType] = None,
        date_from: str = None,
        date_to: str = None,
        **kwargs: Dict,
    ) -> Union[List[Dict], Dict]:
        """Retrieve tax returns for a link

        Retrieve yearly (annual) or monthly tax returns for a fiscal link.

        Args:
            link (str): The fiscal `link.id` you want specific tax return information for.
            year_from (str, optional): The starting year you want to get tax returns for, in `YYYY` format. Defaults to None.
            year_to (str, optional): The year you want to stop geting tax returns for, in `YYYY` format. Defaults to None.
            attach_pdf (bool, optional): When this is set to `True`, you will receive the PDF as a binary string in the response.. Defaults to `False`.
            save_data (bool, optional): Indicates whether or not to persist the data in Belvo. Defaults to `True`.
            raise_exception (bool, optional): Indicates whether to raise an exception or return the API error. Defaults to `False`.
            type_ (Optional[TaxReturnType], optional): The type of tax return to return. For yearly tax returns this must be set to `yearly`. For monthly tax returns, this field must be set to `monthly`. By default, Belvo returns the **yearly** (annual) tax returns.
            date_from (str, optional): The starting date you want to get tax returns for, in `YYYY-MM-DD` format. The value of `date_from` cannot be greater than `date_to`. Defaults to None.
            date_to (str, optional): The date you want to stop geting tax returns for, in `YYYY-MM-DD` format. The value of `date_to` cannot be greater than today's date (in other words, no future dates). Defaults to None.

        Returns:
            Dict: The details of the object. For more information on the response from the API, see our [Tax returns API documentation](https://developers.belvo.com/reference/retrievetaxreturns).
        """

        type_ = type_ if type_ else TaxReturnType.YEARLY

        data = {"link": link, "attach_pdf": attach_pdf, "save_data": save_data, "type": type_.value}

        if data["type"] == "yearly":
            year_to = year_to or str(date.today().year)
            data.update(year_to=year_to, year_from=year_from)
        else:
            data.update(date_to=date_to, date_from=date_from)

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
