from dominate.tags import script
from urlpath import URL

from iolanta.facet import Facet


class TelegramLink(Facet):
    """Embed a Telegram post by link."""

    def html(self):
        url = URL(str(self.iri))

        return script(
            _async=True,
            src='https://telegram.org/js/telegram-widget.js?19',
            data_telegram_post=url.path,
            data_width='100%',
        )
