from .logger import log


class CrawlerError(Exception):
    """Handle errors related to Windows objects
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.logger = log(self.__class__.__name__)
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self,):
        if self.message is None:
            self.message = "Failed browsing."
        self.logger.error(self.message)
        return self.message
