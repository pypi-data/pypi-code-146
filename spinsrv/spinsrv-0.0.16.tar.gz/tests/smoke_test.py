import hashlib
import json
import os

from spinsrv import spin
from spinsrv import spinpy as sp

if "SPINPY_TEST_PUBLIC" not in os.environ:
    raise ValueError("must specify SPINPY_TEST_PUBLIC environment variable")
if "SPINPY_TEST_PRIVATE" not in os.environ:
    raise ValueError("must specify SPINPY_TEST_PRIVATE environment variable")
if "SPINPY_TEST_CITIZEN" not in os.environ:
    raise ValueError("must specify SPINPY_TEST_CITIZEN environment variable")
SPINPY_TEST_PUBLIC = os.environ["SPINPY_TEST_PUBLIC"]
SPINPY_TEST_PRIVATE = os.environ["SPINPY_TEST_PRIVATE"]
SPINPY_TEST_CITIZEN = os.environ["SPINPY_TEST_CITIZEN"]

print("THIS IS SMOKE TEST 1: IT TESTS THE CLIENTS IN src/spin/spinpy.py")

kc = sp.KeyServerHTTPClient()
resp = kc.which(
    spin.KeyWhichRequest(
        public=SPINPY_TEST_PUBLIC,
        private=SPINPY_TEST_PRIVATE,
    )
)
print(resp)
resp = kc.temp(
    spin.KeyTempRequest(
        public=SPINPY_TEST_PUBLIC,
        private=SPINPY_TEST_PRIVATE,
        duration=60000000000,
    )
)
print(resp)

dc = sp.DirServerHTTPClient()
resp = dc.tree(
    spin.DirTreeRequest(
        public=SPINPY_TEST_PUBLIC,
        private=SPINPY_TEST_PRIVATE,
        citizen=SPINPY_TEST_CITIZEN,
        path="/",
        level=0,
    )
)
print(resp)
resp = dc.tree(
    spin.DirTreeRequest(
        public=SPINPY_TEST_PUBLIC,
        private=SPINPY_TEST_PRIVATE,
        citizen=SPINPY_TEST_CITIZEN,
        path="/",
        level=1,
    )
)
print(resp)

resp = dc.apply(
    spin.DirApplyRequest(
        public=SPINPY_TEST_PUBLIC,
        private=SPINPY_TEST_PRIVATE,
        ops=[
            spin.DirOp(
                type=spin.PutDirOperation,
                entry=spin.DirEntry(
                    type=spin.EntryDir,
                    citizen="",
                    path="/test",
                    sequence=spin.SeqIgnore,
                ),
            )
        ],
    )
)
print(resp)

bc = sp.BitServerHTTPClient()
data = "Asdf".encode()
resp = bc.apply(
    spin.BitApplyRequest(
        public=SPINPY_TEST_PUBLIC,
        private=SPINPY_TEST_PRIVATE,
        ops=[
            spin.BitOp(
                type=spin.PutBitOperation,
                ref=spin.SHA256(data),
                bytes=data,
            )
        ],
    )
)
print(resp)
