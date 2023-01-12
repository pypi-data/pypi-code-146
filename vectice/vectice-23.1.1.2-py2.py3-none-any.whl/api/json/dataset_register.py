from __future__ import annotations


from vectice.models.datasource.datawrapper.metadata import FilesMetadata, MetadataDB


class DatasetRegisterOutput(dict):
    @property
    def version(self) -> str:
        return str(self["version"])

    @property
    def use_existing_version(self) -> bool:
        return bool(self["useExistingVersion"])

    @property
    def use_existing_dataset(self) -> bool:
        return bool(self["useExistingDataset"])

    # TODO: complete the jobrun property
    @property
    def job_run(self) -> str:
        return str(self["jobRun"])


class DatasetRegisterInput(dict):
    @property
    def name(self) -> str:
        return str(self["name"])

    @property
    def type(self) -> str:
        return str(self["type"])

    @property
    def data_sources(self) -> list[dict]:
        return list(self["datasetSources"])

    @property
    def inputs(self) -> list[int]:
        return list(self["inputs"])


class DatasetSourceInput(dict):
    @property
    def type(self) -> str:
        return str(self["type"])

    @property
    def usage(self) -> str:
        return str(self["usage"])

    @property
    def origin(self) -> str:
        return str(self["origin"])

    @property
    def size(self) -> int:
        return int(self["size"])

    @property
    def dbs(self) -> list[MetadataDB]:
        return [MetadataDB(**item) for item in self["dbs"]]

    @property
    def filesCount(self) -> int:
        return int(self["filesCount"])

    @property
    def files(self) -> FilesMetadata:
        return FilesMetadata(**self["files"])
