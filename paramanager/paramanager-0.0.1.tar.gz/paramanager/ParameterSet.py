import sys
from datetime import datetime

from .ProtoParameter import ProtoParameter
from .Parameter import Parameter

VERSION_PREFIX = "v-"
NAME_PREFIX = "# "


def get_versions_of_file(lines: list[str]):
    versions = []
    for i, line in enumerate(lines):
        if line.startswith(VERSION_PREFIX):
            versions.append((parse_version_line(line), i))
    return versions


def parse_version_line(line: str):
    line = line.removeprefix(VERSION_PREFIX)
    while line.endswith("\n"):
        line = line.removesuffix("\n")

    return int(line)


def get_last_index_of_version(lines: list[str], version: int):
    versions = get_versions_of_file(lines)

    if not versions:
        return 0

    for v, i in reversed(versions):
        if v == version:
            return i


def get_last_version_of_file(lines: list[str]):
    versions = get_versions_of_file(lines)
    if not versions:
        return 0

    v, _ = versions[len(versions) - 1]
    return v


def is_end_line(line: str):
    return "!" in line


def read_file_lines(filename: str):
    try:
        file = open(filename, "r")
        lines = file.readlines()
        file.close()
        return lines
    except FileNotFoundError:
        return []


class ParameterSet:
    def __init__(self, proto_parameters: list[ProtoParameter], name: str = None, read_version: int = None):
        self.proto_parameters: list[ProtoParameter] = proto_parameters
        self.name: str = name
        self.read_version: ProtoParameter = ProtoParameter("read_version", read_version, int)
        self.parameters: dict[str, Parameter] = {}

        self.update_parameters()

    def __str__(self):
        return f"{[str(p) for p in self.parameters.values()]}"

    def update_parameters(self):
        for p in self.proto_parameters:
            self.parameters[p.name] = p()

    def put(self, name: str, val: str):
        for p in self.proto_parameters:
            if name not in p.pseudonyms:
                continue
            p.set_value(val)
            self.parameters[p.name] = p()


    def get(self, parameter_name: str):
        if parameter_name in self.parameters:
            return self.parameters[parameter_name].value

    def write_file(self, filename: str):
        version = get_last_version_of_file(read_file_lines(filename)) + 1

        file = open(filename, 'a')
        if self.name:
            file.write(f"\n{NAME_PREFIX}{self.name}\n")
        file.write(f'{VERSION_PREFIX}{version}\n')
        file.write(f"t-{datetime.now().strftime('%d/%m/%Y %H-%M-%S')}\n\n")

        file.writelines([f"{p}\n" for p in self.parameters.values()])
        file.write("!\n")
        file.close()

    def read_argv(self):
        args = sys.argv[1:]
        for name, val in [(args[i], args[i+1]) for i in range(0, len(args), 2)]:
            if name == "-read":
                self.read_file(val)
            if name == "-version":
                self.read_version.set_value(val)

            if not name.startswith("-"):
                continue
            self.put(name.removeprefix("-"), val)

    def read_line(self, line: str):
        line.replace(" ", "")

        if ":" not in line:
            return
        if len(line.split(":")) != 2:
            return

        self.put(*line.split(":"))

    def read_file(self, filename: str):
        lines = read_file_lines(filename)
        if not lines:
            print(f"Attempt to read empty/nonexistent file '{filename}'")
            return

        read_version = self.read_version().value
        start = get_last_index_of_version(lines, read_version) if read_version else 0
        for line in lines[start:]:
            if is_end_line(line):
                return
            self.read_line(line)
