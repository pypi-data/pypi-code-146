import pathlib


def __virtual__(hub):
    return False, "Not implemented"


def context(hub, ctx, directory: pathlib.Path):
    ...
