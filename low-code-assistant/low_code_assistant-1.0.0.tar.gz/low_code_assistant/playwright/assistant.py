from playwright.sync_api import Page

from low_code_assistant.playwright.app import AppHelper
from low_code_assistant.playwright.load_data import LoadDataHelper
from low_code_assistant.playwright.transform import TransformHelper


class AssistentHelper:
    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def initializer(self):
        return self.page.locator('[aria-label="Low Code Assistant™"]')

    @property
    def initialized_text(self):
        return self.page.locator("text=Low Code Assistant™ initialized")

    @property
    def domino_logo(self):
        return self.page.locator(".low_code_assistant-assistant-menu")

    @property
    def load_data(self):
        return LoadDataHelper(self.page)

    @property
    def app(self):
        return AppHelper(self.page)

    @property
    def transform(self):
        return TransformHelper(self.page)

    @property
    def insert_code(self):
        return self.page.locator("text=Insert Code")
