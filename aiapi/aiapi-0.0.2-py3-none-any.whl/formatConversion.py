import json
import jsonpath
import xmltodict


# 把dict['xxx']转换成dict.xxx
class DottableDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

    def allowDotting(self, state=True):
        if state:
            self.__dict__ = self
        else:
            self.__dict__ = dict()


def str_to_json(data):
    return json.loads(data)


def json_to_str(data):
    if verify_json(data) is True:
        return json.dumps(data)

    return ""


def search_json(data, search, node="$"):
    ret = jsonpath.jsonpath(data, f"{node}..{search}")
    if ret is False:
        ret = []
    return ret


def verify_json(data):
    json_str = ""
    try:
        json_str = json.dumps(data)
    except Exception as _:
        pass
    try:
        json.loads(json_str)
    except ValueError:
        return False

    return True


def json_to_xml(jsonstr):
    # xmltodict库的unparse()json转xml
    xmlstr = xmltodict.unparse(jsonstr)
    return xmlstr


def xml_to_json(xmlstr):
    # parse是的xml解析器
    xmlparse = xmltodict.parse(xmlstr)
    # json库dumps()是将dict转化成json格式，loads()是将json转化成dict格式。
    # dumps()方法的ident=1，格式化json
    jsonstr = json.dumps(xmlparse, indent=1)
    return jsonstr
