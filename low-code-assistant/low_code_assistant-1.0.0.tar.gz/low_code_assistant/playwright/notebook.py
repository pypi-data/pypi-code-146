import shutil
from pathlib import Path

from playwright.sync_api import Page

from low_code_assistant.playwright import mouse_move_middle

from .assistant import AssistentHelper

timeout = 8 * 1000
HERE = Path(__file__)


class Notebook:
    page: Page

    def __init__(self, page: Page, host: str = "localhost", port: int = 11112):
        self.host = host
        self.port = port
        # # TODO: this should actually happen at the server
        self.page = page
        shutil.copy(
            HERE.parent.parent.parent / "tests/e2e/notebooks/empty.ipynb",
            HERE.parent.parent.parent / "tests/e2e/notebooks/working.ipynb",
        )
        url = f"http://{self.host}:{self.port}/notebooks/working.ipynb"
        self.page.goto(url)
        self.page.set_default_timeout(timeout=timeout)
        # at least wait till the page has loaded some frontend
        self.page.locator("text=Low Code Assistant").wait_for()
        # if we click the kernellink too fast, it can close again
        self.page.wait_for_timeout(1000)
        # restart kernel
        self.page.locator("#kernellink").click()
        self.page.locator('span:has-text("Restart")').click()
        self.page.locator('button:has-text("Restart")').click()

        self.page.locator("Kernel Ready").wait_for(state="detached")

    @property
    def assistant(self):
        return AssistentHelper(self.page)

    def last_cell_assistant_hover(self):
        last_input = self.last_code_cell.locator(".input")
        last_input.scroll_into_view_if_needed()
        mouse_move_middle(self.page, last_input)
        self.assistant.domino_logo.wait_for()
        self.page.wait_for_timeout(100)
        self.assistant.domino_logo.hover()
        self.page.wait_for_timeout(100)

    @property
    def code_cell(self):
        return self.page.locator(".code_cell")

    @property
    def last_code_cell(self):
        self.page.locator("text=In [ ]:").wait_for()
        return self.page.locator(".code_cell").last

    def insert_code(self, code, delay=0):
        # if we don't want, we sometimes jump to 'command' mode
        self.page.wait_for_timeout(500)
        input = self.page.locator("textarea").last
        input.focus()
        self.page.wait_for_timeout(100)
        input.type(code, delay=delay)

        input = self.page.locator("text=In [ ]:").last
        input.press("Shift+Enter")

    def load_csv(self, path: Path, df_var_name: str = "df"):
        self.insert_code(
            f"""
import pandas as pd
{df_var_name} = pd.read_csv("{str(path)}")
{df_var_name}.head(2)""".strip()
        )
