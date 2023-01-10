from typing import List, Optional
from tim.core.api import execute_request
from tim.core.credentials import Credentials
from tim.core.types import (
  Experiment,
  ExperimentListPayload,
  ExperimentPost,
  ExperimentPut,
  ExecuteResponse
)

class Experiments:
  
  def __init__(
    self,
    credentials: Credentials
    ):
    self.credentials = credentials

  def list_experiment(
    self,
    offset:  Optional[int] = None,
    limit:  Optional[int] = None,
    workspace_id: Optional[str] = None,
    use_case_id: Optional[str] = None,
    dataset_id: Optional[str] = None,
    sort: Optional[str] = None,
    type: Optional[str] = None,
    ) -> List[Experiment]:
    payload = ExperimentListPayload()
    if offset: payload['offset'] = offset
    if limit: payload['limit'] = limit
    if workspace_id: payload['workspaceId'] = workspace_id
    if use_case_id: payload['useCaseId'] = use_case_id  
    if dataset_id: payload['datasetId'] = dataset_id
    if sort: payload['sort'] = sort
    if type: payload['type'] = type
    return execute_request(
      credentials=self.credentials,
      method='get',
      path=f'/experiments',
      params=payload
      )

  def create_experiment(
    self,
    configuration: ExperimentPost
    ) -> Experiment:
    return execute_request(
      credentials=self.credentials,
      method='post',
      path='/experiments',
      body=configuration
      )

  def details_experiment(
    self,
    id: str
    ) -> Experiment:
    return execute_request(
      credentials=self.credentials,
      method='get',
      path=f'/experiments/{id}'
      )

  def edit_experiment(
    self,
    id: str,
    configuration: ExperimentPut
    ) -> Experiment:
    return execute_request(
      credentials=self.credentials,
      method='patch',
      path=f'/experiments/{id}',
      body=configuration
      )

  def delete_experiment(
    self,
    id: str,
    ) -> ExecuteResponse:
    return execute_request(
      credentials=self.credentials,
      method='delete',
      path=f'/experiments/{id}',
      )