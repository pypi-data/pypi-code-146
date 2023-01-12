from typing import NewType, Any

ID = NewType("ID", str)
ISODate = NewType("ISODate", str)
UploadURI = NewType("UploadURI", str)

class FileMetaInput:
  def __init__(self, name: str, ct: str, sz: int):
    self.name = name
    self.contentType = ct
    self.contentLength = sz

  def toMap(self) -> Any:
    return self.__dict__

class _Account:
  email: str
  tokens: int
  verifiedEmail: bool
  jobCallbackUri: str | None

class _Resource:
  id: ID
  name: str

class _Dataset:
  id: ID
  name: str
  createdAt: ISODate
  sealedAt: ISODate | None

class _DatasetDetail(_Dataset):
  sealedAt: ISODate
  resources: list[_Resource]

class _CreatedJob:
  id: ID
  state: str

class _Job(_CreatedJob):
  name: str
  args: str
  createdAt: ISODate
  startedAt: ISODate | None
  finishedAt: ISODate | None
  downloadLink: str | None

FileMeta = NewType("FileMeta", FileMetaInput)
Account = NewType("Account", _Account)
Resource = NewType("Resource", _Resource)
Dataset = NewType("Dataset", _Dataset)
DatasetDetail = NewType("DatasetDetail", _DatasetDetail)
CreatedJob = NewType("CreatedJob", _CreatedJob)
Job = NewType("Job", _Job)