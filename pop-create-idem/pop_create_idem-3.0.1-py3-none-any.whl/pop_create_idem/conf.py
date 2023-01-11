CLI_CONFIG = {
    "create_plugin": {"subcommands": ["_global_"], "dyne": "pop_create"},
    "simple_service_name": {
        "options": ["--cloud", "--cloud-name"],
        "subcommands": ["_global_"],
        "dyne": "pop_create",
    },
    "acct_plugin": {
        "subcommands": ["idem-cloud", "openapi3", "swagger"],
        "dyne": "pop_create",
    },
    "specification": {
        "options": ["--spec", "--file", "--url"],
        "subcommands": ["openapi3", "swagger", "idem-cloud"],
        "dyne": "pop_create",
    },
}
CONFIG = {
    "create_plugin": {
        "default": "auto_states",
        "dyne": "pop_create",
        "help": "The `create` plugin to use for exec modules",
    },
    "acct_plugin": {
        "default": None,
        "help": "The acct plugin to use for authentication -- default is to create a new plugin",
        "dyne": "pop_create",
    },
    "simple_service_name": {
        "default": None,
        "help": "Short name of the cloud being bootstrapped",
        "dyne": "pop_create",
    },
    "specification": {
        "default": None,
        "help": "The url or file path to a spec",
        "dyne": "pop_create",
    },
}
SUBCOMMANDS = {
    # https://openapi.tools/#converters
    "idem-cloud": {"help": "Boostrap an idem cloud project", "dyne": "pop_create"},
    "openapi3": {
        "help": "Create idem_cloud modules based off of an openapi3 spec",
        "dyne": "pop_create",
    },
    "swagger": {
        "help": "Create idem_cloud modules based off of a swagger spec",
        "dyne": "pop_create",
    },
}
DYNE = {
    "pop_create": ["pop_create"],
    "cloudspec": ["cloudspec"],
    "tool": ["tool"],
    "jinja": ["jinja"],
}
