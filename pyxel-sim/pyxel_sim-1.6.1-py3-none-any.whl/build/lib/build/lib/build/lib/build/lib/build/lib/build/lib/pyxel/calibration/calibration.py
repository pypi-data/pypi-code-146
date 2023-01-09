#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""TBW."""
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, Mapping, Optional, Sequence, Tuple, Union

import numpy as np
from dask.delayed import Delayed
from typing_extensions import Literal

from pyxel.calibration import (
    Algorithm,
    CalibrationMode,
    DaskBFE,
    DaskIsland,
    Island,
    MyArchipelago,
)
from pyxel.calibration.fitting import ModelFitting
from pyxel.exposure import Readout
from pyxel.observation import ParameterValues
from pyxel.pipelines import FitnessFunction, Processor, ResultType

if TYPE_CHECKING:
    import pandas as pd
    import xarray as xr

    from pyxel.outputs import CalibrationOutputs


def to_path_list(values: Sequence[Union[str, Path]]) -> Sequence[Path]:
    """TBW."""
    return [Path(obj).resolve() for obj in values]


class Calibration:
    """TBW."""

    def __init__(
        self,
        outputs: "CalibrationOutputs",
        target_data_path: Sequence[Union[str, Path]],
        fitness_function: FitnessFunction,
        algorithm: Algorithm,
        parameters: Sequence[ParameterValues],
        readout: Optional["Readout"] = None,
        mode: Literal["pipeline", "single_model"] = "pipeline",
        result_type: Literal["image", "signal", "pixel"] = "image",
        result_fit_range: Optional[Sequence[int]] = None,
        result_input_arguments: Optional[Sequence[ParameterValues]] = None,
        target_fit_range: Optional[Sequence[int]] = None,
        pygmo_seed: Optional[int] = None,
        pipeline_seed: Optional[int] = None,
        num_islands: int = 1,
        num_evolutions: int = 1,
        num_best_decisions: Optional[int] = None,
        topology: Literal["unconnected", "ring", "fully_connected"] = "unconnected",
        type_islands: Literal[
            "multiprocessing", "multithreading", "ipyparallel"
        ] = "multiprocessing",
        weights_from_file: Optional[Sequence[Union[str, Path]]] = None,
        weights: Optional[Sequence[float]] = None,
    ):
        if pygmo_seed is not None and pygmo_seed not in range(100001):
            raise ValueError("'Pygmo seed' must be between 0 and 100000.")

        if num_islands < 1:
            raise ValueError("'num_islands' must superior or equal to 1.")

        self._log = logging.getLogger(__name__)

        self.outputs = outputs
        self.readout: Readout = readout or Readout()

        self._calibration_mode = CalibrationMode(mode)

        self._result_type: ResultType = ResultType(result_type)

        self._result_fit_range: Sequence[int] = result_fit_range or []

        self._result_input_arguments: Sequence[ParameterValues] = (
            result_input_arguments or []
        )

        self._target_data_path: Sequence[Path] = (
            to_path_list(target_data_path) if target_data_path else []
        )
        self._target_fit_range: Sequence[int] = target_fit_range or []

        self._fitness_function: FitnessFunction = fitness_function
        self._algorithm: Algorithm = algorithm

        self._parameters: Sequence[ParameterValues] = parameters or []

        if pygmo_seed is None:
            rng = np.random.default_rng()
            self._pygmo_seed: int = rng.integers(100000)
        else:
            self._pygmo_seed = pygmo_seed

        self._num_islands: int = num_islands
        self._num_evolutions: int = num_evolutions
        self._num_best_decisions: Optional[int] = num_best_decisions
        self._type_islands: Island = Island(type_islands)
        self._pipeline_seed = pipeline_seed
        self._topology: Literal["unconnected", "ring", "fully_connected"] = topology

        if weights and weights_from_file:
            raise ValueError("Cannot define both weights and weights from file.")

        self._weights_from_file: Optional[Sequence[Path]] = (
            to_path_list(weights_from_file) if weights_from_file else None
        )
        self._weights: Optional[Sequence[float]] = weights

    @property
    def calibration_mode(self) -> CalibrationMode:
        """TBW."""
        return self._calibration_mode

    @calibration_mode.setter
    def calibration_mode(self, value: CalibrationMode) -> None:
        """TBW."""
        self._calibration_mode = value

    @property
    def result_type(self) -> ResultType:
        """TBW."""
        return self._result_type

    @result_type.setter
    def result_type(self, value: ResultType) -> None:
        """TBW."""
        self._result_type = value

    @property
    def result_fit_range(self) -> Sequence[int]:
        """TBW."""
        return self._result_fit_range

    @result_fit_range.setter
    def result_fit_range(self, value: Sequence[int]) -> None:
        """TBW."""
        self._result_fit_range = value

    @property
    def result_input_arguments(self) -> Sequence[ParameterValues]:
        """TBW."""
        return self._result_input_arguments

    @result_input_arguments.setter
    def result_input_arguments(self, value: Sequence[ParameterValues]) -> None:
        """TBW."""
        self._result_input_arguments = value

    @property
    def target_data_path(self) -> Sequence[Path]:
        """TBW."""
        return self._target_data_path

    @target_data_path.setter
    def target_data_path(self, value: Sequence[Path]) -> None:
        """TBW."""
        self._target_data_path = value

    @property
    def target_fit_range(self) -> Sequence[int]:
        """TBW."""
        return self._target_fit_range

    @target_fit_range.setter
    def target_fit_range(self, value: Sequence[int]) -> None:
        """TBW."""
        self._target_fit_range = value

    @property
    def fitness_function(self) -> FitnessFunction:
        """TBW."""
        return self._fitness_function

    @fitness_function.setter
    def fitness_function(self, value: FitnessFunction) -> None:
        """TBW."""
        self._fitness_function = value

    @property
    def algorithm(self) -> Algorithm:
        """TBW."""
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value: Algorithm) -> None:
        """TBW."""
        self._algorithm = value

    @property
    def parameters(self) -> Sequence[ParameterValues]:
        """TBW."""
        return self._parameters

    @parameters.setter
    def parameters(self, value: Sequence[ParameterValues]) -> None:
        """TBW."""
        self._parameters = value

    @property
    def pygmo_seed(self) -> int:
        """TBW."""
        return self._pygmo_seed

    @pygmo_seed.setter
    def pygmo_seed(self, value: int) -> None:
        """TBW."""
        if value not in range(100001):
            raise ValueError("Pygmo 'seed' must be between 0 and 100000.")

        self._pygmo_seed = value

    @property
    def pipeline_seed(self) -> Optional[int]:
        """TBW."""
        return self._pipeline_seed

    @pipeline_seed.setter
    def pipeline_seed(self, value: int) -> None:
        """TBW."""
        self._pipeline_seed = value

    @property
    def num_islands(self) -> int:
        """TBW."""
        return self._num_islands

    @num_islands.setter
    def num_islands(self, value: int) -> None:
        """TBW."""
        if value < 1:
            raise ValueError("'num_islands' must superior or equal to 1.")

        self._num_islands = value

    @property
    def num_evolutions(self) -> int:
        """TBW."""
        return self._num_evolutions

    @num_evolutions.setter
    def num_evolutions(self, value: int) -> None:
        """TBW."""
        self._num_evolutions = value

    @property
    def num_best_decisions(self) -> Optional[int]:
        """TBW."""
        return self._num_best_decisions

    @num_best_decisions.setter
    def num_best_decisions(self, value: Optional[int]) -> None:
        """TBW."""
        if isinstance(value, int) and value < 0:
            raise ValueError(
                "'num_best_decisions' must be 'None' or a positive integer"
            )

        self._num_best_decisions = value

    @property
    def topology(self) -> Literal["unconnected", "ring", "fully_connected"]:
        """TBW."""
        return self._topology

    @topology.setter
    def topology(self, value: Any) -> None:
        if value not in ("unconnected", "ring", "fully_connected"):
            raise ValueError(
                "Expecting value: 'unconnected', 'ring' or 'fully_connected'"
            )

        self._topology = value

    @property
    def weights_from_file(self) -> Optional[Sequence[Path]]:
        """TBW."""
        return self._weights_from_file

    @weights_from_file.setter
    def weights_from_file(self, value: Sequence[Path]) -> None:
        """TBW."""
        self._weights_from_file = value

    @property
    def weights(self) -> Optional[Sequence[float]]:
        """TBW."""
        return self._weights

    @weights.setter
    def weights(self, value: Sequence[float]) -> None:
        """TBW."""
        self._weights = value

    def run_calibration(
        self,
        processor: Processor,
        output_dir: Path,
        with_progress_bar: bool = True,
    ) -> Tuple["xr.Dataset", "pd.DataFrame", "pd.DataFrame"]:
        """Run calibration pipeline."""
        try:
            import pygmo as pg
        except ImportError as exc:
            raise ImportError(
                "Missing optional package 'pygmo'.\n"
                "Please install it with 'pip install pyxel-sim[calibration]' "
                "or 'pip install pyxel-sim[all]'"
            ) from exc

        pg.set_global_rng_seed(seed=self.pygmo_seed)
        self._log.info("Pygmo seed: %d", self.pygmo_seed)

        fitting = ModelFitting(
            processor=processor,
            variables=self.parameters,
            readout=self.readout,
            calibration_mode=CalibrationMode(self.calibration_mode),
            simulation_output=ResultType(self.result_type),
            generations=self.algorithm.generations,
            population_size=self.algorithm.population_size,
            fitness_func=self.fitness_function,
            file_path=output_dir,
        )

        fitting.configure(
            target_output=self.target_data_path,
            target_fit_range=self.target_fit_range,
            out_fit_range=self.result_fit_range,
            input_arguments=self.result_input_arguments,
            weights=self.weights,
            weights_from_file=self.weights_from_file,
        )

        if self.num_islands > 1:  # default
            # Create an archipelago
            user_defined_island = DaskIsland()
            user_defined_bfe = DaskBFE()

            if self.topology == "unconnected":
                topo = pg.unconnected()
            elif self.topology == "ring":
                topo = pg.ring()
            elif self.topology == "fully_connected":
                topo = pg.fully_connected()
            else:
                raise NotImplementedError(f"topology {self.topology!r}")

            # Create a new archipelago
            # This operation takes some time ...
            my_archipelago = MyArchipelago(
                num_islands=self.num_islands,
                udi=user_defined_island,
                algorithm=self.algorithm,
                problem=fitting,
                pop_size=self.algorithm.population_size,
                bfe=user_defined_bfe,
                topology=topo,
                pygmo_seed=self.pygmo_seed,
                with_bar=with_progress_bar,
            )

            # Run several evolutions in the archipelago
            ds, df_processors, df_all_logs = my_archipelago.run_evolve(
                readout=self.readout,
                num_evolutions=self._num_evolutions,
                num_best_decisions=self._num_best_decisions,
            )

            ds.attrs["topology"] = self.topology
            ds.attrs["result_type"] = str(fitting.sim_output)

        else:
            raise NotImplementedError("Not implemented for 1 island.")

        self._log.info("Calibration ended.")
        return ds, df_processors, df_all_logs

    def post_processing(
        self,
        ds: "xr.Dataset",
        df_processors: "pd.DataFrame",
        output: "CalibrationOutputs",
    ) -> Sequence[Delayed]:
        """TBW."""
        filenames: Sequence[Delayed] = output.save_processors(processors=df_processors)

        # TODO: Use output.fitting_plot ?
        # TODO: Use output.fitting_plot_close ?
        # TODO: Use output.calibration_plots ?

        return filenames

    @classmethod
    def from_json(cls, dct: Mapping) -> "Calibration":
        """Create a new object from a JSON dictionary."""
        from pyxel.outputs import CalibrationOutputs

        def _from_json(
            outputs: Mapping,
            target_data_path: Sequence[str],
            fitness_function: Mapping,
            algorithm: Mapping,
            parameters: Sequence[Mapping],
            readout: Optional[Mapping] = None,
            result_input_arguments: Optional[Sequence[Mapping]] = None,
            **kwargs,
        ) -> "Calibration":
            """Create a new object from an unpacked JSON dictionary."""
            return cls(
                outputs=CalibrationOutputs(**outputs),
                target_data_path=target_data_path,
                fitness_function=FitnessFunction(func=fitness_function["func"]),
                algorithm=Algorithm(**algorithm),
                parameters=[ParameterValues(**el) for el in parameters],
                readout=(Readout(**readout) if readout else None),
                result_input_arguments=(
                    [ParameterValues(**el) for el in result_input_arguments]
                    if result_input_arguments
                    else None
                ),
                **kwargs,
            )

        return _from_json(**dct)
