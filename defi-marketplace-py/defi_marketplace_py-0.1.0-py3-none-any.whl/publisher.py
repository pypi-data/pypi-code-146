from defi_marketplace_py.cli_wrapper import CliWapper
from defi_marketplace_py.constants import AddressProvider


class Publisher():
    """
    Class to download DeFi data from marketplace
    """

    def __init__(self, network: str):
        self.cli_wrapper: CliWapper = CliWapper(network=network)
        self.network = network

    def publish_dataset(self, dataset_name: str, author: str, file_path: str):

        filecoin_url = self.cli_wrapper.upload_to_filecoin(file_path=file_path)

        self.cli_wrapper.publish_dataset(
            dataset_name=dataset_name,
            author=author,
            subscriptionAddress=AddressProvider.NFT_SUBSCRIPTION[self.network],
            url=filecoin_url
        )
        
