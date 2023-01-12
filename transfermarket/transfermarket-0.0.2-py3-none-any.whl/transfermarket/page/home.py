"""
This module provides logic for parsing the home page.
"""

from transfermarket.models.domain import Domain
from transfermarket.page.object import PageObject
from transfermarket.page.utils import get_href_from_anchor, get_text_from_anchor

# from transfermarket.page.utils import get_href_from_anchor, get_text_from_anchor


class HomePage(PageObject):
    """
    This class provides logic for parsing the home page.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.url = "https://www.transfermarkt.com"

        user_agent = "transfermarkt"

        self.headers = {"user-agent": user_agent}

        if kwargs.get("auto_load", False):
            self.load()

    def get_domains(self):
        """
        Returns the domains.
        """
        switcher = self.soup.select("div.tm-domainswitcher-box > ul")

        if len(switcher) == 0:
            return []

        unordered_list = switcher[0]
        items = unordered_list.select("li")

        domains = []
        for item in items:
            name = get_text_from_anchor(item)
            url = get_href_from_anchor(item)

            domain = Domain(name=name, url=url)
            domains.append(domain)

        return domains
