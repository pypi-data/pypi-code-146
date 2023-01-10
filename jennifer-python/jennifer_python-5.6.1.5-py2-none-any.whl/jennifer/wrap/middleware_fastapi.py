import base64

from starlette.middleware.base import BaseHTTPMiddleware
from contextvars import ContextVar
import jennifer.agent.agent
import secrets
import time
import struct
import os
from email.utils import formatdate

REQUEST_CTX_ID_KEY = "request_ctx_id"

wmonid_pack = struct.Struct('>Q')
_request_ctx_id = ContextVar(REQUEST_CTX_ID_KEY, default=None)


def get_request_ctx_id():
    ctx_value = _request_ctx_id.get()
    return ctx_value

# fastapi requires Python 3.6
class APMMiddleware(BaseHTTPMiddleware):
    _agent = jennifer.agent.jennifer_agent()
    jennifer.agent.agent.Agent.set_context_id_func(_agent, get_request_ctx_id)

    @staticmethod
    def get_wmonid(request):
        wmon_id_value = None
        wmon_id_encoded = None

        cookie_wmonid = request.cookies.get('WMONID')
        if cookie_wmonid is not None:
            try:
                wmon_id_encoded = cookie_wmonid
                wmon_id_value, = wmonid_pack.unpack(base64.b64decode(wmon_id_encoded))
            except Exception as e:
                print(e)

        if wmon_id_value is None:
            wmon_id_value = (os.getpid() << 32) + int(time.time())
            wmon_id_encoded = wmonid_pack.pack(wmon_id_value)

        return wmon_id_value, wmon_id_encoded, cookie_wmonid is not None

    @staticmethod
    def set_wmonid(response, wmon_id_value, cookie_exists_wmonid, app_config):
        wmonid_cookie_expire_sec = 31536000
        wmonid_http_only = False
        wmonid_http_secure = False

        if app_config is not None:
            wmonid_cookie_expire_sec = app_config.expire_date_for_wmonid_cookie * 24 * 60 * 60
            wmonid_http_only = app_config.enable_http_only_for_wmonid_cookie
            wmonid_http_secure = app_config.enable_secure_for_wmonid_cookie

        if cookie_exists_wmonid:
            if wmonid_cookie_expire_sec < 0:
                response.set_cookie('WMONID', "deleted", expires='Thu, 01, Jan 1970 00:00:00 GMT', max_age=-1)
        else:
            expire = formatdate(timeval=time.time() + wmonid_cookie_expire_sec, localtime=False, usegmt=True)
            response.set_cookie('WMONID', base64.b64encode(wmon_id_value).decode('ascii'),
                                expires=expire, max_age=wmonid_cookie_expire_sec,
                                secure=wmonid_http_secure, httponly=wmonid_http_only)

    async def dispatch(self, request, call_next):
        transaction = None
        cookie_exists_wmonid = False
        wmonid_encoded = None
        agent_proxy = None
        profiler = None
        request_id = None

        try:
            request_id = _request_ctx_id.set(int.from_bytes(secrets.token_bytes(4), "big"))
            wmonid, wmonid_encoded, cookie_exists_wmonid = self.get_wmonid(request)

            agent_proxy = APMMiddleware._agent
            if agent_proxy is not None:
                transaction = agent_proxy.start_transaction(request.headers, wmonid, path_info=request.url.path)

                if transaction is not None:
                    profiler = transaction.profiler

                    if profiler is not None:
                        profiler.set_root_name("dispatch")
                        if agent_proxy.app_config.dump_http_query:
                            profiler.message('[%s] %s' % (request.method, str(request.url)))
        except:
            jennifer.agent.log_ex('APMMiddleware.dispatch.pre')

        err = None
        response = None

        try:
            response = await call_next(request)
        except Exception as e:
            err = e

        if profiler is None:
            return response

        if err is not None:
            profiler.service_error(err)

        try:
            if response is not None:
                if response.status_code == 404:
                    profiler.not_found("Not Found")

                self.set_wmonid(response, wmonid_encoded, cookie_exists_wmonid, agent_proxy.app_config)

            transaction.end_of_profile()

            _request_ctx_id.reset(request_id)
        except:
            jennifer.agent.log_ex('APMMiddleware.dispatch.post')

        if err is not None:
            raise err

        return response
