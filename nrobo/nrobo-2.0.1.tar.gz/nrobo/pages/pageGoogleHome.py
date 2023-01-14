from helpers.Page import Page


class PageGoogleHome(Page):

    def open_home_page(self):
        self.get("https://google.com")
        self.log.info("Open google home page")