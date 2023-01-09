from alvin_integration.installer.base import AlvinBaseInstaller
from alvin_integration.producers.dbt.config import DBTProducerConfig


class AlvinDBTInstaller(AlvinBaseInstaller):
    def __init__(self, *args, **kwargs):
        super(AlvinDBTInstaller, self).__init__(
            provider_config=DBTProducerConfig(), *args, **kwargs
        )

    def install_lineage(self):
        pass

    def install_pipelines(self):
        pass
