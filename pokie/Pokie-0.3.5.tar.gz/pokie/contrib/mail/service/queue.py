from typing import List, Optional

from pokie.constants import DI_DB
from pokie.contrib.mail.dto import MessageQueueRecord
from pokie.contrib.mail.repository import MessageQueueRepository
from rick.mixin import Injectable


class MessageQueueService(Injectable):
    STATUS_QUEUED = "Q"
    STATUS_LOCKED = "L"
    STATUS_FAILED = "F"
    STATUS_SENT = "S"

    # communication channels
    CHANNEL_SMTP = 0

    def queue(self, record: MessageQueueRecord) -> str:
        return self.repo_queue.insert(record, cols=[MessageQueueRecord.id])

    def list_by_status(
        self, channel: int, status: str, limit: int = 1000
    ) -> List[MessageQueueRecord]:
        return self.repo_queue.find_by_status(channel, status, limit)

    def update_status(self, id, status):
        self.repo_queue.update_status(id, status)

    def fetch_for_processing(self, channel: int) -> Optional[MessageQueueRecord]:
        """
        Pick & lock a message for processing
        :return: MessageQueueRecord or None
        """
        return self.repo_queue.find_first_and_lock(channel, self.STATUS_QUEUED)

    def purge(self):
        """
        Removes all queued records
        :return:
        """
        return self.repo_queue.truncate()

    @property
    def repo_queue(self) -> MessageQueueRepository:
        return MessageQueueRepository(self.get_di().get(DI_DB))

