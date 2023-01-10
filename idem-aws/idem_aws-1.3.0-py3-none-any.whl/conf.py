CLI_CONFIG = {
    # pop-create options
    "services": {
        "subcommands": ["aws"],
        "dyne": "pop_create",
    },
}
CONFIG = {
    # pop-create options
    "services": {
        "default": [],
        "nargs": "*",
        "help": "The cloud services to target, defaults to all",
        "dyne": "pop_create",
    },
}
SUBCOMMANDS = {
    "aws": {
        "help": "Create idem_aws state modules by parsing boto3",
        "dyne": "pop_create",
    },
}
DYNE = {
    "acct": ["acct"],
    "exec": ["exec"],
    "pop_create": ["autogen"],
    "states": ["states"],
    "tool": ["tool"],
    "esm": ["esm"],
    "reconcile": ["reconcile"],
}
