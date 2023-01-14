# Менеджер управления Notion
import functools

from gdshoplib.core.settings import NotionSettings
from gdshoplib.packages.cache import KeyDBCache
from gdshoplib.services.notion.manager import RequestManager


class Notion(RequestManager):
    def __init__(self, *args, caching=False, **kwargs) -> None:
        self.settings = NotionSettings()
        self.caching = caching
        self.cache = KeyDBCache()
        super(Notion, self).__init__(*args, **kwargs)

    def get_headers(self):
        return {
            **self.auth_headers(),
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
            "Accept": "application/json",
        }

    def cache_one(func):
        @functools.wraps(func)
        def wrap(self, id):
            if not self.settings.CACHE_ENABLED:
                return func(self, id)

            if self.caching or not self.cache.exists(id):
                self.cache[id] = func(self, id)

            return self.cache[id]

        return wrap

    def auth_headers(self):
        return {"Authorization": "Bearer " + self.settings.NOTION_SECRET_TOKEN}

    def get_user(self, user_id):
        return self.make_request(f"blocks/{user_id}", method="get")

    def get_capture(self, block):
        _capture = block[block["type"]].get("caption")
        return _capture[0].get("plain_text") if _capture else ""

    # TODO: Сделать декоратор пагинации
    def get_blocks(self, parent_id, params=None):
        blocks = []
        for block in self.pagination(
            f"blocks/{parent_id}/children", method="get", params=params
        ):
            if not block.get("has_children"):
                blocks.append(block)
            else:
                blocks.extend(self.get_blocks(block.get("id")))
        return blocks

    @cache_one
    def get_block(self, block_id):
        return self.make_request(f"blocks/{block_id}", method="get")

    @cache_one
    def get_page(self, page_id):
        return self.make_request(f"pages/{page_id}", method="get")

    @cache_one
    def get_database(self, database_id):
        return self.make_request(f"databases/{database_id}", method="get")

    def get_pages(self, database_id, params=None):
        return self.pagination(
            f"databases/{database_id}/query", method="post", params=params
        )

    def update_prop(self, product_id, params=None):
        # TODO: Переделать в обновление параметра
        self.make_request(
            f"pages/{product_id}",
            method="patch",
            params=params,
            # params={"properties": {"Наш SKU": [{"text": {"content": sku}}]}},
        )

    def update_block(self, block_id, params):
        self.make_request(
            f"blocks/{block_id}",
            method="patch",
            params=params
            # params={"code": {"rich_text": [{"text": {"content": content}}]}},
        )
