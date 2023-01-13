import os
import sys
from functools import partial
from multiprocessing import Process
from time import sleep
from collections import OrderedDict

# We may need below, we may not. What can I say? Dill waters run deep.
import dill

from pyqalx import QalxBot
from pyqalx.config import BotConfig, UserConfig
from pyqalx.core.adapters import QalxQueue, QalxWorker
from pyqalx.core.enums import ValidStates
from pyqalx.core.session import QalxSession
from pyqalx.core.errors import (
    QalxBotInitialisationFailed,
    QalxStepFunctionNotDefined,
    QalxMultipleEntityReturned,
    QalxEntityNotFound,
    QalxAPIResponseError,
)
from pyqalx.core.errors import QalxError
from pyqalx.core.log import exception_hook, configure_logging
from pyqalx.core.signals import QalxSignal
from pyqalx.factories.factory import Factory

dill.settings["recurse"] = True


def do_nowt(*args, **kwargs):
    pass


def do_nowt_right(*args, **kwargs):
    return True


def cannot_be_undefined(*args, **kwargs):
    """
    Raises an exception if a step function cannot be left undefined.
    Handled here to avoid a user trying to call the specific step function
    directly.
    """
    raise QalxStepFunctionNotDefined(
        f"`{kwargs['step_name']}` function must be defined either "
        f"as a decorator (`@mybot.{kwargs['step_name']}`) or by "
        f"overriding the function entirely "
        f"(`mybot.{kwargs['step_name']}_function = <{kwargs['step_name']}_function>`)"
    )


class QalxJob:
    """a Job to process

    :param worker_process: The instance of the worker that is running this job
    :type worker_process: ~pyqalx.bot.Worker
    """

    __slots__ = (
        "worker_adapter",
        "entity_adapter",
        "entity",
        "session",
        "state",
        "options",
        "progress",
        "warnings",
        "errors",
        "_current_step",
        "_process",
        "_worker_entity",
        "_bot_entity",
        "_queue_message",
        "_step_results",
        "context",
        "do_workflow",
    )

    def __init__(self, worker_process):
        self._process = worker_process
        self.worker_adapter = worker_process.worker_adapter
        self._bot_entity = worker_process.bot_entity
        self._worker_entity = worker_process.api_entity
        self.session = worker_process.session

        self._current_step = "class init"
        # We need to preserve the order of step results and although in Python
        # >= 3.6 this is implemented in the dict class, it cannot be relied upon
        # https://docs.python.org/3.6/whatsnew/3.6.html#whatsnew36-compactdict
        self._step_results = OrderedDict()
        self.context = dict()
        self.do_workflow = True

    @property
    def log(self):
        """
        An instance of the workers log to enable logging from step functions
        """
        return self._process.log

    @property
    def e(self):
        """shortcut to QalxJob().entity"""
        return self.entity

    @property
    def s(self):
        """shortcut to QalxJob().session"""
        return self.session

    @property
    def queue(self):
        """shortcut to the queue instance on the bot entity"""
        return self.session.queue.get_by_name(
            self._bot_entity.config.queue_name
        )

    def stop_processing(self):
        """
        Stop the worker from processing.  Will cause the worker to wait until
        it receives a `resume` signal
        """
        self.worker_adapter.stop(
            entity=self._worker_entity, bot_entity=self._bot_entity
        )

    def resume_processing(self):
        """
        Resume the worker.
        """
        self.worker_adapter.resume(
            entity=self._worker_entity, bot_entity=self._bot_entity
        )

    def terminate(self, warm=True, requeue_job=False):
        """
        The job has been told to terminate the worker

        :param warm: If True will completely finish running through the
                     processes for the current job.  If False will exit as soon
                     as the current process function is complete
        :type warm: bool
        :param requeue_job: Should the job be requeued if we are terminating
                            with `warm=False`
        :type requeue_job: bool
        """
        self.worker_adapter.terminate(
            entity=self._worker_entity,
            bot_entity=self._bot_entity,
            warm=warm,
            requeue_job=requeue_job,
        )

    def publish_status(self, status):
        """update the status of the worker

        :param status: short message about the worker status
        :type status: str
        """
        self.worker_adapter.update_status(
            entity=self._worker_entity,
            bot_entity=self._bot_entity,
            status=status,
        )

    def add_step_result(self, success=True):
        """indicate success or failure of the step function

        :param success: was the step successful or not
        :type success: bool
        """
        self._step_results[self._current_step] = success

    @property
    def last_step_result(self):
        """
        The success flag for the previous step result (or None if no previous
        steps) for this job
        """
        if self._step_results:
            return self._step_results[list(self._step_results)[-1]]
        else:
            return None

    def get_entity(self, entity_type, entity_guid):
        """
        get an entity

        :param entity_type: the type of entity e.g. item, set, group
        :type entity_type: str
        :param entity_guid: the guid of the entity
        :type entity_guid: str
        :return:    a child of :class:`~pyqalx.core.entities.entity.QalxEntity`
                    if the entity is found on the API, otherwise None
        """
        adapter = getattr(self.session, entity_type)
        self.entity_adapter = adapter
        try:
            self.entity = adapter.get(entity_guid, config=self.session.config)
        except QalxAPIResponseError:
            self.log.error(
                f"The {entity_type} with guid {entity_guid} was not found"
                + " on qalx. This probably means that it was manually "
                + f"deleted. The {entity_type} was not processed and the "
                + "message will be deleted from the queue."
            )
            self.delete_message()
            self.entity = None
        return self.entity

    def add_item_data(self, item_key, data, meta=None):
        """
        helper method to add item data to the set

        :param item_key: key on the set to add the item as
        :type item_key: str
        :param data: data to add
        :type data: dict
        :param meta: metadata to add
        :type meta: dict

        :return: The specific :class:`~pyqalx.core.entities.item.Item` instance
                 that has been added
        """
        if not (self.entity.entity_type == "set"):
            raise TypeError(
                "Method add_item_data only works on jobs with a set entity."
            )
        self.entity.items_[item_key] = self.session.item.add(
            data=data, meta=meta
        )
        self.save_entity()
        return self.entity.items_[item_key]

    def save_entity(self):
        """
        Updates the API representation of this entity with the data
        currently stored in the job.

        :return: a child of :class:`~pyqalx.core.entities.entity.QalxEntity` of
                 the correct type based on the type of `self.entity`
        """
        # Always ensure that the entity on the adapter is fully up to date
        # with the entity on the job.
        self.entity_adapter.save(entity=self.entity)
        return self.entity

    def reload_entity(self):
        """
        Reloads `self.entity` from the API

        :return: a child of :class:`~pyqalx.core.entities.entity.QalxEntity` of
                 the correct type based on the type of `self.entity`
        """
        # Always ensure that the entity on the adapter is fully up to date
        # with the entity on the job.
        self.entity = self.entity_adapter.reload(entity=self.entity)
        return self.entity

    def delete_message(self):
        """
        Helper method for deleting a message from a Queue
        """
        return self._process._delete_message()


class Bot:
    """
    Bots allow automation of tasks.  A bot reads messages from a
    :class:`~pyqalx.core.entities.queue.Queue` and processes the response
    through user configured `step_functions`.
    """

    __slots__ = (
        "name",
        "queue_name",
        "initialisation_function",
        "begin_function",
        "preload_function",
        "onload_function",
        "preprocess_function",
        "process_function",
        "precompletion_function",
        "postprocess_function",
        "onwait_function",
        "ontermination_function",
        "bot_entity",
        "bot_adapter",
        "qalx_session_class",
        "user_config_class",
        "bot_config_class",
        "entity_classes",
        "workflow",
    )

    def __init__(self, bot_name):
        """
        :param bot_name: The unique name for this bot
        :type bot_name: str
        """
        self.name = bot_name

        # bot lifecycle functions
        self.initialisation_function = do_nowt_right
        self.begin_function = do_nowt
        self.preload_function = do_nowt
        self.onload_function = do_nowt
        self.preprocess_function = do_nowt

        # Use `partial` so we can ensure the name of the function always goes
        # to the exception.
        self.process_function = partial(
            cannot_be_undefined, step_name=self.process.__name__
        )
        self.precompletion_function = do_nowt
        self.postprocess_function = do_nowt
        self.onwait_function = do_nowt
        self.ontermination_function = do_nowt

    def _collect_steps(self):
        steps = {}

        for fn in self.__dir__():
            if fn.endswith("_function"):
                fn_attr = getattr(self, fn)
                if fn_attr not in [do_nowt, do_nowt_right]:
                    if getattr(fn_attr, "func", None) == cannot_be_undefined:
                        # This function must be defined, call it to raise
                        # an exception pre fork.  Only functions using
                        # `partial` will have the `func` attr
                        fn_attr()
                    steps[fn] = dill.dumps(fn_attr)  # serialise functions
        return steps

    def start(
        self,
        queue_name,
        processes=1,
        qalx_session_class=None,
        user_config_class=None,
        bot_config_class=None,
        entity_classes=None,
        user_profile_name=UserConfig.default,
        bot_profile_name=BotConfig.default,
        skip_ini=False,
        stop=False,
        meta=None,
        workflow=None,
    ):
        """
        Starts the bot with `processes` number of :class:`~pyqalx.bot.Worker`
        instances.  Each worker will be able to read a message from the queue
        in parallel

        :param queue_name: The unique name for the queue
        :type queue_name: str
        :param qalx_session_class: The :class:`~pyqalx.core.session.QalxSession`
                                   class that this Bot and Workers should use
        :type qalx_session_class: pyqalx.core.session.QalxSession
        :param user_config_class: The :class:`~pyqalx.config.configs.UserConfig`
                                  class that will be used when creating the Bot
        :type user_config_class: pyqalx.config.configs.UserConfig
        :param bot_config_class: The :class:`~pyqalx.config.configs.BotConfig`
                                 class that will be used when using the bot session
        :type bot_config_class: pyqalx.config.configs.BotConfig
        :param entity_classes: A list of
                               :class:`~pyqalx.core.entities.entity.QalxEntity`
                               subclasses that you want this Bot to use once
                               it is started
        :type entity_classes: list
        :param user_profile_name: The user profile name that will be used when
                                  creating the Bot
        :type user_profile_name: str
        :param bot_profile_name: The bot profile name that will be used when
                                 using the bot session
        :type bot_profile_name: str
        :param skip_ini: Should reading from the `ini` file be skipped when
                         instantiating the user and bot sessions
        :type skip_ini: bool
        :param processes: The number of :class:`~pyqalx.bot.Worker` processes
                          this bot should spawn
        :type processes: int
        :param stop:    Should the bot be stopped right after startup. This is
                        essential functionality during factory building
        :type  stop:    bool
        :param meta:        Metadata to be saved on the bot. Optional parameter
        :type  meta:        dict
        :param workflow:    An iterable of other bots that defines the
                            interaction of the bot with other bots in the
                            context of a workflow
        :type  workflow:    list
        """

        self.queue_name = queue_name
        # This is needed for starting outside the CLI
        workflow = workflow or []
        if not isinstance(workflow, list) or not all(
            [isinstance(_, str) for _ in workflow]
        ):
            raise QalxError(
                "Workflow argument must be an iterable containing strings"
            )
        self.workflow = workflow

        if entity_classes is None:
            entity_classes = []

        if qalx_session_class is None:
            qalx_session_class = QalxSession

        user_session = qalx_session_class(
            profile_name=user_profile_name,
            config_class=user_config_class,
            skip_ini=skip_ini,
        )

        if bot_config_class is None:
            bot_config_class = BotConfig

        # This configures logging to use the config settings specified
        # on the bot
        bot_session = qalx_session_class(
            profile_name=bot_profile_name,
            config_class=bot_config_class,
            skip_ini=skip_ini,
        )
        queue = user_session.queue.get_or_create(name=self.queue_name)
        # Add the queue_name - this makes it easier to find bots looking at
        # specific queues. Also add the `_region` in case the queue gets
        # reloaded by the worker (which will be using the `bot_session`)
        bot_session.config.update(
            {"queue_name": self.queue_name, "REGION": queue._region}
        )
        # Log all the user and bot session config values for debugging
        for session, title in zip((user_session, bot_session), ("user", "bot")):
            session.log.debug(f"-vvv- Config values for {title} session -vvv-")
            for k, v in session.config.items():
                if k != "TOKEN":
                    session.log.debug(f"{k}: {v}")
            session.log.debug(f"-^^^- Config values for {title} session -^^^-")
        self.bot_entity = user_session.bot.add(
            name=self.name, config=bot_session.config, meta=meta
        )

        self.bot_adapter = bot_session.bot

        self._register_entities(entity_classes)

        if self.initialisation_function:
            init_result = self.initialisation_function(user_session)
            bot_session.log.debug(
                f"Initialisation function returns `{init_result}`"
            )
            if not init_result:
                raise QalxBotInitialisationFailed(
                    "The initialisation function returned a False-like value."
                )
        steps = self._collect_steps()

        # Update the token on the bot_session to ensure all subsequent
        # requests use the token from the bot
        token = self.bot_entity.info.credentials.token
        bot_session.rest_api.token = token

        self.bot_entity = self.bot_adapter.replace_workers(
            bot_entity=self.bot_entity, workers=processes
        )
        if stop is True:
            self.bot_adapter.stop(self.bot_entity)
        workers = []
        # We use the same session and adapter for all workers

        worker_adapter = QalxWorker(session=self.bot_adapter.session)

        for worker in range(processes):
            workers.append(
                Worker(
                    steps,
                    queue,
                    self.bot_entity,
                    self.bot_entity.workers[worker],
                    worker_adapter,
                    index=worker,
                    workflow=self.workflow,
                )
            )
            bot_session.log.debug(
                f"Created worker `{worker}` to read from `{self.queue_name}`"
            )
        for p in workers:
            p.start()
        for p in workers:
            p.join()
        bot_session.log.debug("Workers joined.")

    def _register_entities(self, entity_classes):
        """
        Registers `self.entity_classes` for this Bots session
        """
        for entity_class in entity_classes:
            self.bot_adapter.session.register(entity_class)

    def initialisation(self, func):
        """decorator to to register the initialisation

        `initialisation` is executed with a QalxSession instance
        authenticated againt the `user_config_class` __init__ argument
        :param func: function to be executed
        """
        self.initialisation_function = func

    def begin(self, func):
        """decorator to to register the begin

        `begin` is executed with a QalxJob instance

        :param func: function to be executed
        """
        self.begin_function = func

    def preload(self, func):
        """decorator executed before entity is loaded from qalx.

        `preload` is executed with a QalxJob instance

        :param func: function to be executed
        """
        self.preload_function = func

    def onload(self, func):
        """decorator to register the onload

        `onload` is executed with a QalxJob instance

        :param func: function to be executed
        """
        self.onload_function = func

    def preprocess(self, func):
        """decorator to register preprocess function

        `preprocess` is executed with a QalxJob instance

        :param func: function to register
        """
        self.preprocess_function = func

    def process(self, func):
        """decorator to register process function

        `process` is executed with a QalxJob instance

        :param func: function to register
        """
        self.process_function = func

    def precompletion(self, func):
        """decorator to register precompletion function

        `precompletion` is executed with a QalxJob instance

        :param func: function to register
        """
        self.precompletion_function = func

    def postprocess(self, func):
        """decorator to register postprocess function

        `postprocess` is executed with a QalxJob instance

        :param func: function to register
        """
        self.postprocess_function = func

    def onwait(self, func):
        """decorator to register onwait function

        `onwait` is executed with a QalxJob instance

        :param func: function to register
        """
        self.onwait_function = func

    def ontermination(self, func):
        """decorator to register ontermination function

        `ontermination` is executed with a QalxJob instance

        :param func: function to register
        """
        self.ontermination_function = func


class Worker(Process):
    """

    exit codes (start at 72590):

        - 72590 base exit code
        - 72591 warm exit
        - 72592 cold exit
        - 72593 config triggered (e.g. KILL_AFTER)
    """

    def __init__(
        self,
        steps,
        queue,
        bot_entity,
        api_entity,
        worker_adapter: QalxWorker,
        index,
        workflow,
        **kwargs,
    ):
        super(Worker, self).__init__(**kwargs)
        self._steps = steps
        self.queue = queue
        self.bot_entity = bot_entity
        self.api_entity = api_entity
        self.worker_adapter = worker_adapter
        self.session = self.worker_adapter.session
        # Reinitialise the session due to mulitprocessing
        # https://github.com/psf/requests/issues/4323
        self.session.rest_api._initialise_session()

        self.log = None
        self.queue_adapter = QalxQueue(session=self.session)
        self.bot_adapter = QalxBot(session=self.session)
        self.stop = False
        self.config = self.session.config
        self.index = index
        self.workflow = workflow
        self.worker_signal = None

    def configure_logging(self):
        """
        Configures the log for the Worker. Each Worker logs to its own
        file. This prevents issues with multiple processes trying to write
        to the same file
        """
        directory = self.config["WORKER_LOG_FILE_DIR"]
        level = self.config["LOGGING_LEVEL"]
        filename = os.path.join(
            directory, f".worker_{self.bot_entity.name}.{self.index}.log"
        )
        self.log = configure_logging(f"worker.{self.index}", filename, level)

    def _reload_signal(self):
        """
        Helper method for reloading the signal for this worker
        """
        self.worker_signal = self.worker_adapter.get_signal(
            self.api_entity, bot_entity=self.bot_entity
        )

    def _check_worker_signal(self):
        """
        Reload the worker signal and either terminates the worker or sets the
        stop flag so that the worker can stop processing the next time
        `self._continue_processing` is checked
        """
        # The first time the bot starts the signal won't be set yet unless the
        # bot itself was started with `stop=True` (i.e. when building factories)
        stopped_status = getattr(self.worker_signal, "stop", False)

        # Once we've reloaded the signal we can decide what needs to be done
        # with the bot
        self._reload_signal()

        if self.worker_signal.terminate_warm:
            self._do_exit(**QalxSignal._warm_exit_update())
        else:
            if self.worker_signal.stop != stopped_status:
                # The worker stop signal has changed state - log it so the user
                # knows what's going on
                update = QalxSignal._stop_or_resume_update(
                    stop=self.worker_signal.stop
                )
                self.log.info(f'[{update["code"]}] {update["update"]}')
            self.stop = self.worker_signal.stop

    def _do_exit(self, update, code=QalxSignal.BASE_EXIT_CODE):
        self.job._current_step = "OnTerminate"
        onterm = self.steps.get("ontermination_function")
        if onterm:
            onterm(self.job)
        self.job.publish_status(update)
        self.log.info(f"[{code}] {update}")
        sys.exit(code)

    def _check_cold_exit(self, reload_signal=True):
        """
        Reloads the worker signal and checks whether we should do a cold
        termination
        """
        if reload_signal:
            self._reload_signal()

        if self.worker_signal.terminate_cold:
            # The worker has been asked to cold exit for some reason.
            # Check if the job needs to go back on the queue or if we can
            # delete it
            if self.job._queue_message:
                if self.worker_signal.requeue_job:
                    self.job._queue_message._stop_heartbeat()
                else:
                    self._delete_message()
            self._do_exit(**QalxSignal._cold_exit_update())

    def _check_warm_exit(self):
        """
        Reloads the worker signal and checks whether we should do a warm
        termination
        """
        self._reload_signal()

        if self.worker_signal.terminate_warm:
            # The worker has been asked to warm exit for some reason.
            # The job will have finished and the message should have been
            # deleted.
            self._do_exit(**QalxSignal._warm_exit_update())

    def _workflow(self):
        """
        Workflow step function. Used to handle passing a job to multiple bots
        once all step functions have been completed on the worker
        """
        self.log.debug("Attempting worklow")
        factory_namespace_key = Factory.PYQALX_METADATA_NAMESPACE_KEY
        factory_guid_key = Factory.PYQALX_METADATA_FACTORY_GUID_KEY
        factory_plan_bot_name_key = Factory.PYQALX_METADATA_PLAN_BOT_NAME_KEY
        factory_guid = self.bot_entity.meta.get(factory_namespace_key, {}).get(
            factory_guid_key, None
        )
        for bot_name in self.workflow:
            self.log.debug(
                f"Workflow found." f"Next bot in workflow: `{bot_name}`"
            )
            # By default, just try and find the bot based on the name
            query = {"name": bot_name}
            if factory_guid is not None:
                # If it's a factory bot then we need to use the plan_bot_name
                # and the factory_guid, as the actual bot_name won't be known
                # when the factory was built
                pyqalx_query = f"metadata.data.{factory_namespace_key}"
                query = {
                    "metadata.data._class": "pyqalx.factory",
                    f"{pyqalx_query}.{factory_plan_bot_name_key}": bot_name,
                    f"{pyqalx_query}.{factory_guid_key}": factory_guid,
                }
            try:
                bot = self.session.bot.find_one(query=query)
            except (QalxMultipleEntityReturned, QalxEntityNotFound) as exc:
                warn_msg = (
                    f"There was an error retrieving one bot "
                    f"for `{bot_name}` in the defined workflow. "
                    f"Query was `{query}`: `{exc}`"
                )
                self.log.warning(warn_msg)
                continue
            queue = self.session.queue.get_by_name(name=bot.config.queue_name)
            self.log.debug(
                f"Submitting `{self.job.entity}` "
                f"to `{queue.name}` on workflow bot"
                f" name `{bot_name}`"
            )
            self.job.entity.add_to_queue(self.job.entity, queue)

    def _delete_message(self):
        """
        Helper function for stopping any heartbeat on the job and
        deleting the message
        """
        if getattr(self.job, "_queue_message", None):
            self.queue.delete_message(self.job._queue_message)

    def _wait_with_spreading(self, spread_factor):
        """
        We want to wait for a while before trying something again and wait
        longer and longer every time up to a maximum. This is to help limit the
        request count to qalx while staying responsive.

        :return: the next spreading factor to use
        """

        time_to_wait = self.config["Q_WAITTIMESECONDS"]
        max_spreading = self.config["Q_WAITTIMEMAXSPREADING"]
        self.job._queue_message = None
        self.job._current_step = "OnWait"
        if self.steps.get("onwait_function") is not None:
            self.steps["onwait_function"](self.job)
        total_wait_seconds = time_to_wait * spread_factor
        sleep(total_wait_seconds)
        self.log.debug(f"wait for {total_wait_seconds}s")
        self._check_worker_signal()
        self._check_cold_exit(reload_signal=False)  # we reloaded in prev line
        next_spread = spread_factor + 1
        # never spread beyond a max factor
        return min(max_spreading, next_spread)

    def _continue_processing(self):
        if self.job.last_step_result is not None:
            return (not self.stop) and self.job.last_step_result
        else:
            return not self.stop

    def _check_queue_credentials(self):
        """
        Checks the security token expiration timestamp on the queue and
        refreshes it if necessary
        """
        if self.queue._credentials_expiring_soon():
            self.log.debug(
                f"refreshing security credentials for queue "
                f"`{self.queue.name}`"
            )
            self.queue = self.queue_adapter.reload(self.queue)

    def _run_functions(self):
        # Each worker has its own dedicated log
        self.job = QalxJob(self)
        _startup = True
        # avoid pickle errors
        self.steps = {}
        for f_name, f_dill in self._steps.items():  # de-serialise functions
            self.log.debug(f"try to undill step `{f_name}`")
            try:
                self.steps[f_name] = dill.loads(f_dill)
            except TypeError:
                self.steps[f_name] = f_dill

        self.log.debug("running")
        if self.steps.get("begin_function"):
            self.job._current_step = "Begin"

            self.steps.get("begin_function")(self.job)
            self._check_worker_signal()
            self._check_cold_exit(reload_signal=False)

        kill_after = self.config["KILL_AFTER"]
        spread_factor = 1
        no_message_attempts = 0
        # Checks the worker signal in case the bot is started in a "stopped"
        # state
        self._check_worker_signal()

        while True:
            # Check if the credentials need refreshing. They may have expired
            # due to `_wait_with_spreading` or for another machine related
            # issue (i.e. machine hibernate)
            self._check_queue_credentials()
            if self.stop:
                spread_factor = self._wait_with_spreading(spread_factor)
                self.log.debug(
                    f"Stop signal on Worker waited with factor {spread_factor}"
                )
            else:
                q_msgs = self.queue_adapter.get_messages(worker=self)
                self.log.debug(f"got {len(q_msgs)} messages")
                if q_msgs:
                    for q_msg in q_msgs:
                        if not _startup:
                            self.job = QalxJob(self)
                        _startup = False
                        self.job._queue_message = q_msg
                        self.log.debug(f"process {q_msg.body}")
                        self._process_functions()
                        self._check_worker_signal()
                    no_message_attempts = 0  # reset the attempt counter
                    spread_factor = 1  # reset any wait spreading
                else:
                    spread_factor = self._wait_with_spreading(spread_factor)
                    no_message_attempts += 1

            if (kill_after is not None) and (no_message_attempts >= kill_after):
                self._do_exit(**QalxSignal._config_exit_update())

    def _process_functions(self):
        def process_as_far_as_possible(functions):
            for fn, step_name in functions:
                if self._continue_processing():
                    self.job._current_step = step_name
                    try:
                        # Update bot and worker states here so that the state is correct
                        # after a `resume` signal is sent
                        self.worker_adapter.update_state(
                            self.api_entity,
                            ValidStates.ACTIVE,
                            bot_entity=self.bot_entity,
                        )
                        self.bot_adapter.update_state(
                            self.bot_entity, ValidStates.ACTIVE
                        )
                        fn(self.job)
                    except Exception:
                        # This needs to be a bare exception to handle
                        # something going wrong with the user defined functions
                        _, exc_value, exc_traceback = sys.exc_info()
                        # Send as a `QalxError` to our handler otherwise we
                        # risk consuming exceptions from the users application
                        exception_hook(
                            exc_type=QalxError,
                            exc_value=exc_value,
                            exc_traceback=exc_traceback,
                            extra={
                                "entity_guid": self.job.entity.guid,
                                "entity_type": self.job.entity.entity_type,
                            },
                            log=self.log,
                        )

                    # check if we need to cold exit after every function
                    self._check_cold_exit()
                    if self.config["SAVE_INTERMITTENT"]:
                        self.job.save_entity()
                else:
                    break
            # Processing discontinued due to stop signal, failed step
            # function or completing processing
            self.worker_adapter.update_state(
                self.api_entity,
                ValidStates.IDLE,
                bot_entity=self.bot_entity,
            )
            if ValidStates.ACTIVE.value not in [
                worker.state for worker in self.bot_entity.workers
            ]:
                self.bot_adapter.update_state(self.bot_entity, ValidStates.IDLE)
            if not self.config["SKIP_FINAL_SAVE"]:
                self.job.save_entity()
            # `_workflow` is executed only if the flag on the job entity is True
            if self.job.do_workflow is True:
                self._workflow()
            # We delete the message from the queue once we've processed it
            self._delete_message()
            return self.job

        # PreLoad
        if self.steps.get("preload_function"):
            self.job._current_step = "PreLoad"
            self.steps.get("preload_function")(self.job)
            self._check_cold_exit()
        if self._continue_processing():
            # Process steps
            steps = (
                "OnLoad",
                "PreProcess",
                "Process",
                "PreCompletion",
                "PostProcess",
            )
            process_functions = [
                (self.steps.get(f"{s.lower()}_function"), s)
                for s in steps
                if self.steps.get(f"{s.lower()}_function")
            ]

            entity_type = self.job._queue_message.body["entity_type"]
            entity_guid = self.job._queue_message.body["entity_guid"]
            if self.job.get_entity(entity_type, entity_guid):
                process_as_far_as_possible(process_functions)
        else:
            self._delete_message()

    def run(self):
        """
        Run our custom functions.  Catch any exception
        that may occur with it and pass that to our custom
        uncaught exception handler
        """
        # This is the earliest the log can be configured to avoid
        # pickling issues on windows.  Any logging before this needs
        # to be done using a QalxSession#log instance
        self.configure_logging()
        try:
            self._run_functions()
        except Exception:
            # This needs to be a bare exception to handle something going
            # wrong with the Worker
            _, exc_value, exc_traceback = sys.exc_info()
            # Send as a `QalxError` to our handler otherwise we
            # risk consuming exceptions from the users application
            exception_hook(
                exc_type=QalxError,
                exc_value=exc_value,
                exc_traceback=exc_traceback,
                log=self.log,
            )
