from pathlib import Path
from typing import Dict, Any, Set
import json
import subprocess

from EVMVerifier.Compiler.CompilerCollector import CompilerCollector, CompilerLang
from Shared.certoraUtils import Singleton
from Shared.certoraUtils import print_failed_to_run


class CompilerLangVy(CompilerLang, metaclass=Singleton):
    """
    [CompilerLang] for Vyper.
    """
    _compiler_name: str = "vyper"

    @property
    def name(self) -> str:
        return "Vyper"

    @property
    def compiler_name(self) -> str:
        return self._compiler_name

    @staticmethod
    def normalize_func_hash(func_hash: str) -> str:
        try:
            return hex(int(func_hash, 16))
        except ValueError:
            raise Exception(f'{func_hash} is not convertible to hexadecimal')

    @staticmethod
    def normalize_file_compiler_path_name(file_abs_path: str) -> str:
        if not file_abs_path.startswith('/'):
            return '/' + file_abs_path
        return file_abs_path

    @staticmethod
    def normalize_deployed_bytecode(deployed_bytecode: str) -> str:
        assert deployed_bytecode.startswith("0x"), f'expected {deployed_bytecode} to have hexadecimal prefix'
        return deployed_bytecode[2:]

    @staticmethod
    def get_contract_def_node_ref(contract_file_ast: Dict[int, Any], contract_file: str, contract_name: str) -> \
            int:
        # in vyper, "ContractDefinition" is "Module"
        denormalized_contract_file = contract_file[1:] if contract_file.startswith('/') else contract_file
        contract_def_refs = list(filter(
            lambda node_id: contract_file_ast[node_id].get("ast_type") == "Module" and
            (contract_file_ast[node_id].get("name") == contract_file, contract_file_ast) or
            contract_file_ast[node_id].get("name") == denormalized_contract_file, contract_file_ast))
        assert len(contract_def_refs) != 0, \
            f'Failed to find a "Module" ast node id for the file {contract_file}'
        assert len(contract_def_refs) == 1, f'Found multiple "Module" ast node ids for the same file' \
            f'{contract_file}: {contract_def_refs}'
        return contract_def_refs[0]

    @staticmethod
    def compilation_output_path(sdc_name: str, config_path: Path) -> Path:
        return config_path / f"{sdc_name}"

    # Todo - add this for Vyper too and make it a CompilerLang class method one day
    @staticmethod
    def compilation_error_path(sdc_name: str, config_path: Path) -> Path:
        return config_path / f"{sdc_name}.standard.json.stderr"

    @staticmethod
    def all_compilation_artifacts(sdc_name: str, config_path: Path) -> Set[Path]:
        """
        Returns the set of paths for all files generated after compilation.
        """
        return {CompilerLangVy.compilation_output_path(sdc_name, config_path),
                CompilerLangVy.compilation_error_path(sdc_name, config_path)}

    @staticmethod
    def collect_storage_layout_info(file_abs_path: str,
                                    config_path: Path,
                                    compiler_cmd: str,
                                    data: Dict[str, Any]) -> Dict[str, Any]:
        output_file_name = f'{config_path}.storage.layout'
        stdout_name = output_file_name + '.stdout'
        stderr_name = output_file_name + '.stderr'
        args = [compiler_cmd, '-f', 'layout', '-o', output_file_name, file_abs_path]
        with Path(stdout_name).open('w+') as stdout:
            with Path(stderr_name).open('w+') as stderr:
                try:
                    subprocess.run(args, stdout=stdout, stderr=stderr).returncode
                    with Path(output_file_name).open('r') as output_file:
                        json_dict = json.load(output_file)
                except Exception as e:
                    print(f'Error: {e}')
                    print_failed_to_run(compiler_cmd)
                    raise
        storage_field = [{'label': l,
                          'slot': str(json_dict['storage_layout'][l]['slot']),
                          'offset': '0',
                          'type': json_dict['storage_layout'][l]['type']} for l in json_dict['storage_layout'].keys()]
        types_field = {x['type']: {'numberOfBytes': '32', 'encoding': 'inplace', 'label': 'address'}
                       for x in storage_field}
        contract_name = list(data['contracts'][file_abs_path].keys())[0]
        data['contracts'][file_abs_path][contract_name]['storageLayout'] = {'storage': storage_field,
                                                                            'types': types_field}
        return data

    @staticmethod
    def get_supports_imports() -> bool:
        return False


class CompilerCollectorVy(CompilerCollector):

    @property
    def compiler_name(self) -> str:
        return self.smart_contract_lang.compiler_name

    @property
    def smart_contract_lang(self) -> CompilerLangVy:
        return CompilerLangVy()

    @property
    def compiler_version(self) -> str:
        return "vyper"  # TODO implement to return a valid version
