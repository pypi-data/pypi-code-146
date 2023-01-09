from dbt.adapters.bigquery.impl import BigQueryAdapter

from alvin_integration.producers.dbt.installer import AlvinDBTInstaller


class AlvinBigQueryAdapter(BigQueryAdapter):
    def __init__(self, *args, **kwargs):

        alvin_manager = AlvinDBTInstaller()

        alvin_manager.install()

        super(AlvinBigQueryAdapter, self).__init__(*args, **kwargs)
