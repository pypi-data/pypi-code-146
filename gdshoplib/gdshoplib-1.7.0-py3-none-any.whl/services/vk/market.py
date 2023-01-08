from gdshoplib.services.vk.vk import VK


class VKMarket:
    def __init__(self, manager=None):
        self.manager = manager or VK()

    def get(self):
        return self.manager.request(
            "market.get",
            params={
                "owner_id": f"-{self.manager.settings.VK_GROUP_ID}",
                "extended": 1,
                "with_disabled": 1,
                "need_variants": 1,
            },
        )
