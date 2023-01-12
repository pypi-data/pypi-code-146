def get_obj_value(_obj, key):
    return _obj.__dict__.get(key) if hasattr(_obj, '__dict__') else _obj.get(key)
