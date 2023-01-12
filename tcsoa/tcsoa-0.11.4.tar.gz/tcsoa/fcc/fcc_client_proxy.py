import os
from dataclasses import dataclass
from typing import List, Optional


class FMSException(Exception):
    """ Exception which will have the Native Exception as inner Exception """
    pass


@dataclass
class FccGetLastErrorResponse:
    return_code: int
    error_msg: str


@dataclass
class FccRegisterTicketsResponse:
    return_code: int
    ticket_uids: List[str]
    ifails: List[Optional[int]]


@dataclass
class FccUnRegisterTicketsResponse:
    return_code: int
    ifails: List[Optional[int]]


@dataclass
class FccDownloadFilesFromPlmResponse:
    return_code: int
    local_files: List[str]
    ifails: List[Optional[int]]


@dataclass
class FccDownloadRenderingFilesResponse:
    return_code: int
    results: List[str]
    ifails: List[Optional[int]]


@dataclass
class FccDownloadFilesToLocationResponse:
    return_code: int
    ifails: List[Optional[int]]


@dataclass
class UploadFilesToPlmResponse:
    return_code: int
    volume_ids: List[str]
    ifails: List[Optional[int]]


@dataclass
class RollbackFilesUploadedToPlmResponse:
    return_code: int
    ifails: List[Optional[int]]


def FmsExceptionConv(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            raise FMSException('A C# Exception was thrown, see inner Exception') from ex
    return inner


class FccClientProxy:
    def __init__(self):
        import clr
        dll_location = self._determine_dll_location()
        clr.AddReference(dll_location)
        from Teamcenter.FMS.FCCProxy.ClientCache import NetFileCacheProxy
        self.dll = NetFileCacheProxy()

    def _determine_dll_location(self) -> str:
        dll_location = None
        if 'FMS_HOME' in os.environ:
            dll_location = os.path.join(os.environ['FMS_HOME'], 'lib', 'FCCNetClientProxy4064.dll')
        if 'TCSOA_FSC_NET_DLL' in os.environ:
            dll_location = os.environ['TCSOA_FSC_NET_DLL']
        if not dll_location or not os.path.exists(dll_location):
            raise FMSException('FSC DLL could not be found! Please set either FMS_HOME or TCSOA_FSC_NET_DLL environment var!')
        return dll_location

    @FmsExceptionConv
    def fcc_set_locale(self, locale: str):
        self.dll.SetLocale(locale)

    @FmsExceptionConv
    def fcc_register_tickets(self, tickets: List[str]) -> FccRegisterTicketsResponse:
        ret_val, uids, ifails = self.dll.RegisterTickets(tickets, [], [])
        return FccRegisterTicketsResponse(0, list(uids), list(ifails))

    @FmsExceptionConv
    def fcc_unregister_tickets(self, uids: List[str]) -> FccUnRegisterTicketsResponse:
        ifails = self.dll.UnRegisterTickets(uids, [])
        return FccUnRegisterTicketsResponse(0, list(ifails))

    @FmsExceptionConv
    def fcc_download_file_from_plm(self, policy: str, uid: str, cb: Optional[object], client_object: Optional[object]) -> str:
        local_file = self.dll.DownloadFileFromPLM(policy, uid, cb, client_object)
        return local_file

    @FmsExceptionConv
    def fcc_download_files_from_plm(self, policy: str, uids: List[str], cb: Optional[object], client_object: Optional[object]) -> FccDownloadFilesFromPlmResponse:
        ret_val, local_files, ifails = self.dll.DownloadFilesFromPLM(policy, uids, cb, client_object, [], [])
        return FccDownloadFilesFromPlmResponse(ret_val, list(local_files), list(ifails))

    @FmsExceptionConv
    def fcc_download_file_to_location(self, policy: str, uid: str, cb: Optional[object], client_object: Optional[object], target_dir: str, filename: str):
        self.dll.DownloadFileToLocation(policy, uid, cb, client_object, target_dir, filename)

    @FmsExceptionConv
    def fcc_download_files_to_location(self, policy: str, uids: List[str], cb: Optional[object], client_object: Optional[object], target_dir: str, file_paths: List[str]) -> FccDownloadFilesToLocationResponse:
        ret_val, ifails = self.dll.DownloadFilesToLocation(policy, uids, cb, client_object, target_dir, file_paths, [])
        return FccDownloadFilesToLocationResponse(ret_val, list(ifails))

    @FmsExceptionConv
    def fcc_upload_file_to_plm(self, uid: str, cb: Optional[object], client_object: Optional[object], file_path: str) -> str:
        volume_id = self.dll.UploadFileToPLM(uid, cb, client_object, file_path)
        return volume_id

    @FmsExceptionConv
    def fcc_upload_files_to_plm(self, uids: List[str], cb: Optional[object], client_object: Optional[object], file_paths: List[str]) -> UploadFilesToPlmResponse:
        ret_val, volume_ids, ifails = self.dll.UploadFilesToPLM(uids, cb, client_object, file_paths, True, [], [])
        return UploadFilesToPlmResponse(ret_val, list(volume_ids), list(ifails))

    @FmsExceptionConv
    def fcc_rollback_file_uploaded_to_plm(self, uid: str, volume_id: str):
        self.dll.RollbackFileUploadedToPLM(uid, volume_id)

    @FmsExceptionConv
    def fcc_rollback_files_uploaded_to_plm(self, uids: List[str], volume_ids: List[str]) -> RollbackFilesUploadedToPlmResponse:
        ret_val, ifails = self.dll.RollbackFilesUploadedToPLM(uids, volume_ids, [])
        return RollbackFilesUploadedToPlmResponse(0, list(ifails))
