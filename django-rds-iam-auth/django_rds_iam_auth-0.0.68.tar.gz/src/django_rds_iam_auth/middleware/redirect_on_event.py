from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

class RedirectOnEventRules(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        t=2
        return response

    def process_exception(self, request, exception):
        # from app import settings

        ex_parts = str(exception).split(' ')
        if hasattr(settings, 'REDIRECT_ON_EVENT_RULES') and isinstance(settings.REDIRECT_ON_EVENT_RULES, list) and len(settings.REDIRECT_ON_EVENT_RULES) > 0:
            for item in settings.REDIRECT_ON_EVENT_RULES:
                matched = True
                if 'trigger_path' in item and 'exception' in item and 'redirect_path' in item:
                    if request.path.startswith(item['trigger_path']):
                        exception_match_parts = str(item['exception']).split(' ')
                        part_number = 0
                        for part in exception_match_parts:
                            if part != '{$}' and part != ex_parts[part_number]:
                                matched = False
                                break
                            part_number += 1
                        if matched:
                            return HttpResponseRedirect(reverse(item['redirect_path']))




        return None

    # REDIRECT_ON_EVENT_RULES = [
    #     {
    #         'type': 'token expired',
    #         'exception': "The connection {$} doesn't exist",
    #         'trigger_path': "/sites-admin",
    #         'redirect_path': '/sites-admin/logout'
    #     }
    # ]