"""The Gateway Package queue.
This module contains the classes that:
    - Support the PackageQueue used to receive Driver collected packages.
"""


# ============================ imports =========================================
import os
from typing import Union
from multiprocessing import Queue
from multiprocessing.managers import BaseProxy
from queuelib import FifoDiskQueue
import psutil
import pickle
from txp.devices.package import GatewayPackage
from txp.common.config import settings
import concurrent.futures
import shutil
import threading
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)

# ==============================================================================
# Definition of The Package Queue
# ==============================================================================


class PackageQueue:
    """Provides operations to receive packages produced by drivers.
    This PackageQueue is designed to be safely shared across Gateway and Drivers.
    Drivers will put packages in this queue concurrently.
    """

    def __init__(self):
        if (settings.gateway.queue_clean_old_spilled_packages
                and os.path.exists(settings.gateway.queue_storage_path)):
            shutil.rmtree(settings.gateway.queue_storage_path)

        self.pool_executor = concurrent.futures.ThreadPoolExecutor()
        self.received_packages: "Queue[GatewayPackage]" = Queue()

        try:
            self.disk_received_packages = FifoDiskQueue(settings.gateway.queue_storage_path, chunksize=1)
        except FileNotFoundError as ferror:
            log.error("Trying to open Package Queue chunk, but the file was not found. Queue disk storage corrupted.")
            self._backup_corrupted_files()
            self.disk_received_packages = FifoDiskQueue(settings.gateway.queue_storage_path, chunksize=1)
            log.info("New packages Queue created successfully after recovering from corrupted files.")

        self._q_size: int = 0
        """_q_size: the size of the Queue. In MacOS using the provided qsize() may raise
        NotImplementError https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue.qsize"""

        recovered_packages = 0
        if len(self.disk_received_packages):
            self._q_size = len(self.disk_received_packages)
            recovered_packages = self._pop_spilled_packages()

        self._disk_push_lock: threading.Lock = threading.Lock()
        """_disk_push_lock: Thread safe for the disk write/read."""

        self._memory_push_lock: threading.Lock = threading.Lock()
        """_disk_push_lock: Thread safe for the memory write/read."""

        self._memory_tolerance: int = settings.gateway.queue_memory_size
        """self._memory_tolerance: indicates the memory percentage at which the packages should be spilled."""
        log.info(f"Packages queue created. Stats on creation: \n"
                 f"Number of spilled packages in disk at initialization: {self._q_size}\n"
                 f"RAM tolerance configured to: {self._memory_tolerance}%\n"
                 f"Number of packages loaded from disk to memory: {recovered_packages}\n"
                 f"Current number of packages in disk: {len(self.disk_received_packages)}\n")

        self._disk_spilled_packages_win: int = 0
        """self._disk_spilled_packages_win: This attribute is used to track the count of saved/taken spilled
        packages up to a configured number. 
        When the configured number is reached, the disk queue state will be persisted.
        """
        self._disk_max_spilled_packages_win: int = 20

    def _backup_corrupted_files(self) -> None:
        """Performs a recursive copy of the disk queue storage folder, to allow clean instantiation
        of a new FIFO disk queue"""
        import datetime
        current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_folder_suffix = f'_{current_time}'
        shutil.copytree(
            src=settings.gateway.queue_storage_path,
            dst=settings.gateway.queue_storage_path + backup_folder_suffix
        )
        shutil.rmtree(settings.gateway.queue_storage_path)

    def save_current_disk_state(self) -> None:
        """Call this method to save the current disk state of the packages that are currently
        spilled to disk.

        This guarantees that the packages will be available if the Gateway process ends for some
        reason.
        """
        if not len(self.disk_received_packages):
            log.info("Packages Queue was requested to persist spilled packages, but there are "
                     "not packages on disk.")
            return

        self.disk_received_packages.close()
        self.disk_received_packages = FifoDiskQueue(settings.gateway.queue_storage_path, chunksize=1)
        self._create_disk_queue_bak()
        log.info(f"Packages Queue successfully saved {len(self.disk_received_packages)} spilled packages")

    def _create_disk_queue_bak(self) -> None:
        """This method is called when the disk queue is closed with the intent to
        save the packages after process shutdown. It creates a backup of the
        queue file path."""
        path = self.disk_received_packages._infopath()
        copy_path = path + '.bak'
        shutil.copyfile(path, copy_path)  # if copy_path exists, it'll be replaced

    def _pop_spilled_packages(self) -> int:
        """This method is called when spilled packages were found on disk at __init__ time.

        If there are spilled packages, those should be loaded to memory if there's RAM available.

        Returns:
            returns the number of spilled packages loaded into memory.
        """
        c = 0
        while True:
            if (psutil.virtual_memory().percent <= settings.gateway.queue_memory_size
                    and len(self.disk_received_packages)):
                package = self.disk_received_packages.pop()
                package = pickle.loads(package)
                self.received_packages.put(package)
                c += 1
            else:
                break
        log.debug(f"{c} spilled packages moved from disk to memory")
        self.disk_received_packages.close()
        self.disk_received_packages = FifoDiskQueue(settings.gateway.queue_storage_path, chunksize=1)
        return c

    def close(self):
        # TODO: This close class sometimes corrupts the file after CTRL+C
        #  The backup file created with _create_disk_queue_bak allows a recovery strategy.
        self.disk_received_packages.close()

    def _spill_package(self, package: GatewayPackage):
        encoded_package = pickle.dumps(package)
        self._disk_push_lock.acquire()
        self.disk_received_packages.push(encoded_package)

        # Check if spilled packages requires safe persist
        self._disk_spilled_packages_win += 1
        if self._disk_spilled_packages_win > self._disk_max_spilled_packages_win:
            self.save_current_disk_state()
            self._disk_spilled_packages_win = 0

        self._disk_push_lock.release()
        self._q_size = self._q_size + 1

    def _load_package(self):
        next_package = self.disk_received_packages.pop()
        next_package = pickle.loads(next_package)
        self.received_packages.put(next_package)

        # If taking packages from the disk, persist to keep everything safe
        self._disk_push_lock.acquire()
        self.save_current_disk_state()
        self._disk_push_lock.release()

    def add_package(self, package: GatewayPackage):
        """Adds the package to this queue.
        Args:
            package: The package sent by the Driver.
        """
        self._memory_push_lock.acquire()
        if isinstance(package, GatewayPackage):
            if psutil.virtual_memory().percent >= settings.gateway.queue_memory_size \
                    or len(self.disk_received_packages):
                log.debug(f"Adding GatewayPackage {package.metadata.package_id} in disk storage queue")
                self.pool_executor.submit(self._spill_package, package)
                self._q_size = self._q_size + 1
            else:
                log.debug(f"Adding GatewayPackage {package.metadata.package_id} in memory queue")
                self.received_packages.put(package)
                self._q_size = self._q_size + 1

            log.debug(f"Queue Size: {len(self.disk_received_packages)}")
        self._memory_push_lock.release()

    def get_package(self) -> Union[GatewayPackage, None]:
        """Gets one package from this queue
        Returns:
            A Package if there are at least one package in the queue.
            None otherwise.
        """
        log.debug("Retrieving package from Packages Queue")
        ret = None
        if len(self.disk_received_packages):
            if self.received_packages.empty():
                log.debug("No packages in-memory, retrieving package from disk queue")
                next_package = self.disk_received_packages.pop()
                next_package = pickle.loads(next_package)
                self._q_size = self._q_size - 1
                ret = next_package

                # If taking packages from the disk, persist to keep everything safe
                self._disk_push_lock.acquire()
                self.save_current_disk_state()
                self._disk_push_lock.release()

            else:
                log.debug("Retrieving package from in-memory storage and "
                          "concurrently taking 1 package from disk storage to memory")
                self.pool_executor.submit(self._load_package)

        if not self.received_packages.empty():
            log.debug("Retrieving package from in-memory storage. No packages in disk found.")
            self._q_size = self._q_size - 1
            ret = self.received_packages.get_nowait()

        return ret

    def is_empty(self) -> bool:
        return self._q_size == 0

    def size(self) -> int:
        return self._q_size

    def clear(self) -> None:
        log.info("Clearing Packages Queue")
        del self.received_packages
        self.received_packages = Queue()
        self.disk_received_packages.close()
        if os.path.exists(settings.gateway.queue_storage_path):
            shutil.rmtree(settings.gateway.queue_storage_path)
        self.disk_received_packages = FifoDiskQueue(settings.gateway.queue_storage_path, chunksize=1)
        self._q_size = 0


class PackageQueueProxy(BaseProxy):
    """Custom Proxy for a PackageQueue.
    This custom proxy helps with type hints and autocompletion.
    """

    _exposed_ = ["add_package", "get_package", "is_empty", "size", "close", "save_current_disk_state", "clear"]

    def add_package(self, package: GatewayPackage):
        self._callmethod("add_package", (package,))

    def get_package(self) -> Union[GatewayPackage, None]:
        return self._callmethod("get_package")

    def is_empty(self):
        return self._callmethod("is_empty")

    def size(self):
        return self._callmethod("size")

    def clear(self):
        self._callmethod("clear")

    def close(self):
        return self._callmethod("close")

    def save_current_disk_state(self):
        return self._callmethod("save_current_disk_state")
