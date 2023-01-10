from typing import List, Optional
from tim.core.credentials import Credentials
from tim.core.api import execute_request
from tim.core.types import (
  ExecuteResponse,
  UserGroup,
  UserGroupListPayload,
  CreateUserGroup
)

class UserGroups:
  
  def __init__(
    self,
    credentials: Credentials
    ):
    self.credentials = credentials

  def list_user_group(
    self,
    offset:  Optional[int] = None,
    limit:  Optional[int] = None,
    sort: Optional[str] = None
    ) -> List[UserGroup]:
    payload = UserGroupListPayload()
    if offset: payload['offset'] = offset
    if limit: payload['limit'] = limit
    if sort: payload['sort'] = sort
    return execute_request(
      credentials=self.credentials,
      method='get',
      path=f'/user-groups',
      params=payload
      )

  def create_user_group(
    self,
    configuration: CreateUserGroup
    ) -> UserGroup:
    return execute_request(
      credentials=self.credentials,
      method='post',
      path='/user-groups',
      body=configuration
      )
      
  def details_user_group(
    self,
    id: str
    ) -> UserGroup:
    return execute_request(
      credentials=self.credentials,
      method='get',
      path=f'/user-groups/{id}'
      )

  def update_user_group(
    self,
    id: str,
    configuration: CreateUserGroup
    ) -> UserGroup:
    return execute_request(
      credentials=self.credentials,
      method='put',
      path=f'/user-groups/{id}',
      body=configuration
      )

  def delete_user_group(
    self,
    id: str,
    ) -> ExecuteResponse:
    return execute_request(
      credentials=self.credentials,
      method='delete',
      path=f'/user-groups/{id}',
      )