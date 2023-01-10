import json
import sys
import requests
from websocket import create_connection, WebSocket, enableTrace
import ssl
from devtools import debug
from pawnlib.config.globalconfig import pawnlib_config as pawn
from pawnlib import output

from pawnlib.output import *
from typing import Any, Dict, Iterator, Tuple, Union, Callable, Type
from pawnlib.typing import date_utils, str2bool
from pawnlib.utils import http as pawn_http
from pawnlib.typing import date_utils
from pawnlib.typing import generator, convert_dict_hex_to_int


class CallWebsocket:

    def __init__(
            self,
            connect_url,
            verbose=0,
            timeout=10,
            send_callback: Callable[..., Any] = None,
            recv_callback: Callable[..., Any] = None,
    ):
        self.connect_url = connect_url
        self.verbose = verbose
        self.timeout = timeout
        self.send_callback = send_callback
        self.recv_callback = recv_callback

        self.ws_url = pawn_http.append_ws(connect_url)
        self.http_url = pawn_http.append_http(connect_url)

        if self.verbose > 3:
            enableTrace(True)

    def run(self, api_url="api/v3/icon_dex/block"):
        ws = create_connection(f"{self.ws_url}/{api_url}", timeout=self.timeout, sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.settimeout(self.timeout)

        if callable(self.send_callback):
            ws.send(self.send_callback())

        while True:
            response = ws.recv()
            if callable(self.recv_callback):
                self.recv_callback(response)


class GoloopWebsocket(CallWebsocket):

    def __init__(self,
                 connect_url,
                 verbose=0,
                 timeout=10,
                 blockheight=0,
                 sec_thresholds=4,
                 monitoring_target=None,
                 ):

        self.connect_url = connect_url
        self.verbose = verbose
        self.timeout = timeout
        self.blockheight = blockheight

        self.sec_thresholds = sec_thresholds

        self.monitoring_target = monitoring_target
        if self.monitoring_target is None:
            self.monitoring_target = ["block"]

        self.compare_diff_time = {}
        self.delay_cnt = {}

        self.block_timestamp_prev = 0
        self.block_timestamp = None
        self.tx_count = 0
        self.tx_timestamp = 0
        self.tx_timestamp_dt = None

        self.blockheight_now = 0

        pawn_http.disable_ssl_warnings()

        super().__init__(
            connect_url=self.connect_url,
            verbose=self.verbose,
            timeout=self.timeout,
            send_callback=self.request_blockheight_callback,
            recv_callback=self.parse_blockheight
        )

    def request_blockheight_callback(self):
        if self.blockheight == 0:
            self.blockheight = self.get_last_blockheight()
        pawn.console.log(f"Call request_blockheight_callback - blockheight: {self.blockheight:,}")
        send_data = {
            "height": hex(self.blockheight)
        }
        return json.dumps(send_data)

    def parse_blockheight(self, response=None):
        response_json = json.loads(response)
        self.compare_diff_time = {}

        if response_json and response_json.get('hash'):
            blockheight_now = response_json.get('height')
            hash_result = self.get_block_hash(response_json.get('hash'))
            self.blockheight_now = hash_result.get("height")
            prev_blockheight = pawn.get("LAST_EXECUTE_POINT")
            # pawn.console.log(f"prev_blockheight = {prev_blockheight}, blockheight={blockheight}, hash_result={hash_result}")
            pawn.set(LAST_EXECUTE_POINT=self.blockheight_now)
            self.block_timestamp = hash_result.get("time_stamp")
            pawn.console.debug(f"BH: {self.blockheight_now:,}, Date: {date_utils.timestamp_to_string(self.block_timestamp)}")
            if self.block_timestamp_prev != 0:
                self.compare_diff_time['block'] = abs(self.block_timestamp_prev - self.block_timestamp)

            tx_list = hash_result.get('confirmed_transaction_list')
            self.tx_count = len(tx_list)

            for tx in tx_list:
                self.tx_timestamp = int(tx.get("timestamp", "0x0"), 0)  # 16진수, timestamp가 string이여야한다.
                if self.tx_timestamp:
                    self.compare_diff_time['tx'] = abs(self.block_timestamp - self.tx_timestamp)

                for target in self.monitoring_target:
                    diff_time = self.compare_diff_time.get(target, 0) / 1_000_000
                    if diff_time != 0 and abs(diff_time) > self.sec_thresholds:
                        pawn.console.log(f"[{target.upper()}] {self.output_format(key_string=target, diff_time=diff_time, is_string=True)}")
                        dump(hash_result['confirmed_transaction_list'])
                        # pawn.console.log(f"{self.compare_diff_time}, {tx_count}")
            self.block_timestamp_prev = self.block_timestamp

        else:
            pawn.console.log(response_json)

    def output_format(self, key_string="", diff_time=0, is_string=False):
        self.delay_cnt[key_string] = self.delay_cnt.get(key_string, 0) + 1

        blockheight_date = date_utils.timestamp_to_string(self.block_timestamp)
        if key_string == "block":
            diff_message = f"BH_time(now): {blockheight_date}, " \
                           f"BH_time(prev): {date_utils.timestamp_to_string(self.block_timestamp_prev)}"
        else:
            diff_message = f"BH_time: {blockheight_date}, TX_time: {date_utils.timestamp_to_string(self.tx_timestamp)}"

        result = (f"[{key_string} Delay][{date_utils.second_to_dayhhmm(diff_time)}] ",
                  f"<{self.delay_cnt[key_string]}> BH: {self.blockheight_now}, "
                  # f"diff: {date_utils.second_to_dayhhmm(diff_time)}, "
                  f"TX_CNT:{self.tx_count}, {diff_message}")
        if is_string:
            return "".join(result)
        return result

    def get_last_blockheight(self):
        res = pawn_http.jequest(method="post", url=f"{self.http_url}/api/v3", data=generator.generate_json_rpc(method="icx_getLastBlock"))
        pawn.console.log(res['json'].get('result'))
        if res['json'].get('result'):
            return res['json']['result'].get('height')

    def get_block_hash(self, hash):
        res = pawn_http.jequest(
            method="post",
            url=f"{self.http_url}/api/v3",
            data=generator.generate_json_rpc(method="icx_getBlockByHash", params={"hash": hash})
        )
        if res.get('json'):
            return res['json'].get('result')
        else:
            cprint(res, "red")


def gen_rpc_parms(method=None, params=None):
    default_rpc = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": method,
    }

    if params:
        default_rpc['params'] = params
    return default_rpc


def getBlockByHash(nodeHost, hash):
    url = pawn_http.append_http(f"{nodeHost}/api/v3")
    data = gen_rpc_parms(method="icx_getBlockByHash", params={"hash": hash})
    response = requests.post(url=url, data=json.dumps(data), timeout=10, verify=False)
    return response.json()


def getTransactionByHash(nodeHost, hash):
    url = pawn_http.append_http(f"{nodeHost}/api/v3")
    data = gen_rpc_parms(method="icx_getTransactionByHash", params={"txHash": hash})
    response = requests.post(url=url, data=json.dumps(data), timeout=10, verify=False)
    return response.json()


def getLastBlock(nodeHost):
    url = pawn_http.append_http(f"{nodeHost}/api/v3")
    data = gen_rpc_parms(method="icx_getLastBlock")
    response = requests.post(url=url, data=json.dumps(data), timeout=10, verify=False)

    if response.status_code == 200:
        json_res = response.json()
        if json_res.get("result"):
            return json_res["result"]["height"]
    else:
        print(response)
        sys.exit()
    return 0

