from dateutil import parser

from gdshoplib.services.notion.base import BasePage
from gdshoplib.services.notion.block import Block
from gdshoplib.services.notion.notion import Notion


class Page(BasePage):
    def refresh(self):
        Notion(caching=True).get_page(self.id)
        self.initialize()

    def initialize(self):
        super(Page, self).initialize()
        self.properties = PageProperty(self.page)

    def blocks(self, filter=None):
        if not filter:
            for block in self.notion.get_blocks(self.id):
                yield Block(block["id"], notion=self.notion, parent=self)
            return

        for block in self.notion.get_blocks(self.id):
            for k, v in filter.items():
                block = Block(block["id"], notion=self.notion, parent=self)
                if str(block.__getattr__(k)).lower() == str(v).lower():
                    yield block

    def commit(self):
        # Проитерироваться по изменениям и выполнить в Notion
        ...

    def to_json(self):
        # Вернуть товар в json
        ...


class PageProperty:
    def __init__(self, page):
        self.page = page

    def __getitem__(self, key):
        return self.__dict__.get(key) or self.__search_content(key)

    def __getattr__(self, key):
        return self[key]

    def __search_content(self, key):
        for _, prop in self.page.get("properties", {}).items():
            for prop_field in self.__get_prop(key):
                if prop["id"] == prop_field["id"]:
                    data = self.properties_type_parse_map.get(prop["type"])(prop)
                    handler = prop_field.get("handler")

                    if handler and data:
                        return handler(data)
                    return data
        raise AttributeError

    def __get_prop(self, key):
        return self.properties_keys_map[key]

    def __str__(self) -> str:
        return f"{self.__class__}"

    def __repr__(self) -> str:
        return f"{self.__class__}"

    def relation_handler(self, page_id_in_list):
        _id = page_id_in_list[0]["id"]
        return Page(_id)

    def relation_list_handler(self, page_ids):
        result = []
        for _id in page_ids:
            result.append(Page(_id["id"]))
        return result

    @property
    def properties_keys_map(self):
        return {
            "title": (dict(name="Name", id="title"),),
            "edited_by": (dict(name="Last edited by", id="~%7BrF"),),
            "price_sale_10": (dict(name="Скидка, 10%", id="%7Bh%7D%7B"),),
            "price_general": (dict(name="Ходовая", id="x%3A%5Ci"),),
            "created_time": (dict(name="Created time", id="v%5Dsj"),),
            "short_description": (dict(name="Короткое описание", id="u_tU"),),
            "size": (dict(name="Размер", id="taW%3B"),),
            "notes_field": (dict(name="Примечания", id="sXND"),),
            "price_buy": (dict(name="Закупочная", id="pyiW"),),
            "quantity": (dict(name="Кол-во", id="pXTy"),),
            "price_neutral": (dict(name="Себестоимость", id="opcQ"),),
            "edited_time": (dict(name="Last edited time", id="mVEw"),),
            "price_sale_20": (dict(name="Скидка, 20%", id="cPu~"),),
            "collection": (dict(name="Коллекция", id="W%5BhI"),),
            "price_base": (dict(name="Безубыточность", id="VmWm"),),
            "name": (dict(name="Название на русском", id="Tss%5D"),),
            "created_by": (dict(name="Created by", id="TbyK"),),
            "kit_field": (
                dict(
                    name="Комплект", id="QV%5D%5D", handler=self.relation_list_handler
                ),
            ),
            "tags_field": (dict(name="Теги", id="MqdC"),),
            "status_description": (dict(name="Описание", id="MUl%7C"),),
            "color": (dict(name="Цвет", id="Jvku"),),
            "price_now": (dict(name="Текущая цена", id="Ddaz"),),
            "specifications_field": (
                dict(name="Материалы / Характеристики", id="COmf"),
            ),
            "status_publication": (dict(name="Публикация", id="BeEA"),),
            "sku": (dict(name="Наш SKU", id="BKOs"),),
            "price_sale_15": (dict(name="Скидка, 15%", id="BJPc"),),
            "sku_s": (dict(name="SKU поставщика", id="BHve"),),
            "price_eur": (dict(name="Цена (eur)", id="AyqD"),),
            "platforms": (
                dict(name="Платформы", id="%40Q~A", handler=self.relation_list_handler),
            ),
            "brand": (
                dict(name="Бренд", id="gk%40%3B", handler=self.relation_handler),
            ),
            "categories": (
                dict(name="Категории", id="%7CFzB", handler=self.relation_list_handler),
            ),
            "price_coefficient": (
                dict(name="Коэфицент бренда", id="HjFs"),
                dict(name="Наценка", id="YsUp"),
            ),
        }

    @property
    def properties_type_parse_map(self):
        return {
            "rich_text": lambda data: " ".join(
                [t.get("plain_text", "") for t in data["rich_text"]]
            )
            or "",
            "number": lambda data: data["number"] or 0,
            "title": lambda data: data["title"][0]["text"]["content"],
            "select": lambda data: data.get("select").get("name")
            if data.get("select")
            else None,
            "multi_select": lambda data: data,
            "status": lambda data: data["status"]["name"],
            "date": lambda data: data,
            "formula": lambda data: data["formula"]["number"],
            "relation": lambda data: data["relation"],
            "rollup": lambda data: data,
            "people": lambda data: data,
            "files": lambda data: data,
            "checkbox": lambda data: data,
            "url": lambda data: data["url"],
            "email": lambda data: data,
            "phone_number": lambda data: data,
            "created_time": lambda data: parser(data["created_time"]),
            "created_by": lambda data: str(data["created_by"]),
            "last_edited_time": lambda data: parser(data["last_edited_time"]),
            "last_edited_by": lambda data: str(data["last_edited_by"]),
            "image": lambda data: data["image"]["file"]["url"],
            "video": lambda data: data["video"]["file"]["url"],
        }
