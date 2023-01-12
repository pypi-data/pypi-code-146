from typing import Dict, Generator, List, Union

from belvo.http import APISession


class Resource:
    endpoint: str

    def __init__(self, session: APISession) -> None:
        self._session = session

    @property
    def session(self) -> APISession:
        return self._session

    def list(self, **kwargs) -> Generator:
        """# **List all items for the given resource.**

        With the `.list()` method, you can list all items for a given resource. You can additionally add filters to your method in order to only retrieve results matching your query. If you don't provide any filters, we return all items for that resource.

        Example:

        ```
        # Retrieve all accounts (no filter given)
        accounts = client.Accounts.list()

        # Retrieve accounts for a specific bank
        accounts = client.Accounts.list(institution="erebor_mx_retail")


        # Retrieve all checking accounts with an available balance >= 100
        accounts = client.Accounts.list(type__in="checking", balance_available__gte=100)

        ```

        You can find the filters, along with examples, that you can apply per resource by checking our API reference documentation. For example, if you want to see the filters you can apply to the Links resource, then see our [List all links documentation](https://developers.belvo.com/reference/listlinks).

        Returns:
            _type_: _description_

        Yields:
            Generator: _description_
        """
        endpoint = self.endpoint
        return self.session.list(endpoint, params=kwargs)

    def get(self, id: str, **kwargs) -> Dict:
        """#Get the details for a specific object

        Args:
            id (str): The ID of the item you want to get details for (UUID).

        Returns:
            Dict: The details of the object.
        """
        return self.session.get(self.endpoint, id, params=kwargs)

    def delete(self, id: str) -> bool:
        """# Delete an item from the Belvo API.

        Note: If you delete an account object, all associated transactions and owners are also deleted from your Belvo account.

        Example:

        ```
        # Deleting an account
        client.Accounts.delete("161a5e4d-67f5-4760-ae4f-c1fe85cb20ca")

        ```

        Args:
            id (str): The id of the object to delete.

        Returns:
            bool: Returns `True` if the object was deleted.
        """
        return self.session.delete(self.endpoint, id)

    def resume(
        self, session: str, token: str, *, link: str = None, raise_exception: bool = False, **kwargs
    ) -> Union[List[Dict], Dict]:
        """# Resume a resource sessions

        Example:

        ```
        # Login to Belvo API
        client = Client("Secret Key ID", "Secret Key PASSWORD", "sandbox")

        # Resume a link
        link = client.Links.resume(
          session="session_id",
          token="token",
          link="link_id"
        )

        ```

        Args:
            session (str): The session you want to resume (UUID).
            token (str): The MFA token required to continue the session.
            link (str, optional): The Link ID . Defaults to None.
            raise_exception (bool, optional): Boolean indicating whether to return an API error or to raise an exception. Defaults to False.

        Returns:
            Union[List[Dict], Dict]: On success, returns the resource data requests.
        """

        data = {"session": session, "token": token}

        if link is not None:
            data.update(link=link)

        return self.session.patch(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )
