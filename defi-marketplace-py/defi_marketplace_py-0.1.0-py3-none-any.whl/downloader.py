from datetime import datetime
import queue
import threading
import os

from defi_marketplace_py.cli_wrapper import CliWapper
from defi_marketplace_py.constants import Values


class Downloader():
    """
    Class to download DeFi data from marketplace
    """

    def __init__(self, protocol: str, event_type: str, chain: str, version: int, network: str):
        self.protocol: str = protocol
        self.chain: str = chain
        self.version: int = version
        self.cli_wrapper: CliWapper = CliWapper(network=network)
        self.network: str = network
        self.event_type: str = event_type

    def download_datasets(self, from_date: str, to_date: str, destination: str, account_index: int = 1):

        datasets = self.cli_wrapper.list_assets(
            protocol=self.protocol,
            chain=self.chain,
            event_type=self.event_type,
            from_date=from_date,
            to_date=to_date
        )

        assets_to_download = []

        for dataset in datasets:
            file_name: str = dataset['fileName']
            file_name_split = file_name.split('-')
            date_and_chain = file_name_split[3].split('_')
            date = datetime.strptime(date_and_chain[1], '%Y%m%d').date()
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()

            if (
                self.protocol == file_name_split[0] and
                self.version == int(file_name_split[1][1]) and
                self.chain == date_and_chain[0] and
                from_date_obj <= date and
                to_date_obj >= date
            ):
                assets_to_download.append({
                    'did': dataset['did'],
                    'file_name':  dataset['fileName']
                })

        self.parallel_download(
            assets=assets_to_download,
            destination=destination,
            account_index=account_index
        )

    def parallel_download(self, assets: list, destination: str, account_index: int):
        q = queue.Queue()

        max_workers = os.getenv('MAX_WORKERS', default=Values.MAX_WORKERS)

        for _ in range(int(max_workers)):
            worker = threading.Thread(
                target=self.download_did,
                args=(destination, account_index, q),
                daemon=True)
            worker.start()

        for asset in assets:
            q.put(asset)

        q.join()

    def download_did(self, destination: str, account_index: str, q: queue):
        while True:
            try:
                asset = q.get()

                print(f'Downloading file', asset['file_name'])

                self.cli_wrapper.download_did(
                    did=asset['did'],
                    destination=destination,
                    account_index=account_index
                )

            finally:
                q.task_done()
