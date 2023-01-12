def translate_type(hub, type_name: str):
    if type_name == "string":
        return "Text"
    elif type_name in ("map", "object", "structure"):
        return "Dict"
    elif type_name in ("list", "array"):
        return "List"
    elif type_name == "boolean":
        return "bool"
    elif type_name in ("integer", "long"):
        return "int"
    elif type_name in ("float", "double"):
        return "float"
    elif type_name == "timestamp":
        return "Text"
    elif type_name == "blob":
        return "ByteString"
    elif type_name == "object":
        return "Dict"
    else:
        raise NameError(type_name)
