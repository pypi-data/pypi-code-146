from pathlib import Path
import platform

HOME_DIR = Path.home()

CARGO_DIR = HOME_DIR.joinpath(".cargo")
CARGO_ARTIFACTS_DIR = HOME_DIR.joinpath(".cargo/bin")
SOLC_SELECT_DIR = HOME_DIR.joinpath(".ziion-solc-select")
SOLC_ARTIFACTS_DIR = HOME_DIR.joinpath(".solcx")

S3_BUCKET_URL="https://ziion-binaries.s3.amazonaws.com/"
CARGO_AMD_FOLDER_S3="rust-amd-binaries/"
CARGO_ARM_FOLDER_S3="rust-amd-binaries/"
SOLC_ARM_FOLDER_S3="solc-arm-binaries/"

if platform.machine() == 'x86_64':
    METAPACKAGES = {
        "cargo": "cargo"
        }
elif platform.machine() == 'aarch64':
    METAPACKAGES = {
        "cargo": "cargo",
        "solc": "solc"
        }