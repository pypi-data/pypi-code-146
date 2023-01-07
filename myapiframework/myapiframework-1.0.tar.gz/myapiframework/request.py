class Request:
    def __init__(self, environ):
        self.method = environ['REQUEST_METHOD']
        self.path = environ['PATH_INFO']
        self.data = environ['wsgi.input']
        self.environ = environ
        self.content_type = environ.get('CONTENT_TYPE')
        self.auth_header = environ.get('HTTP_AUTHORIZATION')
