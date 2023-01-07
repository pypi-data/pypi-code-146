from gdshoplib.services.notion.base import BasePage
from gdshoplib.services.notion.notion import Notion
from gdshoplib.services.notion.page import Page


class Database(BasePage):
    def get_source(self):
        return self.notion.get_database(self.id)

    def refresh(self):
        Notion(caching=True).get_database(self.id)
        self.initialize()

    def pages(self, filter=None, params=None):
        if not filter:
            for page in self.notion.get_pages(self.id, params=params):
                yield Page(page["id"], notion=self.notion, parent=self)
            return

        for page in self.notion.get_pages(self.id, params=params):
            filtered = True
            for k, v in filter.items():
                page = Page(page["id"], notion=self.notion, parent=self)
                if str(page.__getattr__(k)).lower() != str(v).lower():
                    filtered = False
            if filtered:
                yield page

    def commit(self):
        # Проитерироваться по изменениям и выполнить в Notion
        ...

    def to_json(self):
        # Вернуть товар в json
        ...
