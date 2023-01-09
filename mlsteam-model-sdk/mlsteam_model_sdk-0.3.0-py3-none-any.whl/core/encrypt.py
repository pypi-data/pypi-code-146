import abc
import enum
from typing import BinaryIO, Callable

from pythemis.scell import SCellSeal
from pythemis.smessage import SMessage
from pythemis.skeygen import GenerateKeyPair, KEY_PAIR_TYPE

from mlsteam_model_sdk.utils.license import get_platform_id


class TrunkIO:

    class Mode(enum.Enum):
        BYTES = 1
        LEN_BYTES = 2

    def __init__(self, trunk_size: int, len_size: int, len_byteorder: str) -> None:
        self.trunk_size = trunk_size
        self.len_size = len_size
        self.len_byteorder = len_byteorder

    def read_file_trunk(self, src_file: BinaryIO) -> bytes:
        trunk_len = int.from_bytes(src_file.read(self.len_size), byteorder=self.len_byteorder)
        trunk = src_file.read(trunk_len)
        return trunk

    def write_file_trunk(self, dst_file: BinaryIO, trunk: bytes) -> None:
        dst_file.write(len(trunk).to_bytes(length=self.len_size, byteorder=self.len_byteorder))
        dst_file.write(trunk)

    def proc_file_in_trunks(self, src_file: BinaryIO, dst_file: BinaryIO,
                            read_mode: 'TrunkIO.Mode', write_mode: 'TrunkIO.Mode',
                            proc_func: Callable[[bytes], bytes]) -> None:
        while True:
            if read_mode == self.Mode.BYTES:
                trunk = src_file.read(self.trunk_size)
            else:
                trunk = self.read_file_trunk(src_file)
            if len(trunk) == 0:
                return
            proc_trunk = proc_func(trunk)
            if write_mode == self.Mode.BYTES:
                dst_file.write(proc_trunk)
            else:
                self.write_file_trunk(dst_file=dst_file, trunk=proc_trunk)


class ModelSealerBase(metaclass=abc.ABCMeta):
    TRUNK_SIZE = 10 * 1024 * 1024  # 10 MB
    trunk_io = TrunkIO(trunk_size=TRUNK_SIZE, len_size=8, len_byteorder='little')

    @abc.abstractmethod
    def _get_sealer(self) -> SCellSeal:
        ...

    def encrypt(self, data: bytes) -> bytes:
        sealer = self._get_sealer()
        return sealer.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        sealer = self._get_sealer()
        return sealer.decrypt(data)

    def encrypt_file_trunk(self, dst_file: BinaryIO, trunk: bytes) -> None:
        """Encrypts a trunk and saves it into file.

        NOTE: The file is not closed by this method.

        Args:
          dst_file: destination file, should be opened in writable binary mode and positioned to the starting location
        """
        trunk_enc = self.encrypt(trunk)
        self.trunk_io.write_file_trunk(dst_file=dst_file, trunk=trunk_enc)

    def decrypt_file_trunk(self, src_file: BinaryIO) -> bytes:
        """Decrypts a trunk from file.

        NOTE: The file is not closed by this method.

        Args:
          src_file: source file, should be opened in readable binary mode and positioned to the starting location
        """
        trunc_enc = self.trunk_io.read_file_trunk(src_file)
        return self.decrypt(trunc_enc)

    def encrypt_file_in_trunks(self, src_file: BinaryIO, dst_file: BinaryIO):
        """Encrypts a potentially large file in trunks.

        NOTE: The files are not closed by this method.

        Args:
          src_file: source file, should be opened in readable binary mode and positioned to the starting location
          dst_file: destination file, should be opened in writable binary mode and positioned to the starting location
        """
        self.trunk_io.proc_file_in_trunks(src_file=src_file, dst_file=dst_file,
                                          read_mode=TrunkIO.Mode.BYTES, write_mode=TrunkIO.Mode.LEN_BYTES,
                                          proc_func=self._get_sealer().encrypt)

    def decrypt_file_from_trunks(self, src_file: BinaryIO, dst_file: BinaryIO):
        """Decrypts a potentially large file from trunks.

        NOTE: The files are not closed by this method.

        Args:
          src_file: source file, should be opened in readable binary mode and positioned to the starting location
          dst_file: destination file, should be opened in writable binary mode and positioned to the starting location
        """
        self.trunk_io.proc_file_in_trunks(src_file=src_file, dst_file=dst_file,
                                          read_mode=TrunkIO.Mode.LEN_BYTES, write_mode=TrunkIO.Mode.BYTES,
                                          proc_func=self._get_sealer().decrypt)


class ClientStorageModelSealer(ModelSealerBase):
    _sealer = None
    __MODEL_CLIENT_STORAGE_DEK_SEED = 'ml:storage-client~'

    def _get_sealer(self) -> SCellSeal:
        if self._sealer is None:
            ph = self.__MODEL_CLIENT_STORAGE_DEK_SEED + '//' + get_platform_id()
            self._sealer = SCellSeal(passphrase=ph)
        return self._sealer


class ClientServerExchSealer(ModelSealerBase):
    _sealer = None
    __MODEL_CLIENT_SERVER_EXCH_DEK_SEED = 'ml-Client-Server-##$##-enc'

    def _get_sealer(self) -> SCellSeal:
        if self._sealer is None:
            ph = self.__MODEL_CLIENT_SERVER_EXCH_DEK_SEED
            self._sealer = SCellSeal(passphrase=ph)
        return self._sealer


class PeerMsgKeypair:

    def __init__(self) -> None:
        self._keypair = GenerateKeyPair(KEY_PAIR_TYPE.EC)

    @property
    def pubkey(self) -> bytes:
        return self._keypair.export_public_key()

    @property
    def privkey(self) -> bytes:
        return self._keypair.export_private_key()


class PeerMsgSealer:
    TRUNK_SIZE = 10 * 1024 * 1024  # 10 MB
    trunk_io = TrunkIO(trunk_size=TRUNK_SIZE, len_size=8, len_byteorder='little')

    def __init__(self, self_privkey: bytes, peer_pubkey: bytes) -> None:
        self._sealer = SMessage(private_key=self_privkey, peer_public_key=peer_pubkey)

    def wrap(self, data: bytes) -> bytes:
        return self._sealer.wrap(data)

    def unwrap(self, data: bytes) -> bytes:
        return self._sealer.unwrap(data)

    def wrap_file_in_trunks(self, src_file: BinaryIO, dst_file: BinaryIO):
        """Encrypts a potentially large file in trunks.

        NOTE: The files are not closed by this method.

        Args:
          src_file: source file, should be opened in readable binary mode and positioned to the starting location
          dst_file: destination file, should be opened in writable binary mode and positioned to the starting location
        """
        self.trunk_io.proc_file_in_trunks(src_file=src_file, dst_file=dst_file,
                                          read_mode=TrunkIO.Mode.BYTES, write_mode=TrunkIO.Mode.LEN_BYTES,
                                          proc_func=self._sealer.wrap)

    def unwrap_file_in_trunks(self, src_file: BinaryIO, dst_file: BinaryIO):
        """Decrypts a potentially large file in trunks.

        NOTE: The files are not closed by this method.

        Args:
          src_file: source file, should be opened in readable binary mode and positioned to the starting location
          dst_file: destination file, should be opened in writable binary mode and positioned to the starting location
        """
        self.trunk_io.proc_file_in_trunks(src_file=src_file, dst_file=dst_file,
                                          read_mode=TrunkIO.Mode.LEN_BYTES, write_mode=TrunkIO.Mode.BYTES,
                                          proc_func=self._sealer.unwrap)
