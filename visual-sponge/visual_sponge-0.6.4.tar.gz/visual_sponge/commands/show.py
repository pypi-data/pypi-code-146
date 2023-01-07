from .. import MACROS, Model

def SHOW(obj, id_):
    if obj is Model:
        instance = Model.models[id_]
        MACROS.CMD = [{"cmd":"SHOW", "obj": "Model", "id": id_}]
    return instance
