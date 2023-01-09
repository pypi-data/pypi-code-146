from .base_client import BaseClient
from typing import Any, Union
from decimal import Decimal


class WiseClient(BaseClient):

    def __init__(self, api_key: str, is_sandbox: bool = True,
                 lang: str = "en") -> None:
        super().__init__(api_key, is_sandbox, lang)
        self.user_id: int = -1

    def _check_user_id(self) -> None:
        if self.user_id < 0:
            raise ValueError("Invalid user id. Have you called "
                             "`self.initialise()` before using this instance?")

    async def _update_user_id(self) -> None:
        resp = await self.get_logged_in_user_detail()
        self.user_id = resp["id"]

    async def initialise(self) -> None:
        """Initialise the instance so it is ready for use, should only be
        called once
        """
        await self._update_user_id()

    async def update_address(self, profile) -> dict[str, Any]:
        """Create or update address info
        https://api-docs.wise.com/#addresses-create-update
        """
        raise NotImplementedError  # TODO
        endpoint = "/v1/addresses"
        params = {"profile"}

        return await self.query("POST", endpoint=endpoint, params=params)

    async def get_currency_pair(self) -> dict[str, Any]:
        """Get list of allowed currency pairs.
        https://api-docs.wise.com/#currency-pairs-get-currency-pairs
        """
        endpoint = "/v1/currency-pairs"
        return await self.query("GET", endpoint=endpoint)

    async def get_rates(self,
                        source: Union[str, None] = None,
                        target: Union[str, None] = None,
                        time: Union[str, None] = None,
                        from_: Union[str, None] = None,
                        to: Union[str, None] = None,
                        group: Union[str, None] = None) -> list[Any]:
        """Get all or specific currency exchange rate.
        https://api-docs.wise.com/#exchange-rates-list
        """
        endpoint = "/v1/rates"
        params = {
            "source": source,
            "target": target,
            "time": time,
            "from": from_,
            "to": to,
            "group": group,
        }
        params = dict((k, v) for k, v in params.items() if v is not None)
        return await self.query("GET", endpoint=endpoint, params=params)

    async def get_user_by_id(self, id: int) -> dict[str, Any]:
        """Get user detail and profile info by user id
        https://api-docs.wise.com/#users-get-by-id
        """
        endpoint = f"/v1/users/{id}"
        return await self.query("GET", endpoint=endpoint)

    async def get_logged_in_user_detail(self) -> dict[str, Any]:
        """Get logged in user id and profile info.
        https://api-docs.wise.com/#users-get-the-currently-logged-in-user"""
        endpoint = "/v1/me"
        return await self.query("GET", endpoint=endpoint)

    async def create_quote(self,
                           source_currency: str,
                           target_currency: str,
                           target_amount: Union[Decimal, None],
                           source_amount: Union[Decimal, None] = None,
                           target_account: Union[int, None] = None,
                           pay_out: Union[str, None] = None,
                           preferred_pay_in: Union[str, None] = None
                           ) -> dict[str, Any]:
        """Create a quote for a transfer.
        https://api-docs.wise.com/#quotes-create

        **Note:** `target_amount` and `source_amount` are mutually exclusive.
        i.e., if `target_amount` is not None, then `source_amount` needs to be
        a `Decimal` larger than 0 and vice versa.

        Args:
          source_currency: Source currency code defined in the
          `get_currency_pair()` call
          target_currency: Target currency code defined in the
          `get_currency_pair()` call
          target_amount: A `Decimal` type that represents the amount in target
          currency, mutually exclusive with `source_amount`
          source_amount: A `Decimal` type that represents the amount in source
          currency, mutually exclusive with `target_amount`
          target_account: Optional, can be provided with `update_quotes()`
          later
          pay_out: Optional, check https://api-docs.wise.com/#quotes-create
          for valid value. Default value will apply if it is `None`.
          preferred_pay_in: Optional. Default value will apply if it is `None`.

        Raise:
          ValueError: `target_amount` or `source_amount` not mutually exclusive
          or both have values equal to or less than 0.
        """
        endpoint = f"/v3/profiles/{self.user_id}/quotes"

        if target_amount is not None and target_amount <= 0:
            target_amount = None
        elif target_amount is not None:
            # Cast to float so it is serialisable
            target_amount = float(target_amount)
        if source_amount is not None and source_amount <= 0:
            source_amount = None
        elif target_amount is not None:
            # Cast to float so it is serialisable
            target_amount = float(target_amount)

        # Need to be mutually exclusive
        if not ((target_amount is None) ^ (source_amount is None)):
            raise ValueError("Either `target_amount` or `source_amount` needs "
                             "to have a value larger than 0, but not both.")

        data = {
            "sourceCurrency": source_currency,
            "targetCurrency": target_currency,
            "targetAmount": target_amount,
            "sourceAmount": source_amount,
            "targetAccount": target_account,
            "payOut": pay_out,
            "preferredPayIn": preferred_pay_in,
        }
        data = dict((k, v) for k, v in data.items() if v is not None)

        return await self.query("POST", endpoint=endpoint, data=data)

    async def create_temporary_quote(self,
                                     source_currency: str,
                                     target_currency: str,
                                     target_amount: Union[Decimal, None],
                                     source_amount: Union[Decimal, None] = None
                                     ) -> dict[str, Any]:
        """Create a temporary quote, not usable for transfer.
        https://api-docs.wise.com/#quotes-get-temporary-quote

        **Note:** `target_amount` and `source_amount` are mutually exclusive.
        i.e., if `target_amount` is not None, then `source_amount` needs to be
        a `Decimal` larger than 0 and vice versa.

        Args:
          source_currency: Source currency code defined in the
          `get_currency_pair()` call
          target_currency: Target currency code defined in the
          `get_currency_pair()` call
          target_amount: A `Decimal` type that represents the amount in target
          currency, mutually exclusive with `source_amount`
          source_amount: A `Decimal` type that represents the amount in source
          currency, mutually exclusive with `target_amount`

        Raise:
          ValueError: `target_amount` or `source_amount` not mutually exclusive
          or both have values equal to or less than 0.
        """
        endpoint = "/v3/quotes"

        if target_amount is not None and target_amount <= 0:
            target_amount = None
        elif target_amount is not None:
            # Cast to float so it is serialisable
            target_amount = float(target_amount)
        if source_amount is not None and source_amount <= 0:
            source_amount = None
        elif target_amount is not None:
            # Cast to float so it is serialisable
            target_amount = float(target_amount)

        # Need to be mutually exclusive
        if not ((target_amount is None) ^ (source_amount is None)):
            raise ValueError("Either `target_amount` or `source_amount` needs "
                             "to have a value larger than 0, but not both.")

        data = {
            "sourceCurrency": source_currency,
            "targetCurrency": target_currency,
            "targetAmount": target_amount,
            "sourceAmount": source_amount,
        }
        data = dict((k, v) for k, v in data.items() if v is not None)

        return await self.query("POST", endpoint=endpoint, data=data)
