import os
from typing import List

from tcsoa.fcc.fcc_client_proxy import FccClientProxy, FMSException


class FccWrapper:
    def __init__(self):
        self.client_proxy = FccClientProxy()

    def register_tickets(self, tickets: List[str]) -> List[str]:
        if tickets is None or len(tickets) == 0:
            raise FMSException('Error -3002: ArgumentError - pass a non-empty list of tickets')
        result = self.client_proxy.fcc_register_tickets(tickets)
        return result.ticket_uids

    def unregister_tickets(self, uids: List[str]):
        if uids is None or len(uids) == 0:
            raise FMSException('Error -3002: ArgumentError - pass a non-empty list of UIDs')
        self.client_proxy.fcc_unregister_tickets(uids)

    def download_files_from_plm(self, policy: str, uids: List[str]) -> List[str]:
        if uids is None or len(uids) == 0:
            raise FMSException('Error -3002: ArgumentError - pass a non-empty list of UIDs')
        result = self.client_proxy.fcc_download_files_from_plm(policy, uids, None, None)
        return result.local_files

    def download_file_to_location(self, policy: str, uid: str, target_dir: str, file_name: str):
        self.client_proxy.fcc_download_file_to_location(policy, uid, None, None, target_dir, file_name)

    def download_files_to_location(self, policy: str, uids: List[str], target_dir: str, file_names: List[str]):
        """
        Downloads multiple files from Teamcenter to the specified directory.
        IMPORTANT: the uids-list and file_names-list must have the same length

        :param policy: unknown - in SOA-SDK, the value "IMD" is used everywhere
        :param uids: the tickets, which should have been registered with FileManagementService#getFileReadTickets
        :param target_dir: the directory the files should be loaded into
        :param file_names: the file names of each of the files.
        """
        if uids is None or len(uids) == 0:
            raise FMSException('Error -3002: ArgumentError - pass a non-empty list of UIDs')
        if not target_dir or not os.path.isdir(target_dir):
            raise FMSException('Error -3002: ArgumentError - please provide a valid, existing path for the files to be downloaded')
        self.client_proxy.fcc_download_files_to_location(policy, uids, None, None, target_dir, file_names)

    def upload_files_to_plm(self, uids: List[str], file_paths: List[str]) -> List[str]:
        if uids is None or len(uids) == 0:
            raise FMSException('Error -3002: ArgumentError - pass a non-empty list of UIDs')
        result = self.client_proxy.fcc_upload_files_to_plm(uids, None, None, file_paths)
        return result.volume_ids

    def rollback_files_uploaded_to_plm(self, uids: List[str], volume_ids: List[str]):
        self.client_proxy.fcc_rollback_files_uploaded_to_plm(uids, volume_ids)
