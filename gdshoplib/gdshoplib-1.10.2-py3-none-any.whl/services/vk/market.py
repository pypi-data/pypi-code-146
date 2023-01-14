from gdshoplib.services.vk.vk import VK


class VKMarket:
    def __init__(self, manager=None):
        self.manager = manager or VK()

    def list(self):
        return self.manager.request(
            "market.get",
            params={
                "owner_id": f"-{self.manager.settings.VK_GROUP_ID}",
                "extended": 1,
                "with_disabled": 1,
                "need_variants": 1,
            },
        )

    def get(self, sku):
        ...

    def add(self, sku):
        ...

    def edit(self, sku):
        ...

    def delete(self, sku):
        ...

    def album_get(self, sku):
        ...

    def album_create(self, sku):
        ...

    def album_edit(self, sku):
        ...

    def album_delete(self, sku):
        ...

    def album_add(self, sku):
        ...
