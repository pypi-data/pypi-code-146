import json
import threading
from datetime import datetime, timezone
import uuid

import boto3
from botocore.exceptions import ClientError

from pyqalx.core.entities import QalxEntity, Group, Item, Set
from pyqalx.core.errors import QalxQueueError


class QueueResponse:
    """a response from a remote queue"""

    def __init__(self, response):
        """make new response

        :param response: response from queue
        """
        self._raw_response = response


class QueueMessage(threading.Thread):
    """a message from the queue.  subclasses `threading.Thread` so that a
    heartbeat can be started as soon as the message is received from the Queue
    """

    def __init__(self, message, worker, visibility, *args, **kwargs):
        """
        :param message: the full raw message from the queue
        :type message: dict
        :param worker: An instance of :class:~pyqalx.bot.Worker
        :type worker: ~pyqalx.bot.Worker
        :param visibility: How long should the heartbeat "beat" for (in seconds)?
        :type visibility: int
        """
        super(QueueMessage, self).__init__(*args, **kwargs)
        self._raw_message = message
        self.body = json.loads(message["Body"])
        self.receipt_handle = message["ReceiptHandle"]

        # Set up the heartbeat event and start the thread.
        # This will "beat" every 50% of visibility seconds and increase
        # the visibility timeout of the message on the queue.
        self._heartbeats = 1
        self._heartbeat = threading.Event()
        self._worker = worker
        self._log = self._worker.log
        self._queue = self._worker.queue
        self._visibility = visibility
        # Start the threaded heartbeat as soon as we can to prevent
        # message timeouts expiring if it takes a while to start processing them
        self.start()

    def _stop_heartbeat(self):
        """
        Stops any heartbeat that might be mid beat.  At this point the message
        should be fully processed or the max visibility has been reached.
        """
        self._heartbeat.set()

    def _increase_visibility_timeout(self, visibility_timeout):
        """
        Helper for increasing the visibility timeout of this message.  If the
        timeout is set to > MAX_VISIBILITY_TIMEOUT an error will be logged and
        the timeout will be set to MAX_VISIBILITY_TIMEOUT
        :param visibility_timeout: The visibility timeout the message should
        have. This will set the timeout to be a total number of seconds from
        when the message first went in flight
        :type visibility_timeout: int
        """
        MAX_VISIBILITY_TIMEOUT = 43200  # 12 hours
        if visibility_timeout > MAX_VISIBILITY_TIMEOUT:
            # SQS doesn't recalculate the max timeout if it were to be given
            # a value greater than the maximum.
            visibility_timeout = MAX_VISIBILITY_TIMEOUT
            docs = "https://docs.qalx.net/queues#in-flight-maximum"
            msg = (
                f"Max visibility timeout of {MAX_VISIBILITY_TIMEOUT} reached."
                f"The job will go back onto the queue when "
                f"this timeout expires. See {docs} for more information. "
            )
            self._log.warning(msg)
            # Stop the heartbeat, it cannot be increased any further than
            # MAX_VISIBILITY_TIMEOUT.
            self._stop_heartbeat()

        try:
            self._queue.broker_client.change_message_visibility(
                QueueUrl=self._queue["info"]["queue_url"],
                ReceiptHandle=self.receipt_handle,
                VisibilityTimeout=visibility_timeout,
            )
        except ClientError as exc:
            # ClientError: There was an issue changing the visibility.
            #              This could be a networking issue or the message no
            #              longer exists on the queue
            self._log.debug(
                f"Received ClientError when extending heartbeat."
                f"  Error was: `{exc}`"
            )
            # Not ideal but the only way to determine from the response
            # if the message is deleted.
            message_deleted = (
                "Message does not exist" in exc.response["Error"]["Message"]
            )

            if message_deleted:
                # The message was deleted from the queue.  The heartbeat should
                # have been stopped but if the user deleted the message in a
                # non standard way it may not have been.  Therefore, make
                # sure the heartbeat is stopped to prevent spamming the logs.
                self._stop_heartbeat()
            return False
        return True

    def run(self):
        """
        A QalxJob might take a long time to process.  Therefore, we
        use a heartbeat on the message to keep it in flight for as long
        as possible.  This runs in a Thread
        on :class:`~pyqalx.core.entities.queue.QueueMessage` instantiation
        to ensure that the message timeout doesn't expire before processing
        even begins (i.e. if a batch of messages was returned)

        As per the SQS docs `here
        <https://docs.aws.amazon.com/AWSSimpleQueueService
        /latest/SQSDeveloperGuide/sqs-visibility-timeout.html>`_

        This will specify the initial visibility timeout (for example, 2 minutes)
        and then — as long as your consumer still works on
        the message — keep extending the visibility timeout by 2
        minutes every minute.
        This uses `visibility` as the initial visibility timeout so every
        `visibility / 2` seconds will increase the timeout by
        `visibility * number of hearbeats` from the initial visibility time.
        """
        while self._heartbeat.is_set() is False:
            # We only do the heartbeat if it hasn't been set (meaning the
            # heartbeat was stopped due to message deletion)

            # Ensure it's an int - it might not be if it's come from the config
            if self._heartbeats != 1:
                # No need to change visibility on the first heartbeat as the
                # message will have the default timeout still.
                visibility_timeout = self._visibility * self._heartbeats

                success = self._increase_visibility_timeout(visibility_timeout)
                if not success:
                    # It wasn't successful, so just return without waiting the
                    # usual amount of time so that the thread can try again.
                    # Wait for a single second to help prevent multiple
                    # requests being fired to AWS
                    self._heartbeat.wait(1)
                    continue

            # Get roughly 50 percent of the default visibility time.
            # Sleep until that time expires and then increase the
            # message visibility the next time this method is called
            self._heartbeat.wait(self._visibility / 2)
            self._worker._check_queue_credentials()

            # We keep track of the number of heartbeats this message has had
            # and increase the timeout by `self._visibility * self._heartbeats`
            # for each heartbeat (after the first one)
            self._heartbeats += 1


class Queue(QalxEntity):
    """QalxEntity with entity_type Queue"""

    entity_type = "queue"

    @staticmethod
    def _stringify(message: dict) -> str:
        return json.dumps(message)

    def __init__(self, *args, **kwargs):
        super(Queue, self).__init__(*args, **kwargs)
        self._broker_client = None

    def _reserved_keys(self):
        reserved_keys = super(Queue, self)._reserved_keys()
        reserved_keys += ["_broker_client"]
        return reserved_keys

    @property
    def broker_client(self):
        """
        An authenticated client to communicate with the remote message broker.

        Windows can't pickle the client if it gets set on __init__ therefore,
        we set it to an internal attribute and cache it for the duration of
        the Queue to avoid getting the client multiple times
        """
        if (
            self._broker_client is None
            and hasattr(self, "info")
            and ("credentials" in self.info)
        ):

            _broker_client = boto3.client(
                "sqs",
                region_name=self._region,
                aws_access_key_id=self.info.credentials.ACCESS_KEY_ID,
                aws_secret_access_key=self.info.credentials.SECRET_ACCESS_KEY,
                aws_session_token=self.info.credentials.SESSION_TOKEN,
            )
            self._broker_client = _broker_client
        return self._broker_client

    def _credentials_expiring_soon(self):
        """
        Returns True if the credentials are expiring soon.  The expiration
        datetime will be a UTC datetime object
        """
        expiration = self.info.credentials.EXPIRATION
        # Refresh when 1 hour or less left on the expiration token
        REFRESH_LIMIT_HOURS = 3600
        return (
            expiration - datetime.now(timezone.utc)
        ).seconds <= REFRESH_LIMIT_HOURS

    def get_messages(self, max_num_msg, visibility, waittime, worker):
        """
        get messages from the queue

        :param max_num_msg: maximum number to retrieve
        :type max_num_msg: int
        :param visibility: time in seconds until the message becomes visible
                           again on the queue
        :type visibility: int
        :param waittime: time to wait for a message
        :type waittime: int
        :param worker: The :class:`~pyqalx.bot.Worker` instance that called this method
        :type worker: ~pyqalx.bot.Worker
        :return: List of :class:`~pyqalx.core.entities.queue.QueueMessage`
        """

        responses = self.broker_client.receive_message(
            QueueUrl=self.info.queue_url,
            MaxNumberOfMessages=max_num_msg,
            VisibilityTimeout=visibility,
            WaitTimeSeconds=waittime,
        )
        if responses.get("Messages"):
            return [
                QueueMessage(
                    message=response, worker=worker, visibility=visibility
                )
                for response in responses["Messages"]
            ]
        return []

    def delete_message(self, message):
        """remove message from the queue

        :param message: message to delete
        :type message: :class:`~pyqalx.core.entities.queue.QueueMessage`
        """
        if message is not None:
            # message could be None if the job it's been
            # on has been told to wait - therefore, don't attempt delete
            self.broker_client.delete_message(
                QueueUrl=self.info.queue_url,
                ReceiptHandle=message.receipt_handle,
            )
            message._stop_heartbeat()

    def _send_message(self, payload, entity_type, **message_kwargs):
        """
        Batch submits the given payload to the instance of Queue.  Figures out
        whether the payload is a subclass of QalxEntity, a string or a list of
        a combination.  Typically this will be invoked via the entity class itself:

        >>> EntityClass.add_to_queue(entity, queue)
        >>> queue._send_message(<entity_instance>)
        >>> queue._send_message(<entity_guid>)
        >>> queue._send_message([<entity_instance>,
        ...                      <entity_instance>,
        ...                      <entity_instance>])
        >>> queue._send_message([<entity_guid>, <entity_guid>, <entity_guid>])

        :param payload: A subclassed instance of QalxEntity, a guid string or a list
                        of QalxEntities/guids
        :type payload:QalxEntity or str
        :param entity_type:The entity type
        :type entity_type: str
        :param message_kwargs:Additional arguments that should be added to the
                              message body
        :return:An instance of QueueResponse
        """

        responses = []
        valid_types = (QalxEntity, uuid.UUID, list)
        if not isinstance(payload, valid_types):
            # Only certain types are supported
            raise QalxQueueError(
                f"Expected one of {', '.join([str(vt) for vt in list(valid_types)])}."
                f" Got {type(payload)}"
            )
        if isinstance(payload, (QalxEntity, uuid.UUID)):
            # Messages always get chunked and added in batches so make
            # sure the entity is a list if it is of these types
            payload = [payload]
        entries = []
        for _entity in payload:
            # Build our list of entries to ensure that they are all valid before
            # submitting to the queue
            entity_guid = _entity
            if isinstance(_entity, QalxEntity):
                # It's an instance of an entity - get the guid for submission
                # to the queue
                if not isinstance(_entity, (Item, Set, Group)):
                    raise QalxQueueError(
                        "Only Item, Set and Group entities can be submitted to the "
                        "queue. No messages submitted to queue."
                    )
                if _entity.entity_type != entity_type:
                    error = (
                        f"Mismatched entity types. Expected "
                        f"`{entity_type}`, got "
                        f"`{_entity.entity_type}`. Did you mean to do "
                        f"`{_entity.__class__.__name__}.add_to_queue("
                        f"entity, queue)?`. No messages submitted to queue."
                    )
                    raise QalxQueueError(error)
                entity_guid = _entity["guid"]

            entries.append(
                {
                    "Id": str(uuid.uuid4()),
                    "MessageBody": json.dumps(
                        {
                            "entity_type": entity_type,
                            # SQS needs the guid as a string - not UUID
                            "entity_guid": str(entity_guid),
                            **message_kwargs,
                        }
                    ),
                    # Unique MessageGroupId to prevent processing
                    # duplicates.
                    "MessageGroupId": str(uuid.uuid4()),
                    # Unique MessageDeduplicationId to allow the user
                    # to put the same entity on the queue multiple times
                    "MessageDeduplicationId": str(uuid.uuid4()),
                }
            )

        if entries:
            MAX_BATCH_SIZE = 10
            # Iterate through all entries and send them to the queue in batches
            for chunk in self._chunks(entries, chunk_size=MAX_BATCH_SIZE):
                chunked_objects = list(filter(None, chunk))
                responses.append(
                    self.broker_client.send_message_batch(
                        QueueUrl=self.info.queue_url, Entries=chunked_objects
                    )
                )

        return QueueResponse(responses)

    def purge(self):
        """
        Purge the queue. All messages on the queue will be deleted.

        This might take up to 60 seconds and any messages sent to the queue
        while it is being purged might also be deleted
        """
        self.broker_client.purge_queue(QueueUrl=self.info.queue_url)
