import contextlib
import logging
import os
import pathlib
import threading
import sys
from typing import Generator, Type

import clr

from aiopi.types import SDK, SDKConnection, SDKSubBatch, SDKUnitBatch



_LOGGER = logging.getLogger(__name__)


class SDKClient:
    """Client object for getting a connection to the PI SDK"""
    _sdk: Type[SDK] = None
    _sub_batch: Type[SDKSubBatch] = None
    _unit_batch: Type[SDKUnitBatch] = None

    def __new__(cls: Type["SDKClient"], *args, **kwargs) -> "SDKClient":
        if cls._sdk is None:
            path = kwargs.get('path') or os.getenv('PISDKPATH') or pathlib.Path("C:/Program Files/PIPC/pisdk/PublicAssemblies")
            assembly = kwargs.get('assembly') or 'OSIsoft.PISDK'
            kwargs.update({'assembly': assembly})
            
            sys.path.append(path.__str__())
            kwargs.update({'path': path})
            clr.AddReference(assembly)
            
            from PISDK import PISDK, PISubBatch, PIUnitBatch
            
            cls._sdk = PISDK
            cls._sub_batch = PISubBatch
            cls._unit_batch = PIUnitBatch
        
        return super(SDKClient, cls).__new__(cls)
    
    def __init__(
        self,
        server: str,
        path: str = None,
        assembly: str = None,
        max_connections: int = 4
    ) -> None:
        self._server_name = server
        self._path = path
        self._assembly = assembly

        self._lock: threading.Semaphore = threading.Semaphore(max_connections)

    @property
    def unit_batch(self) -> Type[SDKUnitBatch]:
        return self._unit_batch

    @property
    def sub_batch(self) -> Type[SDKSubBatch]:
        return self._sub_batch

    @contextlib.contextmanager
    def get_connection(self) -> Generator[SDKConnection, None, None]:
        """Obtain an SDK connection from the pool.
        
        This always opens a new connection. This is done because we have to use
        the clr loader to utilize the SDK and this can cause compatability issues
        with python sometimes so instead of trying to maintain a pool, each connection
        has a single use lifecycle.
        """
        self._lock.acquire()
        try:
            server: SDKConnection = self._sdk().Servers[self._server_name]
            try:
                server.Open()
            except:
                err = ConnectionError("Unable to connect to PI SDK")
                _, _, tb = sys.exc_info()
                err.__traceback__ = tb
                raise err
            _LOGGER.debug("Opened SDK connection: %r", self._lock)
            try:
                yield server
            finally:
                try:
                    if server.Connected:
                        server.Close()
                    _LOGGER.debug("Connection released")
                except:
                    _LOGGER.warning("Exception releasing connection", exc_info=True)
                    pass
                del server
        finally:
            self._lock.release()