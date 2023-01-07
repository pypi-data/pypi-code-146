from .. import MACROS, Model

def HIDE(obj, id_):
    if obj is Model:
        instance = Model.models[id_]
        MACROS.CMD = [{"cmd":"HIDE", "obj": "Model", "id": id_}]
    return instance
