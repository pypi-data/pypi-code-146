"""@Author: Rayane AMROUCHE

Exception classes for the DataManager.
"""


class DataManagerIOException(Exception):
    """Exception raised for errors related to the DataManager reader and saver."""

    def __init__(self, file_info: dict, message: str = ""):
        """Init the Exception.

        Args:
            file_info (dict): File metadata informations.
            message (str, optional): Exception message. Defaults to "Data Type unknown
                or not supported.".
        """
        if not message:
            message = "Data source unknown or not supported."
        self.file_info = file_info
        self.message = message
        super().__init__(self.message)
