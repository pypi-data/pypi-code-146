from typing import List, Optional
from tim.core.api import execute_request
from tim.core.credentials import Credentials
from tim.core.types import (
  UseCase,
  UseCaseListPayload,
  UseCasePost,
  UseCasePostResponse,
  UseCasePut,
  ExecuteResponse
)

class UseCases:
  
  def __init__(
    self,
    credentials: Credentials
    ):
    self.credentials = credentials

  def list_use_case(
    self,
    offset:  Optional[int] = None,
    limit:  Optional[int] = None,
    user_group_id: Optional[str] = None,
    workspace_id: Optional[str] = None,
    dataset_id: Optional[str] = None,
    sort: Optional[str] = None,
    is_panel_data: Optional[str] = None,
    ) -> List[UseCase]:
    payload = UseCaseListPayload()
    if offset: payload['offset'] = offset
    if limit: payload['limit'] = limit
    if user_group_id: payload['userGroupId'] = user_group_id
    if workspace_id: payload['workspaceId'] = workspace_id
    if dataset_id: payload['datasetId'] = dataset_id
    if sort: payload['sort'] = sort
    if is_panel_data: payload['isPanelData'] = is_panel_data
    return execute_request(
      credentials=self.credentials,
      method='get',
      path=f'/use-cases',
      params=payload
      )

  def create_use_case(
    self,
    configuration: UseCasePost
    ) -> UseCasePostResponse:
    return execute_request(
      credentials=self.credentials,
      method='post',
      path='/use-cases',
      body=configuration
      )

  def details_use_case(
    self,
    id: str
    ) -> UseCase:
    return execute_request(
      credentials=self.credentials,
      method='get',
      path=f'/use-cases/{id}'
      )

  def edit_use_case(
    self,
    id: str,
    configuration: UseCasePut
    ) -> UseCase:
    return execute_request(
      credentials=self.credentials,
      method='patch',
      path=f'/use-cases/{id}',
      body=configuration
      )

  def delete_use_case(
    self,
    id: str,
    ) -> ExecuteResponse:
    return execute_request(
      credentials=self.credentials,
      method='delete',
      path=f'/use-cases/{id}',
      )