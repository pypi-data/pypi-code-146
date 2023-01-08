from dataclasses import dataclass, field
from typing import List
from quiltz.domain.anonymizer import anonymize


class Recipient:
    def as_string(self):
        return 'unknown'


@dataclass
class NamedRecipient(Recipient):
    person: any

    @property
    def email(self):
        return self.person.email

    @property
    def anonymized(self):
        return anonymize(self.email)

    def as_string(self):
        return "{name} <{email}>".format(name=self.person.name, email=self.person.email)


@dataclass
class UnnamedRecipient(Recipient):
    email: str

    def as_string(self):
        return self.email

    @property
    def anonymized(self):
        return anonymize(self.email)


@dataclass
class Message:
    to: Recipient
    subject: str
    sender: str
    body: str = ''

    @staticmethod
    def for_unnamed_recipient(to, subject, sender, body):
        return Message(to=UnnamedRecipient(to), subject=subject, sender=sender, body=body)

    @staticmethod
    def for_named_recipient(to, subject, sender, body):
        return Message(to=NamedRecipient(to), subject=subject, sender=sender, body=body)

    @property
    def recipient(self):
        return self.to.as_string()


@dataclass
class Messenger:
    sender: str
    context: object
    messages: List[Message] = field(default_factory=list)

    def send(self, message):
        self.messages.append(message)
        return self
