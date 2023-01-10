import time


def run(all_arguments=None):
    if all_arguments is None:
        raise RuntimeError("Missing argument 'all_arguments'!")
    time.sleep(1)
    value = all_arguments["value"]
    value = value + 1
    all_arguments["value"] = value
    return {"all_arguments": all_arguments}
