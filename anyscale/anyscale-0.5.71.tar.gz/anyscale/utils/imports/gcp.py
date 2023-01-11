import click


# TODO: type the return value
def try_import_gcp_secretmanager():
    try:
        from google.cloud import secretmanager

        return secretmanager
    except ImportError:
        raise click.ClickException(
            "pip package `google-cloud-secret-manager` is not installed locally on this machine but required "
            "for the command. Please install with `pip install 'anyscale[gcp]'`."
        )


def try_import_gcp_discovery():
    try:
        from googleapiclient import discovery

        return discovery
    except ImportError:
        raise click.ClickException(
            "pip package `google-api-python-client` is not installed locally on this machine but required "
            "for the command. Please install with `pip install 'anyscale[gcp]'`."
        )
