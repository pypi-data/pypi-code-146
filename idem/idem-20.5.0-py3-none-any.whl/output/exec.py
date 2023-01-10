from idem.exec.init import ExecReturn

try:
    import colorama

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


def display(hub, data):
    """
    Display the data from an idem run
    """
    if not isinstance(data, ExecReturn):
        return hub.output.nested.display(data)

    if not data.result:
        return colorama.Fore.RED + str(data.comment)
    else:
        return hub.output.nested.display(data.ret)
