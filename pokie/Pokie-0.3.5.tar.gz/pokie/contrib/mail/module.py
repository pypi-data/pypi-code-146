from pokie.contrib.auth.constants import SVC_USER, SVC_ACL, SVC_AUTH
from pokie.contrib.mail.constants import SVC_MESSAGE_TEMPLATE, SVC_MESSAGE_QUEUE
from pokie.core import BaseModule


class Module(BaseModule):
    name = "mail"
    description = "Mail template module"

    services = {
        SVC_MESSAGE_TEMPLATE: "pokie.contrib.mail.service.MessageTemplateService",
        SVC_MESSAGE_QUEUE: "pokie.contrib.mail.service.MessageQueueService",
    }

    cmd = {
        'mail:purge': 'pokie.contrib.mail.cli.PurgeQueueCmd',
        'mail:run': 'pokie.contrib.mail.cli.RunQueueCmd',
    }

    jobs = [
        "pokie.contrib.mail.job.MailQueueJob",
    ]
