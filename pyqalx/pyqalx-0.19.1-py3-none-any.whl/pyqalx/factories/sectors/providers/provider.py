from colorama import Fore

from pyqalx.__version__ import __version__
from pyqalx.core.errors import QalxFactoryBuildError

import logging

from pyqalx.core.utils import _msg_user


class BaseProvider:
    """
    A default class that should handle generic functionality across all
    Providers.  This should always be subclassed for each new provider type.
    Assumes that we will be creating a single stack for each profile:region
     intersection

    Instance Attributes:
    factory:     A ~pyqalx.core.entities.factory.Factory instance
    pyqalx_configs: The configs for a User and a Bot based on the
     user_profile and bot_profile arguments on the stage.
    stage:       The stage that is being built
    stack:       The group of sectors for this stage and provider
    profile_name:  The pyqalx profile config name
    region_name:  The region that is being built for
    stack_id:   The ID of the stack.  Initialises to None and is updated when
                the stack creation call is successful
    created:  Boolean for whether the stack has finished creating
    _type: The type of the provider as a string

    :param factory:         A ~pyqalx.factories.factory.Factory instance
    :param stack:       The group of sectors for this stage and provider
    :param profile_name:  The pyqalx profile config name
    :param region_name:  The region that is being built for
    """

    _type = None
    FORE = Fore.WHITE

    def __init__(self, factory, stack, profile_name, region_name):
        self.factory = factory

        self.pyqalx_configs = {}
        self.stage = self.factory.stage
        self.stack = stack

        self.profile_name = profile_name
        self.region_name = region_name
        self.stack_id = None
        self.created = False

        if self._type is None:
            raise QalxFactoryBuildError(
                "`_type` must be defined on implementing class"
            )

    @property
    def factory_name(self):
        return self.factory.entity.name

    @classmethod
    def _send_message(cls, title, message, level, log, fore=None):
        """
        Actually send the message.  Split into a classmethod to handle
        scenarios where we don't have access to an instance but still need to
        log a message
        :param title: The title of the message
        :param message: The message to show the user/log
        :param level: The log level to log the message at
        :param log: Should the message be logged to disk or just printed to
        :param fore:Optional foreground colour.  Defaults to `cls.FORE`
        screen?
        """
        if fore is None:
            fore = cls.FORE
        title = f"{cls._type} - {title}"
        _msg_user(title=title, fore=fore, msg=message, log=log, level=level)

    def _msg_user(
        self, message, level=logging.DEBUG, should_log=True, fore=None
    ):
        """
        Prints a message to the screen for this provider instance
        and also logs it
        :param message: The message to show the user/log
        :param level: The log level to log the message at
        :param log: Should the message be logged to disk or just printed to
        screen?
        """
        log = None
        if should_log:
            # If we should log then use the log on the factory session
            log = self.factory.session.log
        sector_names = f'[{", ".join(self.stack.keys())}]'
        self._send_message(
            title=sector_names, message=message, log=log, level=level, fore=fore
        )

    @property
    def _description(self):
        return (
            f"Created by pyqalx {__version__} "
            f"for factory `{self.factory_name}`"
        )

    @staticmethod
    def validate_permissions(profile_name, region_name, log):
        """
        Validates that the calling user has permission to create the
        resources required for the stack
        """
        pass

    @staticmethod
    def default_profile_name():
        """
        The default profile to use for this provider
        :return: The default provider as a string
        """
        raise QalxFactoryBuildError("Must be implemented by subclass")

    @staticmethod
    def default_region_name(validate, log):
        """
        The default region to use for this provider
        :return: The default region as a string
        """
        raise QalxFactoryBuildError("Must be implemented by subclass")

    @property
    def ERRORED_STATUSES(self):
        """
        List of statuses that mean that the stack errored
        :return: list of statuses
        """
        raise QalxFactoryBuildError("Must be implemented by subclass")

    @property
    def CREATED_STATUS(self):
        """
        The status that means that the stack creation completed
        :return: string denoting the successful creation status
        """
        raise QalxFactoryBuildError("Must be implemented by subclass")

    def _resource_name(self, sector_name, suffix):
        """
        The name of the resource on AWS.  Appended with the factory name and
        factory guid to help ensure uniqueness
        :param sector_name: The sector that this resource belongs to
        :param suffix: The suffix to append to the name
        :return: A sanitised name for the resource
        """
        return self._sanitise_name(
            f"qalx-{self.factory_name}-{sector_name}-{suffix}"
            f"-{self.factory.entity.guid}"
        )

    @staticmethod
    def _sanitise_name(name):
        """
        Helper for sanitising the name into a cloudformation friendly format
        :param name: The name to sanitise
        :type name:str
        :return: The sanitised name.
        """
        return name.replace("_", "")

    def _stack_name(self):
        return self._sanitise_name(
            f"qalx-factory-{self.factory_name}-{self.profile_name}"
            f"-{self.factory.entity.guid}"
        )

    def _build_stack(self):
        """
        Provider specific method for building the stack template
        """
        raise QalxFactoryBuildError("Must be implemented by subclass")

    def _create_stack(self, stack):
        """
        Provider specific method for creating the stack in the provider
        :param stack: The stack template to create
        :return: The ID of the creating stack
        """
        raise QalxFactoryBuildError("Must be implemented by subclass")

    def _describe_stack(self):
        """
        Provider specific method for getting the status of the stack
        :return: The stacks status
        """
        raise QalxFactoryBuildError("Must be implemented by subclass")

    def _get_error_reason(self):
        """
        Provider specific method for getting the reasons a stack failed
        :return: list of reasons for the failed stack
        """
        raise QalxFactoryBuildError("Must be implemented by subclass")

    def _delete_stack(self, stack_id):
        """
        Provider specific method for deleting the stack
        """
        raise QalxFactoryBuildError("Must be implemented by subclass")

    def describe_stack(self):
        """
        Public interface for describing stacks
        """
        return self._describe_stack()

    def delete_stack(self, stack_id):
        """
        Public interface for deleting stacks
        """
        demolish_on_failure = self.factory._plan_debug._demolish_on_failure
        is_demolish_command = (
            self.factory.entity.status == self.factory.DELETING_STATUS
        )
        if demolish_on_failure or is_demolish_command:
            # Only demolish if the specific debug key is set on the plan OR
            # the user has run the `qalx factory-demolish` command (which updates
            # the entity status)
            self._msg_user("deleting")
            self._delete_stack(stack_id)
        else:
            # User wants to keep failed stack around.  Inform them what is
            # going on
            self._msg_user(
                self.factory._plan_debug._demolish_on_failure_msg,
                level=logging.DEBUG,
                # It's a debug message - but we want it to pop!
                fore=Fore.RED,
            )

    def create_stack(self):
        """
        Builds the stack yaml and then creates the stacks.  Calls out to
        the monitoring helper to ensure that all the stacks get created
        correctly.
        """
        # Build the stack for the specific provider
        stack = self._build_stack()
        if stack is not None:
            # Start creating the stack if there were no problems with building
            # it.
            self._msg_user("creating")
            self._create_stack(stack)
