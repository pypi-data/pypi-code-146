import logging
import sys
from typing import BinaryIO, Callable, List, NoReturn, Optional, Tuple, Iterator

logger = logging.getLogger(__name__)
FLUSH_PACKET = b"0000"


def passThrough(pathname, content: bytes) -> bytes:
  return content


def toPkts(s: bytes) -> Iterator[bytes]:
  size = len(s)
  offset = 0
  limit = min(size, 65516)
  while offset < size:
    yield b"%04x%s" % (limit + 4, s[offset:offset + limit])
    offset += limit
    limit = min(size - offset, 65516)


class GitProtocolBase:
  """ Implements git-protocol. To aid debugging export GIT_TRACE_PACKET=1
      Roughly, a packet-based protocol. Each packet starts with 4 hex digits specifying
      the length.
      https://github.com/git/git/blob/master/Documentation/gitprotocol-common.txt
  """

  def __init__(self, inStream: BinaryIO = sys.stdin.buffer, outStream: BinaryIO = sys.stdout.buffer):
    self.inStream = inStream
    self.outStream = outStream

  def write(self, b) -> None:
    if b is FLUSH_PACKET:
      self.outStream.write(b)
    else:
      for pkt in toPkts(b):
        self.outStream.write(pkt)
    self.outStream.flush()

  def readKVData(self) -> List[Tuple[str, str]]:
    data = []
    while True:
      sizeHex = self.inStream.read(4)
      if len(sizeHex) == 0:
        raise EOFError
      size = int(sizeHex, 16)
      if size == 0:
        break
      pkt = self.inStream.read(size - 4)
      if b"=" in pkt:
        (k, v) = parseKv(pkt)
        data.append((k, v))
    return data

  def readBinaryData(self) -> bytes:
    data = b''
    while True:
      size = int(self.inStream.read(4), 16)
      if size == 0:
        break
      data += self.inStream.read(size - 4)
    return data


class GitProtocol(GitProtocolBase):

  def __init__(self,
               smudge: Optional[Callable[[str, bytes], bytes]] = None,
               clean: Optional[Callable[[str, bytes], bytes]] = None):
    super().__init__()
    self.smudge = smudge if smudge is not None else passThrough
    self.clean = clean if clean is not None else passThrough

  def versionHandshake(self) -> None:
    [version] = self.readKVData()
    # TODO: Process handshake
    self.write(b"git-filter-server\n")
    self.write(b"version=2\n")
    self.write(FLUSH_PACKET)

  def capabilitiesHandshake(self) -> None:
    caps = self.readKVData()
    # TODO: Process capabilities
    self.write(b"capability=clean\n")
    self.write(b"capability=smudge\n")
    # TODO: Support delay to allow parallel file downloads
    # self.write(b"capability=delay\n")
    self.write(FLUSH_PACKET)

  def readCommand(self) -> Tuple[str, str, bytes]:
    hdr = dict(self.readKVData())
    command = hdr["command"].strip()
    pathname = hdr["pathname"].strip()
    content = self.readBinaryData()
    return (command, pathname, content)

  def writeSuccess(self, content: Optional[bytes]) -> None:
    self.write(b"status=success\n")
    self.write(FLUSH_PACKET)
    if content and len(content):
      self.write(content)
    self.write(FLUSH_PACKET)
    self.write(FLUSH_PACKET)

  def writeError(self) -> None:
    self.write(b"status=error\n")
    self.write(FLUSH_PACKET)

  def filterProcess(self) -> NoReturn:
    """ https://git-scm.com/docs/gitattributes#_long_running_filter_process """
    try:
      self.versionHandshake()
      self.capabilitiesHandshake()

      while True:
        command, pathname, content = self.readCommand()
        try:
          if command == "clean":
            res = self.clean(pathname, content)
            self.writeSuccess(res)
          elif command == "smudge":
            res = self.smudge(pathname, content)
            self.writeSuccess(res)
        except Exception as e:
          logger.error(f"Error processing {command} on {pathname}", exc_info=e)
          self.writeError()
    except EOFError:
      exit(0)


def parseKv(s: bytes) -> Tuple[str, str]:
  [k, v] = s.split(b"=", 1)
  return (k.decode("utf-8"), v.decode("utf-8"))
