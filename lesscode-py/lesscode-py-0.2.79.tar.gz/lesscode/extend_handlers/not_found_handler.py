import json
import logging

from tornado.web import RequestHandler

from lesscode.utils.json import JSONEncoder
from lesscode.web.response_result import ResponseResult
from lesscode.web.status_code import StatusCode


class NotFoundHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Request-Id", self.request.headers.get("Request-Id", ""))
        self.set_header("Plugin-Running-Time", self.request.headers.get("Plugin-Running-Time", ""))
        self.set_header("Access-Control-Allow-Headers",
                        "x-requested-with,Authorization,Can-read-cache,Content-Type,User")
        self.set_header("Access-Control-Allow-Methods", "POST,GET,PUT,DELETE,OPTIONS")
        self.set_header("Access-Control-Expose-Headers", "Access-Token")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    def data_received(self, chunk: bytes):
        pass

    async def get(self):
        self.write(json.dumps(ResponseResult(StatusCode.REQUEST_PATH_NOT_FOUND), ensure_ascii=False, cls=JSONEncoder))

    async def post(self):
        self.write(json.dumps(ResponseResult(StatusCode.REQUEST_PATH_NOT_FOUND), ensure_ascii=False, cls=JSONEncoder))

    async def put(self):
        self.write(json.dumps(ResponseResult(StatusCode.REQUEST_PATH_NOT_FOUND), ensure_ascii=False, cls=JSONEncoder))

    async def patch(self):
        self.write(json.dumps(ResponseResult(StatusCode.REQUEST_PATH_NOT_FOUND), ensure_ascii=False, cls=JSONEncoder))

    async def delete(self):
        self.write(json.dumps(ResponseResult(StatusCode.REQUEST_PATH_NOT_FOUND), ensure_ascii=False, cls=JSONEncoder))

    async def head(self):
        self.write(json.dumps(ResponseResult(StatusCode.REQUEST_PATH_NOT_FOUND), ensure_ascii=False, cls=JSONEncoder))

    async def options(self):
        self.write(json.dumps(ResponseResult(StatusCode.REQUEST_PATH_NOT_FOUND), ensure_ascii=False, cls=JSONEncoder))
