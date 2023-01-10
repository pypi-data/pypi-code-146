from pandas import DataFrame
from copy import copy
from typing import List, Union, Optional
from tim.core.api import execute_request
from tim.core.credentials import Credentials
from tim.core.helper import is_valid_csv_configuration
from tim.core.types import (
  CSVSeparator,
  ExecuteResponse,
  UploadDatasetConfiguration,
  UpdateDatasetConfiguration,
  DatasetCreated,
  DatasetVersion,
  DatasetDetails,
  DatasetListPayload,
  DatasetVersionListPayload,
  DatasetVersionDetails,
  DatasetStatusResponse,
  DatasetLog,
  DatasetVersionLog,
  DatasetUpdate
  )

class Datasets:
  
  def __init__(
    self,
    credentials: Credentials
    ):
    self.credentials = credentials

  def upload_dataset(
      self,
      dataset: DataFrame,
      configuration: UploadDatasetConfiguration = None,
      ) -> DatasetCreated:
      if not is_valid_csv_configuration(configuration):
        raise ValueError("Invalid configuration input.")
      if configuration is None: 
        configuration = UploadDatasetConfiguration()
      conf_with_csv_separator: UploadDatasetConfiguration = copy(configuration)
      conf_with_csv_separator["csvSeparator"] = CSVSeparator.SEMICOLON.value  # pyright: reportTypedDictNotRequiredAccess=false
      return execute_request(
        credentials=self.credentials,
        method="post",
        path="/datasets/csv",
        body=conf_with_csv_separator,
        file=dataset.to_csv(sep=conf_with_csv_separator["csvSeparator"], index=False),
        )

  def update_dataset(
      self,
      id: str,
      dataset: DataFrame,
      configuration: UpdateDatasetConfiguration=None,
      ) -> DatasetVersion:
    if not is_valid_csv_configuration(configuration):
      raise ValueError("Invalid configuration input.")
    if configuration is None: 
      configuration = UploadDatasetConfiguration()
    conf_with_csv_separator: UpdateDatasetConfiguration = copy(configuration)
    conf_with_csv_separator["csvSeparator"] = CSVSeparator.SEMICOLON.value  # pyright: reportTypedDictNotRequiredAccess=false
    return execute_request(
        credentials=self.credentials,
        method="patch",
        path=f"/datasets/{id}/csv",
        body=conf_with_csv_separator,
        file=dataset.to_csv(sep=conf_with_csv_separator["csvSeparator"], index=False),
        )

  def list_dataset(
    self,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    workspace_id: Optional[str] = None,
    sort: Optional[str] = None
    ) -> List[DatasetDetails]:
    payload = DatasetListPayload(offset=offset, limit=limit)
    if offset: payload['offset'] = offset
    if limit: payload['limit'] = limit
    if workspace_id: payload['workspaceId'] = workspace_id
    if sort: payload['sort'] = sort
    return execute_request(
      credentials=self.credentials,
      method='get',
      path=f'/datasets',
      params=payload
      )

  def delete_dataset_list(
    self,
    from_datetime: Optional[str] = None,
    to_datetime: Optional[str] = None,
    workspaceId: Optional[str] = None
    ) -> ExecuteResponse:
    payload = {
      "from": from_datetime,
      "to": to_datetime,
      "workspaceId": workspaceId
    }
    return execute_request(
      credentials=self.credentials,
      method='delete',
      path=f'/datasets',
      params=payload
      )

  def details_dataset(
    self,
    id: str
    ) -> DatasetDetails:
    return execute_request(
      credentials=self.credentials,
      method="get",
      path=f"/datasets/{id}"
      )

  def edit_dataset_details(
    self,
    id: str,
    configuration: DatasetUpdate
    ) -> DatasetDetails:
    return execute_request(
      credentials=self.credentials,
      method="patch",
      path=f"/datasets/{id}",
      body=configuration
      )

  def delete_dataset(
    self,
    id: str
    ) -> ExecuteResponse:
    return execute_request(
      credentials=self.credentials,
      method="delete",
      path=f"/datasets/{id}"
      )

  def dataset_logs(
    self,
    id: str
    ) -> List[DatasetLog]:
    return execute_request(
        credentials=self.credentials,
        method="get",
        path=f"/datasets/{id}/log",
    )

  def logs_dataset_version(
    self,
    id: str,
    version: str,
    offset: Optional[int] = None,
    limit: Optional[int] = None
    ) -> DatasetVersionLog:
    payload = {
      "offset":offset,
      "limit":limit
    }
    return execute_request(
      credentials=self.credentials,
      method="get",
      path=f"/datasets/{id}/versions/{version}/log",
      params=payload
    )

  def list_dataset_versions(
    self,
    id: str,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    ) -> List[DatasetVersionDetails]:
    payload = DatasetVersionListPayload()
    if offset: payload['offset'] = offset
    if limit: payload['limit'] = limit
    return execute_request(
        credentials=self.credentials,
        method='get',
        path=f'/datasets/{id}/versions',
        params=payload
    )

  def details_dataset_version(
    self,
    id: str,
    version: str
    ) -> DatasetVersionDetails:
    return execute_request(
      credentials=self.credentials,
      method="get",
      path=f"/datasets/{id}/versions/{version}"
      ) 

  def delete_dataset_version(
    self,
    id: str,
    version: str
    ) -> ExecuteResponse:
    return execute_request(
      credentials=self.credentials,
      method="delete",
      path=f"/datasets/{id}/versions/{version}"
      ) 

  def status_dataset_version(
    self,
    id: str,
    version_id: str
    ) -> DatasetStatusResponse:
    return execute_request(
        credentials=self.credentials,
        method="get",
        path=f"/datasets/{id}/versions/{version_id}/status",
        )