from typing import List

from nmk_base.common import TemplateBuilder


class ActionFileBuilder(TemplateBuilder):
    def build(self, python_versions: List[str], command: str, images: List[str]):
        # Verify if current project is building a python package
        var_name = "pythonPackage"
        has_python_package = var_name in self.model.config and len(self.model.config[var_name].resolve())

        # Create directory and build from template
        self.main_output.parent.mkdir(parents=True, exist_ok=True)
        self.build_from_template(
            self.main_input, self.main_output, {"pythonVersions": python_versions, "command": command, "images": images, "hasPythonPackage": has_python_package}
        )
