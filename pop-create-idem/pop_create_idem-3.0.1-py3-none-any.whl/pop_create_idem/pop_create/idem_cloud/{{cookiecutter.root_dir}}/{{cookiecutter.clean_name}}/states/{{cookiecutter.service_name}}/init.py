def __init__(hub):
    # This enables acct profiles that begin with "{{cookiecutter.service_name}}" for states
    hub.states.{{cookiecutter.service_name}}.ACCT = ["{{cookiecutter.acct_plugin}}"]
