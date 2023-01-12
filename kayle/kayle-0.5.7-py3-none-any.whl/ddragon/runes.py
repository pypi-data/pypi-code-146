import requests
from PIL import Image
from io import BytesIO


class DDragonRune:
    def __init__(self, data, cdragon_patch):
        self.id = data["id"]
        try:
            self.key = data["key"]
            self.shortDesc = data["shortDesc"]
            self.longDesc = data["longDesc"]
            self.icon_file = "/".join(data["icon"].split("/")[1:]).lower()
        except:
            self.key = data["name"]
            self.shortDesc = data["description"]
            self.longDesc = self.shortDesc
            self.icon_file = "/".join(data["image"]["full"].split("/")[1:]).lower()

        self.name = data["name"]
        self.cdragon_patch = cdragon_patch

        self._icon = None

    def icon(self):
        if self._icon is not None:
            return self._icon
        r = requests.get(
            "https://raw.communitydragon.org/{}/game/assets/perks/{}".format(
                self.cdragon_patch, self.icon_file
            )
        )
        print(r.url)
        self._icon = Image.open(BytesIO(r.content))
        return self._icon


class DDragonRuneTree:
    def __init__(self, data, cdragon_patch):
        self.id = data["id"]
        self.key = data["key"]
        self.icon_file = "/".join(data["icon"].split("/")[1:]).lower()
        self.name = data["name"]
        self.cdragon_patch = cdragon_patch

        self._icon = None

    def icon(self):
        if self._icon is not None:
            return self._icon
        r = requests.get(
            "https://raw.communitydragon.org/{}/game/assets/perks/{}".format(
                self.cdragon_patch, self.icon_file
            )
        )
        print(r.url)
        self._icon = Image.open(BytesIO(r.content))
        return self._icon
