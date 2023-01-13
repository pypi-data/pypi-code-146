import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Union

from multiversx_sdk_rust_contract_builder.build_outcome import BuildOutcome
from multiversx_sdk_rust_contract_builder.cargo_toml import (
    get_contract_name_and_version, promote_cargo_lock_to_contract_directory)
from multiversx_sdk_rust_contract_builder.codehash import \
    generate_code_hash_artifact
from multiversx_sdk_rust_contract_builder.constants import (
    HARDCODED_BUILD_DIRECTORY, MAX_OUTPUT_ARTIFACTS_ARCHIVE_SIZE,
    MAX_SOURCE_CODE_ARCHIVE_SIZE)
from multiversx_sdk_rust_contract_builder.filesystem import (
    archive_directory, find_file_in_folder)
from multiversx_sdk_rust_contract_builder.packaged_source_code import \
    PackagedSourceCode
from multiversx_sdk_rust_contract_builder.source_code import \
    is_source_code_file
from multiversx_sdk_rust_contract_builder.wabt import generate_wabt_artifacts


def build_project(
        project_path: Path,
        parent_output_directory: Path,
        specific_contract: Union[Path, None],
        cargo_target_dir: Path,
        no_wasm_opt: bool) -> BuildOutcome:
    project_path = project_path.expanduser().resolve()
    parent_output_directory = parent_output_directory.expanduser().resolve()
    cargo_target_dir = cargo_target_dir.expanduser().resolve()

    outcome = BuildOutcome()
    contracts_directories = get_contracts_directories(project_path)

    # We copy the whole project folder to the build path, to ensure that all local dependencies are available.
    project_within_build_directory = copy_project_directory_to_build_directory(project_path)

    for contract_directory in sorted(contracts_directories):
        contract_name, contract_version = get_contract_name_and_version(contract_directory)
        logging.info(f"Contract = {contract_name}, version = {contract_version}")

        output_subdirectory = parent_output_directory / f"{contract_name}"
        output_subdirectory.mkdir(parents=True, exist_ok=True)

        relative_contract_directory = contract_directory.relative_to(project_path)
        build_directory = project_within_build_directory / relative_contract_directory

        if specific_contract and contract_name != specific_contract:
            logging.info(f"Skipping {contract_name}.")
            continue

        # Clean directory - useful if it contains externally-generated build artifacts
        clean_contract(build_directory)
        build_contract(build_directory, output_subdirectory, cargo_target_dir, no_wasm_opt)

        # We do not clean the "output" folder, since it will be included in one of the generated archives.
        clean_contract(build_directory, clean_output=False)

        promote_cargo_lock_to_contract_directory(build_directory, contract_directory)

        # The archives are created after build, so that Cargo.lock files are included (if previously missing).
        create_archives(contract_name, contract_version, build_directory, output_subdirectory)
        create_packaged_source_code(contract_name, contract_version, build_directory, output_subdirectory)

        outcome.gather_artifacts(contract_name, build_directory, output_subdirectory)

    return outcome


def get_contracts_directories(project_path: Path) -> List[Path]:
    directories = [project_config_json.parent for project_config_json in project_path.glob("**/elrond.json")]
    return sorted(directories)


def copy_project_directory_to_build_directory(project_directory: Path):
    shutil.rmtree(HARDCODED_BUILD_DIRECTORY, ignore_errors=True)
    HARDCODED_BUILD_DIRECTORY.mkdir()
    shutil.copytree(project_directory, HARDCODED_BUILD_DIRECTORY, dirs_exist_ok=True)
    return HARDCODED_BUILD_DIRECTORY


def clean_contract(directory: Path, clean_output: bool = True):
    logging.info(f"Cleaning: {directory}")

    # On a best-effort basis, remove directories that (usually) hold build artifacts
    shutil.rmtree(directory / "wasm" / "target", ignore_errors=True)
    shutil.rmtree(directory / "meta" / "target", ignore_errors=True)

    if clean_output:
        shutil.rmtree(directory / "output", ignore_errors=True)


def build_contract(build_directory: Path, output_directory: Path, cargo_target_dir: Path, no_wasm_opt: bool):
    cargo_output_directory = build_directory / "output"
    meta_directory = build_directory / "meta"
    cargo_lock = build_directory / "wasm" / "Cargo.lock"

    # Best-effort on passing CARGO_TARGET_DIR: both as environment variable and as meta-crate parameter.
    env = os.environ.copy()
    env["CARGO_TARGET_DIR"] = str(cargo_target_dir)

    args = ["cargo", "run", "build"]
    args.extend(["--target-dir", str(cargo_target_dir)])
    args.extend(["--no-wasm-opt"] if no_wasm_opt else [])
    # If the lock file is missing, or it needs to be updated, Cargo will exit with an error.
    # See: https://doc.rust-lang.org/cargo/commands/cargo-build.html
    args.extend(["--locked"] if cargo_lock.exists() else [])

    logging.info(f"Building: {args}")
    return_code = subprocess.run(args, cwd=meta_directory, env=env).returncode
    if return_code != 0:
        exit(return_code)

    wasm_file = find_file_in_folder(cargo_output_directory, "*.wasm")
    generate_wabt_artifacts(wasm_file)
    generate_code_hash_artifact(wasm_file)

    shutil.copytree(cargo_output_directory, output_directory, dirs_exist_ok=True)


def create_archives(contract_name: str, contract_version: str, input_directory: Path, output_directory: Path):
    source_code_archive_file = output_directory / f"{contract_name}-src-{contract_version}.zip"
    output_artifacts_archive_file = output_directory / f"{contract_name}-output-{contract_version}.zip"

    archive_directory(source_code_archive_file, input_directory, is_source_code_file)
    archive_directory(output_artifacts_archive_file, input_directory / "output")

    size_of_source_code_archive = source_code_archive_file.stat().st_size
    size_of_output_artifacts_archive = output_artifacts_archive_file.stat().st_size

    if size_of_source_code_archive > MAX_SOURCE_CODE_ARCHIVE_SIZE:
        warn_file_too_large(source_code_archive_file, size_of_source_code_archive, MAX_SOURCE_CODE_ARCHIVE_SIZE)
    if size_of_output_artifacts_archive > MAX_OUTPUT_ARTIFACTS_ARCHIVE_SIZE:
        warn_file_too_large(output_artifacts_archive_file, size_of_output_artifacts_archive, MAX_OUTPUT_ARTIFACTS_ARCHIVE_SIZE)


def warn_file_too_large(path: Path, size: int, max_size: int):
    logging.warning(f"""File is too large (this might cause issues with using downstream applications, such as the contract build verification services): 
file = {path}, size = {size}, maximum size = {max_size}""")


def create_packaged_source_code(contract_name: str, contract_version: str, input_directory: Path, output_directory: Path):
    package = PackagedSourceCode.from_folder(input_directory)
    package_path = output_directory / f"{contract_name}-{contract_version}.source.json"
    package.save_to_file(package_path)
