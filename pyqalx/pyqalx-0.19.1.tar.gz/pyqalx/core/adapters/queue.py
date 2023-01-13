from pyqalx.core.adapters.adapter import QalxNamedEntityAdapter
from pyqalx.core.entities import Queue


class QalxQueue(QalxNamedEntityAdapter):
    """
    Provides an interface for accessing the API for
    :class:`~pyqalx.core.entities.queue.Queue` entities
    """

    _entity_class = Queue
    _bot_only_methods = ["get_messages"]

    @property
    def _queue_params(self):
        """
        The configurable parameters for a `Queue`
        :return:
        """
        return {"VisibilityTimeout": self.session.config["MSG_BLACKOUTSECONDS"]}

    def add(self, name, meta=None, **kwargs):
        """
        Queues are created with a name.  This name is stored in the metadata
        of the `Queue` instance

        :param name: The name we want to assign the Queue
        :type name: str
        :param meta: A dictionary of metadata to store
        :type meta: dict
        :param kwargs: Any other kwargs we are setting on the Queue
        :return: A newly created :class:`~pyqalx.core.entities.queue.Queue` instance
        """
        return super(QalxQueue, self).add(
            parameters=self._queue_params, name=name, meta=meta, **kwargs
        )

    def get_messages(self, worker):
        """
        Gets the messages on the `Queue` instance

        :param worker:An instance of :class:`~pyqalx.core.entities.worker.Worker`
                      that called this method

        :return: A list of :class:`~pyqalx.core.entities.queue.QueueMessage` instances
        """
        config = self.session.config
        max_msgs = config["Q_MSGBATCHSIZE"]
        visibility = config["MSG_BLACKOUTSECONDS"]
        waittime = config["MSG_WAITTIMESECONDS"]

        message = worker.queue.get_messages(
            max_num_msg=max_msgs,
            visibility=visibility,
            waittime=waittime,
            worker=worker,
        )
        return message

    def get_by_name(self, name, **kwargs):
        """a single queue by name

        :param name: name of queue
        :type name: str
        :return: :class:`~pyqalx.core.entities.queue.Queue`
        :raises QalxMultipleEntityReturned:
        :raises QalxEntityNotFound:
        """
        return super(QalxQueue, self).get_by_name(name, **kwargs)

    def get_or_create(self, name, meta=None, **kwargs):
        """
        Gets a Queue by the given name or creates it if it doesn't exist

        :param name:
        :type name: str
        :param meta: metadata about the queue
        :type meta: dict
        :return: :class:`~pyqalx.core.entities.queue.Queue`
        """
        return super(QalxQueue, self).get_or_create(name, meta=meta)

    def get(self, guid, *args, **kwargs):
        # extended to create better autodocs
        return super(QalxQueue, self).get(guid, *args, **kwargs)

    def save(self, entity, *args, **kwargs):
        # extended to create better autodocs
        return super(QalxQueue, self).save(entity, *args, **kwargs)

    def find(
        self,
        query=None,
        sort=None,
        skip=0,
        limit=25,
        many=True,
        include_session_tags=True,
        **kwargs
    ):
        # extended to create better autodocs
        return super(QalxQueue, self).find(
            query=query,
            sort=sort,
            skip=skip,
            limit=limit,
            many=many,
            include_session_tags=include_session_tags,
            **kwargs
        )

    def find_one(self, query, **kwargs):
        # extended to create better autodocs
        return super(QalxQueue, self).find_one(query=query, **kwargs)

    def reload(self, entity, *args, **kwargs):
        # extended to create better autodocs
        return super(QalxQueue, self).reload(entity=entity, **kwargs)

    def aggregate(self, aggregate, **kwargs):
        # extended to create better autodocs
        return super(QalxQueue, self).aggregate(aggregate=aggregate, **kwargs)
