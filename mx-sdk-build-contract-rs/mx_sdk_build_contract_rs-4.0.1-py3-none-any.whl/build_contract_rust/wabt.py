
import json
import logging
import subprocess
from pathlib import Path
from typing import List


def generate_wabt_artifacts(wasm_file: Path):
    wat_file = wasm_file.with_suffix(".wat")
    imports_file = wasm_file.with_suffix(".imports.json")

    logging.info(f"Convert WASM to WAT: {wasm_file}")
    subprocess.check_output(["wasm2wat", str(wasm_file), "-o", str(wat_file)], shell=False, universal_newlines=True, stderr=subprocess.STDOUT)

    logging.info(f"Extract imports: {wasm_file}")
    imports_text = subprocess.check_output(["wasm-objdump", str(wasm_file), "--details", "--section", "Import"], shell=False, universal_newlines=True, stderr=subprocess.STDOUT)

    imports = _parse_imports_text(imports_text)

    with open(imports_file, "w") as f:
        json.dump(imports, f, indent=4)


def _parse_imports_text(text: str) -> List[str]:
    lines = [line for line in text.splitlines() if "func" in line and "env" in line]
    imports = [line.split(".")[-1] for line in lines]
    return imports
