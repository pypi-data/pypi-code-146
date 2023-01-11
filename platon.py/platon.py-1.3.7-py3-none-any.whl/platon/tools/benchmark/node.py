import os
import socket
from subprocess import (
    PIPE,
    Popen,
    check_output,
)
from tempfile import (
    TemporaryDirectory,
)
from typing import (
    Any,
    Generator,
    Sequence,
)
import zipfile

from node.install import (
    get_executable_path,
    install_node,
)

from platon.tools.benchmark.utils import (
    kill_proc_gracefully,
)

NODE_FIXTURE_ZIP = "node-1.10.4-fixture.zip"


class PnodeBenchmarkFixture:
    def __init__(self) -> None:
        self.rpc_port = self._rpc_port()
        self.endpoint_uri = self._endpoint_uri()
        self.node_binary = self._node_binary()

    def build(self) -> Generator[Any, None, None]:
        with TemporaryDirectory() as base_dir:
            zipfile_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "../../../tests/integration/",
                    NODE_FIXTURE_ZIP,
                )
            )
            tmp_datadir = os.path.join(str(base_dir), "data_dir")
            with zipfile.ZipFile(zipfile_path, "r") as zip_ref:
                zip_ref.extractall(tmp_datadir)
            self.datadir = tmp_datadir

            genesis_file = os.path.join(self.datadir, "genesis.json")

            yield self._node_process(self.datadir, genesis_file, self.rpc_port)

    def _rpc_port(self) -> str:
        sock = socket.socket()
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
        sock.close()
        return str(port)

    def _endpoint_uri(self) -> str:
        return "http://localhost:{0}".format(self.rpc_port)

    def _node_binary(self) -> str:
        if "NODE_BINARY" in os.environ:
            return os.environ["NODE_BINARY"]
        elif "NODE_VERSION" in os.environ:
            node_version = os.environ["NODE_VERSION"]
            _node_binary = get_executable_path(node_version)
            if not os.path.exists(_node_binary):
                install_node(node_version)
            assert os.path.exists(_node_binary)
            return _node_binary
        else:
            return "node"

    def _node_command_arguments(self, datadir: str) -> Sequence[str]:
        return (
            self.node_binary,
            "--data_dir",
            str(datadir),
            "--nodiscover",
            "--fakepow",
            "--http",
            "--http.port",
            self.rpc_port,
            "--http.api",
            "admin,platon,net,platon,personal,miner",
            "--ipcdisable",
            "--allow-insecure-unlock",
        )

    def _node_process(
        self, datadir: str, genesis_file: str, rpc_port: str
    ) -> Generator[Any, None, None]:
        init_datadir_command = (
            self.node_binary,
            "--data_dir",
            str(datadir),
            "init",
            str(genesis_file),
        )
        check_output(
            init_datadir_command, stdin=PIPE, stderr=PIPE,
        )
        proc = Popen(
            self._node_command_arguments(datadir),
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
        )
        try:
            yield proc
        finally:
            kill_proc_gracefully(proc)
