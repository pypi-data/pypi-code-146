
def dataclass_format(dataclass_name, _dict) -> str:
    attributes = []
    for k, v in _dict.items():
        attributes.append(f"{k}: {type(v).__name__}")
    return """
    @dataclass
    class %s:
        %s
    """ % (dataclass_name, "\n\t".join(attributes))
