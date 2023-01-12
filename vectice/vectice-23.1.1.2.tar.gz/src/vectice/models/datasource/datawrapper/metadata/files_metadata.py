from __future__ import annotations


from vectice.models.datasource.datawrapper.metadata.metadata import (
    DatasetSourceUsage,
    Metadata,
    SourceOrigin,
    SourceType,
)


class FilesMetadata(Metadata):
    """
    The metadata of a set of files.
    """

    def __init__(
        self,
        files_count: int,
        files: list[File],
        size: int,
        origin: SourceOrigin,
        usage: DatasetSourceUsage | None = None,
    ):
        """
        :param files_count: the number of files contained in the list
        :param files: the list of files of the dataset
        :param size: the size of the set of files
        :param usage: the usage of the dataset
        :param origin: where the dataset files come from
        """
        super().__init__(size, SourceType.FILES.name, origin.name, usage if usage else None)
        self.files = files
        self.files_count = files_count

    def asdict(self) -> dict:
        return {
            "filesCount": self.files_count,
            "files": [file.asdict() for file in self.files],
            "size": self.size,
            "usage": self.usage.value if self.usage else None,
            "origin": self.origin if self.origin else None,
            "type": self.type,
        }


class File:
    """
    Describe a dataset file.
    """

    def __init__(
        self,
        name: str,
        size: int,
        fingerprint: str,
        created_date: str | None = None,
        updated_date: str | None = None,
        uri: str | None = None,
    ):
        """
        :param name: the name of the file
        :param size: the size of the file
        :param fingerprint: the hash of the file
        :param created_date: the date of creation of the file
        :param updated_date: the date of last update of the file
        :param uri: the uri of the file
        """
        self.name = name
        self.size = size
        self.fingerprint = fingerprint
        self.created_date = created_date
        self.updated_date = updated_date
        self.uri = uri

    def asdict(self) -> dict:
        return {
            "name": self.name,
            "size": self.size,
            "fingerprint": self.fingerprint,
            "createdDate": self.created_date,
            "updatedDate": self.updated_date,
            "uri": self.uri,
        }
