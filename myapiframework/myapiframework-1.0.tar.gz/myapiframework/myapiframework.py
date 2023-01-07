from .request import Request
from parse import parse
from .exceptions import HandlerWasNotFoundException
from .backends import BaseBackend


class RoutersConstructor:
    def __init__(self) -> None:
        self._routers = {'GET': {},
                         'POST': {},
                         'PUT': {},
                         'PATCH': {}}
        
    def get(self, path):
        def wrapper(handler):
            self._routers['GET'][path] = handler
        return wrapper

    def post(self, path):
        def wrapper(handler):
            self._routers['POST'][path] = handler
        return wrapper

    def put(self, path):
        def wrapper(handler):
            self._routers['PUT'][path] = handler
        return wrapper
    
    def patch(self, path):
        def wrapper(handler):
            self._routers['PATCH'][path] = handler
        return wrapper


class MyAPI(RoutersConstructor):
    authentication_class = BaseBackend

    def __init__(self):
        super(MyAPI, self).__init__()

    def __call__(self, environ: dict, start_response):
        request = Request(environ)
        request.user = self.authentication_class.authenticate(request)
        data = self.request_handle(request, start_response)
        return iter([data])

    def get_handler(self, request_path, method):
        for path, handler in self._routers[method].items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return parse_result.named, handler
        raise HandlerWasNotFoundException

    def request_handle(self, request, start_response):
        try:
            request_data, handler = self.get_handler(request.path, request.method)
        except HandlerWasNotFoundException:
            start_response('404', [])
            return b'page not found'

        result = handler(request, **request_data)
        start_response(result.status, [])
        return result.data

