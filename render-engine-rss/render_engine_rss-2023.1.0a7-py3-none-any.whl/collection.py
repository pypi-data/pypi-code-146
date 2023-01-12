from typing import Type
from .parsers import RSSFeedPageParser
import feedparser
import time
from render_engine.collection import Collection
from render_engine.page import Page


class RSSPage(Page):
    @property
    def date_friendly(self):
        return  time.strftime("%b %d, %Y %H:%M", self.published_parsed)

class RSSCollection(Collection):
    PageParser = RSSFeedPageParser
    content_type = RSSPage
    content_path = str
    sort_by = "published_parsed"
    sort_reverse = True

    def __init__(self):
        self.content = feedparser.parse(self.content_path)
        super().__init__()

    @property
    def pages(self):
        """Entries for this would be """

        for entry in self.content['entries']:
            yield self.gen_page(content=entry)