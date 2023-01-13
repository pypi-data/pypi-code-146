from pyqalx.core.adapters.adapter import (
    QalxSignalAdapter,
    QalxUpdateStatusAdapter,
    QalxUpdateStateAdapter,
)
from pyqalx.core.entities.worker import Worker
from pyqalx.core.enums import ValidStates
from pyqalx.core.signals import QalxWorkerSignal


class QalxWorker(
    QalxSignalAdapter, QalxUpdateStatusAdapter, QalxUpdateStateAdapter
):
    """
    Provides an interface for accessing the API for
    :class:`~pyqalx.core.entities.worker.Worker` entities
    """

    _entity_class = Worker
    signal_class = QalxWorkerSignal

    def _process_api_request(self, *args, **kwargs):
        """
        Ensures that the `bot_entity` kwarg doesn't get sent to the API. This
        variable will have been passed down through kwargs from any endpoint
        method and is required for building the urls for a worker
        """
        # `bot_entity` may not be in kwargs anymore if we are calling
        # `_process_api_request` twice (i.e. when getting a list of workers)
        kwargs.pop("bot_entity", None)
        return super(QalxWorker, self)._process_api_request(*args, **kwargs)

    def list_endpoint(self, *args, bot_entity, **kwargs):
        """
        Builds the list_endpoint for workers.  This requires the bot_entity
        which will get passed down from the calling method via kwargs.
        :param bot_entity:An instance of Bot
        :type bot_entity:~entities.bot.Bot
        :return:The Worker list endpoint
        """
        bot_endpoint = self.session.bot.detail_endpoint(guid=bot_entity["guid"])
        return f"{bot_endpoint}/{self.entity_class.entity_type}"

    def detail_endpoint(self, guid, *args, bot_entity, **kwargs):
        """
        Builds the detail_endpoint for workers.  This requires the bot_entity
        which will get passed down from the calling method via kwargs.

        :param guid: The guid of the Worker
        :type guid: `uuid`
        :param bot_entity: An instance of Bot
        :type bot_entity: ~pyqalx.core.entities.bot.Bot
        :return: The Worker list endpoint
        """
        bot_endpoint = self.list_endpoint(bot_entity=bot_entity)
        return f"{bot_endpoint}/{guid}"

    def get(self, guid, bot_entity, *args, **kwargs):
        """
        Gets an individual worker.

        :param guid: The guid of the Worker
        :type guid: `uuid`
        :param bot_entity: An instance of Bot
        :type bot_entity: ~pyqalx.core.entities.bot.Bot
        :return: :class:`~pyqalx.core.entities.worker.Worker`
        """
        return super(QalxWorker, self).get(
            guid, bot_entity=bot_entity, *args, **kwargs
        )

    def get_signal(self, entity, bot_entity, *args, **kwargs):
        """
        Gets the signal for a specific entity

        :param entity: An instance of Worker
        :type entity: ~pyqalx.core.entities.worker.Worker
        :param bot_entity: An instance of Bot
        :type bot_entity: ~pyqalx.core.entities.bot.Bot
        :return: :class:`~pyqalx.core.signals.QalxWorkerSignal`
        """
        return super(QalxWorker, self).get_signal(
            entity=entity, bot_entity=bot_entity, *args, **kwargs
        )

    def terminate(self, entity, bot_entity, *args, **kwargs):
        """
        Terminates a specific entity

        :param entity: An instance of Worker
        :type entity: ~pyqalx.core.entities.worker.Worker
        :param bot_entity: An instance of Bot
        :type bot_entity: ~pyqalx.core.entities.bot.Bot
        """
        self.update_state(entity, ValidStates.TERMINATED, bot_entity=bot_entity)
        return super(QalxWorker, self).terminate(
            entity=entity, bot_entity=bot_entity, *args, **kwargs
        )

    def _stop_or_resume(self, entity, stop, bot_entity, **kwargs):
        """
        Stops or resumes a specific entity

        :param entity: An instance of Worker
        :type entity: ~pyqalx.core.entities.worker.Worker
        :param stop: Whether we should stop or resume
        :type stop: bool
        :param bot_entity: An instance of Bot
        :type bot_entity: ~pyqalx.core.entities.bot.Bot
        """
        # Update to `idle` on a resume - if there are extant jobs the state
        # will be updated to active at the next process function
        state = ValidStates.STOPPED if stop else ValidStates.IDLE
        self.update_state(entity, state, bot_entity=bot_entity)
        return super(QalxWorker, self)._stop_or_resume(
            entity=entity, stop=stop, bot_entity=bot_entity, **kwargs
        )

    def reload(self, entity, bot_entity, **kwargs):
        """
        Reloads the current entity from the API

        :param entity: An instance of Worker
        :type entity: ~pyqalx.core.entities.worker.Worker
        :param bot_entity: An instance of Bot
        :type bot_entity: ~pyqalx.core.entities.bot.Bot
        :return: :class:`~pyqalx.core.entities.worker.Worker`
        """
        return super(QalxWorker, self).reload(
            entity=entity, bot_entity=bot_entity
        )

    def update_status(self, entity, bot_entity, status):
        """
        Updates the workers status

        :param entity: An instance of Worker
        :type entity: ~pyqalx.core.entities.worker.Worker
        :param bot_entity: An instance of Bot
        :type bot_entity: ~pyqalx.core.entities.bot.Bot
        :param status: The status to update to
        :type status: str
        """
        return super(QalxWorker, self).update_status(
            entity=entity, bot_entity=bot_entity, status=status
        )

    def stop(self, entity, bot_entity, **kwargs):
        """
        Sends a stop signal to the worker

        :param entity: An instance of Worker
        :type entity: ~pyqalx.core.entities.worker.Worker
        :param bot_entity: An instance of Bot
        :type bot_entity: ~pyqalx.core.entities.bot.Bot
        """
        return super(QalxWorker, self).stop(
            entity=entity, bot_entity=bot_entity, **kwargs
        )

    def resume(self, entity, bot_entity, **kwargs):
        """
        Sends a resume signal to the worker

        :param entity: An instance of Worker
        :type entity: ~pyqalx.core.entities.worker.Worker
        :param bot_entity: An instance of Bot
        :type bot_entity: ~pyqalx.core.entities.bot.Bot
        """
        return super(QalxWorker, self).resume(
            entity=entity, bot_entity=bot_entity, **kwargs
        )

    def save(self, entity, bot_entity, *args, **kwargs):
        """
        Saves the Worker instance

        :param entity: An instance of Worker
        :type entity: ~pyqalx.core.entities.worker.Worker
        :param bot_entity: An instance of Bot
        :type bot_entity: ~pyqalx.core.entities.bot.Bot
        :return: :class:`~pyqalx.core.entities.worker.Worker`
        """
        return super(QalxWorker, self).save(
            entity=entity, bot_entity=bot_entity, *args, **kwargs
        )
