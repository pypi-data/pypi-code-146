import io
import os
import tarfile
from pathlib import Path
from typing import ByteString
from typing import Tuple

import msgpack
from cryptography.fernet import Fernet

MIMETYPES = [".epkg", "epkg"]

"""
Process encrypted archive source
"""

__virtualname__ = "epkg"


def __init__(hub):
    hub.source.file.ACCT = ["file"]


async def cache(
    hub, ctx, protocol: str, source: str, location: str
) -> Tuple[str, ByteString]:
    # name of epkg and key name (to decrypt the package) should match
    source_path = Path(source)
    key = source_path.stem
    # Normalize the location so that it can be matched with member name
    location = location.replace(os.sep, ".")
    f = Fernet(ctx.acct.get(key))

    with open(source, "rb") as rfh:
        data = msgpack.loads(rfh.read())

    decrypted_data = f.decrypt(data["token"])
    raw = io.BytesIO(decrypted_data)

    with tarfile.open(fileobj=raw, mode="r:xz") as tar:
        members = tar.getmembers()

        for member in members:
            # The inner member.name will always have slashes regardless of OS
            member_name = member.name.replace("/", ".")
            if member_name.endswith(location):
                # Use the unmodified member name
                location = member.name
                break
        else:
            # Never reached the break
            return "", b""
        file = tar.extractfile(location)

        if file:
            # Use <source>/<sls file> as the unique sls_ref
            return f"{source}/{location}", file.read()
    return "", b""
