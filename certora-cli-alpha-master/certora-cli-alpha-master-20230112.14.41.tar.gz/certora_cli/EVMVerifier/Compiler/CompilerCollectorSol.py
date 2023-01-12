from pathlib import Path
from typing import Any, Tuple, Dict, Set

from EVMVerifier.Compiler.CompilerCollector import CompilerLang, CompilerCollector
from Shared.certoraUtils import Singleton


class CompilerLangSol(CompilerLang, metaclass=Singleton):
    """
    [CompilerLang] for Solidity.
    """

    @property
    def name(self) -> str:
        return "Solidity"

    @property
    def compiler_name(self) -> str:
        return "solc"

    @staticmethod
    def get_contract_def_node_ref(contract_file_ast: Dict[int, Any], contract_file: str, contract_name: str) -> \
            int:
        contract_def_refs = list(filter(
            lambda node_id: contract_file_ast[node_id].get("nodeType") == "ContractDefinition" and
            contract_file_ast[node_id].get("name") == contract_name, contract_file_ast))
        assert len(contract_def_refs) != 0, \
            f'Failed to find a "ContractDefinition" ast node id for the contract {contract_name}'
        assert len(
            contract_def_refs) == 1, f'Found multiple "ContractDefinition" ast node ids for the same contract ' \
                                     f'{contract_name}: {contract_def_refs}'
        return contract_def_refs[0]

    @staticmethod
    def compilation_output_path(sdc_name: str, config_path: Path) -> Path:
        return config_path / f"{sdc_name}.standard.json.stdout"

    @staticmethod
    def get_supports_imports() -> bool:
        return True

    # Todo - add this for Vyper too and make it a CompilerLang class method one day
    @staticmethod
    def compilation_error_path(sdc_name: str, config_path: Path) -> Path:
        return config_path / f"{sdc_name}.standard.json.stderr"

    @staticmethod
    def all_compilation_artifacts(sdc_name: str, config_path: Path) -> Set[Path]:
        """
        Returns the set of paths for all files generated after compilation.
        """
        return {CompilerLangSol.compilation_output_path(sdc_name, config_path),
                CompilerLangSol.compilation_error_path(sdc_name, config_path)}


# This class is intended for calculations of compiler-settings related queries
class CompilerCollectorSol(CompilerCollector):

    def __init__(self, version: Tuple[int, int, int], solc_flags: str = ""):
        self._compiler_version = version
        self._optimization_flags = solc_flags   # optimize, optimize_runs, solc_mapping

    @property
    def compiler_name(self) -> str:
        return self.smart_contract_lang.compiler_name

    @property
    def smart_contract_lang(self) -> CompilerLangSol:
        return CompilerLangSol()

    @property
    def compiler_version(self) -> Tuple[int, int, int]:
        return self._compiler_version

    @property
    def optimization_flags(self) -> str:
        return self._optimization_flags

    def normalize_storage(self, is_storage: bool, arg_name: str) -> str:
        if not is_storage:
            return arg_name
        if self._compiler_version[0] == 0 and self._compiler_version[1] < 7:
            return arg_name + "_slot"
        else:
            return arg_name + ".slot"

    def supports_calldata_assembly(self, arg_name: str) -> bool:
        return (self._compiler_version[1] > 7 or (
                self._compiler_version[1] == 7 and self._compiler_version[2] >= 5)) and arg_name != ""
