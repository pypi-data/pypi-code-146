import warnings
from typing import Dict, List, Optional, Union

from belvo.enums import AccessMode
from belvo.resources.base import Resource
from belvo.utils import read_file_to_b64


class Links(Resource):
    endpoint = "/api/links/"

    def create(
        self,
        institution: str,
        username: str,
        password: str,
        *,
        username2: str = None,
        username3: str = None,
        password2: str = None,
        token: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        access_mode: Optional[AccessMode] = None,
        username_type: str = None,
        certificate: str = None,
        private_key: str = None,
        external_id: str = None,
    ) -> Union[List[Dict], Dict]:
        """Register a new Link

        Register a new link with your Belvo account. For in-depth information for all the request parameters, please see our [Links API documentation](https://developers.belvo.com/reference/registerlink).

        <div style="background-color:#f4f6f8; border-left: 6px solid #0663F9;padding: 12px;margin-left: 25px; border-radius: 4px; margin-right: 25px">
        <strong>Info:</strong> We really recommend using our Connect Widget to create links. It'll save you a lot of headaches!.
        </div>


        Args:
            institution (str): The Belvo name for the institution.
            username (str): The end-user's username used to log in to the institution.
            password (str): The end-user's password used to log in to the institution.
            username2 (str, optional): The end-user's second username used to log in to the institution. Defaults to None.
            username3 (str, optional): The end-user's third username used to log in to the institution. Defaults to None.
            password2 (str, optional): The end-user's second password used to log in to the institution. Defaults to None.
            token (str, optional): The MFA token required by the bank to log in. We do not recommend sending the authentication token in the same request as registering the user. See our Handling multi-factor authentication article for more information and best practices. Defaults to None.
            save_data (bool, optional): Indicates whether or not to persist the data in Belvo. Defaults to `True`.
            raise_exception (bool, optional): Indicates whether to raise an exception or return the API error. Defaults to `False`.
            access_mode (Optional[AccessMode], optional): The type of link to create. Defaults to None.
            username_type (str, optional): Type of document to be used as a username. Defaults to None.
            certificate (str, optional): For certain fiscal institutions, it is possible to log in using a certificate and a private key, which enables a faster connection to the institution. Defaults to None.
            private_key (str, optional): For certain fiscal institutions, it is possible to log in using a certificate and a private key, which enables a faster connection to the institution. Defaults to None.
            external_id (str, optional): An additional identifier for the link, provided by you, to store in the Belvo database. Defaults to None.

        Returns:
            Union[List[Dict], Dict]: For more information on the response from the API, see our [Links API documentation](https://developers.belvo.com/reference/registerlink).
        """

        data = {
            "institution": institution,
            "username": username,
            "password": password,
            "save_data": save_data,
            "access_mode": access_mode and access_mode.value,
            "username2": username2,
            "username3": username3,
            "password2": password2,
            "token": token,
            "username_type": username_type,
            "certificate": certificate and read_file_to_b64(certificate),
            "private_key": private_key and read_file_to_b64(private_key),
            "external_id": external_id,
        }

        clean_data = {key: value for key, value in data.items() if value}

        return self.session.post(self.endpoint, data=clean_data, raise_exception=raise_exception)

    def update(
        self,
        link: str,
        *,
        password: str = None,
        password2: str = None,
        token: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        username_type: str = None,
        certificate: str = None,
        private_key: str = None,
    ) -> Union[List[Dict], Dict]:
        """Update a link's credentials

        Update the credentials of a specific link. If the successfully updated link is a recurrent one, we automatically trigger an update of the link. If we find fresh data, you'll receive historical update webhooks.

        Args:
            link (str): The link.id you want to update.
            password (str): The end-user's password used to log in to the institution.
            password2 (str, optional): The end-user's second password used to log in to the institution. Defaults to None.
            token (str, optional): The MFA token required by the bank to log in. We do not recommend sending the authentication token in the same request as registering the user. See our Handling multi-factor authentication article for more information and best practices. Defaults to None.
            save_data (bool, optional): Indicates whether or not to persist the data in Belvo. Defaults to `True`.
            raise_exception (bool, optional): Indicates whether to raise an exception or return the API error. Defaults to `False`.
            username_type (str, optional): Type of document to be used as a username. Defaults to None.
            certificate (str, optional): For certain fiscal institutions, it is possible to log in using a certificate and a private key, which enables a faster connection to the institution. Defaults to None.
            private_key (str, optional): For certain fiscal institutions, it is possible to log in using a certificate and a private key, which enables a faster connection to the institution. Defaults to None.

        Returns:
            Union[List[Dict], Dict]: For more information on the response from the API, see our [Links API documentation](https://developers.belvo.com/reference/patchlinks).
        """

        data = {
            "password": password,
            "save_data": save_data,
            "password2": password2,
            "token": token,
            "username_type": username_type,
            "certificate": certificate and read_file_to_b64(certificate),
            "private_key": private_key and read_file_to_b64(private_key),
        }

        clean_data = {key: value for key, value in data.items() if value}

        return self.session.put(
            self.endpoint, id=link, data=clean_data, raise_exception=raise_exception
        )

    def token(
        self, link: str, scopes: str, *, widget: dict = None, raise_exception: bool = False
    ) -> Union[List[Dict], Dict]:
        from belvo.resources import WidgetToken

        warnings.warn(
            "Please make use of `client.WidgetToken.create(link=<link:uuid>)` "
            "to request a link scoped token instead.",
            DeprecationWarning,
        )

        token = WidgetToken(self.session)
        return token.create(
            scopes=scopes, link=link, widget=widget, raise_exception=raise_exception
        )

    def patch(
        self, link: str, *, access_mode: Optional[AccessMode] = None, raise_exception: bool = False
    ) -> Union[List[Dict], Dict]:
        """Update a link's access_mode

        Args:
            link (str): The `link.id` you want to update the `access_mode` for (UUID).
            access_mode (Optional[AccessMode], optional): The new `access_mode` you want to assign to the link. Can be either `single` or `recurrent`. Defaults to None.
            raise_exception (bool, optional): Indicates whether to raise an exception or return the API error. Defaults to `False`.

        Returns:
            Dict: The details of the object.
        """
        data = {"access_mode": access_mode and access_mode.value}
        return self.session.patch(
            f"{self.endpoint}{link}/", data=data, raise_exception=raise_exception
        )
