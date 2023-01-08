from jinja2 import Environment, FileSystemLoader, select_autoescape

from gdshoplib.core.settings import GeneralSettings
from gdshoplib.services.notion.block import Block


class ProductDescription:
    def __init__(self, product):
        self.product = product
        self.general_settings = GeneralSettings()
        self.description_blocks = {}
        self.jinja2_env = self.jinja2_env()

    def warm_description_blocks(self):
        for block in self.product.blocks(filter={"type": "code"}):
            capture = block.get_capture()
            if "description" in capture:
                self.description_blocks[capture] = ProductDescriptionBlock(
                    block.id,
                    notion=self.product.notion,
                    parent=self.product.parent,
                )

    def get_description_block(self, platform_key=None):
        if not self.description_blocks:
            self.warm_description_blocks()

        if platform_key:
            return self.description_blocks.get(f"description:{platform_key.lower()}")
        return self.description_blocks.get("description")

    def generate(self, platform):
        return self.render(platform)

    def get_template(self, platform):
        return self.jinja2_env.get_template(platform.DESCRIPTION_TEMPLATE)

    def render(self, platform):
        return self.get_template(platform).render(product=self.product)

    def jinja2_env(self):
        return Environment(
            loader=FileSystemLoader(self.general_settings.TEMPLATES_PATH),
            autoescape=select_autoescape(),
        )


class ProductDescriptionBlock(Block):
    def __init__(self, *args, **kwargs):
        super(ProductDescriptionBlock, self).__init__(*args, **kwargs)

    @property
    def content(self):
        return self.code["rich_text"][0]["plain_text"]

    @property
    def check(self):
        return bool(self.code["rich_text"][0]["plain_text"])
