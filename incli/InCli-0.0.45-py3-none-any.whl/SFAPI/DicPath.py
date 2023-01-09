from . import jsonFile



def open():
    filename = "/Users/uormaechea/Documents/Dev/python/Industries copy 3/tests/output/debug/11:58:40--getBasketDetail_res.json"
    dic = jsonFile.read(filename)
    return dic

def find(dic, path):
    chunks = path.split(".")
    return _find(dic,chunks)

def _pop0(paths):
    p = paths.copy()
    return p.pop(0)

def _find(dic,paths):
    if type(dic) is list:
        for d in dic:
            _find(dic,paths)

    for key in dic.keys():
        if key == paths[0]:
            _paths = _pop0(paths)
            if len(_paths) == 0:
                return dic[key]
            else:
                found = _find(dic['key'],_paths)
                if found != None:
                    return found
        _obj = dic[key]
        if type(_obj) is list or type(_obj) is dict:
            return 
        if type(_obj) is dict:
            return 2
        return None
    