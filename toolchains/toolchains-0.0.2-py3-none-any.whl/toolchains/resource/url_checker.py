#!/usr/bin/env python3
# pip3 install --compile --install-option="--with-openssl" pycurl
import pycurl
from devtools import debug, Timer
import json
from ..__version__ import __version__
from ..models.http_models import ResponseField, TimingInfo
from typing import Union, Literal
from pawnlib.typing import check, converter, list_depth
import operator as _operator
from pawnlib.config import pawnlib_config as pawn
from pawnlib.output import dump
from pawnlib.typing.converter import FlatDict

DEFAULT_UA = f"url-checker Agent/{__version__}"
DEFAULT_LANGUAGE = "en"
DEFAULT_ENCODING = "utf-8"
# ALLOW_OPERATOR = ["!=", "==", ">=", "<=", ">", "<", "include", "exclude"]


def get_operator_truth(inp, relate, cut):
    ops = {
        '>': _operator.gt,
        '<': _operator.lt,
        '>=': _operator.ge,
        '<=': _operator.le,
        '==': _operator.eq,
        '!=': _operator.ne,
        'include': lambda y, x: x in y,
        'exclude': lambda y, x: x not in y
    }
    return ops[relate](inp, cut)


def guess_key(find_key, data):
    guessed_result = []
    if isinstance(data, dict):
        for k, v in data.keys():
            if find_key in k:
                guessed_result.append(k)
    elif isinstance(data, list):
        for k in data:
            if find_key in k:
                guessed_result.append(k)
    return guessed_result


class SuccessCriteria:
    def __init__(
            self,
            target: str = "",
            operator: Literal["!=", "==", ">=", "<=", ">", "<", "include", "exclude"] = "",
            expected: Union[str, int, float] = "",
            # operator: Literal[tuple(ALLOW_OPERATOR)] = ""
    ):
        if target:
            self.target = target
        self.operator = operator
        self.expected = expected
        self.result = False

        if (self.expected or self.expected == 0) and self.target and self.operator:
            try:
                if check.is_float(self.target):
                    self.target = float(self.target)
                elif check.is_int(self.target):
                    self.target = int(self.target)

                if check.is_float(self.expected):
                    self.expected = float(self.expected)
                elif check.is_int(self.expected):
                    self.expected = int(self.expected)

                self.result = get_operator_truth(self.target, self.operator, self.expected)
            except:
                self.result = False

    def __str__(self):
        return "<SuccessCriteria %s>" % self.__dict__

    def __repr__(self):
        return "<SuccessCriteria %s>" % self.__dict__

    def to_dict(self):
        return self.__dict__


class SuccessResponse(SuccessCriteria):
    def __init__(
            self,
            target_key: str = "",
            operator: Literal["!=", "==", ">=", "<=", ">", "<", "include", "exclude"] = "",
            expected: Union[str, int, float] = "",
            target: dict = {},
    ):
        # if not target or not operator or not expected or target_key:
        #     raise ValueError(f"target: {target}, operator: {operator}, expected: {expected}, target_key: {target_key} ")

        if not isinstance(target, dict):
            pawn.console.log(f"[red]<Error>[/red] '{target}' is not dict")
            self.result = False
            raise ValueError(f"target is not dict - '{target}'")

        self.target_key = target_key
        self.target = FlatDict(target)

        _selected_flatten_target = self.target.get(self.target_key)
        super().__init__(target=_selected_flatten_target, operator=operator, expected=expected)

        if not _selected_flatten_target:
            pawn.console.debug(f"[red]<Error>[/red] '{self.target_key}' is not attribute in {list(self.target.keys())}")
            pawn.console.log(f"[red]<Error>[/red] '{self.target_key}' not found. \n Did you mean {guess_key(self.target_key, self.target.keys())} ?")
            self.result = False


class CheckURL:

    # TODO : Cookies / success_criteria

    def __init__(self,
                 url: str = None,
                 method: str = "GET",
                 params: dict = {},  ### jsshin
                 headers: dict = {},
                 data: dict = {},
                 timeout: int = 3000,
                 encoding: str = DEFAULT_ENCODING,
                 ignore_ssl: bool = False,
                 verbose: int = 0,
                 success_criteria: Union[dict, list] = None,
                 success_operator: Literal["and", "or"] = "and",
                 cookielist: dict = {}  ### jsshin
                 ):

        self.curl = pycurl.Curl()
        self.url = url
        self.method = method
        self.params = converter.dict_to_line(params).replace(",", "&")  ### jsshin
        self.headers = headers
        self.data = data
        self.timeout = timeout
        self.encoding = encoding
        self.ignore_ssl = ignore_ssl
        self.verbose = verbose
        self.success_criteria = success_criteria
        self.success_operator = success_operator

        self.success = None
        self._success_results = []
        self._success_criteria = None

        self._response_line = ""
        self._response_headers = {}
        self._response_body = []

        self.response = ResponseField()

        self._url = ''
        self._timing = ''
        self._redirectcount = 0
        self._cookielist = ""
        self.cookielist = converter.dict_to_line(cookielist).replace(",", ";")  ### jsshin

        self.count = 0

        if self.url:
            self.run()
        else:
            pawn.console.log("[red] url not found")

    def run(self):
        self.prepare()

        try:
            self.curl.perform()
        except pycurl.error:
            self.response.error = self.curl.errstr()
        except Exception as e:
            self.response.error = f"not pycurl error -  {e}"
            # self.response.status_code = 999
        # self.status_code = self.curl.getinfo(pycurl.RESPONSE_CODE)
        self.finalize()
        self.check_criteria()
        self.success = self.is_success()
        pawn.console.debug(f"url: {self._url}, method: {self.method}")

    def check_criteria(self, success_criteria=None, success_operator=None):
        if success_criteria:
            self.success_criteria = success_criteria
        if success_operator:
            self.success_operator = success_operator

        depth = list_depth(self.success_criteria)
        if depth == 1:
            self.success_criteria = [self.success_criteria]

        for criteria in self.success_criteria:
            if isinstance(criteria, list):
                criteria.append(self.get_response())
                self._success_results.append(SuccessResponse(*criteria))
            elif isinstance(criteria, dict):
                criteria['target'] = self.get_response()
                self._success_results.append(SuccessResponse(**criteria))
        pawn.console.debug(self._success_results)

    def is_success(self):
        success_count = 0
        expected_count = len(self._success_results)

        if isinstance(self._success_results, list):
            for _result in self._success_results:
                if _result.result:
                    success_count += 1

        if self.success_operator == "and" and success_count == expected_count:
            return True
        elif self.success_operator == "or" and success_count > 0:
            return True
        return False

    def get_response(self):
        if isinstance(self.response, dict):
            return self.response
        return self.response.__dict__

    def _gathering_response(self):
        status_code = self.curl.getinfo(pycurl.RESPONSE_CODE)
        if status_code:
            self.response.status_code = int(status_code)
        self.response.text = "".join(self._response_body)
        try:
            json_dict = json.loads(self.response.text)
        except:
            json_dict = {}
        self.response.json = json_dict
        self.response.headers = self._response_headers
        self.response.timing = self._timing

    def _header_callback(self, header_buffer):
        if isinstance(header_buffer, bytes):
            header_buffer = header_buffer.decode('UTF-8')
        header_buffer = header_buffer.replace("\r\n", "")

        if header_buffer.startswith("HTTP"):
            if self._response_line and self._response_line.find("302") >= 0:
                self._response_headers = {}  # clear headers if redirected.
            self._response_line = header_buffer
        else:
            header_buffer_arr = header_buffer.split(":", maxsplit=1)
            if len(header_buffer_arr) > 1:
                header_key = header_buffer_arr[0].strip().title()
                self._response_headers[header_key] = header_buffer_arr[1].strip()

    def _body_callback(self, body_buffer):
        if isinstance(body_buffer, bytes):
            body_buffer = body_buffer.decode('UTF-8')
        body_buffer = body_buffer.replace("\r\n", "")
        self._response_body.append(body_buffer)

    def prepare(self):
        if len(self.headers) > 0:
            self.headers = {k.title(): v for k, v in self.headers.items()}
        if self.headers.get('User-Agent', None) is None:
            self.headers['User-Agent'] = DEFAULT_UA
        self.curl.setopt(pycurl.OPT_CERTINFO, 1)
        self.curl.setopt(pycurl.VERBOSE, self.verbose)
        ### jsshin
        if self.params:
            self.curl.setopt(pycurl.URL, self.url + '?' + self.params)
        else:
            self.curl.setopt(pycurl.URL, self.url)
        ###
        self.curl.setopt(pycurl.FOLLOWLOCATION, 1)
        self.curl.setopt(pycurl.TIMEOUT_MS, self.timeout)
        self.curl.setopt(pycurl.CONNECTTIMEOUT, int(self.timeout / 1000))
        self.curl.setopt(pycurl.MAXREDIRS, 5)
        ### jsshin
        if self.cookielist:
            self.curl.setopt(pycurl.COOKIE, self.cookielist + ";HttpOnly")
        ###
        # self.curl.setopt(pycurl.HEADER, 1)
        self.curl.setopt(pycurl.HEADERFUNCTION, self._header_callback)
        self.curl.setopt(pycurl.WRITEFUNCTION, self._body_callback)

        if self.data:
            self.data = json.dumps(self.data)  # dict to json

        if self.headers:
            headers_list = ["%s: %s" % t for t in self.headers.items()]
            self.curl.setopt(pycurl.HTTPHEADER, headers_list)

        if self.ignore_ssl:
            self.curl.setopt(pycurl.SSL_VERIFYPEER, False)
            self.curl.setopt(pycurl.SSL_VERIFYHOST, False)

        self.set_method()

    def set_method(self):
        self.method = self.method.upper()
        allowed_methods = ['POST', 'GET', 'HEAD', 'PATCH', 'POST', 'PUT', 'DELETE']
        if self.method == "POST":
            self.curl.setopt(pycurl.POST, 1)
            self.curl.setopt(pycurl.POSTFIELDS, self.data)
            # self.curl.setopt(pycurl.READDATA, self.body)
            # self.curl.setopt(pycurl.POSTFIELDSIZE, len(self.body))

        elif self.method == "GET":
            self.curl.setopt(pycurl.HTTPGET, 1)
        elif self.method in allowed_methods:
            self.curl.setopt(pycurl.CUSTOMREQUEST, self.method)
        else:
            raise Exception(f"Unsupported method. {self.method}")

    def finalize(self, c=None):
        """finalize a Curl object and extract information from it."""
        self._url = self.curl.getinfo(pycurl.EFFECTIVE_URL)
        # timing info
        nt = self.curl.getinfo(pycurl.NAMELOOKUP_TIME)
        ct = self.curl.getinfo(pycurl.CONNECT_TIME)
        pt = self.curl.getinfo(pycurl.PRETRANSFER_TIME)
        st = self.curl.getinfo(pycurl.STARTTRANSFER_TIME)
        tt = self.curl.getinfo(pycurl.TOTAL_TIME)
        rt = self.curl.getinfo(pycurl.REDIRECT_TIME)
        self._timing = TimingInfo(nt, ct, pt, st, tt, rt).to_dict()
        self._redirectcount = self.curl.getinfo(pycurl.REDIRECT_COUNT)
        self._cookielist = self.curl.getinfo(pycurl.INFO_COOKIELIST)
        self._gathering_response()
        self.curl.close()
        # self._downloadfile = None
