import json
import cgi
from .fields import FileField


def parse_json(data):
    return json.loads(str(data.read(), 'utf-8'))


def parse_form(data, request):
    content_type, pdict = cgi.parse_header(request.content_type)
    pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
    form = cgi.parse_multipart(data, pdict)
    for key, value in form.items():
        for i in range(len(value)):
            if type(value[i]) == bytes:
                value[i] = FileField(value[i])
        if len(value) == 1:
            form[key] = value[0]
    return form
