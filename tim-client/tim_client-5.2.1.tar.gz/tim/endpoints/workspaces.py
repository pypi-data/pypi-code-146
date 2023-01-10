from typing import List, Optional
from tim.core.credentials import Credentials
from tim.core.api import execute_request
from tim.core.types import (
  ExecuteResponse,
  WorkspaceListPayload, 
  Workspace,
  WorkspacePost,
  WorkspacePut
)

class Workspaces:
  
  def __init__(
    self,
    credentials: Credentials
    ):
    self.credentials = credentials

  def list_workspace(
    self,
    offset:  Optional[int] = None,
    limit:  Optional[int] = None,
    user_group_id: Optional[str] = None,
    sort: Optional[str] = None
    ) -> List[Workspace]:
    payload = WorkspaceListPayload()
    if offset: payload['offset'] = offset
    if limit: payload['limit'] = limit
    if user_group_id: payload['userGroupId'] = user_group_id
    if sort: payload['sort'] = sort
    return execute_request(
      credentials=self.credentials,
      method='get',
      path=f'/workspaces',
      params=payload
      )

  def create_workspace(
    self,
    configuration: WorkspacePost
    ) -> Workspace:
    return execute_request(
      credentials=self.credentials,
      method='post',
      path='/workspaces',
      body=configuration
      )
      
  def details_workspace(
    self,
    id: str
    ) -> Workspace:
    return execute_request(
      credentials=self.credentials,
      method='get',
      path=f'/workspaces/{id}'
      )

  def edit_workspace(
    self,
    id: str,
    configuration: WorkspacePut
    ) -> Workspace:
    return execute_request(
      credentials=self.credentials,
      method='patch',
      path=f'/workspaces/{id}',
      body=configuration
      )

  def delete_workspace(
    self,
    id: str,
    ) -> ExecuteResponse:
    return execute_request(
      credentials=self.credentials,
      method='delete',
      path=f'/workspaces/{id}',
      )