def run(value=None, limit=10, **kwargs):
    if value is None:
        raise RuntimeError("Missing argument 'value'!")
    if limit is None:
        raise RuntimeError("Missing argument 'limit'!")
    doContinue = "true"
    value += 1
    if value >= limit:
        doContinue = "false"
    return {"value": value, "doContinue": doContinue}
