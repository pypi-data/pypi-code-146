
class SetCustomAuthCookie(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # before view execution.

        response = self.get_response(request)

        # after view finished
        if request.path.startswith('/sites-admin/'):
            return response

        return response
