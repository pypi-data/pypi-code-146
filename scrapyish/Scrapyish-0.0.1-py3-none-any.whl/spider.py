"""
Spider base class was mostly copied from the original scrapy project.
More information can be found https://github.com/scrapy/scrapy.
"""
import logging
from scrapyish.request import Request

class Spider:
    """
    Base class for scrapyish spiders.
    """

    name: str

    def __init__(self, crawler, name=None):
        if name is not None:
            self.name = name
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

    @property
    def logger(self):
        logger = logging.getLogger(self.name)
        return logging.LoggerAdapter(logger, {'spider': self})

    def log(self, message, level=logging.DEBUG, **kw):
        """Log the given message at the given log level
        This helper wraps a log call to the logger within the spider, but you
        can use it directly (e.g. Spider.logger.info('msg')) or use any other
        Python logger too.
        """
        self.logger.log(level, message, **kw)

    async def start_requests(self):
        if not self.start_urls and hasattr(self, 'start_url'):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)")
        for url in self.start_urls:
            yield Request(url, dont_filter=True)

    async def parse(self, response, **kwargs):
        raise NotImplementedError(f'{self.__class__.__name__}.parse callback is not defined')

    @staticmethod
    def close(spider, reason):
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)

    def __repr__(self):
        return f"<{type(self).__name__} {self.name!r} at 0x{id(self):0x}>"
