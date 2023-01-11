import atexit

from Shared.certoraUtils import run_solc_cmd
from pathlib import Path
from functools import lru_cache
from typing import Tuple, Dict
import re
import logging
from EVMVerifier.Compiler.CompilerCollector import CompilerLang, CompilerCollector
from EVMVerifier.Compiler.CompilerCollectorSol import CompilerCollectorSol, CompilerLangSol
from EVMVerifier.Compiler.CompilerCollectorVy import CompilerCollectorVy, CompilerLangVy
from Shared.certoraUtils import is_windows, match_path_to_mapping_key, remove_file

# logger for running the Solidity compiler and reporting any errors it emits
solc_logger = logging.getLogger("solc")


def get_relevant_solc(contract_file_path: Path, solc: str, solc_mappings: Dict[str, str]) -> str:
    """
    @param contract_file_path: the contract that we are working on
    @param solc_mappings: input arg mapping contract to solc
    @param solc: solc we want to run in case the specified file_name is not in solc_mappings
    @return: the name of the solc executable we want to run on this contract (as a string, could be a path
             or a resolvable executable name)
    """
    match = match_path_to_mapping_key(contract_file_path, solc_mappings)
    if match is not None:
        base = match
    else:
        base = solc
    if is_windows() and not base.endswith(".exe"):
        base = base + ".exe"
    solc_logger.debug(f"relevant solc is {base}")
    return base


def get_extra_solc_args(contract_path: Path, solc_args: list, optimize_map: Dict[str, str]) -> str:
    """
    Adds all args in --solc_args, if any, and the optimization found in --optimize_map, if exists.
    We assume that there are no conflicts between the two (the input was validated).
    @param contract_path: the contract that we are working on
    @param solc_args: input args optimize and optimize_runs
    @param optimize_map: input arg mapping contract to optimized number of runs
    @return str of solc args or optimizations found
    """
    extra_solc_args = ""
    if solc_args is not None:
        extra_solc_args += ' '.join(solc_args)

    match = match_path_to_mapping_key(contract_path, optimize_map)
    if match is not None:
        num_runs = match
        if int(num_runs) > 0:  # If the contract has 0 in its number of runs in the map, we skip optimizing
            extra_solc_args += f" --optimize --optimize-runs {num_runs}"
    return extra_solc_args


class CompilerCollectorFactory:
    """
    Returns [CompilerCollector] instance, based on type of the file [file_name] and the file path
    solc_args: input args optimize and optimize_runs
    optimize_map: input arg mapping contract to optimized number of runs
    solc_mappings: input arg mapping contract to solc
    solc: solc we want to run in case the specified file_name is not in solc_mappings
    config_path: path to Certora config dir
    """

    def __init__(self, solc_args: list, optimize_map: Dict[str, str], solc: str, solc_mappings: Dict[str, str],
                 config_path: Path):
        self._solc_args = solc_args
        self._optimize_map = optimize_map
        self._solc = solc
        self._solc_mappings = solc_mappings
        self._config_path = config_path

    @lru_cache(maxsize=32)
    def get_compiler_collector(self, path: Path) -> CompilerCollector:
        """
        1. Same file path will get the same compiler collector
        2. autoFinder_X file will get the compiler collector of X file
        @returns [CompilerCollector] instance, based on type of the file [file_name] and the file path
        @param path: path of the file to create [CompilerCollector] for
        """
        if str(path).endswith(".vy"):
            return CompilerCollectorVy()
        elif str(path).endswith(".sol"):
            version = self.__get_solc_version(path)
            return CompilerCollectorSol(version, get_extra_solc_args(path, self._solc_args, self._optimize_map))
        else:
            raise RuntimeError(f'expected {path} to represent a Solidity or Vyper file')

    def __get_solc_version(self, contract_file_path: Path) -> Tuple[int, int, int]:
        """
        @param contract_file_path: the contract that we are working on
        @return: the running solc version
        """
        solc_logger.debug(f"visiting contract file {contract_file_path}")
        solc_path = get_relevant_solc(contract_file_path, self._solc, self._solc_mappings)
        version = self.__get_solc_exe_version(solc_path)
        return version

    @lru_cache(maxsize=32)
    def __get_solc_exe_version(self, solc_name: str) -> Tuple[int, int, int]:
        """
        @param solc_name: name of the solc we want to run on this contract
        @return: the running solc version
        """
        out_name = f"version_check_{Path(solc_name).name}"
        stdout_path = self._config_path / f'{out_name}.stdout'
        stderr_path = self._config_path / f'{out_name}.stderr'

        # ascertain that version check output files are always deleted
        atexit.register(remove_file, stdout_path)
        atexit.register(remove_file, stderr_path)

        run_solc_cmd(
            f"{solc_name} --version",
            output_file_name=out_name, config_path=self._config_path)

        with stdout_path.open() as r:
            version_string = r.read(-1)
        version_matches = [(int(m.group(1)), int(m.group(2)), int(m.group(3))) for m in
                           [re.match(r'^(\d+)\.(\d+).(\d+)', l[len("Version: "):]) for l in
                            version_string.splitlines() if l.startswith("Version: ")] if m is not None]
        if len(version_matches) != 1:
            msg = f"Couldn't extract Solidity version from output {version_string}, giving up"
            solc_logger.debug(msg)
            raise RuntimeError(msg)
        return version_matches[0]


def get_compiler_lang(file_name: str) -> CompilerLang:
    """
    Returns [CompilerLang] instance, based on type of the file [file_name]
    :param file_name: name of the file to create [CompilerLang] from
    """
    if file_name.endswith(".vy"):
        return CompilerLangVy()
    elif file_name.endswith(".sol"):
        return CompilerLangSol()
    else:
        raise RuntimeError(f'expected {file_name} to represent a Solidity or Vyper file')
