from django.http import HttpResponse


def serve(request, template):
    content = template.render({}, request)
    return HttpResponse(content)
