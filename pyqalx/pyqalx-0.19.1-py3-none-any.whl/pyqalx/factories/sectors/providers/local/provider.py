import concurrent.futures
import logging

from colorama import Fore

from pyqalx.core.errors import QalxFactoryBuildError
from pyqalx.factories.sectors.providers.provider import BaseProvider


class LocalProvider(BaseProvider):
    """
    A provider subclass for bots that run locally.

    Instance attributes

        _error_reasons:  A list of errors for any bots that have failed
    """

    _type = "local"

    FORE = Fore.GREEN
    REGION_NAME_KEY = "region_name"
    PROFILE_NAME_KEY = "profile_name"
    CREATED = "CREATED"
    DELETED = "DELETED"
    DELETE_FAILED = "DELETED"
    ERRORED = "ERRORED"

    def __init__(self, *args, **kwargs):
        super(LocalProvider, self).__init__(*args, **kwargs)
        self._error_reasons = []
        self._deleted = False

    @staticmethod
    def default_profile_name():
        return "local"

    @staticmethod
    def default_region_name(validate, log):
        return "local"

    @property
    def ERRORED_STATUSES(self):
        return [self.ERRORED]

    @property
    def CREATED_STATUS(self):
        return self.CREATED

    @property
    def DELETED_STATUSES(self):
        return [self.DELETED]

    def _install_and_start_bot(self, bot_source, sector):
        """
        Helper for installing and starting the bot
        :param bot_source: An instance of BotSource
        :param sector: The sector that the bot is on.
        :return: The response from `start_bot`
        """
        try:
            bot_source.install_bot()
        except QalxFactoryBuildError as exc:
            # QalxFactoryBuildError: There was a problem installing the bot

            # Make a fake "output" object that has the returncode
            # attribute so `futures.as_completed` can treat a failure here
            # in the same way as a failure to `start_bot`
            output = type("", (object,), {})()
            output.returncode = 1
            error = str(exc)
        else:
            bot_arguments = sector["bots"][bot_source.bot_name]
            # if skip-ini is present on the plan then it's assumed that
            # the user wants to skip-ini - regardless of the value of the key.
            # This mirrors the behaviour of `--skip-ini` on the CLI
            skip_ini = "skip-ini" in bot_arguments.keys()
            # Need to remove `skip-ini` from the bot arguments as it's handled
            # differently in `self.factory.start_bot`
            bot_arguments.pop("skip-ini", None)

            output, error = self.factory.start_bot(
                plan_bot_name=bot_source.bot_name,
                build_path=bot_source.build_path,
                bot_path=bot_source.bot["bot_path"],
                bot_arguments=bot_arguments,
                sector=sector,
                skip_ini=skip_ini,
            )
        return output, error

    def _create_stack(self, *args, **kwargs):
        """
        Starts each bot on the local sector.  If any error during starting then
        stop immediately and return that error so that the manager can
         handle stopping the build

        :return: The stack_id of `success` if starting the bot is successful
        """
        bots = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            for sector in self.stack.values():
                for bot_source in self.factory.bot_sources:
                    if bot_source.bot_name in sector["bots"]:
                        bots[
                            executor.submit(
                                self._install_and_start_bot,
                                bot_source=bot_source,
                                sector=sector,
                            )
                        ] = bot_source.bot_name
            for future in concurrent.futures.as_completed(bots):
                plan_bot_name = bots[future]
                output, error = future.result()
                if output.returncode is not None:
                    # There was an error starting up this bot.
                    self._msg_user(str(error), level=logging.ERROR)
                    self._error_reasons.append(f"{plan_bot_name}: {error}")
                else:
                    # Local sectors won't have a stack ID.
                    # But it is still required for the manager to monitor the
                    # creation of all stacks.  If one bot starts, but another local
                    # bot fails, the manager will handle shutting down the started
                    # bot.
                    self.stack_id = "success"
        return self.stack_id

    def _describe_stack(self):
        """
        Local bot startup needs to be atomic.  Therefore, if any of them error
        then we should show the whole stack as failed.
        """
        status = self.CREATED

        if self._error_reasons:
            status = self.ERRORED
        if self._deleted or (self._error_reasons and self.stack_id is None):
            # Regardless of whether or not there are errors,
            # if the _deleted flag is set then the stack has been deleted.
            # There may be errors and no stack id if no bots at all were able
            # to start.  In which case, nothing was created so the stack can be
            # marked as "DELETED"
            status = self.DELETED
        return status

    def _delete_stack(self, stack_id):
        """
        The stack needs to be deleted because either a single local bot failed
        to start, or a remote sector failed to create properly.  There could
        be bots running (albeit in a stopped state), so use the same termination
        process as what would be used when demolishing a factory.  The actual
        bot process will then get terminated by the bot itself as
         if `qalx bot-terminate` had been called.  This will most likely be very
         quick as the bots won't have started working on anything.
        """
        self.factory.breadth_first_terminate()
        # Flag so we can update `_describe_stack`
        self._deleted = True
        return

    def _get_error_reason(self):
        """
        A local stack could have multiple bots running on it.  Therefore
        the error reasons needs to be a list of reasons
        """
        return self._error_reasons or ["Unknown Error"]

    def _build_stack(self):
        """
        This method is used for remote sectors to build a template to build
        remote resources.  As such, a local sector does not require it so it
        should just return True
        """
        return True
