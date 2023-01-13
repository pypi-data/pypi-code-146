import platform

from pyqalx.config import UserConfig, Config
from pyqalx.core.adapters import (
    QalxBlueprint,
    QalxBot,
    QalxGroup,
    QalxItem,
    QalxQueue,
    QalxSet,
    QalxWorker,
    QalxFactory,
    QalxNotification,
)
from pyqalx.core.log import configure_logging, session_logging_suffix
from pyqalx.core.registry import Registry
from pyqalx.core.tags import Tags
from pyqalx.transport import PyQalxAPI


class QalxSession:
    """The session that any interaction with the API will use."""

    def __init__(
        self,
        profile_name=Config.default,
        config_class=None,
        skip_ini=False,
        rest_api_class=None,
        project_name=None,
    ):
        """
        :param profile_name:    profile name to get from `config_class`
                                (default=Config.default)
        :type profile_name: str
        :param config_class:  The class for the config that will be used for
                                this session
        :type config_class: ~pyqalx.config.configs.Config
        :param skip_ini: Should loading the config from the inifile be skipped?
        :type skip_ini: bool
        :param rest_api_class: The class to use for the rest api
        :type rest_api_class: ~pyqalx.transport.api.PyQalxAPI
        :param project_name: An optional name of a project. This will be used
                              to tag all data that is created/modified with this session
        :type project_name: str
        """

        if config_class is None:
            config_class = UserConfig
        self.config = config_class()
        self.profile_name = profile_name
        if not skip_ini:
            self.config.from_inifile(profile_name)
        # Configure the log for this session.  This cannot be set on an
        # instance attribute due to pickling issues with windows.  However,
        # it needs to be configured as early as possibly after config
        # initialisation so that if there is an unhandled exception this can be
        # logged properly
        self.configure_logging()

        if rest_api_class is None:
            rest_api_class = PyQalxAPI
        self.rest_api = rest_api_class(self)
        self._registry = Registry()
        self._registry._register_defaults()
        self.tags = Tags([], rest_api=self.rest_api)
        if project_name:
            self.tags.add(name="project_name", value=project_name)

    def configure_logging(self):
        """
        Configures the log for this session.  A log is namespaced for the
        config type and the profile name to allow a user to have multiple
        session instances with different configs/profiles logging to different
        places.

        :return: An instance of `logging.getLogger`
        """
        # Ensures that the log directories are created if they don't already
        # exist
        self.config._create_log_directories()
        return configure_logging(
            f"{session_logging_suffix(self.config)}.{self.profile_name}",
            self.config.get("LOG_FILE_PATH"),
            self.config.get("LOGGING_LEVEL"),
        )

    @property
    def log(self):
        """
        Returns an instance of `logging.getLogger` for this QalxSession instance
        This cannot be set as an instance attribute due to pickling issues on
        windows.  Will log depending on the `LOGGING_LEVEL` config value.

        Usage:

        >>> QalxSession().log.debug("A debug message")
        >>> QalxSession().log.info("An info message")
        >>> QalxSession().log.warning("A warning message")
        >>> QalxSession().log.error("An error message")

        :returns: `logging.getLogger`
        """
        return self.configure_logging()

    def __setattr__(self, key, value):
        if key == "tags" and hasattr(self, "tags"):
            # The user is completely replacing the tags.
            # Attempt to validate them before replacing them.
            self.tags._validate(value)
        return super(QalxSession, self).__setattr__(key, value)

    def _update_config(self, config):
        """
        Method to use if the config needs to be updated after the session has
        been created.
        Also updates the rest_api with the updated config

        :param config:A config dict
        :type config: dict
        :return:
        """
        self.config.update(config)
        self.rest_api = self.rest_api.__class__(self)

    def register(self, cls):
        """
        Registers the given :class:`~pyqalx.core.entities.entity.QalxEntity`
        subclass with the session.   See entities docs for more info

        :param cls: subclass of QalxEntity.
        :type cls: pyqalx.core.entities.entity.QalxEntity
        """
        self._registry.register(cls)

    def unregister(self, cls):
        """
        Unregisters the given :class:`~pyqalx.core.entities.entity.QalxEntity`
        subclass from the session.   See entities docs for more info

        :param cls: subclass of QalxEntity.
        :type cls: pyqalx.core.entities.entity.QalxEntity
        """
        self._registry.unregister(cls)

    @property
    def _host_info(self):
        return {
            "node": platform.node(),
            "platform": platform.platform(),
            "ip": self.rest_api._get_external_ip(),
        }

    @property
    def item(self):
        """
        returns a :class:`~pyqalx.core.adapters.item.QalxItem` adapter for
        this session

        :return: Instance of :class:`~pyqalx.core.adapters.item.QalxItem`
        """
        return QalxItem(self)

    @property
    def set(self):
        """
        returns a :class:`~pyqalx.core.adapters.set.QalxSet` adapter for
        this session

        :return: Instance of :class:`~pyqalx.core.adapters.set.QalxSet`
        """
        return QalxSet(self)

    @property
    def group(self):
        """
        returns a :class:`~pyqalx.core.adapters.group.QalxGroup` adapter for
        this session

        :return: Instance of :class:`~pyqalx.core.adapters.group.QalxGroup`
        """
        return QalxGroup(self)

    @property
    def queue(self):
        """
        returns a :class:`~pyqalx.core.adapters.queue.QalxQueue` adapter for
        this session

        :return: Instance of :class:`~pyqalx.core.adapters.queue.QalxQueue`
        """
        return QalxQueue(self)

    @property
    def bot(self):
        """
        returns a :class:`~pyqalx.core.adapters.bot.QalxBot` adapter for
        this session

        :return: Instance of :class:`~pyqalx.core.adapters.bot.QalxBot`
        """
        return QalxBot(self)

    @property
    def worker(self):
        """
        returns a :class:`~pyqalx.core.adapters.worker.QalxWorker` adapter
        for this session

        :return: Instance of :class:`~pyqalx.core.adapters.worker.QalxWorker`
        """
        return QalxWorker(self)

    @property
    def factory(self):
        """
        returns a :class:`~pyqalx.core.adapters.factory.QalxFactory` adapter
        for this session

        :return: Instance of :class:`~pyqalx.core.adapters.factory.QalxFactory`
        """
        return QalxFactory(self)

    @property
    def blueprint(self):
        """
        returns a :class:`~pyqalx.core.adapters.blueprint.QalxBlueprint`
        adapter for this session

        :return: Instance of :class:`~pyqalx.core.adapters.blueprint.QalxBlueprint`
        """
        return QalxBlueprint(self)

    @property
    def notification(self):
        """
        returns a :class:`~pyqalx.core.adapters.notification.QalxNotification`
        adapter for this session

        :return: Instance of
                :class:`~pyqalx.core.adapters.notification.QalxNotification`
        """
        return QalxNotification(self)
