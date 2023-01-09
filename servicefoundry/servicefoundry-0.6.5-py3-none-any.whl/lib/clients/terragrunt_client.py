import json
import os
from shutil import which

from servicefoundry.lib.binarydownloader import BinaryDependencies, BinaryName
from servicefoundry.lib.clients.shell_client import Shell


class Terragrunt:
    def __init__(self) -> None:
        self.terragrunt_output_cache = {}

    def apply_all(self, dir):
        print(
            Shell().execute_shell_command(
                [
                    BinaryDependencies().which(BinaryName.TERRAGRUNT),
                    "run-all",
                    "apply",
                    "--terragrunt-non-interactive",
                    f"--terragrunt-working-dir={dir}",
                    f"--terragrunt-tfpath={BinaryDependencies().which(BinaryName.TERRAFORM)}",
                ]
            )
        )

    def fetch_terragrunt_output(self, dir, path):
        if dir in self.terragrunt_output_cache:
            return self.terragrunt_output_cache[dir][path]["value"]

        current_dir = os.getcwd()
        os.chdir(dir)
        v = Shell().execute_shell_command(
            [
                BinaryDependencies().which(BinaryName.TERRAGRUNT),
                "output",
                f"--terragrunt-working-dir={dir}",
                f"--terragrunt-tfpath={BinaryDependencies().which(BinaryName.TERRAFORM)}",
                "--json",
            ]
        )
        os.chdir(current_dir)

        self.terragrunt_output_cache[dir] = json.loads(v)
        return self.terragrunt_output_cache[dir][path]["value"]
