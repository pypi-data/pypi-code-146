""" MCLI Entrypoint mcli config """

from mcli.cli.m_get.clusters import get_clusters
from mcli.cli.m_get.envvars import get_environment_variables
from mcli.cli.m_get.secrets import get_secrets
from mcli.config import FeatureFlag, MCLIConfig


def m_get_config(**kwargs) -> int:
    """Gets the current mcli config details and prints it out

    Args:
        **kwargs:
    """
    del kwargs

    conf = MCLIConfig.load_config()

    spacer = '-' * 20

    def print_padded(text: str):
        print(f'{spacer} {text: ^20} {spacer}')

    print_padded('MCLI Config')
    print(conf)
    print_padded('END')

    if not conf.feature_enabled(FeatureFlag.USE_MCLOUD):
        print_padded('MCLI Clusters')
        get_clusters()
        print_padded('END')

        print_padded('MCLI EnvVars')
        get_environment_variables()
        print_padded('END')

    print_padded('MCLI Secrets')
    get_secrets()
    print_padded('END')

    return 0
