from argparse import ArgumentParser

from pokie.constants import DI_SERVICES, DI_APP
from pokie.contrib.base.constants import SVC_FIXTURE
from pokie.contrib.base.dto import FixtureRecord
from pokie.contrib.base.service.fixture import FixtureService
from pokie.contrib.mail.constants import SVC_MESSAGE_QUEUE
from pokie.contrib.mail.job import MailQueueJob
from pokie.contrib.mail.service import MessageQueueService
from pokie.core import CliCommand


class QueueCmd(CliCommand):
    @property
    def svc_queue(self) -> MessageQueueService:
        return self.get_di().get(DI_SERVICES).get(SVC_MESSAGE_QUEUE)


class RunQueueCmd(CliCommand):
    description = "run mail queue"

    def run(self, args) -> bool:
        self.tty.write("Running mail queue...")
        job_runner = MailQueueJob(self.get_di())
        job_runner.run(self.get_di())
        self.tty.write("Done!")

        return True


class PurgeQueueCmd(QueueCmd):
    description = "purge mail queue (delete all entries)"

    def arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "--yes",
            default=False,
            action="store_true",
            help="Confirm purge",
        )

    def run(self, args) -> bool:
        if not args.yes:
            self.tty.error("missing --yes argument, aborting...")
            return False

        self.tty.write("Removing all mail queue entries...")
        self.svc_queue.purge()
        self.tty.write("Purging finished.")
        return True
