from io import StringIO
import pandas as pd
from typing import List, Optional
from tim.core.api import execute_request
from tim.core.credentials import Credentials
from tim.core.types import(
  StatusResponse,
  JobLogs,
  JobResponse,
  ExecuteResponse,
  DetectionBuildKPIModel,
  DetectionBuildSystemModel,
  DetectionUploadModel,
  DetectionRebuildKPIModel,
  DetectionDetect,
  DetectionModelResult,
  DetectionJobDetails,
  Id,
  WhatIf,
  CopyExperiment,
  DetectionErrorMeasures
)
class Detection:

  def __init__(
    self,
    credentials: Credentials
    ):
    self.credentials = credentials

  def build_kpi_model(
    self,
    configuration: DetectionBuildKPIModel
    ) -> JobResponse:
    return execute_request(
      credentials=self.credentials,
      method='post',
      path='/detection-jobs/build-model/kpi-driven',
      body=configuration
      )

  def build_system_model(
    self,
    configuration: DetectionBuildSystemModel
    ) -> JobResponse:
    return execute_request(
      credentials=self.credentials,
      method='post',
      path='/detection-jobs/build-model/system-driven',
      body=configuration
      )

  def upload_model(
    self,
    configuration: DetectionUploadModel
    ) -> JobResponse:
    return execute_request(
      credentials=self.credentials,
      method='post',
      path='/detection-jobs/upload-model/',
      body=configuration
      )  

  def rebuild_kpi_model(
    self,
    parent_job_id: str,
    configuration: Optional[DetectionRebuildKPIModel]
    ) -> JobResponse:
    return execute_request(
      credentials=self.credentials,
      method='post',
      path=f'/detection-jobs/{parent_job_id}/rebuild-model/kpi-driven',
      body=configuration
      )

  def detect(
    self,
    parent_job_id: str,
    configuration: Optional[DetectionDetect]
    ) -> JobResponse:
    return execute_request(
      credentials=self.credentials,
      method='post',
      path=f'/detection-jobs/{parent_job_id}/detect',
      body=configuration
      )

  def rca(
    self,
    parent_job_id: str,
    ) -> Id:
    return execute_request(
        credentials=self.credentials,
        method='post',
        path=f'/detection-jobs/{parent_job_id}/rca',
        )

  def what_if(
    self,
    parent_job_id: str,
    configuration: WhatIf
    ) -> Id:
    return execute_request(
        credentials=self.credentials,
        method='post',
        path=f'/detection-jobs/{parent_job_id}/what-if',
        body=configuration
        )

  def job_list(
    self,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    experiment_id: Optional[str] = None,
    use_case_id: Optional[str] = None,
    type: Optional[str] = None,
    status: Optional[str] = None,
    parent_id: Optional[str] = None,
    from_datetime: Optional[str] = None,
    to_datetime: Optional[str] = None
    ) -> List[DetectionJobDetails]:
    payload = {
      "experimentId": experiment_id,
      "useCaseId": use_case_id,
      "sort": sort,
      "type": type,
      "status": status,
      "parentId": parent_id,
      "from": from_datetime,
      "to": to_datetime,
      "limit": limit,
      "offset": offset
      }
    return execute_request(
      credentials=self.credentials,
      method='get',
      path=f'/detection-jobs',
      params=payload
      )

  def delete_job_list(
    self,
    experiment_id: Optional[str] = None,
    use_case_id: Optional[str] = None,
    type: Optional[str] = None,
    approach: Optional[str] = None,
    status: Optional[str] = None,
    parent_id: Optional[str] = None,
    from_datetime: Optional[str] = None,
    to_datetime: Optional[str] = None,
    ) -> ExecuteResponse:
    payload = {
      "experimentId": experiment_id,
      "useCaseId": use_case_id,
      "type": type,
      "approach": approach,
      "status": status,
      "parentId": parent_id,
      "from": from_datetime,
      "to": to_datetime
      }
    return execute_request(
      credentials=self.credentials,
      method="delete",
      path=f"/detection-jobs",
      params=payload
      )

  def job_details(
    self,
    id: str
    ) -> DetectionJobDetails:
    return execute_request(
      credentials=self.credentials,
      method='get',
      path=f'/detection-jobs/{id}'
      )

  def delete_job(
    self,
    id: str
    ) -> ExecuteResponse:
    return execute_request(
      credentials=self.credentials,
      method="delete",
      path=f"/detection-jobs/{id}"
      )

  def copy_job(
    self,
    id: str,
    configuration: Optional[CopyExperiment] = None
    ) -> Id:
    return execute_request(
        credentials=self.credentials,
        method='post',
        path=f'/detection-jobs/{id}/copy',
        body=configuration
        )  

  def execute(
    self,
    id: str
    ) -> ExecuteResponse:
    return execute_request(
      credentials=self.credentials,
      method='post',
      path=f'/detection-jobs/{id}/execute'
      )

  def job_logs(
    self,
    id: str
    ) -> List[JobLogs]:
    return execute_request(
      credentials=self.credentials,
      method='get',
      path=f'/detection-jobs/{id}/log'
      )

  def status(
    self,
    id: str
    ) -> StatusResponse:
    return execute_request(
      credentials=self.credentials,
      method='get',
      path=f'/detection-jobs/{id}/status'
      )

  def status_collect(
    self,
    id: str,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    ) -> List[StatusResponse]:
    payload = {
        "offset": offset,
        "limit": limit,
        "sort": sort
        }
    return execute_request(
        credentials=self.credentials,
        method='get',
        path=f'/detection-jobs/{id}/status/collect',
        params=payload
        )

  def results_table(
    self,
    id: str
    ) -> pd.DataFrame:
    response = execute_request(
      credentials=self.credentials,
      method='get',
      path=f'/detection-jobs/{id}/results/table'
      )
    data_string = StringIO(response)
    return pd.read_csv(data_string)  # pyright: reportGeneralTypeIssues=false, reportUnknownMemberType=false

  def results_model(
    self,
    id: str
    ) -> DetectionModelResult:
    return execute_request(
      credentials=self.credentials,
      method='get',
      path=f'/detection-jobs/{id}/results/model'
      )

  def results_accuracies(
    self,
    id: str
    ) -> DetectionErrorMeasures:
    return execute_request(
        credentials=self.credentials,
        method='get',
        path=f'/detection-jobs/{id}/results/accuracies'
        )

  def results_rca(
    self,
    id: str,
    index_of_model: Optional[int] = None,
    timestamp: Optional[str] = None,
    radius: Optional[int] = None,
    ) -> pd.DataFrame:
    payload = {
      "indexOfModel": index_of_model,
      "timestamp": timestamp,
      "radius": radius
      }
    response = execute_request(
        credentials=self.credentials,
        method='get',
        path=f'/detection-jobs/{id}/results/rca',
        params=payload
        )
    data_string = StringIO(response)
    return pd.read_csv(data_string)

  def results_production_table(
    self,
    sequence_job_id : str,
    dataset_version_id: Optional[str] = None,
    from_datetime: Optional[str] = None,
    to_datetime: Optional[str] = None,
    allow_overlapping: Optional[bool] = None,
    colocated_jobs: Optional[bool] = None,
    ) -> pd.DataFrame:
    payload = {
      "sequenceJobId": sequence_job_id,
      "datasetVersionId": dataset_version_id,
      "from": from_datetime,
      "to": to_datetime,
      "allowOverlapping": allow_overlapping,
      "colocatedJobs": colocated_jobs
      }
    response = execute_request(
        credentials=self.credentials,
        method='get',
        path='/detection-jobs/results/production-table',
        params=payload
        )
    data_string = StringIO(response)
    return pd.read_csv(data_string) 

  def results_production_accuracies(
      self,
      sequence_job_id : str,
      dataset_version_id: Optional[str] = None,
      from_datetime: Optional[str] = None,
      to_datetime: Optional[str] = None,
      allow_overlapping: Optional[bool] = None,
      colocated_jobs: Optional[bool] = None,
      individual_accuracies: Optional[bool] = None,
      ) -> DetectionErrorMeasures:
      payload = {
        "sequenceJobId": sequence_job_id,
        "datasetVersionId": dataset_version_id,
        "from": from_datetime,
        "to": to_datetime,
        "allowOverlapping": allow_overlapping,
        "colocatedJobs": colocated_jobs,
        "individualAccuracies": individual_accuracies
        }
      return execute_request(
          credentials=self.credentials,
          method='get',
          path='/detection-jobs/results/production-accuracies',
          params=payload
          )