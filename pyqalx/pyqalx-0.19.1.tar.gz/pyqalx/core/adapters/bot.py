from pyqalx.core.adapters.adapter import (
    QalxNamedEntityAdapter,
    QalxUpdateStatusAdapter,
    QalxUpdateStateAdapter,
)
from pyqalx.core.entities import Bot
from pyqalx.core.enums import ValidStates


class QalxBot(
    QalxNamedEntityAdapter, QalxUpdateStatusAdapter, QalxUpdateStateAdapter
):
    """
    Provides an interface for accessing the API for
    :class:`~pyqalx.core.entities.bot.Bot` entities
    """

    _entity_class = Bot
    _user_only_methods = ["add"]
    _bot_only_methods = ["replace_workers"]

    def add(self, name, config, meta=None, **kwargs):
        """
        Creates a `Bot` instance.

        :param name: The name that this bot will be given
        :type name: str
        :param config: The bots config
        :type config: dict
        :param meta: A dictionary of metadata to store
        :type meta: dict
        :return: The newly created :class:`~pyqalx.core.entities.bot.Bot` instance
        """
        return super(QalxBot, self).add(
            host=self.session._host_info,
            name=name,
            meta=meta,
            config=config,
            **kwargs,
        )

    def get_by_name(self, name, **kwargs):
        # extended to create better autodocs
        return super(QalxBot, self).get_by_name(name=name, **kwargs)

    def get_or_create(self, name, meta=None, **kwargs):
        # extended to create better autodocs
        return super(QalxBot, self).get_or_create(
            name=name, meta=meta, **kwargs
        )

    def get(self, guid, *args, **kwargs):
        # extended to create better autodocs
        return super(QalxBot, self).get(guid, *args, **kwargs)

    def save(self, entity, *args, **kwargs):
        # extended to create better autodocs
        return super(QalxBot, self).save(entity, *args, **kwargs)

    def find(
        self,
        query=None,
        sort=None,
        skip=0,
        limit=25,
        many=True,
        include_session_tags=True,
        **kwargs,
    ):
        # extended to create better autodocs
        return super(QalxBot, self).find(
            query=query,
            sort=sort,
            skip=skip,
            limit=limit,
            many=many,
            include_session_tags=include_session_tags,
            **kwargs,
        )

    def find_one(self, query, **kwargs):
        # extended to create better autodocs
        return super(QalxBot, self).find_one(query=query, **kwargs)

    def reload(self, entity, *args, **kwargs):
        # extended to create better autodocs
        return super(QalxBot, self).reload(entity=entity, **kwargs)

    def aggregate(self, aggregate, **kwargs):
        # extended to create better autodocs
        return super(QalxBot, self).aggregate(aggregate=aggregate, **kwargs)

    def replace_workers(self, bot_entity, workers):
        """
        Completely replaces any Workers on the given bot.  Will return the
        replaced workers in an unpacked state

        :param bot_entity: The Bot instance that is being changed
        :type bot_entity: :class:`~pyqalx.core.entities.bot.Bot`
        :param workers: The number of workers that this bot should have
        :type workers: int
        :return: A :class:`~pyqalx.core.entities.bot.Bot` instance with
                 the updated workers
        """
        guid = bot_entity["guid"]
        detail_endpoint = self.detail_endpoint(guid=guid)
        endpoint = f"{detail_endpoint}/replace-workers"
        self.session.log.debug(
            f"replace workers on `{self.entity_class.entity_type}` with"
            f" guid `{guid}` with `/{endpoint}`"
        )

        resp = self._process_api_request("patch", endpoint, workers=workers)
        return self._process_api_response(resp)

    def _signal_workers(self, entity, signal_method, *args, **kwargs):
        """
        Helper method for calling signals on workers.  A bot doesn't have
        the concept of `signals`.  Instead, we call a signal method we just
        apply this to all the workers on the bot
        """

        for worker in entity.get("workers", []):
            worker_method = getattr(self.session.worker, signal_method)
            worker_method(worker, bot_entity=entity, *args, **kwargs)

    def stop(self, entity, **kwargs):
        """
        Stops all the workers on the bot

        :param entity: Bot instance
        :type entity: :class:`~pyqalx.core.entities.bot.Bot`
        """
        self.update_state(entity, ValidStates.STOPPED)
        self._signal_workers(entity, signal_method="stop", **kwargs)

    def resume(self, entity, **kwargs):
        """
        Resumes all the workers on the bot

        :param entity: Bot instance
        :type entity: :class:`~pyqalx.core.entities.bot.Bot`
        """
        # Update to `idle` - if there are extant jobs the state will be
        # updated to active by the worker at the next process function
        self.update_state(entity, ValidStates.IDLE)
        self._signal_workers(entity, signal_method="resume", **kwargs)

    def terminate(self, entity, *args, **kwargs):
        """
        Terminates all the workers on the bot

        :param entity: Bot instance
        :type entity: :class:`~pyqalx.core.entities.bot.Bot`
        """
        self.update_state(entity, ValidStates.TERMINATED)
        self._signal_workers(entity, signal_method="terminate", *args, **kwargs)

    def update_status(self, entity, status, **kwargs):
        # extended to create better autodocs
        return super(QalxBot, self).update_status(
            entity=entity, status=status, **kwargs
        )
