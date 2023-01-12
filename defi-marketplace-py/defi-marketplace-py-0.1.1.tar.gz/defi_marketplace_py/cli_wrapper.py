import json
import subprocess
from dotenv import load_dotenv

from defi_marketplace_py.constants import Commands
from defi_marketplace_py.utils import create_command, create_search_query
from defi_marketplace_py.constants import NetworkValues


class CliWapper:

    def __init__(self, network: str) -> None:
        self.network = network
        load_dotenv()
        self.__install_cli__()

    def __execute_command__(self, command_array, shell=False):
        result = subprocess.run(
            command_array,
            stdout=subprocess.PIPE,
            shell=shell
        )

        subprocess_return = result.stdout

        return subprocess_return

    def __install_cli__(self):
        try:
            result = self.__execute_command__(
                create_command(
                    Commands.CLI_HELP,
                    {},
                ))
        except:
            result = b''

        if 'Usage' not in result.decode('utf-8'):

            print('Nevermined CLI dependency not installed, installing...')

            self.__execute_command__(
                create_command(
                    Commands.INSTALL_CLI,
                    {}
                )
            )

            self.__execute_command__(
                create_command(
                    Commands.DOWNLOAD_ARTIFACTS,
                    {
                        'version': NetworkValues.ARTIFACTS_VERSION[self.network],
                        'networkId': NetworkValues.NETWORKD_ID[self.network],
                        'destination': NetworkValues.ARTIFACTS_FOLDER,
                    }
                )
            )

    def list_assets(self, protocol: str, event_type: str, chain: str, from_date: str, to_date: str) -> None:

        page = 1
        total_pages = 1
        files_to_download = []

        while (total_pages >= page):
            result = self.__execute_command__(
                create_command(
                    Commands.LIST_ASSETS,
                    {
                        'query': create_search_query(protocol, event_type, chain, from_date, to_date),
                        'network': self.network,
                        'page': page
                    }
                )
            )

            result_json = json.loads(result)
            results = json.loads(result_json['data'][0]['results'])
            total_pages = results['totalPages']
            page += 1
            content = results['results']
            files_to_download = [*files_to_download, *content]

        files = []

        for file in files_to_download:
            try:
                start_index = file['serviceEndpoint'].find('did')
                files.append({
                    'fileName': file['attributes']['additionalInformation']['file_name'],
                    'did': file['serviceEndpoint'][start_index:]
                })

            except:
                print('File name does not exit')

        return files

    def download_did(self, did: str, destination: str, account_index: int):
        result = self.__execute_command__(
            create_command(
                Commands.DOWNLOAD_DID,
                {
                    'did': did,
                    'network': self.network,
                    'destination': destination,
                    'accountIndex': account_index
                }
            )
        )

    def publish_dataset(self, subscriptionAddress: str, metadata_file: str):
        result = self.__execute_command__(
            create_command(
                command=Commands.PUBLISH_ASSET,
                args={
                    'network': self.network,
                    'nftAddress': subscriptionAddress,
                    'metadata': metadata_file
                }
            ))

        return result

    def upload_to_filecoin(self, file_path: str):
        result = self.__execute_command__(
            create_command(
                command=Commands.UPLOAD_TO_FILECOIN,
                args={
                    'file_path': file_path
                }
            )
        )

        json_return = json.loads(result)
        cid = json.loads(json_return['data'][0]['results'])['url']

        return cid
