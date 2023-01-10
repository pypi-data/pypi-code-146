import shutil
import subprocess
import sys
from typing import Dict

from nmk.model.builder import NmkTaskBuilder
from nmk.model.keys import NmkRootConfig


class PytestBuilder(NmkTaskBuilder):
    def build(self, pytest_args: Dict[str, str]):
        # Clean outputs
        for p in self.outputs:
            if p.is_dir():
                shutil.rmtree(p)
            elif p.is_file():  # pragma: no cover
                p.unlink()

        # Compute extra args
        args = []
        for opt_k, opt_v in pytest_args.items():
            if isinstance(opt_v, bool):
                if opt_v:
                    # Simple option
                    args.append(f"--{opt_k}")
            else:
                # Key + value
                args.append(f"--{opt_k}={opt_v}")

        # Invoke pytest
        subprocess.run([sys.executable, "-m", "pytest"] + args, check=True, cwd=self.model.config[NmkRootConfig.PROJECT_DIR].value)
