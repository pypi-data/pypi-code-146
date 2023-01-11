from ast import literal_eval
from bank_sync.models import RequestLogs, ResponseLogs
from django.db import connections

class APILogsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        # Confirm the path requested
        if len(request.path.split("/"))>2:
            # confirm that this is not the django admin page path
            if request.path.split("/")[1] != 'admin':
                self.log_request(request)

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        
        # Confirm the path requested
        if len(request.path.split("/"))>2:
            # confirm that this is not the django admin page path
            if request.path.split("/")[1] != 'admin':
                self.log_response(response,request.headers.get("Host", ""))

        return response

    def log_request(self, request):
        request_logs = None
        try:
            request_logs = RequestLogs.objects.create(
                ip=request.headers.get("Host", ""),
                method=request.method,
                path=request.path,
                content_type=request.content_type,
                content_params=request.content_params,
                headers=dict(request.headers),
                user=str(request.user)
            )

            if len(request.body):
                request_logs.body = literal_eval(request.body.decode("utf-8").replace("false","False").replace("true","True").replace("null","None"))
                request_logs.save()
                connections.close_all()
        except Exception as e:
            if request_logs is not None:
                request_logs.error = e
                request_logs.save()
                connections.close_all()

    def log_response(self, response, ip):  
        response_logs = None      
        try:
            response_logs = ResponseLogs.objects.create(ip=ip,headers=dict(response.headers))
            if len(response.data):
                response_logs.content = response.data
                response_logs.save()
                connections.close_all()
        except Exception as e:
            if response_logs is not None:
                response_logs.error = e
                response_logs.save()
                connections.close_all()
