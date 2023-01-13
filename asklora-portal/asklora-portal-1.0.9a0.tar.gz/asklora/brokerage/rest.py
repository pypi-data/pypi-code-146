# flake8: noqa
import json
import os
import time
from collections.abc import Callable
from threading import Thread

import requests
import sseclient
from requests.exceptions import HTTPError
from urllib3.exceptions import ProtocolError

from . import logs, vars
from .common import URL
from .exceptions import APIError, RetryException

"""
will be moved to own repository as module / submodules
will be installable to app that need this modules
"""


def default_event_handler(event: dict):
    logs.logger.info(event)


class ConnectionBroker:
    _base_url = vars.BROKER_API_URL

    def __init__(self):
        self._auth = (vars.BROKER_KEY, vars.BROKER_SECRET)
        self._session = requests.Session()
        self._session.auth = self._auth
        self._retry = int(os.environ.get("APCA_RETRY_MAX", 3))
        self._retry_wait = int(os.environ.get("APCA_RETRY_WAIT", 3))
        self._retry_codes = [
            int(o) for o in os.environ.get("APCA_RETRY_CODES", "429,504").split(",")
        ]

    def _request(
        self,
        method,
        path,
        data=None,
        base_url=None,
    ):
        base_url = base_url or self._base_url
        url = base_url + "/" + path
        opts = {"allow_redirects": False}
        if method.upper() in ["GET", "DELETE"]:
            opts["params"] = data
        else:
            opts["json"] = data

        retry = self._retry
        if retry < 0:
            retry = 0
        while retry >= 0:
            try:
                return self._one_request(method, url, opts, retry)
            except RetryException:
                retry_wait = self._retry_wait
                logs.logger.warning(
                    "sleep {} seconds and retrying {} "
                    "{} more time(s)...".format(retry_wait, url, retry)
                )
                time.sleep(retry_wait)
                retry -= 1
                continue

    def _one_request(self, method: str, url: URL, opts: dict, retry: int):
        """
        Perform one request, possibly raising RetryException in the case
        the response is 429. Otherwise, if error text contain "code" string,
        then it decodes to json object and returns APIError.
        Returns the body json in the 200 status.
        """
        retry_codes = self._retry_codes
        resp = self._session.request(method, url, **opts)
        logs.logger.debug(
            {
                "method": method,
                "url": resp.request.url,
                "status": resp.status_code,
                "header": resp.request.headers,
                "body": resp.request.body,
            }
        )
        try:
            resp.raise_for_status()
        except HTTPError as http_error:
            # retry if we hit Rate Limit
            if resp.status_code in retry_codes and retry > 0:
                raise RetryException()
            if "code" in resp.text:
                error = resp.json()
                if "code" in error:
                    logs.logger.critical(
                        {
                            "method": method,
                            "url": resp.request.url,
                            "status": resp.status_code,
                            "header": resp.request.headers,
                            "body": resp.request.body,
                            "error_response": error,
                        }
                    )
                    raise APIError(error, http_error)
            else:
                raise
        if resp.text != "":
            logs.logger.debug(f"{method} {url} {resp.status_code}")
            return resp.json()
        return None

    def get(self, path, data=None):
        return self._request("GET", path, data)

    def post(self, path, data=None):
        return self._request("POST", path, data)

    def put(self, path, data=None):
        return self._request("PUT", path, data)

    def patch(self, path, data=None):
        return self._request("PATCH", path, data)

    def delete(self, path, data=None):
        return self._request("DELETE", path, data)

    def is_open(self):
        resp = self.get("v1/clock")
        return resp["is_open"]


class MarketData(ConnectionBroker):
    _base_url = vars.MARKET_API_URL

    def get_quote(self, symbol: str):
        return self.get(f"v2/stocks/{symbol}/quotes/latest")

    def get_trade(self, symbol: str):
        return self.get(f"v2/stocks/{symbol}/trades/latest")


class Broker(ConnectionBroker):
    def get_assests(self, params=None):
        return self.get("v1/assets", params)

    def get_asset_by_symbol(self, symbol: str) -> dict:
        return self.get(f"v1/assets/{symbol}")

    def create_account(self, data):
        resp = self.post("v1/accounts", data)
        return resp

    def delete_account(self, account_id):
        return self.delete(f"v1/accounts/{account_id}")

    def get_account(self, account_id):
        """Get the account"""
        resp = self.get(f"v1/accounts/{account_id}")
        return resp

    def get_cip_result(self, account_id):
        """Get CIP result account"""
        resp = self.get(f"v1/accounts/{account_id}/cip")
        return resp

    def get_all_accounts(self, params: dict = None):
        """Get the all accounts"""
        resp = self.get("v1/accounts", params)
        return resp

    def get_onfido_token(self, account_id, params: dict = None):
        """Get the onfido token"""
        resp = self.get(f"v1/accounts/{account_id}/onfido/sdk/tokens/", params)
        return resp

    def update_onfido_outcome(self, account_id, data):
        """A successful outcome is required for Alpaca to continue the KYC process"""
        resp = self.patch(f"v1/accounts/{account_id}/onfido/sdk/", data)
        return resp

    def get_trading_account(self, account_id):
        resp = self.get(f"v1/trading/accounts/{account_id}/account")
        return resp

    def get_transfer_data_all(self, account_id):
        resp = self.get(f"v1/accounts/{account_id}/transfers")
        return resp

    def delete_transfer_data_id(self, account_id, transfer_id):
        resp = self.delete(f"v1/accounts/{account_id}/transfers/{transfer_id}")
        return resp

    def upload_document_account(self, account_id, data):
        return self.post(f"v1/accounts/{account_id}/documents/upload", data)

    def upload_cip_account(self, account_id, data):
        return self.post(f"v1/accounts/{account_id}/cip", data)

    def get_document_account(self, account_id):
        return self.get(f"v1/accounts/{account_id}/documents")

    def create_bank_relation(self, account_id, data):
        return self.post(f"v1/accounts/{account_id}/recipient_banks", data)

    def delete_bank_relation(self, account_id, bank_id):
        return self.delete(f"v1/accounts/{account_id}/recipient_banks/{bank_id}")

    def get_bank_relation(self, account_id):
        return self.get(f"v1/accounts/{account_id}/recipient_banks?status=ACTIVE")

    def create_clearing_house_relationship(self, account_id: str, data: dict):
        resp = self.post(f"v1/accounts/{account_id}/ach_relationships", data)
        return resp

    def delete_clearing_house_relationship(self, account_id: str, relationship_id: str):
        resp = self.delete(
            f"v1/accounts/{account_id}/ach_relationships/{relationship_id}"
        )
        return resp

    def get_related_clearing_house(self, account_id):
        return self.get(f"v1/accounts/{account_id}/ach_relationships")

    def deposit_account(self, to_account: str, amount: str):
        clearing = self.get_related_clearing_house(to_account)
        clearing_id = clearing[0].get("id")
        resp = self.ach_funding(to_account, clearing_id, "INCOMING", amount)
        return resp

    def withdrawal_account(self, to_account: str, amount: str):
        clearing = self.get_related_clearing_house(to_account)
        clearing_id = clearing[0].get("id")
        resp = self.ach_funding(to_account, clearing_id, "OUTGOING", amount)
        return resp

    def transfer(self, from_account, to_account, amount):
        data = {
            "from_account": from_account,
            "entry_type": "JNLC",
            "to_account": to_account,
            "amount": amount,
            # "description": "test text /fixtures/status=rejected/fixtures/"
        }

        return self.post("v1/journals", data)

    def get_transfer_data(self):
        return self.get("v1/journals")

    def retrive_transfer_data(self, transfer_id):
        return self.get(f"v1/journals/{transfer_id}")

    def create_order_with_setup(
        self,
        account_id: str,
        symbol: str,
        qty: float,
        limit_price: float,
        take_profit: float,
        stop_loss: float,
    ):
        data = {}
        data["symbol"] = symbol
        data["side"] = "buy"
        data["qty"] = qty
        data["type"] = "limit"
        data["time_in_force"] = "gtc"
        data["limit_price"] = limit_price
        data["commission"] = 0.85
        if take_profit:
            data["order_class"] = "bracket"
            data["take_profit"] = {"limit_price": take_profit}
        if stop_loss:
            data["order_class"] = "bracket"
            data["stop_loss"] = {
                "limit_price": stop_loss,
                "stop_price": stop_loss,
            }
        resp = self.submit_order(account_id, data)
        return resp

    def buy_order_direct(self, account_id: str, symbol: str, qty: float):
        data = {}
        data["symbol"] = symbol
        data["side"] = "buy"
        data["qty"] = qty
        data["type"] = "market"
        data["time_in_force"] = "day"
        data["commission"] = 0.85

        resp = self.submit_order(account_id, data)
        return resp

    def sell_order_direct(self, account_id: str, symbol: str, qty: float):
        data = {}
        data["symbol"] = symbol
        data["side"] = "sell"
        data["time_in_force"] = "day"
        data["qty"] = qty
        data["type"] = "market"
        resp = self.submit_order(account_id, data)
        return resp

    def buy_order_limit(
        self, account_id: str, symbol: str, qty: float, limit_price: float
    ):
        data = {}
        data["symbol"] = symbol
        data["side"] = "buy"
        data["qty"] = qty
        data["type"] = "limit"
        data["time_in_force"] = "gtc"
        data["limit_price"] = limit_price
        resp = self.submit_order(account_id, data)
        return resp

    def sell_order_limit(
        self, account_id: str, symbol: str, qty: float, limit_price: float
    ):
        data = {}
        data["symbol"] = symbol
        data["side"] = "sell"
        data["qty"] = qty
        data["type"] = "limit"
        data["time_in_force"] = "gtc"
        data["limit_price"] = limit_price
        resp = self.submit_order(account_id, data)
        return resp

    def get_orders(self, account_id, params: dict = None):
        if params:
            params["limit"] = 50
        else:
            params = dict(limit=50)
        return self.get(f"v1/trading/accounts/{account_id}/orders", params)

    def get_orders_by_order_id(self, account_id, order_id) -> dict:
        return self.get(f"/v1/trading/accounts/{account_id}/orders/{order_id}")

    def cancel_order(self, account_id: str, order_id: str):
        return self.delete(f"v1/trading/accounts/{account_id}/orders/{order_id}")

    def submit_order(self, account_id: str, data: dict):
        resp = self.post(f"v1/trading/accounts/{account_id}/orders", data)
        return resp

    def patch_order(self, account_id: str, order_id: str, data: dict):
        return self.patch(f"v1/trading/accounts/{account_id}/orders/{order_id}", data)

    def get_open_positions(self, account_id) -> list:
        return self.get(f"v1/trading/accounts/{account_id}/positions")

    def get_open_positions_by_symbol(self, account_id, symbol: str) -> dict:
        return self.get(f"v1/trading/accounts/{account_id}/positions/{symbol}")

    def close_position(self, account_id: str, symbol: str):
        resp = self.delete(f"v1/trading/accounts/{account_id}/positions/{symbol}")
        return resp

    def close_all(self, account_id: str):
        resp = self.delete(f"v1/trading/accounts/{account_id}/positions")
        return resp

    def ach_funding(self, account_id: str, ach_id: str, direction: str, amount: str):
        data = {}
        data["transfer_type"] = "ach"
        data["relationship_id"] = ach_id
        data["direction"] = direction
        data["amount"] = amount

        resp = self.post(f"v1/accounts/{account_id}/transfers", data)
        return resp

    def bank_funding(self, account_id: str, bank_id: str, direction: str, amount: str):
        data = {}
        data["transfer_type"] = "wire"
        data["bank_id"] = bank_id
        data["direction"] = direction
        data["amount"] = amount

        resp = self.post(f"v1/accounts/{account_id}/transfers", data)
        return resp


class BrokerEvents(ConnectionBroker):
    def __init__(
        self,
        account_events_handler: Callable[[dict], None] = default_event_handler,
        journal_events_handler: Callable[[dict], None] = default_event_handler,
        trade_events_handler: Callable[[dict], None] = default_event_handler,
        transfer_events_handler: Callable[[dict], None] = default_event_handler,
        non_trade_events_handler: Callable[[dict], None] = default_event_handler,
    ):
        self.account_events_handler = account_events_handler
        self.journal_events_handler = journal_events_handler
        self.trade_events_handler = trade_events_handler
        self.transfer_events_handler = transfer_events_handler
        self.non_trade_events_handler = non_trade_events_handler
        super().__init__()

    def _request(
        self,
        method,
        path,
        data=None,
        base_url=None,
    ):
        base_url = base_url or self._base_url
        url = base_url + "/" + path
        headers = {"Accept": "text/event-stream"}
        opts = {"stream": True, "headers": headers, "auth": self._auth}
        if method.upper() in ["GET", "DELETE"]:
            opts["params"] = data
        else:
            opts["json"] = data

        retry = self._retry
        if retry < 0:
            retry = 0
        while retry >= 0:
            try:
                return self.stream_request(url, opts)
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ChunkedEncodingError,
                ProtocolError,
            ) as err:
                logs.logger.exception(f"{err}\nPut to sleep before retrying.")
                time.sleep(self._retry_wait)
                continue
            except RetryException:
                retry_wait = self._retry_wait
                logs.logger.warning(
                    "sleep {} seconds and retrying {} "
                    "{} more time(s)...".format(retry_wait, url, retry)
                )
                time.sleep(retry_wait)
                retry -= 1
                continue

    def stream_request(self, url, opts):
        response = requests.get(url, **opts)
        return response

    def stream_account_events(self):
        response = self.get("v1/events/accounts/status")
        client = sseclient.SSEClient(response)
        for event in client.events():
            event_data = json.loads(event.data)
            event_data["event_type"] = "account_status"
            self.account_events_handler(event_data)

    def stream_journal_events(self):
        response = self.get("v1/events/journals/status")
        client = sseclient.SSEClient(response)
        for event in client.events():
            event_data = json.loads(event.data)
            event_data["event_type"] = "journal"
            self.journal_events_handler(event_data)

    def stream_trade_events(self):
        response = self.get("v1/events/trades")
        client = sseclient.SSEClient(response)
        for event in client.events():
            event_data = json.loads(event.data)
            event_data["event_type"] = "trade"
            self.trade_events_handler(event_data)

    def stream_transfer_events(self):
        response = self.get("v1/events/transfers/status")
        client = sseclient.SSEClient(response)
        for event in client.events():
            event_data = json.loads(event.data)
            event_data["event_type"] = "transfer"
            self.transfer_events_handler(event_data)

    def stream_non_trade_events(self):
        response = self.get("v1/events/nta")
        client = sseclient.SSEClient(response)
        for event in client.events():
            event_data = json.loads(event.data)
            event_data["event_type"] = "non trading events"
            self.non_trade_events_handler(event_data)

    def stream_all_events(self):
        # Start all threads.
        threads = [
            Thread(
                target=self.stream_account_events,
                daemon=True,
                name="account events",
            ),
            Thread(
                target=self.stream_transfer_events,
                daemon=True,
                name="transfer events",
            ),
            Thread(
                target=self.stream_journal_events,
                daemon=True,
                name="journal events",
            ),
            Thread(
                target=self.stream_trade_events,
                daemon=True,
                name="trade events",
            ),
            Thread(
                target=self.stream_non_trade_events,
                daemon=True,
                name="non trade events",
            ),
        ]
        for event in threads:
            event.start()
            logs.logger.info(f"start listen : {event.name}")

        # Wait all threads to finish.
        for event in threads:
            event.join()
