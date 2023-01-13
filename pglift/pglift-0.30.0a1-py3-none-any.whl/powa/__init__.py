import logging
from typing import TYPE_CHECKING, Optional, Type

from pgtoolkit.conf import Configuration

from .. import hookimpl
from ..models import interface, system
from . import models
from .impl import POWA_EXTENSIONS, POWA_LIBRARIES
from .impl import available as available

if TYPE_CHECKING:

    from ..ctx import Context
    from ..settings import Settings

logger = logging.getLogger(__name__)


def register_if(settings: "Settings") -> bool:
    return available(settings) is not None


@hookimpl
def instance_settings(ctx: "Context") -> Configuration:
    conf = Configuration()
    conf["shared_preload_libraries"] = ", ".join(POWA_LIBRARIES)
    return conf


@hookimpl
def interface_model() -> Type[models.ServiceManifest]:
    return models.ServiceManifest


@hookimpl
def get(ctx: "Context", instance: "system.Instance") -> models.ServiceManifest:
    return models.ServiceManifest()


@hookimpl
def rolename(settings: "Settings") -> str:
    assert settings.powa
    return settings.powa.role


@hookimpl
def role(
    settings: "Settings", manifest: "interface.Instance"
) -> Optional[interface.Role]:
    name = rolename(settings)
    service_manifest = manifest.service_manifest(models.ServiceManifest)
    password = None
    if service_manifest.password:
        password = service_manifest.password.get_secret_value()
    return interface.Role(
        name=name,
        password=password,
        login=True,
        superuser=True,
    )


@hookimpl
def database(
    settings: "Settings", manifest: "interface.Instance"
) -> Optional[interface.Database]:
    assert settings.powa
    return interface.Database(name=settings.powa.dbname, extensions=POWA_EXTENSIONS)
