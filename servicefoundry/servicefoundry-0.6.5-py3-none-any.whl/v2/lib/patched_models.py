from typing import Union

from pydantic import Field, constr

from servicefoundry.auto_gen import models


class DockerFileBuild(models.DockerFileBuild):
    class Config:
        extra = "forbid"

    type: constr(regex=r"dockerfile") = "dockerfile"


class PythonBuild(models.PythonBuild):
    class Config:
        extra = "forbid"

    type: constr(regex=r"tfy-python-buildpack") = "tfy-python-buildpack"


class RemoteSource(models.RemoteSource):
    class Config:
        extra = "forbid"

    type: constr(regex=r"remote") = "remote"


class LocalSource(models.LocalSource):
    class Config:
        extra = "forbid"

    type: constr(regex=r"local") = "local"


class Build(models.Build):
    class Config:
        extra = "forbid"

    type: constr(regex=r"build") = "build"
    build_source: Union[
        models.RemoteSource, models.GitSource, models.LocalSource
    ] = Field(default_factory=LocalSource)


class Manual(models.Manual):
    class Config:
        extra = "forbid"

    type: constr(regex=r"manual") = "manual"


class Schedule(models.Schedule):
    class Config:
        extra = "forbid"

    type: constr(regex=r"scheduled") = "scheduled"


class GitSource(models.GitSource):
    class Config:
        extra = "forbid"

    type: constr(regex=r"git") = "git"


class HttpProbe(models.HttpProbe):
    class Config:
        extra = "forbid"

    type: constr(regex=r"http") = "http"


class BasicAuthCreds(models.BasicAuthCreds):
    class Config:
        extra = "forbid"

    type: constr(regex=r"basic_auth") = "basic_auth"


class TruefoundryModelRegistry(models.TruefoundryModelRegistry):
    class Config:
        extra = "forbid"

    type: constr(regex=r"tfy-model-registry") = "tfy-model-registry"


class HuggingfaceModelHub(models.HuggingfaceModelHub):
    class Config:
        extra = "forbid"

    type: constr(regex=r"hf-model-hub") = "hf-model-hub"


class HealthProbe(models.HealthProbe):
    class Config:
        extra = "forbid"


class Image(models.Image):
    class Config:
        extra = "forbid"

    type: constr(regex=r"image") = "image"


class Port(models.Port):
    class Config:
        extra = "forbid"


class Resources(models.Resources):
    class Config:
        extra = "forbid"


class Param(models.Param):
    class Config:
        extra = "forbid"
