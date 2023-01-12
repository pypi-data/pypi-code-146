# https://pop.readthedocs.io/en/latest/tutorial/quickstart.html#adding-configuration-data


CONFIG = {}

SUBCOMMANDS = {
    "k8s": {
        "help": "Create idem_k8s state modules by parsing openapi spec",
        "dyne": "pop_create",
    },
}

CLI_CONFIG = {
    "resource": {
        "subcommands": ["k8s"],
        "dyne": "pop_create",
    },
}

DYNE = {
    "acct": ["acct"],
    "exec": ["exec"],
    "states": ["states"],
    "tool": ["tool"],
    "pop_create": ["autogen"],
}
