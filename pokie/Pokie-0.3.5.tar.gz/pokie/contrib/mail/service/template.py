from typing import Optional

from pokie.constants import DI_DB
from rick.mixin import Injectable

from pokie.contrib.mail.dto import MessageTemplateRecord
from pokie.contrib.mail.helpers import MessageBuilder
from pokie.contrib.mail.repository import MessageTemplateRepository


class MessageTemplateService(Injectable):
    def get_template(
        self, template: str, locale: str, channel: int
    ) -> Optional[MessageTemplateRecord]:
        return self.repo_template.find_template(template, locale, channel)

    def get_builder(
        self, template: str, locale: str, channel: int
    ) -> Optional[MessageBuilder]:
        template = self.repo_template.find_template(template, locale, channel)
        if template is None:
            return None
        return MessageBuilder(template)

    @property
    def repo_template(self) -> MessageTemplateRepository:
        return MessageTemplateRepository(self.get_di().get(DI_DB))
