from pathlib import Path
from typing import List

from nmk.model.keys import NmkRootConfig
from nmk.model.resolver import NmkListConfigResolver
from nmk_base.common import TemplateBuilder


class ActionFileBuilder(TemplateBuilder):
    def build(self, python_versions: List[str], command: str, images: List[str]):
        # Verify if current project is building a python package
        var_name = "pythonPackage"
        has_python_package = var_name in self.model.config and len(self.model.config[var_name].resolve())
        coverage_report = (
            Path(self.model.config["pythonCoverageXmlReport"].value).relative_to(self.model.config[NmkRootConfig.PROJECT_DIR].value)
            if has_python_package
            else ""
        )

        # Create directory and build from template
        self.main_output.parent.mkdir(parents=True, exist_ok=True)
        self.build_from_template(
            self.main_input,
            self.main_output,
            {
                "pythonVersions": python_versions,
                "command": command,
                "images": images,
                "hasPythonPackage": has_python_package,
                "coverageReport": coverage_report,
            },
        )


class PythonVersionsResolver(NmkListConfigResolver):
    def get_value(self, name: str) -> List[str]:
        # If "manual" configuration is provided
        gh_versions = self.model.config["githubPythonVersions"].value
        if len(gh_versions):
            return gh_versions

        # If python plugin is present
        if "pythonSupportedVersions" in self.model.config:
            return self.model.config["pythonSupportedVersions"].value

        # Default: no version
        return []
