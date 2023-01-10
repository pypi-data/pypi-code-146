import shutil
from configparser import ConfigParser
from pathlib import Path
from typing import List, Union

from nmk.model.resolver import NmkListConfigResolver
from nmk_base.common import TemplateBuilder

LIST_SEPARATOR = "\n"


class PythonSupportedVersionsResolver(NmkListConfigResolver):
    def get_value(self, name: str) -> List[str]:
        # Get min/max values, and verify consistency
        min_ver, max_ver = self.model.config["pythonMinVersion"].value, self.model.config["pythonMaxVersion"].value
        min_split, max_split = list(map(int, min_ver.split("."))), list(map(int, max_ver.split(".")))
        prefix = "Inconsistency in python min/max supported versions: "
        assert len(min_split) == len(max_split), prefix + "not the same segments count"
        assert len(min_split) == 2, prefix + "can only deal with X.Y versions (2 segments expected)"
        assert min_split[0] == max_split[0], prefix + "can't deal with different major versions"
        assert max_split[1] > min_split[1], prefix + "max isn't greater than min"

        # Iterate and return versions range
        return [f"{min_split[0]}.{sub}" for sub in range(min_split[1], max_split[1] + 1)]


class PythonSetupBuilder(TemplateBuilder):
    def handle_ini_values(self, values: Union[str, List[str]]):
        # Turn list into a single block of text values
        return (LIST_SEPARATOR + LIST_SEPARATOR.join([self.relative_path(str(v)) for v in values])) if isinstance(values, list) else values

    def build(self, setup_py_template: str, setup_cfg_files: List[str], setup_items: dict):
        # Copy setup.py
        setup_py_output = self.outputs[0]
        shutil.copyfile(Path(setup_py_template), setup_py_output)

        # Merge setup fragments to generate final setup
        setup_cfg_output = self.outputs[1]
        c = ConfigParser()
        for f_path in map(Path, setup_cfg_files):
            # Update config with rendered template
            c.read_string(self.render_template(f_path, {}))

        # Iterate on items contributed through yml project files (only ones contributing maps)
        for section, values in filter(lambda t: isinstance(t[1], dict), setup_items.items()):
            # Create new section is not done yet
            if not c.has_section(section):
                c.add_section(section)

            # Handle list of values
            prepared_values = {k: self.handle_ini_values(v) for k, v in values.items()}

            # Finally update section values
            c[section].update(prepared_values)

        # Finally write config to output file
        with setup_cfg_output.open("w") as f:
            c.write(f)
