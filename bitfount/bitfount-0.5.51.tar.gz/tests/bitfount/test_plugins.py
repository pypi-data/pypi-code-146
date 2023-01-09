"""Tests plugin functionality."""

from importlib import import_module, reload
import inspect
from pathlib import Path
import time

from _pytest.logging import LogCaptureFixture
from _pytest.monkeypatch import MonkeyPatch
from _pytest.tmpdir import TempPathFactory
from pytest import fixture
from pytest_mock import MockerFixture

import bitfount
from bitfount.runners.config_schemas import (
    AlgorithmConfig,
    DataStructureAssignConfig,
    DataStructureConfig,
    DataStructureTableConfig,
    ModelConfig,
    ModellerConfig,
    PodConfig,
    PodDataConfig,
    PodsConfig,
    ProtocolConfig,
    TaskConfig,
)
from bitfount.runners.modeller_runner import setup_modeller_from_config
from bitfount.runners.pod_runner import setup_pod_from_config
from tests.utils.helper import get_error_logs, get_warning_logs, unit_test

BITFOUNT_DATA_MODULE_PATH = "bitfount.data"
BITFOUNT_DATASOURCES_MODULE_PATH = f"{BITFOUNT_DATA_MODULE_PATH}.datasources"
BITFOUNT_FEDERATED_MODULE_PATH = "bitfount.federated"
BITFOUNT_FEDERATED_ALGORITHM_MODULE_PATH = (
    f"{BITFOUNT_FEDERATED_MODULE_PATH}.algorithms"
)
BITFOUNT_FEDERATED_PROTOCOL_MODULE_PATH = f"{BITFOUNT_FEDERATED_MODULE_PATH}.protocols"

DUMMY_MODULE_NAME = "dummy_module"
DUMMY_SOURCE_NAME = "DummySource"
DUMMY_ALGORITHM_NAME = "DummyAlgorithm"
DUMMY_PROTOCOL_NAME = "DummyProtocol"


@unit_test
class TestDatasourcePlugins:
    """Tests datasource plugin functionality."""

    @fixture(autouse=True)
    def patch_plugins_dir(
        self, monkeypatch: MonkeyPatch, tmp_path_factory: TempPathFactory
    ) -> None:
        """Monkeypatch `BITFOUNT_PLUGIN_PATH` in bitfount.config to temporary directory.

        We must do it this way instead of by monkeypatching the `BITFOUNT_HOME`
        environment variable to avoid having to reload the `bitfount.config` module as
        this causes issues with the cache of the `_get_environment` function.
        """
        tmpdir = str(tmp_path_factory.mktemp("temp", numbered=True))
        monkeypatch.setattr(
            "bitfount.config.BITFOUNT_PLUGIN_PATH",
            Path(tmpdir) / ".bitfount/_plugins",
        )

    @fixture(scope="function")
    def plugin_suffix(self) -> str:
        """Generates a unique suffix for each plugin in this test run."""
        return str(int(time.time_ns()))  # unix nanosecond timestamp

    @fixture(scope="function")
    def dummy_module_name(self, plugin_suffix: str) -> str:
        """Generates a unique plugin module name for each plugin in this test run."""
        return f"{DUMMY_MODULE_NAME}_{plugin_suffix}"

    @fixture(scope="function")
    def dummy_source_plugin_name(self, plugin_suffix: str) -> str:
        """Generates a unique plugin source name for each plugin in this test run."""
        return f"{DUMMY_SOURCE_NAME}_{plugin_suffix}"

    @fixture(scope="function")
    def dummy_plugin(self, dummy_source_plugin_name: str) -> str:
        """Returns a dummy plugin class."""
        return inspect.cleandoc(
            f"""
        import os
        from typing import Any, Dict, Iterable, List, Optional, Union

        import numpy as np
        import pandas as pd
        from pydantic import AnyUrl

        from bitfount.data.datasources.base_source import BaseSource
        from bitfount.types import _Dtypes

        class {dummy_source_plugin_name}:

            def __init__(
                self,
                path: Union[os.PathLike, AnyUrl, str],
                read_excel_kwargs: Optional[Dict[str, Any]] = None,
                **kwargs: Any,
            ):
                ...

            def get_data(self, **kwargs: Any) -> pd.DataFrame:
                ...

            def get_values(
                self, col_names: List[str], **kwargs: Any
            ) -> Dict[str, Iterable[Any]]:
                ...

            def get_colunm(  # intentional typo
                self, col_name: str, **kwargs: Any
            ) -> Union[np.ndarray, pd.Series]:
                ...

            def get_dtypes(self, **kwargs: Any) -> _Dtypes:
                ...

            def __len__(self) -> int:
                ...
        """
        )

    @fixture(scope="function")
    def dummy_abstract_source_plugin(
        self, dummy_plugin: str, dummy_source_plugin_name: str
    ) -> str:
        """Returns a class that subclasses but doesn't fully implement BaseSource."""
        return dummy_plugin.replace(
            dummy_source_plugin_name, f"{dummy_source_plugin_name}(BaseSource)"
        )

    @fixture(scope="function")
    def dummy_source_plugin(self, dummy_abstract_source_plugin: str) -> str:
        """Returns a class that fully implements BaseSource."""
        return dummy_abstract_source_plugin.replace("get_colunm", "get_column")

    def test_no_plugins_dir_created(self) -> None:
        """Tests that the plugin directory is created if it doesn't exist.

        Also tests that it's okay for there to be no plugins within the directory.
        """
        assert bitfount.config.BITFOUNT_PLUGIN_PATH.exists() is False
        reload(bitfount.data.datasources)
        assert bitfount.config.BITFOUNT_PLUGIN_PATH.exists() is True

    def test_plugin_in_wrong_dir_gets_ignored(
        self, dummy_module_name: str, dummy_source_plugin: str
    ) -> None:
        """Tests that plugins in the wrong directory are ignored."""
        reload(bitfount.data.datasources)  # Creates the plugin directory
        # `data_sources` is intentionally the wrong directory, should be `datasources`
        dummy_plugin_path = bitfount.config.BITFOUNT_PLUGIN_PATH / "data_sources"
        dummy_plugin_path.mkdir()
        (dummy_plugin_path / f"{dummy_module_name}.py").touch()
        (dummy_plugin_path / f"{dummy_module_name}.py").write_text(dummy_source_plugin)
        reload(bitfount.data)
        reload(bitfount.data.datasources)
        datasources = import_module("bitfount.data.datasources")
        assert not hasattr(datasources, dummy_module_name)

    def test_plugin_with_error_gets_ignored(
        self,
        caplog: LogCaptureFixture,
        dummy_module_name: str,
        dummy_source_plugin: str,
    ) -> None:
        """Tests that plugins with errors are ignored."""
        # Replacing numpy import with a non-existent module to cause an error
        dummy_source_plugin = dummy_source_plugin.replace("numpy", "numpyz")
        reload(bitfount.data.datasources)  # Creates the plugin directory
        dummy_plugin_path = bitfount.config.BITFOUNT_PLUGIN_PATH / "datasources"
        (dummy_plugin_path / f"{dummy_module_name}.py").touch()
        (dummy_plugin_path / f"{dummy_module_name}.py").write_text(dummy_source_plugin)
        reload(bitfount.data)
        reload(bitfount.data.datasources)

        # Tests that the module is still imported but the class is not
        datasources = import_module(BITFOUNT_DATASOURCES_MODULE_PATH)
        data = import_module(BITFOUNT_DATA_MODULE_PATH)
        assert not hasattr(datasources, dummy_module_name)
        assert not hasattr(data, dummy_source_plugin)

        # Tests that the appropriate debug message is logged
        assert (
            f"Error importing datasource plugin {dummy_module_name}"
        ) in get_error_logs(caplog)

    def test_datasource_plugin_that_doesnt_subclass_base_source_gets_ignored(
        self, dummy_module_name: str, dummy_plugin: str, dummy_source_plugin_name: str
    ) -> None:
        """Tests that plugins that don't subclass BaseSource are ignored."""
        reload(bitfount.data.datasources)  # Creates the plugin directory
        dummy_plugin_path = bitfount.config.BITFOUNT_PLUGIN_PATH / "datasources"
        (dummy_plugin_path / f"{dummy_module_name}.py").touch()
        (dummy_plugin_path / f"{dummy_module_name}.py").write_text(dummy_plugin)
        reload(bitfount.data)
        reload(bitfount.data.datasources)

        # Tests that the module is still imported but the class is not
        datasources = import_module(BITFOUNT_DATASOURCES_MODULE_PATH)
        data = import_module(BITFOUNT_DATA_MODULE_PATH)
        assert hasattr(datasources, dummy_module_name)
        assert not hasattr(data, dummy_source_plugin_name)

    def test_datasource_plugin_that_doesnt_implement_base_source_gets_ignored(
        self,
        caplog: LogCaptureFixture,
        dummy_abstract_source_plugin: str,
        dummy_module_name: str,
        dummy_source_plugin_name: str,
    ) -> None:
        """Tests that plugins that don't implement BaseSource are ignored."""
        caplog.set_level("DEBUG")
        reload(bitfount.data.datasources)  # Creates the plugin directory
        dummy_plugin_path = bitfount.config.BITFOUNT_PLUGIN_PATH / "datasources"
        (dummy_plugin_path / f"{dummy_module_name}.py").touch()
        (dummy_plugin_path / f"{dummy_module_name}.py").write_text(
            dummy_abstract_source_plugin
        )
        reload(bitfount.data)
        reload(bitfount.data.datasources)

        # Tests that the module is still imported but the class is not
        datasources = import_module(BITFOUNT_DATASOURCES_MODULE_PATH)
        data = import_module(BITFOUNT_DATA_MODULE_PATH)
        assert hasattr(datasources, dummy_module_name)
        assert not hasattr(data, dummy_source_plugin_name)

        # Tests that the appropriate warning message is logged
        assert (
            f"Found class {dummy_source_plugin_name} in module {dummy_module_name}"
            f" which did not fully implement BaseSource. Skipping."
        ) in get_warning_logs(caplog)

    def test_datasource_plugin_gets_loaded_via_api(
        self,
        dummy_module_name: str,
        dummy_source_plugin: str,
        dummy_source_plugin_name: str,
    ) -> None:
        """Tests that plugins that implement BaseSource are loaded via the API."""
        reload(bitfount.data.datasources)  # Creates the plugin directory
        dummy_plugin_path = bitfount.config.BITFOUNT_PLUGIN_PATH / "datasources"
        (dummy_plugin_path / f"{dummy_module_name}.py").touch()
        (dummy_plugin_path / f"{dummy_module_name}.py").write_text(dummy_source_plugin)
        reload(bitfount.data.datasources)
        reload(bitfount.data)

        # Tests that the module and class can both be imported
        datasources = import_module(BITFOUNT_DATASOURCES_MODULE_PATH)
        data = import_module(BITFOUNT_DATA_MODULE_PATH)

        assert hasattr(datasources, dummy_module_name)
        assert hasattr(data, dummy_source_plugin_name)

    def test_datasource_plugin_gets_loaded_via_yaml(
        self,
        dummy_module_name: str,
        dummy_source_plugin: str,
        dummy_source_plugin_name: str,
        mocker: MockerFixture,
    ) -> None:
        """Tests that plugins that implement BaseSource are loaded via YAML."""
        reload(bitfount.data.datasources)  # Creates the plugin directory
        dummy_plugin_path = bitfount.config.BITFOUNT_PLUGIN_PATH / "datasources"
        (dummy_plugin_path / f"{dummy_module_name}.py").touch()
        (dummy_plugin_path / f"{dummy_module_name}.py").write_text(dummy_source_plugin)
        reload(bitfount.data)
        reload(bitfount.data.datasources)

        mocker.patch("bitfount.runners.pod_runner._create_bitfounthub")
        mocker.patch("bitfount.runners.pod_runner._create_access_manager")
        mocker.patch("bitfount.runners.pod_runner._get_pod_keys")
        mock_pod = mocker.patch("bitfount.runners.pod_runner.Pod")

        # Sets up the YAML config
        pod_config = PodConfig(
            datasource=dummy_source_plugin_name,
            name="dummy_pod",
            data_config=PodDataConfig(datasource_args={"path": "dummy_module.csv"}),
        )

        # Creates the pod
        setup_pod_from_config(pod_config)

        # Checks that the pod was created
        mock_pod.assert_called_once()

        # Checks that the pod was created with the correct datasource argument
        assert (
            mock_pod.call_args.kwargs["datasource"].__class__.__name__
            == dummy_source_plugin_name
        )


@unit_test
class TestAlgorithmPlugins:
    """Tests algorithm plugin functionality."""

    @fixture(autouse=True)
    def patch_plugins_dir(
        self, monkeypatch: MonkeyPatch, tmp_path_factory: TempPathFactory
    ) -> None:
        """Monkeypatch `BITFOUNT_PLUGIN_PATH` in bitfount.config to temporary directory.

        We must do it this way instead of by monkeypatching the `BITFOUNT_HOME`
        environment variable to avoid having to reload the `bitfount.config` module as
        this causes issues with the cache of the `_get_environment` function.
        """
        tmpdir = str(tmp_path_factory.mktemp("temp", numbered=True))
        monkeypatch.setattr(
            "bitfount.config.BITFOUNT_FEDERATED_PLUGIN_PATH",
            Path(tmpdir) / ".bitfount/_plugins/federated/",
        )

    @fixture(scope="function")
    def plugin_suffix(self) -> str:
        """Generates a unique suffix for each plugin in this test run."""
        return str(int(time.time_ns()))  # unix nanosecond timestamp

    @fixture(scope="function")
    def dummy_module_name(self, plugin_suffix: str) -> str:
        """Generates a unique plugin module name for each plugin in this test run."""
        return f"{DUMMY_MODULE_NAME}_{plugin_suffix}"

    @fixture(scope="function")
    def dummy_alg_plugin_name(self, plugin_suffix: str) -> str:
        """Generates a unique plugin source name for each plugin in this test run."""
        return f"{DUMMY_ALGORITHM_NAME}_{plugin_suffix}"

    @fixture(scope="function")
    def dummy_plugin(self, dummy_alg_plugin_name: str) -> str:
        """Returns a dummy plugin class."""
        return inspect.cleandoc(
            f"""
        from __future__ import annotations
        from typing import Mapping, Dict, Any

        import numpy as np

        from bitfount.hub.api import BitfountHub
        from bitfount.data import BaseSource
        from bitfount.federated.algorithms.model_algorithms.base import (
            _BaseWorkerModelAlgorithm,
            _BaseModelAlgorithmFactory,
            _BaseModellerModelAlgorithm,
        )
        from bitfount.federated.algorithms.base import BaseAlgorithmFactory
        from bitfount.federated.logging import _get_federated_logger
        logger = _get_federated_logger("bitfount.federated")

        class _ModellerSide(_BaseModellerModelAlgorithm):
            def run(
                self, results: Mapping[str,  np.ndarray]
            ) -> Dict[str,  np.ndarray]:
                # could also add option to save results for the modeller here.
                return dict(results)

        class _WorkerSide(_BaseWorkerModelAlgorithm):
            def run(self, data: BaseSource,) -> np.ndarray:
                preds = self.model.predict(data=data)
                # could also add option to save results directly on the pod.
                return preds
        class {dummy_alg_plugin_name}:

            def modeller(self, **kwargs: Any) -> _ModellerSide:
                model = self._get_model_from_reference()
                return _ModellerSide(model=model, **kwargs)

            def worker(self, hub: BitfountHub, **kwargs: Any) -> _WorkerSide:
                model = self._get_model_from_reference(hub=hub)
                return _WorkerSide(model=model, **kwargs)
        """
        )

    @fixture(scope="function")
    def dummy_alg_plugin(self, dummy_plugin: str, dummy_alg_plugin_name: str) -> str:
        """Returns a class that subclasses _BaseModelAlgorithmFactory."""
        return dummy_plugin.replace(
            dummy_alg_plugin_name,
            f"{dummy_alg_plugin_name}(_BaseModelAlgorithmFactory)",
        )

    def test_no_plugins_dir_created(self) -> None:
        """Tests that the plugin directory is created if it doesn't exist.

        Also tests that it's okay for there to be no plugins within the directory.
        """
        assert bitfount.config.BITFOUNT_FEDERATED_PLUGIN_PATH.exists() is False
        reload(bitfount.federated.algorithms)
        assert bitfount.config.BITFOUNT_FEDERATED_PLUGIN_PATH.exists() is True

    def test_plugin_in_wrong_dir_gets_ignored(
        self, dummy_module_name: str, dummy_plugin: str
    ) -> None:
        """Tests that plugins in the wrong directory are ignored."""
        reload(bitfount.federated.algorithms)  # Creates the plugin directory
        # `algo_rithms` is intentionally the wrong directory, should be `algorithms`
        dummy_plugin_path = (
            bitfount.config.BITFOUNT_FEDERATED_PLUGIN_PATH / "algo_rithms"
        )
        dummy_plugin_path.mkdir()
        (dummy_plugin_path / f"{dummy_module_name}.py").touch()
        (dummy_plugin_path / f"{dummy_module_name}.py").write_text(dummy_plugin)
        reload(bitfount.federated.algorithms)
        algorithms = import_module("bitfount.federated.algorithms")
        assert not hasattr(algorithms, dummy_module_name)

    def test_plugin_with_error_gets_ignored(
        self, caplog: LogCaptureFixture, dummy_alg_plugin: str, dummy_module_name: str
    ) -> None:
        """Tests that plugins with errors are ignored."""
        # Replacing numpy import with a non-existent module to cause an error
        dummy_alg_plugin = dummy_alg_plugin.replace("numpy", "numpyz")
        reload(bitfount.federated.algorithms)  # Creates the plugin directory
        dummy_plugin_path = (
            bitfount.config.BITFOUNT_FEDERATED_PLUGIN_PATH / "algorithms"
        )
        (dummy_plugin_path / f"{dummy_module_name}.py").touch()
        (dummy_plugin_path / f"{dummy_module_name}.py").write_text(dummy_alg_plugin)
        reload(bitfount.federated)
        reload(bitfount.federated.algorithms)

        # Tests that the module is still imported but the class is not
        algorithms = import_module(BITFOUNT_FEDERATED_ALGORITHM_MODULE_PATH)
        federated = import_module(BITFOUNT_FEDERATED_MODULE_PATH)
        assert not hasattr(algorithms, dummy_module_name)
        assert not hasattr(federated, dummy_alg_plugin)

        # Tests that the appropriate error message is logged
        assert (f"Error importing module {dummy_module_name}") in get_error_logs(caplog)

    def test_algorithm_plugin_that_doesnt_subclass_base_alg_gets_ignored(
        self, dummy_alg_plugin_name: str, dummy_module_name: str, dummy_plugin: str
    ) -> None:
        """Tests that plugins that don't subclass BaseAlgorithmFactory are ignored."""
        reload(bitfount.federated.algorithms)  # Creates the plugin directory
        dummy_plugin_path = (
            bitfount.config.BITFOUNT_FEDERATED_PLUGIN_PATH / "algorithms"
        )
        (dummy_plugin_path / f"{dummy_module_name}.py").touch()
        (dummy_plugin_path / f"{dummy_module_name}.py").write_text(dummy_plugin)
        reload(bitfount.federated)
        reload(bitfount.federated.algorithms)
        # Tests that the module is still imported but the class is not
        algorithms = import_module(BITFOUNT_FEDERATED_ALGORITHM_MODULE_PATH)
        federated = import_module(BITFOUNT_FEDERATED_MODULE_PATH)
        assert hasattr(algorithms, dummy_module_name)
        assert not hasattr(algorithms, dummy_alg_plugin_name)
        assert not hasattr(federated, dummy_alg_plugin_name)

    def test_algorithm_plugin_gets_loaded_via_api(
        self, dummy_alg_plugin: str, dummy_alg_plugin_name: str, dummy_module_name: str
    ) -> None:
        """Tests that BaseAlgorithmFactory plugins are loaded via API."""
        reload(bitfount.federated.algorithms)  # Creates the plugin directory
        dummy_plugin_path = (
            bitfount.config.BITFOUNT_FEDERATED_PLUGIN_PATH / "algorithms"
        )
        (dummy_plugin_path / f"{dummy_module_name}.py").touch()
        (dummy_plugin_path / f"{dummy_module_name}.py").write_text(dummy_alg_plugin)
        reload(bitfount.federated)
        reload(bitfount.federated.algorithms)

        # Tests that the module and class can both be imported
        algorithms = import_module(BITFOUNT_FEDERATED_ALGORITHM_MODULE_PATH)
        assert hasattr(algorithms, dummy_module_name)
        assert hasattr(algorithms, dummy_alg_plugin_name)

    def test_algorithm_plugin_gets_loaded_via_yaml(
        self,
        dummy_alg_plugin: str,
        dummy_alg_plugin_name: str,
        dummy_module_name: str,
        mocker: MockerFixture,
    ) -> None:
        """Tests that BaseAlgorithmFactory plugins are loaded via YAML."""
        reload(bitfount.federated.algorithms)  # Creates the plugin directory
        dummy_plugin_path = (
            bitfount.config.BITFOUNT_FEDERATED_PLUGIN_PATH / "algorithms"
        )
        (dummy_plugin_path / f"{dummy_module_name}.py").touch()
        (dummy_plugin_path / f"{dummy_module_name}.py").write_text(dummy_alg_plugin)
        reload(bitfount.federated)
        reload(bitfount.federated.algorithms)

        mocker.patch("bitfount.runners.modeller_runner.get_pod_schema")
        mocker.patch("bitfount.runners.modeller_runner._create_message_service")
        mocker.patch("bitfount.runners.modeller_runner._create_bitfounthub")
        mocker.patch("bitfount.runners.modeller_runner._check_and_update_pod_ids")
        mocker.patch(
            "bitfount.federated.protocols.results_only.ResultsOnly._validate_algorithm",
            return_value=True,
        )
        mock_modeller = mocker.patch("bitfount.runners.modeller_runner._Modeller")

        # Sets up the YAML config
        modeller_config = ModellerConfig(
            pods=PodsConfig(identifiers=["test"]),
            task=TaskConfig(
                protocol=ProtocolConfig(name="bitfount.ResultsOnly"),
                algorithm=AlgorithmConfig(
                    name=dummy_alg_plugin_name,
                    pretrained_file=Path("test.py"),
                    model=ModelConfig(
                        name="PyTorchTabularClassifier", hyperparameters={"epochs": 1}
                    ),
                ),
                data_structure=DataStructureConfig(
                    table_config=DataStructureTableConfig("test"),
                    assign=DataStructureAssignConfig(target="target"),
                ),
            ),
        )

        # Creates the pod
        setup_modeller_from_config(modeller_config)

        # Checks that the pod was created
        mock_modeller.assert_called_once()

        # Checks that the modeller was created with the correct algorithm argument
        assert (
            mock_modeller.call_args.kwargs["protocol"].algorithm.class_name
            == f"{dummy_alg_plugin_name}"
        )


@unit_test
class TestProtocolPlugins:
    """Tests protocol plugin functionality."""

    @fixture(autouse=True)
    def patch_plugins_dir(
        self, monkeypatch: MonkeyPatch, tmp_path_factory: TempPathFactory
    ) -> None:
        """Monkeypatch `BITFOUNT_PLUGIN_PATH` in bitfount.config to temporary directory.

        We must do it this way instead of by monkeypatching the `BITFOUNT_HOME`
        environment variable to avoid having to reload the `bitfount.config` module as
        this causes issues with the cache of the `_get_environment` function.
        """
        tmpdir = str(tmp_path_factory.mktemp("temp", numbered=True))
        monkeypatch.setattr(
            "bitfount.config.BITFOUNT_FEDERATED_PLUGIN_PATH",
            Path(tmpdir) / ".bitfount/_plugins/federated/",
        )

    @fixture(scope="function")
    def plugin_suffix(self) -> str:
        """Generates a unique suffix for each plugin in this test run."""
        return str(int(time.time_ns()))  # unix nanosecond timestamp

    @fixture(scope="function")
    def dummy_module_name(self, plugin_suffix: str) -> str:
        """Generates a unique plugin module name for each plugin in this test run."""
        return f"{DUMMY_MODULE_NAME}_{plugin_suffix}"

    @fixture(scope="function")
    def dummy_protocol_plugin_name(self, plugin_suffix: str) -> str:
        """Generates a unique plugin source name for each plugin in this test run."""
        return f"{DUMMY_PROTOCOL_NAME}_{plugin_suffix}"

    @fixture(scope="function")
    def dummy_plugin(self, dummy_protocol_plugin_name: str) -> str:
        """Returns a dummy plugin class."""
        return inspect.cleandoc(
            f"""
        from __future__ import annotations

        from typing import TYPE_CHECKING, Any, List, Optional, Union
        import pandas as pd

        from bitfount.data.datasources.base_source import BaseSource
        from bitfount.federated.logging import _get_federated_logger
        from bitfount.federated.pod_vitals import _PodVitals
        from bitfount.federated.privacy.differential import DPPodConfig
        from bitfount.federated.protocols.base import (
            BaseModellerProtocol,
            BaseProtocolFactory,
            BaseWorkerProtocol,
            BaseCompatibleAlgoFactory,
        )
        from bitfount.federated.transport.modeller_transport import _ModellerMailbox
        from bitfount.federated.transport.worker_transport import _WorkerMailbox
        from bitfount.federated.types import SerializedProtocol

        if TYPE_CHECKING:
            from bitfount.hub.api import BitfountHub

        logger = _get_federated_logger("bitfount.federated.protocols" + __name__)


        class _ModellerSide(BaseModellerProtocol):
            async def run(
                self,
                **kwargs: Any,
            ) -> Union[List[Any], pd.DataFrame]:
                ...


        class _WorkerSide(BaseWorkerProtocol):
            async def run(
                self,
                datasource: BaseSource,
                pod_dp: Optional[DPPodConfig] = None,
                pod_vitals: Optional[_PodVitals] = None,
                pod_identifier: Optional[str] = None,
                **kwargs: Any,
            ) -> None:
                ...


        class {dummy_protocol_plugin_name}:

            @classmethod
            def _validate_algorithm(cls, algorithm: BaseCompatibleAlgoFactory) -> None:
                ...

            def dump(self) -> SerializedProtocol:
                ...

            def modeller(self, mailbox: _ModellerMailbox, **kwargs: Any) -> _ModellerSide:
                ...

            def worcker(  # intentionally misspelled
                self, mailbox: _WorkerMailbox, hub: BitfountHub, **kwargs: Any
            ) -> _WorkerSide:
                ...

        """  # noqa: B950
        )

    @fixture(scope="function")
    def dummy_abstract_protocol_plugin(
        self, dummy_plugin: str, dummy_protocol_plugin_name: str
    ) -> str:
        """Returns a class that subclasses BaseProtocolFactory."""
        return dummy_plugin.replace(
            dummy_protocol_plugin_name,
            f"{dummy_protocol_plugin_name}(BaseProtocolFactory)",
        )

    @fixture(scope="function")
    def dummy_protocol_plugin(
        self,
        dummy_abstract_protocol_plugin: str,
    ) -> str:
        """Returns a class that subclasses BaseProtocolFactory."""
        return dummy_abstract_protocol_plugin.replace("worcker", "worker")

    def test_no_plugins_dir_created(self) -> None:
        """Tests that the plugin directory is created if it doesn't exist.

        Also tests that it's okay for there to be no plugins within the directory.
        """
        assert bitfount.config.BITFOUNT_FEDERATED_PLUGIN_PATH.exists() is False
        reload(bitfount.federated.protocols)
        assert bitfount.config.BITFOUNT_FEDERATED_PLUGIN_PATH.exists() is True

    def test_plugin_in_wrong_dir_gets_ignored(
        self, dummy_module_name: str, dummy_plugin: str
    ) -> None:
        """Tests that plugins in the wrong directory are ignored."""
        reload(bitfount.federated.protocols)  # Creates the plugin directory
        # `proto_cols` is intentionally the wrong directory, should be `protocols`
        dummy_plugin_path = (
            bitfount.config.BITFOUNT_FEDERATED_PLUGIN_PATH / "proto_cols"
        )
        dummy_plugin_path.mkdir()
        (dummy_plugin_path / f"{dummy_module_name}.py").touch()
        (dummy_plugin_path / f"{dummy_module_name}.py").write_text(dummy_plugin)
        reload(bitfount.federated.protocols)
        protocols = import_module("bitfount.federated.protocols")
        assert not hasattr(protocols, dummy_module_name)

    def test_plugin_with_error_gets_ignored(
        self,
        caplog: LogCaptureFixture,
        dummy_module_name: str,
        dummy_protocol_plugin: str,
    ) -> None:
        """Tests that plugins with errors are ignored."""
        # Replacing numpy import with a non-existent module to cause an error
        dummy_protocol_plugin = dummy_protocol_plugin.replace("pandas", "pandaz")
        reload(bitfount.federated.protocols)  # Creates the plugin directory
        dummy_plugin_path = bitfount.config.BITFOUNT_FEDERATED_PLUGIN_PATH / "protocols"
        (dummy_plugin_path / f"{dummy_module_name}.py").touch()
        (dummy_plugin_path / f"{dummy_module_name}.py").write_text(
            dummy_protocol_plugin
        )
        reload(bitfount.federated)
        reload(bitfount.federated.protocols)

        # Tests that the module is still imported but the class is not
        protocols = import_module(BITFOUNT_FEDERATED_PROTOCOL_MODULE_PATH)
        federated = import_module(BITFOUNT_FEDERATED_MODULE_PATH)
        assert not hasattr(protocols, dummy_module_name)
        assert not hasattr(federated, dummy_protocol_plugin)

        # Tests that the appropriate error message is logged
        assert (f"Error importing module {dummy_module_name}") in get_error_logs(caplog)

    def test_protocol_plugin_that_doesnt_subclass_base_protocol_gets_ignored(
        self, dummy_module_name: str, dummy_plugin: str, dummy_protocol_plugin_name: str
    ) -> None:
        """Tests that plugins that don't subclass BaseProtocolFactory are ignored."""
        reload(bitfount.federated.protocols)  # Creates the plugin directory
        dummy_plugin_path = bitfount.config.BITFOUNT_FEDERATED_PLUGIN_PATH / "protocols"
        (dummy_plugin_path / f"{dummy_module_name}.py").touch()
        (dummy_plugin_path / f"{dummy_module_name}.py").write_text(dummy_plugin)
        reload(bitfount.federated)
        reload(bitfount.federated.protocols)
        # Tests that the module is still imported but the class is not
        protocols = import_module(BITFOUNT_FEDERATED_PROTOCOL_MODULE_PATH)
        federated = import_module(BITFOUNT_FEDERATED_MODULE_PATH)
        assert not hasattr(protocols, dummy_protocol_plugin_name)
        assert not hasattr(federated, dummy_protocol_plugin_name)
        assert hasattr(protocols, dummy_module_name)

    def test_abstract_protocol_plugin_gets_ignored(
        self,
        caplog: LogCaptureFixture,
        dummy_abstract_protocol_plugin: str,
        dummy_module_name: str,
        dummy_protocol_plugin_name: str,
    ) -> None:
        """Tests that plugins that are abstract are ignored."""
        reload(bitfount.federated.protocols)  # Creates the plugin directory
        dummy_plugin_path = bitfount.config.BITFOUNT_FEDERATED_PLUGIN_PATH / "protocols"
        (dummy_plugin_path / f"{dummy_module_name}.py").touch()
        (dummy_plugin_path / f"{dummy_module_name}.py").write_text(
            dummy_abstract_protocol_plugin
        )
        reload(bitfount.federated)
        reload(bitfount.federated.protocols)
        # Tests that the module is still imported but the class is not
        protocols = import_module(BITFOUNT_FEDERATED_PROTOCOL_MODULE_PATH)
        federated = import_module(BITFOUNT_FEDERATED_MODULE_PATH)
        assert not hasattr(protocols, dummy_protocol_plugin_name)
        assert not hasattr(federated, dummy_protocol_plugin_name)
        assert hasattr(protocols, dummy_module_name)

        # Tests that the appropriate warning message is logged
        assert (
            f"Found class {dummy_protocol_plugin_name} in module {dummy_module_name}"
            f" which did not fully implement BaseProtocolFactory. Skipping."
        ) in get_warning_logs(caplog)

    def test_protocol_plugin_plugin_gets_loaded_via_api(
        self,
        dummy_module_name: str,
        dummy_protocol_plugin: str,
        dummy_protocol_plugin_name: str,
    ) -> None:
        """Tests that BaseProtocolFactory plugins are loaded via API."""
        reload(bitfount.federated.protocols)  # Creates the plugin directory
        dummy_plugin_path = bitfount.config.BITFOUNT_FEDERATED_PLUGIN_PATH / "protocols"
        (dummy_plugin_path / f"{dummy_module_name}.py").touch()
        (dummy_plugin_path / f"{dummy_module_name}.py").write_text(
            dummy_protocol_plugin
        )
        reload(bitfount.federated)
        reload(bitfount.federated.protocols)

        # Tests that the module and class can both be imported
        protocols = import_module(BITFOUNT_FEDERATED_PROTOCOL_MODULE_PATH)
        assert hasattr(protocols, dummy_module_name)
        assert hasattr(protocols, dummy_protocol_plugin_name)

    def test_protocol_plugin_gets_loaded_via_yaml(
        self,
        dummy_module_name: str,
        dummy_protocol_plugin: str,
        dummy_protocol_plugin_name: str,
        mocker: MockerFixture,
    ) -> None:
        """Tests that BaseProtocolFactory plugins are loaded via YAML."""
        reload(bitfount.federated.protocols)  # Creates the plugin directory
        dummy_plugin_path = bitfount.config.BITFOUNT_FEDERATED_PLUGIN_PATH / "protocols"
        (dummy_plugin_path / f"{dummy_module_name}.py").touch()
        (dummy_plugin_path / f"{dummy_module_name}.py").write_text(
            dummy_protocol_plugin
        )
        reload(bitfount.federated)
        reload(bitfount.federated.protocols)

        mocker.patch("bitfount.runners.modeller_runner.get_pod_schema")
        mocker.patch("bitfount.runners.modeller_runner._create_message_service")
        mocker.patch("bitfount.runners.modeller_runner._create_bitfounthub")
        mocker.patch("bitfount.runners.modeller_runner._check_and_update_pod_ids")

        mock_modeller = mocker.patch("bitfount.runners.modeller_runner._Modeller")

        # Sets up the YAML config
        modeller_config = ModellerConfig(
            pods=PodsConfig(identifiers=["test"]),
            task=TaskConfig(
                protocol=ProtocolConfig(name=dummy_protocol_plugin_name),
                algorithm=AlgorithmConfig(
                    name="bitfount.ColumnAverage",
                    arguments=dict(field="test", table_name="test"),
                ),
            ),
        )

        # Creates the pod
        setup_modeller_from_config(modeller_config)

        # Checks that the pod was created
        mock_modeller.assert_called_once()

        # Checks that the modeller was created with the correct protocol argument
        assert (
            mock_modeller.call_args.kwargs["protocol"].class_name
            == f"{dummy_protocol_plugin_name}"
        )
