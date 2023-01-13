import configparser
import os
from inspect import ismodule
from os import environ
from .types import (
    BOOL,
    LOGGING_OPTIONS,
    DIR_PATH_NON_EXISTING,
    FILE_PATH_NON_EXISTING,
    FILE_PATH_EXISTING,
    POSITIVE_INT,
)

from click.types import STRING
from click import BadParameter

from . import defaults
from pyqalx.config.defaults import bots
from pyqalx.core.errors import (
    QalxConfigProfileNotFound,
    QalxConfigFileNotFound,
    QalxConfigError,
)


class Config(dict):
    key_prefix = ""
    filename = ""
    default = "default"
    default_type_map = {
        "TOKEN": STRING,
        "KEYFILE": FILE_PATH_EXISTING,
        "LOGGING_LEVEL": LOGGING_OPTIONS,
        "LOG_FILE_PATH": FILE_PATH_NON_EXISTING,
        "MSG_BLACKOUTSECONDS": POSITIVE_INT,
        "MAX_RETRY_500": POSITIVE_INT,
        "FACTORY_PACK_DIR": DIR_PATH_NON_EXISTING,
        "DOWNLOAD_DIR": DIR_PATH_NON_EXISTING,
        "REGION": STRING,
    }

    def __init__(self):
        dict.__init__(self, self.defaults)
        for key, value in [
            (k, v) for k, v in environ.items() if k.startswith(self.key_prefix)
        ]:
            self[key.replace(self.key_prefix, "")] = value
        self._validate(self)

    @classmethod
    def config_path(cls):
        return os.path.join(os.path.expanduser("~"), cls.filename)

    @classmethod
    def _load_inifile(cls, profile_name):
        """
        Loads the inifile and returns the values of the specific
        profile_name as a dict
        :param profile_name: The name of the profile to load
        :return: Dict of config options
        :raises: QalxConfigProfileNotFound
        """
        if os.path.exists(cls.config_path()):
            config = configparser.ConfigParser()
            config.optionxform = str
            with open(cls.config_path()) as cfg:
                config.read_string(
                    cfg.read()
                )  # this makes mocks easier over config.read(filepath)
            if profile_name in config.keys():
                config_dict = config[profile_name]
            else:
                profiles = "\n".join(config.keys())
                msg = (
                    "Couldn't find profile named {} in {} file."
                    " Did you mean one of:\n{}".format(
                        profile_name, cls.filename, profiles
                    )
                )
                raise QalxConfigProfileNotFound(msg)
            return dict(config_dict)
        else:
            raise QalxConfigFileNotFound(
                "Couldn't find {}".format(cls.config_path())
            )

    def from_inifile(self, profile_name=None):
        if profile_name is None:
            profile_name = self.default
        config_dict = self._load_inifile(profile_name=profile_name)
        self.update(config_dict)
        self._validate(self)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, dict.__repr__(self))

    @property
    def defaults(self):
        """
        Returns a dict of default values for config options from
        `~pyqalx.config.defaults.__init__`

        :return : dict of options
        """
        return {
            k: v
            for k, v in vars(defaults).items()
            if (not k.startswith("__")) and (not ismodule(v))
        }

    @classmethod
    def configure(cls, profile_name, config_items=None):
        """
        When given a profile name and dict of config items will write the
        config file to disk.  If a `profile_name` is given that already exists
        on the profile then the `profile_name` on the profile will be
        completely replaced with the values from config_items

        :param profile_name: The name of the profile to write
        :type profile_name: str
        :param config_items: A dict of items that should be written to the
                             config
        :type config_items: dict
        """
        if config_items is None:
            # We might just be writing a blank config (i.e. for `.bots`)
            config_items = {}
        validated_items = cls._validate(config_items)
        with open(cls.config_path(), "a") as cfg:
            config_string = f"[{profile_name}]\n"
            for config_key, config_value in validated_items.items():
                config_string += f"{config_key}={config_value}\n"
            cfg.write(config_string)

    @staticmethod
    def _get_logging_details():
        raise QalxConfigError("Must be implemented by implementing class")

    def _create_log_directories(self):
        """
        Creates the directory structure for the log files.  Iterates through
        a list of data from `_get_logging_details()` to handle different types
        of logging directories for each config
        """
        for logging_details in self._get_logging_details():
            # expects_file, key, dir_path = self._get_logging_details()
            CONFIG_KEY = logging_details["CONFIG_KEY"]
            logger_path = self[CONFIG_KEY]
            ISFILE = logging_details["ISFILE"]
            method = "isdir" if ISFILE else "isfile"
            if getattr(os.path, method)(logger_path):
                # If its a file, check it isn't already on disk as a directory,
                # and vice-versa
                msg = (
                    f"`{CONFIG_KEY}`: {logger_path} exists, but it is"
                    f" not a {'file' if ISFILE else 'directory'}."
                )
                raise QalxConfigError(msg)
            if ISFILE:
                logger_path = os.path.dirname(logger_path)
            try:
                os.makedirs(logger_path, exist_ok=True)
            except (OSError, PermissionError):
                msg = (
                    f"`{CONFIG_KEY}`: {logger_path}"
                    f" does not exist and it could not be created."
                )
                raise QalxConfigError(msg)

    @classmethod
    def _validate(cls, config_dict):
        """
        Validate and parse the values for the default config keys according to
        their respective type. For the provided config_dict with raw
        values, these are parsed and replaced
        """
        for config_key, config_value in config_dict.items():
            parse_type = cls.default_type_map.get(config_key, None)
            if parse_type is not None:
                try:
                    parsed_value = parse_type(config_value)
                except BadParameter as exc:
                    message = (
                        "There was an error parsing the config value for "
                        + f"{config_key}:\n\n{exc}"
                    )
                    raise QalxConfigError(message)
                else:
                    config_dict[config_key] = parsed_value
        return config_dict


class BotConfig(Config):
    """
    Works exactly like a dict but provides ways to fill it from ini files
    and environment variables.  There are two common patterns to populate the
    config.

    Either you can add them to the `.bots` file:

    >>> bot.config.from_botsfile(profile_name=BotConfig.default)

    Or alternatively you can define the configuration from environment variables
    starting with `QALX_BOT_`. These will be populated automatically
    but values defined in `.bots` will overwrite these if
    `bot.config.from_botsfile()` is called.

    To set environment variables before launching the application you have to set this
    environment variable to the name and value you want to use.
    On Linux and OS X use the export statement::

    >>> export QALX_BOT_LICENCE_FILE='/path/to/licence/file'

    On windows use `set` instead.
    """

    key_prefix = "QALX_BOT_"
    filename = ".bots"
    default_type_map = dict(Config.default_type_map)
    default_type_map.update(
        {
            "WORKER_LOG_FILE_DIR": DIR_PATH_NON_EXISTING,
            "SAVE_INTERMITTENT": BOOL,
            "SKIP_FINAL_SAVE": BOOL,
            "KILL_AFTER": POSITIVE_INT,
            "Q_WAITTIMESECONDS": POSITIVE_INT,
            "Q_MSGBATCHSIZE": POSITIVE_INT,
            "Q_WAITTIMEMAXSPREADING": POSITIVE_INT,
            "MSG_WAITTIMESECONDS": POSITIVE_INT,
        }
    )

    @property
    def defaults(self):
        """
        Loads the default bot config from `~pyqalx.config.defaults.bots`.  Any
        config items that exists in `~pyqalx.config.defaults.__init__` will be
        overwritten by config values that exist in `~pyqalx.config.defaults.bots`

        :return: dict of default config options
        """
        config = super(BotConfig, self).defaults
        bot_config = {
            k: v
            for k, v in vars(bots).items()
            if not k.startswith("__") and (not ismodule(v))
        }
        config.update(bot_config)
        # `REGION` will come from the super() class defaults.  However, it isn't
        # a valid option when creating a `BotConfig`, so remove it from
        # the defaults
        config.pop("REGION", None)
        return config

    @staticmethod
    def _get_logging_details():
        return [{"CONFIG_KEY": "WORKER_LOG_FILE_DIR", "ISFILE": False}]

    @classmethod
    def _validate(cls, config_dict):
        config_dict = super(BotConfig, cls)._validate(config_dict)
        if config_dict.get("REGION"):
            # To avoid confusing issues with a Bot config looking at a
            # different region to a user config, the ability to set the region
            # on a bot config inifile is prohibited.  The region can only be
            # set manually to help ensure that the region on the bot qalx session
            # matches the region on the user qalx session when initialising Bots
            raise QalxConfigError(
                "`REGION` is not a valid config option "
                f"for `{cls.__name__}`.  Did you mean to add"
                " `REGION` to a user config?"
            )
        return config_dict


class UserConfig(Config):
    """Works exactly like a dict but provides ways to fill it from ini files
    and environment variables.  There are two common patterns to populate the
    config.
    Either you can add them to the `.qalx_bot` file:

    >>> qalx_bot.config.from_qalxfile(profile_name=UserConfig.default)

    Or alternatively you can define the configuration from environment variables
    starting with `QALX_USER_`. These will be populated automatically
    but values defined in `.qalx` will overwrite these if
    `qalx_bot.config.from_qalxfile()` is called.

    To set environment variables before launching the application you have to set this
    environment variable to the name and value you want to use.
    On Linux and OS X use the export statement::

    >>>export QALX_USER_EMPLOYEE_NUMBER=1280937

    On windows use `set` instead.
    """

    key_prefix = "QALX_USER_"
    filename = ".qalx"
    # The default region to use when prompting the user as part of `qalx configure`
    DEFAULT_REGION = "london"
    # The region mapping to use when validating the region chosen by the user
    # Nested under `aws` to make it easier to add different providers in the
    # future
    REGION_MAPPING = {"aws": {DEFAULT_REGION: "eu-west-2"}}

    @staticmethod
    def _get_logging_details():
        return [{"CONFIG_KEY": "LOG_FILE_PATH", "ISFILE": True}]
