"""
Process zip source
"""
import pathlib
import zipfile
from typing import ByteString
from typing import Tuple

__virtualname__ = "zip"

MIMETYPES = ["application/zip", "application/x-zip-compressed", "zip", ".zip"]


async def cache(
    hub, ctx, protocol: str, source: str, location: str
) -> Tuple[str, ByteString]:
    if zipfile.is_zipfile(source):
        zip_source = zipfile.ZipFile(source)

        try:
            # Normalize the path within the zipfile, it will always be a posix style path, even on windows
            location = pathlib.Path(location).as_posix()
            # This could be integrated with acct to read encrypted archives
            contents = zip_source.read(location, pwd=None)
            # Store the contents of the zip file in memory
            # Use <source>/<sls file> as the unique sls_ref
            return f"{source}/{location}", contents
        except KeyError:
            ...
