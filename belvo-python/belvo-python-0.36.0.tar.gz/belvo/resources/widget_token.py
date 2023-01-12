from typing import Any, Dict, Optional

from belvo.resources.base import Resource


class WidgetToken(Resource):
    endpoint = "/api/token/"

    def create(
        self,
        *,
        scopes: Optional[str] = None,
        link: Optional[str] = None,
        widget: Optional[Dict[str, Any]] = None,
        raise_exception: bool = False,
    ):
        """Create a widget access token

        Args:
            scopes (Optional[str], optional): The scope of data to retrieve. We automatically default to`read_institutions, write_links, read_links`.
            link (Optional[str], optional): The `link_id` you want to update credentials for. For more information, see our [Connect Widget in Update Mode](https://developers.belvo.com/docs/connect-widget-update-mode) devportal article. Defaults to None.
            widget (Optional[Dict[str, Any]], optional): Optional object where you can provide custom branding. For more information, see our [Branding and customization](https://developers.belvo.com/docs/widget-branding-and-customization) devportal article. Defaults to None.
            raise_exception (bool, optional): Indicates whether to raise an exception or return the API error. Defaults to `False`.

        Returns:
            Your widget access token.
        """
        if scopes is None:
            scopes = "read_institutions,write_links,read_links"

        data: Dict[str, Any] = {
            "id": self.session._secret_key_id,
            "password": self.session._secret_key_password,
            "scopes": scopes,
        }

        if link:
            data.update(link_id=link)

        if widget:
            data.update(widget=widget)

        return self.session.post(self.endpoint, data=data, raise_exception=raise_exception)
