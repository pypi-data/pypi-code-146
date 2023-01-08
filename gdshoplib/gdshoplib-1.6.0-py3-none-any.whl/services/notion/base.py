from gdshoplib.services.notion.notion import Notion


class BasePage:
    def __init__(self, id, *, notion=None, parent=None):
        self.properties = None
        self.id = id
        self.notion = notion or Notion()
        self.parent = parent
        self.history = {}
        self.change_log = {}
        self.initialize()

    def initialize(self):
        self.page = self.get_source()

    def get_source(self):
        return self.notion.get_page(self.id)

    def __str__(self) -> str:
        return f"{self.__class__}: {self.id}"

    def __repr__(self) -> str:
        return f"{self.__class__}: {self.id}"

    def __getitem__(self, key):
        try:
            return super(BasePage, self).__getattribute__(key)
        except AttributeError:
            return self.__getattr__(key)

    def __getattr__(self, name: str):
        if self.page and name in self.page.keys():
            return self.page[name]

        if self.properties:
            return self.properties[name]

        raise AttributeError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if not exc_type:
            self.set_update_time()

    def get_update_time(self):
        return self.notion.cache.get_update_time(self.id, type=self.__class__.__name__)

    def set_update_time(self):
        return self.notion.cache.set_update_time(self.id, type=self.__class__.__name__)

    def edited_filter(self):
        update_time = self.get_update_time()
        if not update_time:
            return None
        return {
            "filter": {
                "timestamp": "last_edited_time",
                "last_edited_time": {"after": update_time},
            }
        }
