CLI_CONFIG = {
    "input_file": {"positional": True, "subcommands": ["validate", "create"]},
    "create_plugins": {"options": ["--plugin", "-P"], "subcommands": ["create"]},
    "output": {"source": "rend", "subcommands": ["validate"]},
    "directory": {
        "options": ["-D"],
        "subcommands": ["create_plugins"],
        "source": "pop_create",
    },
}
CONFIG = {
    "input_file": {
        "default": None,
        "help": "A json file to validate for idem-cloud cloudspec format",
    },
    "create_plugins": {
        "default": [],
        "help": "cloudspec create plugins to run against the spec",
    },
}
SUBCOMMANDS = {
    "validate": {},
    "create": {},
}
DYNE = {"pop_create_idem": ["cloudspec"]}
