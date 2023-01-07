from .. import MACROS, Model

def DELETE(obj, id_):
    if obj is Model:
        instance = Model.models[id_]
        Model.models[id_] = None
        while Model.models and Model.models.get(Model.id - 1, None) is None:
            Model.models.pop(Model.id - 1, None)
            Model.id -= 1
        MACROS.CMD = [{"cmd":"DELETE", "obj": "Model", "id": id_}]
        if Model.WORKING is instance:
            if Model.models:
                Model.WORKING = next(reversed(Model.models.values()))
                MACROS.CMD.append({"cmd":"DEFAULT", "mid": Model.WORKING.id})
            else:
                Model.WORKING = None
    return instance
