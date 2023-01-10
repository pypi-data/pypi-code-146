import logging
import os
from dataclasses import dataclass
from typing import List, Dict

from tcsoa.gen.Core._2006_03.FileManagement import GetDatasetWriteTicketsInputData, CommitDatasetFileInfo, \
    DatasetFileInfo, DatasetFileTicketInfo, FileTicketsResponse
from tcsoa.gen.Core.services import FileManagementService
from tcsoa.gen.Server import ServiceData, ErrorStack
from tcsoa.gen.BusinessObjects import BusinessObject

from tcsoa.fcc.fcc_wrapper import FccWrapper


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


@dataclass
class PutFileRecord:
    file_info: DatasetFileInfo
    physical_path: str
    ticket_info: DatasetFileTicketInfo = None
    volume_id: str = None


@dataclass
class GetFileResponse:
    named_ref: BusinessObject
    path: str
    partial_errors: List[ErrorStack]


@dataclass
class GetFilesEntry:
    named_ref: BusinessObject
    file_name: str


class FileManagementUtility:
    fcc: FccWrapper = None

    @classmethod
    def ensure_init(cls):
        if cls.fcc is None:
            cls.fcc = FccWrapper()

    @classmethod
    def put_files(cls, inputs: List[GetDatasetWriteTicketsInputData]) -> List[ErrorStack]:
        cls.ensure_init()
        all_partial_errors = list()
        put_file_recors = dict()
        for i in inputs:
            for dataset_info in i.datasetFileInfos:
                if dataset_info.clientId not in put_file_recors:
                    put_file_recors[dataset_info.clientId] = PutFileRecord(dataset_info, os.path.abspath(dataset_info.fileName))
                dataset_info.fileName = os.path.basename(dataset_info.fileName)
        for chunk in chunks(inputs, 100):
            get_tickets_response = FileManagementService.getDatasetWriteTickets(chunk)
            all_partial_errors.extend(get_tickets_response.serviceData.partialErrors)
            cls._process_upload_commits(get_tickets_response.commitInfo, put_file_recors)
        return all_partial_errors

    @classmethod
    def get_files_to_location(cls, get_file_entries: List[GetFilesEntry], destination_dir: str) -> List[ErrorStack]:
        cls.ensure_init()
        if not os.path.isdir(destination_dir):
            raise ValueError('FMSException - ArgumentError: please provide a valid, existing destination directory.')

        named_refs = [e.named_ref for e in get_file_entries]
        file_read_tickets: FileTicketsResponse = FileManagementService.getFileReadTickets(named_refs)
        partial_errors = file_read_tickets.serviceData.partialErrors
        if partial_errors is None:
            partial_errors = list()

        ticket2filename_map = dict()
        nr2filename_map = {gfe.named_ref.uid: gfe.file_name for gfe in get_file_entries}
        for nr, ticket in file_read_tickets.tickets.items():
            ticket2filename_map[ticket] = nr2filename_map[nr.uid]
        cls.get_files_by_tickets(ticket2filename_map, destination_dir)
        return partial_errors

    @classmethod
    def get_file_to_location(cls, named_ref: BusinessObject, destination_path: str) -> GetFileResponse:
        cls.ensure_init()

        file_read_tickets: FileTicketsResponse = FileManagementService.getFileReadTickets([named_ref])
        partial_errors = file_read_tickets.serviceData.partialErrors
        result = GetFileResponse(named_ref, destination_path, partial_errors)
        if not file_read_tickets.tickets:
            logging.debug('No Tickets returned for the named reference')
            return result
        ticket = next(iter(file_read_tickets.tickets.values())) if file_read_tickets.tickets else None
        cls.get_file_by_ticket(ticket, destination_path)

        return result

    @classmethod
    def get_files_by_tickets(cls, ticket2filename_map: Dict[str, str], destination_dir: str):
        if not ticket2filename_map:
            return
        soa_tickets = list(ticket2filename_map.keys())
        fcc_tickets = cls.fcc.register_tickets(soa_tickets)
        try:
            file_names = [ticket2filename_map[t] for t in soa_tickets]
            cls.fcc.download_files_to_location("IMD", fcc_tickets, destination_dir, file_names)
        finally:
            cls.fcc.unregister_tickets(fcc_tickets)

    @classmethod
    def get_file_by_ticket(cls, ticket: str, destination_path: str):
        if not ticket:
            return

        cls.ensure_init()
        full_path = os.path.abspath(destination_path)
        parent_dir = os.path.dirname(full_path)
        file_name = os.path.basename(full_path)

        fcc_tickets = cls.fcc.register_tickets([ticket])
        if not fcc_tickets:
            logging.warning('Tried to register ticket to FMS, but got no valid ticket')
            return
        try:
            cls.fcc.download_file_to_location("IMD", fcc_tickets[0], parent_dir, file_name)
        finally:
            cls.fcc.unregister_tickets(fcc_tickets)

    @classmethod
    def _process_upload_commits(cls, commit_infos: List[CommitDatasetFileInfo], put_file_records: Dict[str, PutFileRecord]):
        for comm_info in commit_infos:
            tickets = list()
            file_paths = list()
            for ticket_info in comm_info.datasetFileTicketInfos:
                tickets.append(ticket_info.ticket)
                put_file_info = put_file_records[ticket_info.datasetFileInfo.clientId]
                file_paths.append(put_file_info.physical_path)
            ticket_uids = cls.fcc.register_tickets(tickets)
            try:
                cls.fcc.upload_files_to_plm(ticket_uids, file_paths)
            finally:
                cls.fcc.unregister_tickets(ticket_uids)
        commit_sd = FileManagementService.commitDatasetFiles(commitInput=commit_infos)
        cls._rollback_failed_uploads(commit_sd, put_file_records)

    @classmethod
    def _rollback_failed_uploads(cls, commit_service_data: ServiceData, put_file_records: Dict[str, PutFileRecord]):
        if not commit_service_data.partialErrors:
            return

        failed_client_ids = set(partial_error.clientId for partial_error in commit_service_data.partialErrors)
        tickets = list()
        volume_ids = list()
        for failed_client_id in failed_client_ids:
            put_file_record = put_file_records[failed_client_id]
            tickets.append(put_file_record.ticket_info.ticket)
            volume_ids.append(put_file_record.volume_id)
        ticket_uids = cls.fcc.register_tickets(tickets)
        try:
            cls.fcc.rollback_files_uploaded_to_plm(ticket_uids, volume_ids)
        finally:
            cls.fcc.unregister_tickets(ticket_uids)
