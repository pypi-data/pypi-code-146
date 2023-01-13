# ape context manager

import atexit
import logging
import os
import shutil
import tempfile
from pathlib import Path

import ape
from ape.contracts.base import ContractCallHandler, ContractTransactionHandler
from eth_utils import is_same_address

from .account import KeyAccount
from .contract import ContractCallResult

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("APEMAN_LOG_LEVEL", "WARNING"))


class APE:
    def __init__(
        self,
        ecosystem=None,
        network=None,
        provider=None,
        selector=None,
        connect=False,
        project_dir=None,
        data_dir=None,
    ):
        self.connection = None
        self.project_dir = self.init_dir(project_dir, "APE_PROJECT_DIR")
        self.data_dir = self.init_dir(data_dir, "APE_DATA_DIR")

        ape.config.DATA_FOLDER = self.data_dir
        ape.config.PROJECT_FOLDER = self.project_dir

        ape.project = ape.Project(self.project_dir)

        ape.config.load(force_reload=True)
        if selector is None:
            ecosystem = ecosystem or os.environ["APE_ECOSYSTEM"]
            network = network or os.environ["APE_NETWORK"]
            provider = provider or os.environ["APE_PROVIDER"]
            selector = os.environ.get(
                "APE_SELECTOR", f"{ecosystem}:{network}:{provider}"
            )
        self.context_manager = ape.networks.parse_network_choice(selector)
        if connect is True:
            self.connect()

    def init_dir(self, param, key):
        dir = param or os.environ.get(key)
        if dir:
            dir = Path(dir)
            dir.mkdir(exist_ok=True)
        else:
            dir = Path(tempfile.mkdtemp()).resolve()
            atexit.register(shutil.rmtree, str(dir))
            logger.debug(f"created temp directory {str(dir)} as {key}")

        if isinstance(dir, Path) is False or dir.is_dir() is False:
            raise TypeError(f"{dir} is not a directory")
        dir.chmod(0o700)
        return dir

    def __del__(self):
        if self.connection:
            self.disconnect()

    def account(
        self,
        private_key,
        alias=None,
        password=None,
        autosign=False,
    ):
        return KeyAccount(
            ape=self,
            private_key=private_key,
            alias=alias,
            password=password,
            autosign=autosign,
        )

    def connect(self, *args, **kwargs):
        if self.connection is None:

            self.connection = self.context_manager.__enter__(*args, **kwargs)

            self.__all__ = ape.__all__

            for attr in ape.__all__:
                setattr(self, attr, getattr(ape, attr))

            self.provider = self.connection
            self.network = self.connection.network
            self.explorer = self.provider.network.explorer
            self.web3 = self.provider.web3
            self.contracts = self.network.chain_manager.contracts

            # assert self.provider is self.project.provider
            # assert self.network is self.project.provider.network
            # assert self.explorer is self.project.provider.network.explorer
            # assert self.web3 is self.project.provider.web3
            # assert self.contracts is self.project.provider.network.chain_manager.contracts

            logger.debug(f"connected: {self}")

        return self

    def disconnect(self, *args, **kwargs):
        if self.connection:
            self.context_manager.__exit__(*args, **kwargs)
            logger.debug(f"disconnected: {self}")
        self.connection = None

    def __enter__(self, *args, **kwargs):
        return self.connect(*args, **kwargs)

    def __exit__(self, *args, **kwargs):
        self.disconnect(*args, **kwargs)

    def call_contract(self, contract_address, function_name, *args, **kwargs):
        """call a lookup or mutable contract function, returning a ContractCallResult

        kwargs:
          sender (ADDRESS if lookup, PRIVATE_KEY if mutable/transaction
          autosign: (bool) automatically sign transaction
          max_fee:  max fee per GAS to be used
          max_priority_fee: specify amount of 'tip' per GAS
        """
        result = ContractCallResult()
        contract = self.Contract(contract_address)
        function = getattr(contract, function_name)
        if isinstance(function, ContractCallHandler):
            # lookup call may include sender=ADDRESS
            result.ret = function(*args, **kwargs)
        elif isinstance(function, ContractTransactionHandler):
            # mutable call uses transaction, sender must be a private_key
            sender = kwargs.pop("sender", None)
            private_key = kwargs.pop("private_key", None)
            account = kwargs.pop("account", None)
            if private_key:
                account = self.account(private_key=private_key)

            elif account:
                account = account
            else:
                raise RuntimeError(
                    "mutable call requires 'private_key' or 'account'"
                )

            account.autosign = kwargs.pop("autosign", True)

            if sender is not None:
                if not is_same_address(sender, account.address):
                    raise ValueError(
                        f"account key mismatches sender address {sender}"
                    )

            with account as ape_account:
                receipt = function(*args, **kwargs, sender=ape_account)
                result.set_receipt(receipt)

        else:
            raise TypeError(
                f"function {function_name} not found in contract at {contract_address}"
            )

        return result
