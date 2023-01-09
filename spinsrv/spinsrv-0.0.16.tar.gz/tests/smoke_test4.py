import os

from spinsrv import spinfs

if "SPINPY_TEST_PUBLIC" not in os.environ:
    raise ValueError("must specify SPINPY_TEST_PUBLIC environment variable")
if "SPINPY_TEST_PRIVATE" not in os.environ:
    raise ValueError("must specify SPINPY_TEST_PRIVATE environment variable")
if "SPINPY_TEST_CITIZEN" not in os.environ:
    raise ValueError("must specify SPINPY_TEST_CITIZEN environment variable")
SPINPY_TEST_PUBLIC = os.environ["SPINPY_TEST_PUBLIC"]
SPINPY_TEST_PRIVATE = os.environ["SPINPY_TEST_PRIVATE"]
SPINPY_TEST_CITIZEN = os.environ["SPINPY_TEST_CITIZEN"]

print("THIS IS SMOKE TEST 4: IT TESTS A CHUNKED UPLOAD")

fs = spinfs.SpinFileSystem(
    spinfs.Config(
        public=SPINPY_TEST_PUBLIC,
        private=SPINPY_TEST_PRIVATE,
        citizen=SPINPY_TEST_CITIZEN,
    )
)
import shutil

src = open("./tests/test.mp4", "rb")
dst = fs.open("/test.mp4", "wb")
shutil.copyfileobj(src, dst)
src.close()
dst.close()
resp = fs.rm("/test.mp4")
