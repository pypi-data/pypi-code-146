
import json
from pathlib import Path
from typing import Any, Dict

from build_contract_rust.cargo_toml import get_contract_name_and_version
from build_contract_rust.filesystem import find_file_in_folder


class BuildOutcome:
    def __init__(self):
        self.contracts: Dict[str, BuildOutcomeEntry] = dict()

    def gather_artifacts(self, contract_name: str, build_directory: Path, output_subdirectory: Path):
        self.contracts[contract_name] = BuildOutcomeEntry.from_directories(build_directory, output_subdirectory)

    def get_entry(self, contract_name: str) -> 'BuildOutcomeEntry':
        return self.contracts[contract_name]

    def save_to_file(self, file: Path):
        data = self.to_dict()

        with open(file, "w") as f:
            json.dump(data, f, indent=4)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = dict()

        for key, value in self.contracts.items():
            data[key] = value.to_dict()

        return data


class BuildOutcomeEntry:
    def __init__(self) -> None:
        self.version = ""
        self.codehash = ""
        self.build_path = ""
        self.artifacts = BunchOfBuildArtifacts()

    @classmethod
    def from_directories(cls, build_directory: Path, output_directory: Path) -> 'BuildOutcomeEntry':
        entry = BuildOutcomeEntry()
        _, entry.version = get_contract_name_and_version(build_directory)

        with open(find_file_in_folder(output_directory, "*.codehash.txt")) as file:
            entry.codehash = file.read()

        entry.artifacts = BunchOfBuildArtifacts.from_output_directory(output_directory)
        return entry

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "codehash": self.codehash,
            "buildPath": self.build_path,
            "artifacts": self.artifacts.to_dict()
        }


class BunchOfBuildArtifacts:
    def __init__(self) -> None:
        self.bytecode = BuildArtifact(Path(""))
        self.text = BuildArtifact(Path(""))
        self.abi = BuildArtifact(Path(""))
        self.imports = BuildArtifact(Path(""))
        self.src_package = BuildArtifact(Path(""))
        self.src_archive = BuildArtifact(Path(""))
        self.output_archive = BuildArtifact(Path(""))

    @classmethod
    def from_output_directory(cls, output_directory: Path) -> 'BunchOfBuildArtifacts':
        artifacts = BunchOfBuildArtifacts()
        artifacts.bytecode = BuildArtifact.find_in_output("*.wasm", output_directory)
        artifacts.text = BuildArtifact.find_in_output("*.wat", output_directory)
        artifacts.abi = BuildArtifact.find_in_output("*.abi.json", output_directory)
        artifacts.imports = BuildArtifact.find_in_output("*.imports.json", output_directory)
        artifacts.src_package = BuildArtifact.find_in_output("*.source.json", output_directory)
        artifacts.src_archive = BuildArtifact.find_in_output("*-src-*.zip", output_directory)
        artifacts.src_archive = BuildArtifact.find_in_output("*-output-*.zip", output_directory)

        return artifacts

    def to_dict(self) -> Dict[str, str]:
        return {
            "bytecode": self.bytecode.path.name,
            "text": self.text.path.name,
            "abi": self.abi.path.name,
            "imports": self.imports.path.name,
            "srcPackage": self.src_package.path.name,
            "srcArchive": self.src_archive.path.name,
            "outputArchive": self.output_archive.path.name
        }


class BuildArtifact:
    def __init__(self, path: Path) -> None:
        self.path = path

    @classmethod
    def find_in_output(cls, name_pattern: str, output_directory: Path) -> 'BuildArtifact':
        path = find_file_in_folder(output_directory, name_pattern)
        return BuildArtifact(path)

    def read(self) -> bytes:
        with open(self.path, "rb") as f:
            return f.read()
