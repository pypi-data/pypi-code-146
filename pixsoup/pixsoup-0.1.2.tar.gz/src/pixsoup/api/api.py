#!/usr/bin/python3
from typing import Dict, Any, Optional
from graphql import DocumentNode
from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport, BasicAuth
from gql.transport.exceptions import TransportQueryError
from dotmap import DotMap
from .queries import *
from .data import *

class APIError(Exception):
  """PixSoup API error.

  Attributes:
    code -- error code (if any)
    message -- error message
    meta -- additional error information
  """

  def __init__(self, error: Any):
    if error['extensions']:
      ext = error['extensions']
      self.code = ext.get('code')
      self.meta = ext.get('meta')
    self.message = error['message']
    super().__init__(self.message)

class APIErrors(Exception):
  """PixSoup API error container.

  Attributes:
    errors -- API errors
    message -- generic error message
  """

  def __init__(self, e: TransportQueryError):
    self.errors = []
    for err in e.errors:
      self.errors.append(APIError(err))
    super().__init__('API returned one or multiple errors')

class PixSoupAPI:
  endpoint = 'https://api.pixsoup.com/graphql'

  def __init__(self, api_key: str, api_token: str):
    transport = AIOHTTPTransport(
      url=self.endpoint,
      auth=BasicAuth(api_key, api_token)
    )
    self.client = Client(transport=transport, fetch_schema_from_transport=True)

  def account(self) -> Account:
    return self._exec(q_account).viewer

  # TODO: support pagination
  def datasets(self) -> list[Dataset]:
    edges = self._exec(q_list_datasets).viewer.datasets.edges
    return [e.node for e in edges]

  def dataset(self, id: ID):
    return self._exec(q_dataset_detail, { 'id': id }).viewer.dataset

  def create_dataset(self, name: str) -> ID:
    return self._exec(m_create_dataset, { 'input': { 'name': name } }).createDataset.dataset.id

  def delete_dataset(self, id: ID) -> bool:
    return self._exec(m_delete_dataset, { 'input': { 'id': id } }).deleteDataset.success

  def seal_dataset(self, id: ID) -> bool:
    return self._exec(m_seal_dataset, { 'input': { 'id': id } }).sealDataset.success

  def create_resource(self, dataset_id: ID, file: FileMeta) -> UploadURI:
    input = { 'dataset': dataset_id, 'file': file.toMap() }
    return self._exec(m_create_resource, { 'input': input }).createResource.uploadUri

  def delete_resource(self, id: ID) -> bool:
    return self._exec(m_delete_resource, { 'input': { 'id': id } }).deleteResource.success

  # TODO: support pagination
  def jobs(self) -> list[Job]:
    edges = self._exec(q_list_jobs).viewer.jobs.edges
    return [e.node for e in edges]

  def job(self, id: ID) -> Job:
    return self._exec(q_job, { 'id': id }).viewer.job

  def run_job(self, dataset_id: ID, name: str, args: dict[str, Any]) -> CreatedJob:
    return self._exec(m_run_dreambooth_job, { 'input': { 'dataset': dataset_id, 'name': name, 'args': args } }).runDreamboothJob.job

  def delete_job(self, id: ID) -> bool:
    return self._exec(m_delete_job, { 'input': { 'id': id } }).deleteJob.success

  def _exec(self, query: DocumentNode, variables: Optional[Dict[str, Any] | None] = None) -> DotMap:
    try:
      return DotMap(self.client.execute(query, variable_values=variables))
    except TransportQueryError as e:
      raise APIErrors(e)
