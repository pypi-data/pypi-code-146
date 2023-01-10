from typing import Optional, List
from tim.core.credentials import Credentials
from tim.core.api import execute_request
from tim.core.types import (
  DatasetCall,
  JobType,
  JobState,
  JobCall
)

class Telemetry:

    def __init__(
      self,
      credentials: Credentials
      ):
      self.credentials = credentials

    def dataset_calls(
      self,
      offset: Optional[int] = None,
      limit: Optional[int] = None,
      dataset_id: Optional[str] = None,
      experiment_id: Optional[str] = None,
      user_id: Optional[str] = None,
      dataset_state: Optional[str] = None,
      dataset_version_state: Optional[str] = None,
      endpoint_id: Optional[List[str]] = None,
      from_datetime: Optional[str] = None,
      to_datetime: Optional[str] = None,
      sort: Optional[str] = None,
      ) -> List[DatasetCall]:
      payload = {
        "offset": offset,
        "limit": limit,
        "datasetId": dataset_id,
        "experimentId": experiment_id,
        "userId": user_id,
        "datasetState": dataset_state,
        "datasetVersionState": dataset_version_state,
        "endpointId": endpoint_id,
        "from": from_datetime,
        "to": to_datetime,
        "sort": sort,
      }
      return execute_request(
        credentials=self.credentials,
        method='get',
        path=f'/ops/dataset-calls',
        params=payload
        )

    def job_calls(
      self,
      offset: Optional[int] = None,
      limit: Optional[int] = None,
      dataset_id: Optional[str] = None,
      dataset_version_id: Optional[str] = None,
      experiment_id: Optional[str] = None,
      job_id: Optional[str] = None,
      parent_job_id: Optional[str] = None,
      user_id: Optional[str] = None,
      type: Optional[JobType] = None,
      job_state: Optional[JobState] = None,
      endpoint_id: Optional[List[str]] = None,
      from_datetime: Optional[str] = None,
      to_datetime: Optional[str] = None,
      from_calculation_time: Optional[str] = None,
      to_calculation_time: Optional[str] = None,
      sort: Optional[str] = None,
      ) -> List[JobCall]:
      payload = {
        "offset": offset,
        "limit": limit,
        "datasetId": dataset_id,
        "datasetVersionId": dataset_version_id,
        "experimentId": experiment_id,
        "jobId": job_id,
        "parentJobId": parent_job_id,
        "userId": user_id,
        "type": type,
        "jobState": job_state,
        "endpointId": endpoint_id,
        "from": from_datetime,
        "to": to_datetime,
        "fromCalculationTime": from_calculation_time,
        "toCalculationTime": to_calculation_time,
        "sort": sort
        }
      return execute_request(
        credentials=self.credentials,
        method='get',
        path=f'/ops/job-calls',
        params=payload
        )