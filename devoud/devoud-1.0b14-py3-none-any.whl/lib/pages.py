from .control_page import ControlPage
from .not_found_page import NotFoundPage
from .void_page import VoidPage

embedded_pages = {'devoud://control': ControlPage,
                  'devoud://notfound': NotFoundPage,
                  'devoud://void': VoidPage}

redirects = {'about:blank': NotFoundPage.url}


class PagesObserver:
    _pages = []

    @classmethod
    def pages(cls):
        return cls._pages

    @classmethod
    def urls(cls):
        return list(map(lambda page: page.url, cls._pages))

    @classmethod
    def add_page(cls, page):
        cls._pages.append(page)

    @classmethod
    def remove_page(cls, page):
        cls._pages.remove(page)

    @classmethod
    def control_update_lists(cls):
        for page in cls._pages:
            if isinstance(page.view, ControlPage):
                page.view.update_lists()

    @classmethod
    def update_control_pages(cls):
        for page in cls._pages:
            if isinstance(page.view, ControlPage):
                page.reload()