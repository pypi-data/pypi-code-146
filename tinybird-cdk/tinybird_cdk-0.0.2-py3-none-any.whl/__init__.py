import importlib
import tinybird_cdk.errors

def connector_for(name):
    try:
        mod_name = f'tinybird_cdk.connectors.{name}'
        mod = importlib.import_module(mod_name)
    except ModuleNotFoundError as e:
        if e.name == mod_name:
            raise tinybird_cdk.errors.UnknownConnector(name)
        raise e
    return mod.Connector()
