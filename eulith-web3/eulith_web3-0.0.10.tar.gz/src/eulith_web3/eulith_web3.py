import time
import urllib.parse
from urllib.parse import urljoin
import uuid
from typing import Union, Any, cast, Callable, Dict, Optional, List

import requests
import web3.middleware
from eth_typing import URI, ChecksumAddress
from eth_utils import is_hex_address
from requests import Response
from web3 import Web3, HTTPProvider
from web3.types import RPCEndpoint, RPCResponse, TxParams

from eulith_web3.erc20 import EulithERC20, TokenSymbol, EulithWETH
from eulith_web3.swap import EulithSwapProvider, EulithSwapRequest, EulithLiquiditySource


class EulithAuthException(Exception):
    pass


class EulithRpcException(Exception):
    pass


class ApiToken:
    def __init__(self, token: str, expire: int) -> None:
        self.token = token
        self.expire = expire

    def expires_in_hours(self) -> float:
        now = int(time.time())
        return (self.expire - now) / 3600


def get_api_access_token(eulith_url: URI, eulith_refresh_token: str) -> ApiToken:
    headers = {"Authorization": "Bearer " + eulith_refresh_token, "Content-Type": "application/json"}
    url = urljoin(eulith_url, URI("v0/api/access"))
    response = requests.get(url, headers=headers)
    handle_http_response(response)
    json = response.json()
    token = ApiToken(json['token'], json['exp'])
    return token


def handle_http_response(resp: Response):
    if resp.status_code == 400:
        raise EulithAuthException(f"status: {str(resp.status_code)}, message: {resp.text}")
    if resp.status_code != 200:
        raise EulithRpcException(f"status: {str(resp.status_code)}, message: {resp.text}")


def handle_rpc_response(resp: RPCResponse):
    if 'error' in resp and resp['error'] != "":
        raise EulithRpcException("RPC Error: " + str(resp['error']))


def add_params_to_url(url: str, params) -> str:
    url_parts = urllib.parse.urlparse(url)
    query = dict(urllib.parse.parse_qsl(url_parts.query))
    query.update(params)

    return url_parts._replace(query=urllib.parse.urlencode(query)).geturl()


def get_headers(url: str, token: str) -> Dict:
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    if 'localhost' in url:
        headers['X-Test'] = 'true'

    return headers


class EulithData:
    def __init__(self, eulith_url: Union[URI, str],
                 eulith_refresh_token: str, private: bool) -> None:
        self.eulith_url: URI = URI(eulith_url)
        self.private = private
        self.eulith_refresh_token: str = eulith_refresh_token
        self.atomic: bool = False
        self.tx_id: str = ""
        self.api_access_token: ApiToken = get_api_access_token(self.eulith_url, self.eulith_refresh_token)
        headers = get_headers(eulith_url, self.api_access_token.token)
        self.http = HTTPProvider(endpoint_uri=eulith_url, request_kwargs={
            'headers': headers
        })

    def send_transaction(self, params) -> RPCResponse:
        try:
            return self.http.make_request(RPCEndpoint("eth_sendTransaction"), params)
        except requests.exceptions.HTTPError as e:
            message = e.response.json().get('error', 'request failed for unknown reason')
            raise EulithRpcException(message)

    def start_transaction(self, account: str, gnosis: str):
        self.atomic = True
        self.tx_id = str(uuid.uuid4())
        params = {'auth_address': account, 'atomic_tx_id': self.tx_id}
        if len(gnosis) > 0:
            params['gnosis_address'] = gnosis
        new_url = add_params_to_url(self.eulith_url, params)
        self.http.endpoint_uri = new_url

    def commit(self) -> TxParams:
        self.atomic = False  # we need to do this even if things fail
        params = {}
        try:
            response = self.http.make_request(RPCEndpoint("eulith_commit"), params)
            handle_rpc_response(response)
            self.tx_id = ""
            return cast(TxParams, response['result'])
        except requests.exceptions.HTTPError as e:
            message = e.response.json().get('error', 'request failed for unknown reason')
            raise EulithRpcException(message)

    def rollback(self):
        self.commit()

    def refresh_api_token(self):
        self.api_access_token: ApiToken = get_api_access_token(self.eulith_url, self.eulith_refresh_token)
        headers = get_headers(self.eulith_url, self.api_access_token.token)
        self.http = HTTPProvider(endpoint_uri=self.eulith_url, request_kwargs={
            'headers': headers
        })

    def is_close_to_expiry(self) -> bool:
        return self.api_access_token.expires_in_hours() < 6

    def swap_quote(self, params: EulithSwapRequest) -> (bool, RPCResponse):
        try:
            sell_token: EulithERC20
            buy_token: EulithERC20
            sell_amount: float
            recipient: Optional[ChecksumAddress]
            route_through: Optional[EulithSwapProvider]
            slippage_tolerance: Optional[float]
            liquidity_source: Optional[EulithLiquiditySource]

            sell_address = params.get('sell_token').address
            buy_address = params.get('buy_token').address
            parsed_params = {
                'sell_token': sell_address,
                'buy_token': buy_address,
                'sell_amount': params.get('sell_amount')
            }
            recipient = params.get('recipient', None)
            route_through = params.get('route_through', None)
            liquidity_source = params.get('liquidity_source', None)
            slippage_tolerance = params.get('slippage_tolerance', None)

            if recipient:
                parsed_params['recipient'] = recipient
            if route_through:
                parsed_params['route_through'] = route_through
            if liquidity_source:
                parsed_params['liquidity_source'] = liquidity_source
            if slippage_tolerance:
                parsed_params['slippage_tolerance'] = slippage_tolerance

            return True, self.http.make_request(RPCEndpoint("eulith_swap"), [parsed_params])
        except requests.exceptions.HTTPError as e:
            message = e.response.json().get('error', 'request failed for unknown reason')
            return False, RPCResponse(error=message)

    def lookup_token_symbol(self, symbol: TokenSymbol) -> (bool, ChecksumAddress):
        try:
            res = self.http.make_request(RPCEndpoint("eulith_erc_lookup"), [{'symbol': symbol}])
            parsed_res = res.get('result', [])
            if len(parsed_res) != 1:
                return False, RPCResponse(error=f"unexpected response for {symbol} lookup, token isn't recognized")
            return True, parsed_res[0].get('contract_address')
        except requests.exceptions.HTTPError as e:
            message = e.response.json().get('error', 'request failed for unknown reason')
            return False, RPCResponse(error=message)


class EulithWeb3(Web3):
    def __init__(self,
                 eulith_url: Union[URI, str],
                 eulith_refresh_token: str,
                 signing_middle_ware: Any = None,
                 private: bool = False,
                 **kwargs
                 ) -> None:
        if signing_middle_ware:
            eulith_url = add_params_to_url(eulith_url, {'auth_address': signing_middle_ware.address})

        self.eulith_data = EulithData(eulith_url, eulith_refresh_token, private)
        http = self._make_http()
        kwargs.update(provider=http)
        super().__init__(**kwargs)

        if signing_middle_ware:
            self.middleware_onion.add(signing_middle_ware)
        self.middleware_onion.add(eulith_atomic_middleware)
        self.middleware_onion.add(web3.middleware.request_parameter_normalizer)
        self.middleware_onion.add(web3.middleware.pythonic_middleware, "eulith_pythonic")
        self.middleware_onion.add(eulith_api_token_middleware)

    def _eulith_send_atomic(self, params) -> RPCResponse:
        return self.eulith_data.send_transaction(params)

    def eulith_start_transaction(self, account: str, gnosis: str = "") -> None:
        if not is_hex_address(account):
            raise TypeError("account must be a hex formatted address")
        if len(gnosis) > 0 and not is_hex_address(gnosis):
            raise TypeError("gnosis must either be blank or a hex formatted address")
        self.eulith_data.start_transaction(account, gnosis)

    def eulith_commit_transaction(self) -> TxParams:
        return self.eulith_data.commit()

    def eulith_rollback_transaction(self):
        self.eulith_data.rollback()

    def eulith_contract_address(self, account: str) -> str:
        if not is_hex_address(account):
            raise TypeError("account must be a hex formatted address")
        params = {}
        try:
            response = self.manager.provider.make_request("eulith_get_contracts", params)
            handle_rpc_response(response)
            contracts = response['result']['contracts']
            for c in contracts:
                if c['authorized_address'].lower() == account.lower():
                    return c['contract_address']
            return ""
        except requests.exceptions.HTTPError as e:
            message = e.response.json().get('error', 'request failed for unknown reason')
            raise EulithRpcException(message)

    def eulith_create_contract_if_not_exist(self, account: str) -> str:
        c = self.eulith_contract_address(account)
        if c == "":
            c = self.eulith_create_contract(account)

        return c

    def eulith_create_contract(self, account: str) -> str:
        if not is_hex_address(account):
            raise TypeError("account must be a hex formatted address")
        params = [{'authorized_address': account}]
        try:
            response = self.manager.provider.make_request("eulith_new_contract", params)
            handle_rpc_response(response)
            result = response['result']
            self.eth.wait_for_transaction_receipt(result['new_contract_tx_hash'])

            return result['contract_address']
        except requests.exceptions.HTTPError as e:
            message = e.response.json().get('error', 'request failed for unknown reason')
            raise EulithRpcException(message)

    def eulith_refresh_api_token(self):
        self.eulith_data.refresh_api_token()
        http = self._make_http()
        self.provider = http

    def eulith_refresh_api_token_if_necessary(self):
        if self.eulith_data.is_close_to_expiry():
            self.eulith_refresh_api_token()

    def eulith_swap_quote(self, params: EulithSwapRequest) -> (float, List[TxParams]):
        status, res = self.eulith_data.swap_quote(params)
        if status:
            price = res.get('result', {}).get('price', 0.0)
            txs = res.get('result', {}).get('txs', [])
            return price, txs
        else:
            raise EulithRpcException(res)

    def _make_http(self):
        url = self.eulith_data.eulith_url
        if self.eulith_data.private:
            url = add_params_to_url(url, {'private': 'true'})

        headers = get_headers(url, self.eulith_data.api_access_token.token)

        http = HTTPProvider(endpoint_uri=url, request_kwargs={
            'headers': headers
        })

        return http

    def eulith_send_multi_transaction(self, txs: [TxParams]):
        for tx in txs:
            tx_hash = self.eth.send_transaction(tx)
            if not self.eulith_data.atomic:
                self.eth.wait_for_transaction_receipt(tx_hash)

    def eulith_get_erc_token(self, symbol: TokenSymbol) -> Union[EulithERC20, EulithWETH]:
        status, contract_address_or_error = self.eulith_data.lookup_token_symbol(symbol)
        if status:
            if symbol == TokenSymbol.WETH:
                return EulithWETH(self, contract_address_or_error)
            else :
                return EulithERC20(self, contract_address_or_error)
        else:
            raise EulithRpcException(contract_address_or_error)


def eulith_atomic_middleware(
        make_request: Callable[[RPCEndpoint, Any], Any], web3: "Web3"
) -> Callable[[RPCEndpoint, Any], RPCResponse]:
    def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
        try:
            if method != "eth_sendTransaction" or not web3.eulith_data.atomic:
                return make_request(method, params)

            return cast(EulithWeb3, web3)._eulith_send_atomic(params)
        except requests.exceptions.HTTPError as e:
            message = e.response.json().get('error', 'request failed for unknown reason')
            raise EulithRpcException(message)

    return middleware


def eulith_api_token_middleware(
        make_request: Callable[[RPCEndpoint, Any], Any], web3: "Web3"
) -> Callable[[RPCEndpoint, Any], RPCResponse]:
    def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
        try:
            ew3 = cast(EulithWeb3, web3)
            ew3.eulith_refresh_api_token_if_necessary()

            return make_request(method, params)
        except requests.exceptions.HTTPError as e:
            message = e.response.json().get('error', 'request failed for unknown reason')
            raise EulithRpcException(message)

    return middleware
