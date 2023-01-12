from pathlib import Path

HARDCODED_BUILD_DIRECTORY = Path("/tmp/contract")
HARDCODED_UNWRAP_DIRECTORY = Path("/tmp/unwrapped")
ONE_KB_IN_BYTES: int = 1024
MAX_SOURCE_CODE_ARCHIVE_SIZE: int = ONE_KB_IN_BYTES * 1024
# The output archive contains not only the *.wasm, but also *.wat, *.abi.json files etc.
MAX_OUTPUT_ARTIFACTS_ARCHIVE_SIZE: int = ONE_KB_IN_BYTES * 1024
