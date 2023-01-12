import subprocess
from pathlib import Path
from typing import Callable


from grippy.parse import parse_rpc
from grippy.types import P, RPC, T


class App:
    def __init__(self, name: str = "Grippy", path: str = "grippy_files"):
        self.name = name
        self.services: list[RPC] = []
        self.path = Path(path)
        self.path.mkdir(exist_ok=True)

    def rpc(self, func: Callable[P, T]) -> RPC[P, T]:
        func._request_message, func._return_message = parse_rpc(func)
        self.services.append(func)
        return func

    @property
    def proto(self) -> str:
        proto = 'syntax = "proto3";\n\n'

        for func in self.services:
            proto += f"{func._request_message}\n\n{func._return_message}\n\n"

        proto += f"service {self.name} " + "{\n"
        for func in self.services:
            proto += (
                f"    rpc {func.__name__} ({func._request_message.name}) "
                f"returns ({func._return_message.name}) "
                "{};\n"
            )
        proto += "}"
        return proto

    def build(self):
        proto_file = self.path / "grippy.proto"
        proto_file.write_text(self.proto)
        subprocess.run([
            "python", "-m", "grpc_tools.protoc", f"--python_out={self.path}",
            f"--grpc_python_out={self.path}", f"-I{self.path}", str(proto_file)
        ])
