import json
import tempfile
from datetime import datetime

from defi_marketplace_py.cli_wrapper import CliWapper
from defi_marketplace_py.constants import AddressProvider, Nevermined


class Publisher():
    """
    Class to download DeFi data from marketplace
    """

    def __init__(self, network: str):
        self.cli_wrapper: CliWapper = CliWapper(network=network)
        self.network = network

    def publish_dataset(
        self,
        dataset_name: str,
        file_path: str,
        price: float
    ):
        print("Publishing your asset")

        metadata = Nevermined.METADATA
        filecoin_url = self.cli_wrapper.upload_to_filecoin(file_path=file_path)

        now = datetime.now()
        metadata['main']['name'] = dataset_name
        metadata['main']['dateCreated'] = now.strftime(
            '%Y-%m-%dT%H:%M:%SZ'
        )
        metadata['main']['price'] = str(price)
        metadata['main']['datePublished'] = now.strftime(
            '%Y-%m-%dT%H:%M:%SZ'
        )
        metadata['main']['files'][0]['url'] = filecoin_url
        metadata['main']['files'][0]['name'] = dataset_name

        metadata_file = tempfile.NamedTemporaryFile(mode="w+")
        json.dump(metadata, metadata_file)
        metadata_file.flush()

        self.cli_wrapper.publish_dataset(
            subscriptionAddress=AddressProvider.NFT_SUBSCRIPTION[self.network],
            metadata_file=metadata_file.name
        )

        print("Your asset has been published")


