from tinybird_cdk import connector
from tinybird_cdk.cloud import gcs

class Connector(connector.CloudConnector):
    def __init__(self):
        super().__init__()
        self.client = gcs.Client()
