from .. import MACROS, Model

def DEFAULT(mid):
    Model.WORKING = Model.models[mid]
    MACROS.CMD = [{"cmd":"DEFAULT", "mid": Model.WORKING.id}]
    return Model.WORKING
