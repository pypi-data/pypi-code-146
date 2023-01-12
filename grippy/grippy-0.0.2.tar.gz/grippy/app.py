import subprocess
import sys
from concurrent import futures
from pathlib import Path
from typing import Callable, ParamSpec, TypeVar

import grpc

from grippy.import_helpers import GrippyLoader
from grippy.parse import parse_rpc
from grippy.types import RPC

T = TypeVar('T')
P = ParamSpec('P')


class App:
    def __init__(self, name: str = "Grippy", path: str = "grippy_files"):
        self.name = name
        self.services: list[RPC] = []
        self.path = Path(path)
        self.path.mkdir(exist_ok=True)
        self.proto_file = self.path / "grippy.proto"

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
        self.proto_file.write_text(self.proto)
        subprocess.run([
            "python", "-m", "grpc_tools.protoc", f"--python_out={self.path}",
            f"--grpc_python_out={self.path}", f"-I{self.path}", self.proto_file
        ])
        sys.meta_path.insert(0, GrippyLoader(self.path))

    def run(self):
        import grippy_pb2
        import grippy_pb2_grpc

        class Grippy(grippy_pb2_grpc.GrippyServicer):
            pass

        for func in self.services:
            def servicer(self, request, context):
                return getattr(grippy_pb2, f"{func.__name__}Response")(
                    return_val=func(**{
                        f.name: getattr(request, f.name)
                        for f in func._request_message.fields
                    })
                )
            setattr(Grippy, func.__name__, servicer)

        port = '50051'
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        grippy_pb2_grpc.add_GrippyServicer_to_server(Grippy(), server)
        server.add_insecure_port('[::]:' + port)
        server.start()
        print("Server started, listening on " + port)
        server.wait_for_termination()
