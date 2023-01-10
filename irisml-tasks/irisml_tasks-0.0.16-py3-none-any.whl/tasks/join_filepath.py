import dataclasses
import pathlib
import irisml.core


class Task(irisml.core.TaskBase):
    """Join a given dir_path and a filename.

    Config:
        dir_path (pathlib.Path): Directory path.
        filename (str): A filename.

    Outputs:
        path (pathlib.Path): Joined filepath.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Config:
        dir_path: pathlib.Path
        filename: str

    @dataclasses.dataclass
    class Outputs:
        path: pathlib.Path

    def execute(self, inputs):
        return self.Outputs(self.config.dir_path / self.config.filename)

    def dry_run(self, inputs):
        return self.execute(inputs)
