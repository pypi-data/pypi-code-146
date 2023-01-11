import base64, io, logging, os, sys, requests
from zstd import compress, decompress  # type: ignore
from hashlib import sha1
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
from typing import NamedTuple, cast

from .local_config import getCacheDir

logger = logging.getLogger(__name__)


class EncryptedObjectInfo(NamedTuple):
  contentHash: str
  signedDataUrl: str
  key64: str
  iv64: str
  objectExists: bool


def calcHash(content: bytes) -> str:
  return f"sha1:{sha1(content).hexdigest()}"


def objectCacheFilePath(workspaceId: str, contentHash: str) -> str:
  contentHash = contentHash.replace(":", "_")
  return os.path.join(getCacheDir(workspaceId, "largeFiles"), f"{contentHash}.zstd.enc")


def putSecureData(oui: EncryptedObjectInfo, obj: bytes, desc: str) -> None:
  data = cast(bytes, compress(obj, 10))

  cipher = AES.new(  # type: ignore
      mode=AES.MODE_CBC, key=base64.b64decode(oui.key64), iv=base64.b64decode(oui.iv64))
  body = cipher.encrypt(pad(data, AES.block_size))

  with io.BytesIO(body) as b:
    with tqdm(total=len(data),
              unit='B',
              unit_scale=True,
              miniters=1,
              desc=f"Uploading '{desc}'",
              file=sys.stderr) as t:
      wrapped_data = CallbackIOWrapper(t.update, b, "read")
      requests.put(oui.signedDataUrl, data=wrapped_data)  # type: ignore


def getSecureData(workspaceId: str, dri: EncryptedObjectInfo, desc: str) -> bytes:
  if not dri:
    raise Exception("Download info missing from API response.")
  filepath = objectCacheFilePath(workspaceId, dri.contentHash)

  if os.path.exists(filepath):  # Try cache
    try:
      return readAndDecryptFile(filepath, dri)
    except Exception as e:
      logger.info("Failed to read from cache", exc_info=e)

  downloadFile(dri, filepath, desc)
  return readAndDecryptFile(filepath, dri)


def downloadFile(dri: EncryptedObjectInfo, filepath: str, desc: str) -> None:
  logger.info(f"Downloading to {filepath}")
  resp = requests.get(dri.signedDataUrl, stream=True)
  total = int(resp.headers.get('content-length', 0))
  with open(filepath, "wb") as f, tqdm(total=total,
                                       unit='B',
                                       unit_scale=True,
                                       miniters=1,
                                       desc=f"Downloading '{desc}'",
                                       file=sys.stderr) as t:
    for data in resp.iter_content(chunk_size=32 * 1024):
      size = f.write(data)
      t.update(size)


def readAndDecryptFile(filepath: str, dri: EncryptedObjectInfo) -> bytes:
  with open(filepath, "rb") as f:
    data = f.read()
  return decryptAndValidate(dri, data)


def decryptAndValidate(dri: EncryptedObjectInfo, data: bytes) -> bytes:
  cipher = AES.new(base64.b64decode(dri.key64), AES.MODE_CBC, iv=base64.b64decode(dri.iv64))  # type: ignore
  data = unpad(cipher.decrypt(data), AES.block_size)
  data = decompress(data)
  actualHash = calcHash(data)
  if actualHash != dri.contentHash:
    raise Exception(f"Hash mismatch. Tried to fetch {dri.contentHash}, calculated {actualHash}")
  return data
