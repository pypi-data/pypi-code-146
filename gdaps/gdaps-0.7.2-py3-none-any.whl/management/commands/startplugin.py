import logging

from pathlib import Path
from django.conf import settings
from django.core.management.base import CommandError, BaseCommand

from gdaps.conf import gdaps_settings

# from gdaps.pluginmanager import PluginManager

logger = logging.getLogger(__name__)

try:
    # if git is available, make use of git username/email config data
    import git

    reader = git.Repo.init(settings.BASE_DIR).config_reader()
except:
    reader = None
    logger.info(
        "If you want to take author/email automatically from current git repo, "
        "install gitpython using pip, and provide your data in the .gitconfig file."
    )


def get_user_data(key, default=""):
    if reader:
        return reader.get_value("user", key, default)
    else:
        return ""


class Command(BaseCommand):
    """This is the managemant command to add a plugin from a cookiecutter template to a Django application."""

    # absolute path to internal plugins of application
    # plugin_path = PluginManager.plugin_path()
    plugin_path = Path.cwd()
    help = (
        "Creates a basic GDAPS plugin from a cookiecutter template in the current working directory, e.g.\n"
        "You can also do a \n"
        "    cookiecutter gl:nerdocs/gdaps-plugin-cookiecutter"
    )
    missing_args_message = "You must provide a plugin name."

    def add_arguments(self, parser):
        parser.add_argument("name")

    def handle(self, name: str, **options):

        try:
            from cookiecutter.main import cookiecutter
        except ImportError:
            raise CommandError(
                "You have to install cookiecutter to make this command work."
            )

        if not name.isidentifier():
            raise CommandError(
                "The <name> parameter has to be a valid Python identifier."
            )

        logger.debug(f"Using plugin directory: {self.plugin_path}")

        try:
            target_path = Path(
                cookiecutter(
                    "gl:nerdocs/gdaps-plugin-cookiecutter",
                    extra_context={
                        "project_slug": settings.PROJECT_NAME,
                        "project_title": gdaps_settings.PROJECT_TITLE,
                        "plugin_title": name.replace("_", " ").capitalize(),
                        "app_name": name,
                        "author": get_user_data("name"),
                        "author_email": get_user_data("email"),
                    },
                    output_dir=self.plugin_path,
                )
            )
            # FIXME pip install -e only accepts relative paths (self.plugin_path)
            logger.info(
                f"\nSuccessfully created plugin: {target_path}\n"
                f"* Please edit '{target_path / 'setup.cfg'}' to your needs.\n"
                f"* Install the plugin locally using 'pip install -e {self.plugin_path}/{settings.PROJECT_NAME}-{name}'\n"
                f"  or with flit: 'flit install --symlink {self.plugin_path}/{settings.PROJECT_NAME}-{name}'\n"
                f"  Or you can add the plugin directly to your INSTALLED_APPS if you want it bundled with your application.\n"
                f"* Don't forget to call './manage.py syncplugins' after installing a new plugin to keep "
                f"your DB in sync.\n"
            )
        except Exception as e:
            logger.critical(f"There was an error with cookiecutter: \n {e}")
