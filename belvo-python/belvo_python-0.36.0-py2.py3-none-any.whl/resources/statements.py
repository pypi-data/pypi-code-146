from typing import Dict, List, Union

from belvo.resources.base import Resource


class Statements(Resource):
    """
    <br>
    <div style="background-color:#f9c806; border-left: 6px solid #f9c806;padding: 12px;margin-left: 25px; border-radius: 4px; margin-right: 25px">
    <strong>⚠️ Sunset notice: </strong> The Statements resource is due to be sunsetted on 09.05.2022. After which, we will no longer support the resource and we will remove it from our documentation, API, and SDKs.
    </div>

    """

    endpoint = "/api/statements/"

    def create(
        self,
        link: str,
        account: str,
        year: str,
        month: str,
        *,
        attach_pdf: bool = False,
        save_data: bool = True,
        raise_exception: bool = False,
        **kwargs: Dict,
    ) -> Union[List[Dict], Dict]:
        """
        <br>
        <div style="background-color:#f9c806; border-left: 6px solid #f9c806;padding: 12px;margin-left: 25px; border-radius: 4px; margin-right: 25px">
        <strong>⚠️ Sunset notice: </strong> The Statements resource is due to be sunsetted on 09.05.2022. After which, we will no longer support the resource and we will remove it from our documentation, API, and SDKs.
        </div>

        """

        data = {
            "link": link,
            "account": account,
            "year": year,
            "month": month,
            "attach_pdf": attach_pdf,
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
        account: str = None,
        raise_exception: bool = False,
        **kwargs,
    ) -> Union[List[Dict], Dict]:

        data = {"session": session, "token": token}

        if link is not None:
            data.update(link=link)

        if account is not None:
            data.update(account=account)

        return self.session.patch(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )
