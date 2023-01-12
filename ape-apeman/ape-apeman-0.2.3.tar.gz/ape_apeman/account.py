# stateless ape account

import atexit
import json
from pathlib import Path
from secrets import token_hex

from eth_account import Account
from eth_utils import to_normalized_address


class KeyAccount:
    def __init__(
        self,
        *,
        ape,
        private_key,
        alias=None,
        password=None,
        autosign=False,
    ):
        self.ape = ape
        self.autosign = autosign
        self.alias = alias or token_hex(16)
        self.password = password or token_hex(32)
        account = Account.encrypt(private_key, self.password)
        self.address = to_normalized_address(account["address"])
        accounts_dir = self.ape.accounts.containers["accounts"].data_folder
        self.keyfile = Path(accounts_dir) / f"{self.alias}.json"
        self.keyfile.write_text(json.dumps(account))
        atexit.register(self.keyfile.unlink, missing_ok=True)
        self.ape_account = None
        self.load()

    def __del__(self):
        if self.keyfile:
            self.keyfile.unlink(missing_ok=True)

    def autosign_enabled(self):
        self.autosign = True
        return self

    def __enter__(self):
        return self.load()

    def load(self, autosign=False):
        if self.ape_account is None:
            self.ape_account = self.ape.accounts.load(self.alias)
        if self.autosign or autosign:
            self.ape_account.set_autosign(True, self.password)
        return self.ape_account

    def __exit__(self, *args, **kwargs):
        self.ape_account.set_autosign(False)
        self.autosign = False
