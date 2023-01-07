import logging
import sys

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from gdaps import __version__
from gdaps.api import PluginConfig
from gdaps.pluginmanager import PluginManager

logger = logging.getLogger(__name__)


class GdapsPluginMeta:
    """This is the PluginMeta class of GDAPS itself."""

    version = __version__
    verbose_name = "Generic Django Application Plugin System"
    author = "Christian Gonzalez"
    author_email = "christian.gonzalez@nerdocs.at"
    category = "GDAPS"
    # hidden = True


class GdapsConfig(PluginConfig):
    name = "gdaps"
    PluginMeta = GdapsPluginMeta

    def ready(self):
        import pkg_resources

        # walk through all installed plugins and check some things
        for app in PluginManager.plugins():
            if hasattr(app.PluginMeta, "compatibility"):
                try:
                    pkg_resources.require(app.PluginMeta.compatibility)
                except pkg_resources.VersionConflict as e:
                    logger.critical("Incompatible plugins found!")
                    logger.critical(
                        f"Plugin {app.name} requires you to have {e.req}, but you installed {e.dist}."
                    )

                    sys.exit(1)

        if not settings.PROJECT_NAME:
            raise ImproperlyConfigured("GDAPS needs a PROJECT_NAME settings variable.")

        # load all generic gdaps.plugins - they must be implementations of GDAPS Interfaces
        logger.info("Loading gdaps plugins...")
        for entry_point in pkg_resources.iter_entry_points(
            group="gdaps.plugins", name=None
        ):  # type: pkg_resources.EntryPoint
            # it is enough to have them instantiated, as they are remembered internally in their interface.
            entry_point.load()
