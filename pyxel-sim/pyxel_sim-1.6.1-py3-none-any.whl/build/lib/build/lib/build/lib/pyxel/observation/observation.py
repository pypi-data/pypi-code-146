#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""Parametric mode class and helper functions."""
import itertools
import logging
from collections import Counter
from copy import deepcopy
from enum import Enum
from functools import partial
from numbers import Number
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generator,
    Iterator,
    List,
    Mapping,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import dask.bag as db
import numpy as np
from tqdm.auto import tqdm
from typing_extensions import Literal

from pyxel.exposure import Readout, run_exposure_pipeline
from pyxel.observation.parameter_values import ParameterType, ParameterValues
from pyxel.pipelines import ResultType
from pyxel.state import get_obj_att, get_value

if TYPE_CHECKING:
    import xarray as xr

    from pyxel.outputs import ObservationOutputs
    from pyxel.pipelines import Processor


class ParameterMode(Enum):
    """Parameter mode class."""

    Product = "product"
    Sequential = "sequential"
    Custom = "custom"


class ObservationResult(NamedTuple):
    """Result class for observation class."""

    dataset: Union["xr.Dataset", Dict[str, "xr.Dataset"]]
    parameters: "xr.Dataset"
    logs: "xr.Dataset"


def _get_short_name_with_model(name: str) -> str:
    _, _, model_name, _, param_name = name.split(".")

    return f"{model_name}.{param_name}"


def _get_final_short_name(name: str, param_type: ParameterType) -> str:
    if param_type == ParameterType.Simple:
        return name
    elif param_type == ParameterType.Multi:
        return _id(name)
    else:
        raise NotImplementedError


def _get_short_dimension_names(types: Mapping[str, ParameterType]) -> Mapping[str, str]:
    # Create potential names for the dimensions
    potential_dim_names: Dict[str, str] = {}
    for param_name, param_type in types.items():
        short_name: str = short(param_name)

        potential_dim_names[param_name] = _get_final_short_name(
            name=short_name, param_type=param_type
        )

    # Find possible duplicates
    count_dim_names: Mapping[str, int] = Counter(potential_dim_names.values())

    duplicate_dim_names: Sequence[str] = [
        name for name, freq in count_dim_names.items() if freq > 1
    ]

    if duplicate_dim_names:
        dim_names: Dict[str, str] = {}
        for param_name, param_type in types.items():
            short_name = potential_dim_names[param_name]

            if short_name in duplicate_dim_names:
                new_short_name: str = _get_short_name_with_model(param_name)
                dim_names[param_name] = _get_final_short_name(
                    name=new_short_name, param_type=param_type
                )

            else:
                dim_names[param_name] = short_name

        return dim_names

    return potential_dim_names


class Observation:
    """Observation class."""

    def __init__(
        self,
        outputs: "ObservationOutputs",
        parameters: Sequence[ParameterValues],
        readout: Optional[Readout] = None,
        mode: str = "product",
        from_file: Optional[str] = None,
        column_range: Optional[Tuple[int, int]] = None,
        with_dask: bool = False,
        result_type: Literal["image", "signal", "pixel", "all"] = "all",
        pipeline_seed: Optional[int] = None,
    ):
        self.outputs = outputs
        self.readout: Readout = readout or Readout()
        self.parameter_mode: ParameterMode = ParameterMode(mode)
        self._parameters = parameters
        self.file = from_file
        self.data: Optional[np.ndarray] = None
        if column_range:
            self.columns = slice(*column_range)
        self.with_dask = with_dask
        self.parameter_types: Dict[str, ParameterType] = {}
        self._result_type = ResultType(result_type)
        self._pipeline_seed = pipeline_seed

        if self.parameter_mode == ParameterMode.Custom:
            self._load_custom_parameters()

    def __repr__(self):
        cls_name: str = self.__class__.__name__
        return f"{cls_name}<mode={self.parameter_mode!s}>"

    @property
    def result_type(self) -> ResultType:
        """TBW."""
        return self._result_type

    @result_type.setter
    def result_type(self, value: ResultType) -> None:
        """TBW."""
        self._result_type = value

    @property
    def pipeline_seed(self) -> Optional[int]:
        """TBW."""
        return self._pipeline_seed

    @pipeline_seed.setter
    def pipeline_seed(self, value: int) -> None:
        """TBW."""
        self._pipeline_seed = value

    @property
    def enabled_steps(self) -> Sequence[ParameterValues]:
        """Return a list of enabled ParameterValues.

        Returns
        -------
        out: list
        """
        out = [step for step in self._parameters if step.enabled]
        return out

    # TODO: is self.data really needed?
    def _load_custom_parameters(self) -> None:
        """Load custom parameters from file."""
        from pyxel import load_table

        if self.file is not None:
            result: np.ndarray = load_table(self.file).to_numpy()[:, self.columns]
        else:
            raise ValueError("File for custom parametric mode not specified!")
        self.data = result

    def _custom_parameters(self) -> Generator[Tuple[int, dict], None, None]:
        """Generate custom mode parameters based on input file.

        Yields
        ------
        index: int
        parameter_dict: dict
        """
        if isinstance(self.data, np.ndarray):
            for index, data_array in enumerate(self.data):
                i = 0
                parameter_dict = {}
                for step in self.enabled_steps:
                    key = step.key

                    # TODO: this is confusing code. Fix this.
                    #       Furthermore 'step.values' should be a `List[int, float]` and not a `str`
                    if step.values == "_":
                        value = data_array[i]
                        i += 1
                        parameter_dict.update({key: value})

                    elif isinstance(step.values, list):

                        values: np.ndarray = np.asarray(deepcopy(step.values))
                        sh: tuple = values.shape
                        values_flattened = values.flatten()

                        # TODO: find a way to remove the ignore
                        if all(x == "_" for x in values_flattened):
                            value = data_array[
                                i : i + len(values_flattened)
                            ]  # noqa: E203
                            i += len(value)
                            value = value.reshape(sh).tolist()
                            parameter_dict.update({key: value})
                        else:
                            raise ValueError(
                                'Only "_" characters (or a list of them) should be used to '
                                "indicate parameters updated from file in custom mode"
                            )
                yield index, parameter_dict

        else:
            raise TypeError("Custom parameters not loaded from file.")

    def _sequential_parameters(self) -> Generator[Tuple[int, dict], None, None]:
        """Generate sequential mode parameters.

        Yields
        ------
        index: int
        parameter_dict: dict
        """
        step: ParameterValues
        for step in self.enabled_steps:
            key: str = step.key
            for index, value in enumerate(step):
                parameter_dict = {key: value}
                yield index, parameter_dict

    def _product_indices(self) -> "Iterator[Tuple]":
        """Return an iterator of product parameter indices.

        Returns
        -------
        out: iterator
        """
        step_ranges = [range(len(step)) for step in self.enabled_steps]
        out = itertools.product(*step_ranges)
        return out

    def _product_parameters(
        self,
    ) -> Generator[Tuple[Tuple, Dict[str, Any]], None, None]:
        """Generate product mode parameters.

        Yields
        ------
        indices: tuple
        parameter_dict: dict
        """
        all_steps = self.enabled_steps
        keys = [step.key for step in self.enabled_steps]
        for indices, params in zip(
            self._product_indices(), itertools.product(*all_steps)
        ):
            parameter_dict = {}
            for key, value in zip(keys, params):
                parameter_dict.update({key: value})
            yield indices, parameter_dict

    def _parameter_it(self) -> Callable:
        """Return the method for generating parameters based on parametric mode.

        Returns
        -------
        callable
        """
        if self.parameter_mode == ParameterMode.Product:
            return self._product_parameters

        elif self.parameter_mode == ParameterMode.Sequential:
            return self._sequential_parameters

        elif self.parameter_mode == ParameterMode.Custom:
            return self._custom_parameters
        else:
            raise NotImplementedError

    def _processors_it(
        self, processor: "Processor"
    ) -> Generator[Tuple["Processor", Union[int, Tuple[int]], Dict], None, None]:
        """Generate processors with different product parameters.

        Parameters
        ----------
        processor: Processor

        Yields
        ------
        new_processor: Processor
        index: tuple of int
        parameter_dict: dict
        """

        parameter_it = self._parameter_it()

        for index, parameter_dict in parameter_it():
            new_processor = create_new_processor(
                processor=processor, parameter_dict=parameter_dict
            )
            yield new_processor, index, parameter_dict

    def _get_parameter_types(self) -> Mapping[str, ParameterType]:
        """Check for each step if parameters can be used as dataset coordinates (1D, simple) or not (multi).

        Returns
        -------
        self.parameter_types: dict
        """
        for step in self.enabled_steps:
            self.parameter_types.update({step.key: step.type})
        return self.parameter_types

    def run_debug_mode(
        self, processor: "Processor"
    ) -> Tuple[List["Processor"], "xr.Dataset"]:
        """Run observation pipelines in debug mode and return list of processors and parameter logs.

        Parameters
        ----------
        processor: Processor

        Returns
        -------
        processors: list
        final_logs: Dataset
        """
        # Late import to speedup start-up time
        import xarray as xr

        processors = []
        logs: List[xr.Dataset] = []

        for processor_id, (proc, _index, parameter_dict) in enumerate(
            tqdm(self._processors_it(processor))
        ):
            log: xr.Dataset = log_parameters(
                processor_id=processor_id, parameter_dict=parameter_dict
            )
            logs.append(log)
            _ = run_exposure_pipeline(
                processor=proc,
                readout=self.readout,
                outputs=self.outputs,
                pipeline_seed=self.pipeline_seed,
            )
            processors.append(processor)

        # See issue #276
        final_logs = xr.combine_by_coords(logs)
        if not isinstance(final_logs, xr.Dataset):
            raise TypeError("Expecting 'Dataset'.")

        return processors, final_logs

    def validate_steps(self, processor: "Processor") -> None:
        """Validate enabled parameter steps in processor before running the pipelines.

        Parameters
        ----------
        processor: Processor

        Raises
        ------
        KeyError
            If a 'step' is missing in the configuration.
        ValueError
            If a model referenced in the configuration has not been enabled.
        """
        step: ParameterValues
        for step in self.enabled_steps:

            key: str = step.key
            if not processor.has(key):
                raise KeyError(f"Missing parameter: {key!r} in steps.")

            # TODO: the string literal expressions are difficult to maintain.
            #     Example: 'pipeline.', '.arguments', '.enabled'
            #     We may want to consider an API for this.
            # Proposed API:
            # value = operator.attrgetter(step.key)(processor)
            if "pipeline." in step.key:
                model_name: str = step.key[: step.key.find(".arguments")]
                model_enabled: str = model_name + ".enabled"
                if not processor.get(model_enabled):
                    raise ValueError(
                        f"The '{model_name}' model referenced in Observation configuration "
                        f"has not been enabled in yaml config!"
                    )

            if (
                any(x == "_" for x in step.values[:])
                and self.parameter_mode != ParameterMode.Custom
            ):
                raise ValueError(
                    "Either define 'custom' as parametric mode or "
                    "do not use '_' character in 'values' field"
                )

    def run_observation(self, processor: "Processor") -> ObservationResult:
        """Run the observation pipelines.

        Parameters
        ----------
        processor: Processor

        Returns
        -------
        result: Result
        """
        # Late import to speedup start-up time
        import xarray as xr

        # validation
        self.validate_steps(processor)

        types: Mapping[str, ParameterType] = self._get_parameter_types()

        dim_names: Mapping[str, str] = _get_short_dimension_names(types)

        y = range(processor.detector.geometry.row)
        x = range(processor.detector.geometry.col)
        times = self.readout.times

        if self.parameter_mode == ParameterMode.Product:

            apply_pipeline = partial(
                self._apply_exposure_pipeline_product,
                dimension_names=dim_names,
                x=x,
                y=y,
                processor=processor,
                times=times,
                types=types,
            )
            lst = [
                (index, parameter_dict, n)
                for n, (index, parameter_dict) in enumerate(self._parameter_it()())
            ]

            if self.with_dask:
                dataset_list = db.from_sequence(lst).map(apply_pipeline).compute()
            else:
                dataset_list = list(map(apply_pipeline, tqdm(lst)))

            # prepare lists for to-be-merged datasets
            parameters: List[List[xr.Dataset]] = [
                [] for _ in range(len(self.enabled_steps))
            ]
            logs = []

            for processor_id, (indices, parameter_dict, _) in enumerate(lst):
                # log parameters for this pipeline
                log = log_parameters(
                    processor_id=processor_id, parameter_dict=parameter_dict
                )
                logs.append(log)

                # save parameters with appropriate product mode indices
                for i, coordinate in enumerate(parameter_dict):
                    parameter_ds = parameter_to_dataset(
                        parameter_dict=parameter_dict,
                        dimension_names=dim_names,
                        index=indices[i],
                        coordinate_name=coordinate,
                    )
                    parameters[i].append(parameter_ds)

            # merging/combining the outputs
            final_parameters_list: List[xr.Dataset] = []
            for p in parameters:
                # See issue #276
                new_dataset = xr.combine_by_coords(p)
                if not isinstance(new_dataset, xr.Dataset):
                    raise TypeError("Expecting 'Dataset'.")

                final_parameters_list.append(new_dataset)

            final_parameters_merged = xr.merge(final_parameters_list)

            # See issue #276
            final_logs = xr.combine_by_coords(logs)
            if not isinstance(final_logs, xr.Dataset):
                raise TypeError("Expecting 'Dataset'.")

            # See issue #276
            final_dataset = xr.combine_by_coords(dataset_list)
            if not isinstance(final_dataset, xr.Dataset):
                raise TypeError("Expecting 'Dataset'.")

            result = ObservationResult(
                dataset=final_dataset,
                parameters=final_parameters_merged,
                logs=final_logs,
            )

            return result

        elif self.parameter_mode == ParameterMode.Sequential:

            apply_pipeline = partial(
                self._apply_exposure_pipeline_sequential,
                dimension_names=dim_names,
                x=x,
                y=y,
                processor=processor,
                times=times,
                types=types,
            )

            lst = [
                (index, parameter_dict, n)
                for n, (index, parameter_dict) in enumerate(self._parameter_it()())
            ]

            if self.with_dask:
                dataset_list = db.from_sequence(lst).map(apply_pipeline).compute()
            else:
                dataset_list = list(map(apply_pipeline, tqdm(lst)))

            # prepare lists/dictionaries for to-be-merged datasets
            parameters = [[] for _ in range(len(self.enabled_steps))]
            logs = []

            # overflow to next parameter step counter
            step_counter = -1

            for processor_id, (index, parameter_dict, _) in enumerate(lst):
                # log parameters for this pipeline
                # TODO: somehow refactor logger so that default parameters
                #  from other steps are also logged in sequential mode
                log = log_parameters(
                    processor_id=processor_id, parameter_dict=parameter_dict
                )
                logs.append(log)

                # Figure out current coordinate
                coordinate = str(list(parameter_dict)[0])
                # Check for overflow to next parameter
                if index == 0:
                    step_counter += 1

                # save sequential parameter with appropriate index
                parameter_ds = parameter_to_dataset(
                    parameter_dict=parameter_dict,
                    dimension_names=dim_names,
                    index=index,
                    coordinate_name=coordinate,
                )
                parameters[step_counter].append(parameter_ds)

            # merging/combining the outputs
            # See issue #276
            final_logs = xr.combine_by_coords(logs)
            if not isinstance(final_logs, xr.Dataset):
                raise TypeError("Expecting 'Dataset'.")

            final_datasets = compute_final_sequential_dataset(
                list_of_index_and_parameter=lst,
                list_of_datasets=dataset_list,
                dimension_names=dim_names,
            )

            final_parameters_list = []
            for p in parameters:
                # See issue #276
                new_dataset = xr.combine_by_coords(p)
                if not isinstance(new_dataset, xr.Dataset):
                    raise TypeError("Expecting 'Dataset'.")

                final_parameters_list.append(new_dataset)

            final_parameters_merged = xr.merge(final_parameters_list)

            result = ObservationResult(
                dataset=final_datasets,
                parameters=final_parameters_merged,
                logs=final_logs,
            )
            return result

        elif self.parameter_mode == ParameterMode.Custom:

            apply_pipeline = partial(
                self._apply_exposure_pipeline_custom,
                x=x,
                y=y,
                processor=processor,
                times=times,
            )
            lst = [
                (index, parameter_dict, n)
                for n, (index, parameter_dict) in enumerate(self._parameter_it()())
            ]

            if self.with_dask:
                dataset_list = db.from_sequence(lst).map(apply_pipeline).compute()
            else:
                dataset_list = list(map(apply_pipeline, tqdm(lst)))

            # prepare lists for to-be-merged datasets
            logs = []

            for index, parameter_dict, _ in lst:
                # log parameters for this pipeline
                log = log_parameters(processor_id=index, parameter_dict=parameter_dict)
                logs.append(log)

            # merging/combining the outputs
            final_ds = xr.combine_by_coords(dataset_list)
            final_log = xr.combine_by_coords(logs)

            # See issue #276
            if not isinstance(final_ds, xr.Dataset):
                raise TypeError("Expecting 'Dataset'.")
            if not isinstance(final_log, xr.Dataset):
                raise TypeError("Expecting 'Dataset'.")

            final_parameters = final_log  # parameter dataset same as logs

            result = ObservationResult(
                dataset=final_ds, parameters=final_parameters, logs=final_log
            )
            return result

        else:
            raise ValueError("Parametric mode not specified.")

    def _apply_exposure_pipeline_product(
        self,
        index_and_parameter: Tuple[
            Tuple[int, ...],
            Mapping[
                str,
                Union[str, Number, np.ndarray, List[Union[str, Number, np.ndarray]]],
            ],
            int,
        ],
        dimension_names: Mapping[str, str],
        processor: "Processor",
        x: range,
        y: range,
        times: np.ndarray,
        types: Mapping[str, ParameterType],
    ):

        index, parameter_dict, n = index_and_parameter

        new_processor = create_new_processor(
            processor=processor, parameter_dict=parameter_dict
        )

        # run the pipeline
        _ = run_exposure_pipeline(
            processor=new_processor,
            readout=self.readout,
            result_type=self.result_type,
            pipeline_seed=self.pipeline_seed,
        )

        _ = self.outputs.save_to_file(processor=new_processor, run_number=n)

        ds: xr.Dataset = new_processor.result_to_dataset(
            x=x,
            y=y,
            times=times,
            result_type=self.result_type,
        )

        # Can also be done outside dask in a loop
        ds = _add_product_parameters(
            ds=ds,
            parameter_dict=parameter_dict,
            dimension_names=dimension_names,
            indices=index,
            types=types,
        )

        ds.attrs.update({"running mode": "Observation - Product"})

        return ds

    def _apply_exposure_pipeline_custom(
        self,
        index_and_parameter: Tuple[
            int,
            Mapping[
                str,
                Union[str, Number, np.ndarray, List[Union[str, Number, np.ndarray]]],
            ],
            int,
        ],
        processor: "Processor",
        x: range,
        y: range,
        times: np.ndarray,
    ):

        index, parameter_dict, n = index_and_parameter

        new_processor = create_new_processor(
            processor=processor, parameter_dict=parameter_dict
        )

        # run the pipeline
        _ = run_exposure_pipeline(
            processor=new_processor,
            readout=self.readout,
            result_type=self.result_type,
            pipeline_seed=self.pipeline_seed,
        )

        _ = self.outputs.save_to_file(processor=new_processor, run_number=n)

        ds: xr.Dataset = new_processor.result_to_dataset(
            x=x, y=y, times=times, result_type=self.result_type
        )

        # Can also be done outside dask in a loop
        ds = _add_custom_parameters(
            ds=ds,
            index=index,
        )
        ds.attrs.update({"running mode": "Observation - Custom"})

        return ds

    def _apply_exposure_pipeline_sequential(
        self,
        index_and_parameter: Tuple[
            int,
            Mapping[
                str,
                Union[str, Number, np.ndarray, List[Union[str, Number, np.ndarray]]],
            ],
            int,
        ],
        dimension_names: Mapping[str, str],
        processor: "Processor",
        x: range,
        y: range,
        times: np.ndarray,
        types: Mapping[str, ParameterType],
    ):

        index, parameter_dict, n = index_and_parameter

        new_processor = create_new_processor(
            processor=processor, parameter_dict=parameter_dict
        )

        coordinate = str(list(parameter_dict)[0])

        # run the pipeline
        _ = run_exposure_pipeline(
            processor=new_processor,
            readout=self.readout,
            result_type=self.result_type,
            pipeline_seed=self.pipeline_seed,
        )

        _ = self.outputs.save_to_file(processor=new_processor, run_number=n)

        ds: xr.Dataset = new_processor.result_to_dataset(
            x=x, y=y, times=times, result_type=self.result_type
        )

        # Can also be done outside dask in a loop
        ds = _add_sequential_parameters(
            ds=ds,
            parameter_dict=parameter_dict,
            dimension_names=dimension_names,
            index=index,
            coordinate_name=coordinate,
            types=types,
        )

        ds.attrs.update({"running mode": "Observation - Sequential"})

        return ds

    def debug_parameters(self, processor: "Processor") -> list:
        """List the parameters using processor parameters in processor generator.

        Parameters
        ----------
        processor: Processor

        Returns
        -------
        result: list
        """
        result = []
        processor_generator = self._processors_it(processor=processor)
        for i, (proc, _, _) in enumerate(processor_generator):
            values = []
            for step in self.enabled_steps:
                _, att = get_obj_att(proc, step.key)
                value = get_value(proc, step.key)
                values.append((att, value))
            logging.debug("%d: %r" % (i, values))
            result.append((i, values))
        return result


def create_new_processor(
    processor: "Processor",
    parameter_dict: Mapping[
        str, Union[str, Number, np.ndarray, List[Union[str, Number, np.ndarray]]]
    ],
) -> "Processor":
    """Create a copy of processor and set new attributes from a dictionary before returning it.

    Parameters
    ----------
    processor: Processor
    parameter_dict: dict

    Returns
    -------
    new_processor: Processor
    """

    new_processor = deepcopy(processor)

    for key in parameter_dict.keys():
        new_processor.set(key=key, value=parameter_dict[key])

    return new_processor


def _id(s: str) -> str:
    """Add _id to the end of a string.

    Parameters
    ----------
    s: str

    Returns
    -------
    out: str
    """
    out = s + "_id"
    return out


def short(s: str) -> str:
    """Split string with . and return the last element.

    Parameters
    ----------
    s: str

    Returns
    -------
    out: str
    """
    out = s.split(".")[-1]
    return out


def log_parameters(processor_id: int, parameter_dict: dict) -> "xr.Dataset":
    """Return parameters in the current processor in a xarray dataset.

    Parameters
    ----------
    processor_id: int
    parameter_dict: dict

    Returns
    -------
    out: Dataset
    """
    # Late import to speedup start-up time
    import xarray as xr

    out = xr.Dataset()
    for key, value in parameter_dict.items():
        da = xr.DataArray(value)
        da = da.assign_coords(coords={"id": processor_id})
        da = da.expand_dims(dim="id")
        out[short(key)] = da
    return out


def parameter_to_dataset(
    parameter_dict: dict,
    dimension_names: Mapping[str, str],
    index: int,
    coordinate_name: str,
) -> "xr.Dataset":
    """Return a specific parameter dataset from a parameter dictionary.

    Parameters
    ----------
    parameter_dict: dict
    dimension_names
    index: int
    coordinate_name: str

    Returns
    -------
    parameter_ds: Dataset
    """
    # Late import to speedup start-up time
    import xarray as xr

    parameter_ds = xr.Dataset()
    parameter = xr.DataArray(parameter_dict[coordinate_name])

    # TODO: Dirty hack. Fix this !
    short_name: str = dimension_names[coordinate_name]

    if short_name.endswith("_id"):
        short_coord_name = short_name[:-3]
        short_coord_name_id = short_name
    else:
        short_coord_name = short_name
        short_coord_name_id = f"{short_name}_id"

    parameter = parameter.assign_coords({short_coord_name_id: index})
    parameter = parameter.expand_dims(dim=short_coord_name_id)
    parameter_ds[short_coord_name] = parameter

    return parameter_ds


def _add_custom_parameters(ds: "xr.Dataset", index: int) -> "xr.Dataset":
    """Add coordinate coordinate "index" to the dataset.

    Parameters
    ----------
    ds: Dataset
    index: int

    Returns
    -------
    ds: Dataset
    """

    ds = ds.assign_coords({"id": index})
    ds = ds.expand_dims(dim="id")

    return ds


def _add_sequential_parameters(
    ds: "xr.Dataset",
    parameter_dict: Mapping[
        str, Union[str, Number, np.ndarray, List[Union[str, Number, np.ndarray]]]
    ],
    dimension_names: Mapping[str, str],
    index: int,
    coordinate_name: str,
    types: Mapping[str, ParameterType],
) -> "xr.Dataset":
    """Add true coordinates or index to sequential mode dataset.

    Parameters
    ----------
    ds: Dataset
    parameter_dict: dict
    index: int
    dimension_names
    coordinate_name: str
    types: dict

    Returns
    -------
    ds: Dataset
    """

    #  assigning the right coordinates based on type
    short_name: str = dimension_names[coordinate_name]

    if types[coordinate_name] == ParameterType.Simple:
        ds = ds.assign_coords(coords={short_name: parameter_dict[coordinate_name]})
        ds = ds.expand_dims(dim=short_name)

    elif types[coordinate_name] == ParameterType.Multi:
        ds = ds.assign_coords({short_name: index})
        ds = ds.expand_dims(dim=short_name)

    return ds


def _add_product_parameters(
    ds: "xr.Dataset",
    parameter_dict: Mapping[
        str, Union[str, Number, np.ndarray, List[Union[str, Number, np.ndarray]]]
    ],
    dimension_names: Mapping[str, str],
    indices: Tuple[int, ...],
    types: Mapping[str, ParameterType],
) -> "xr.Dataset":
    """Add true coordinates or index to product mode dataset.

    Parameters
    ----------
    ds: Dataset
    parameter_dict: dict
    indices: tuple
    types: dict

    Returns
    -------
    ds: Dataset
    """
    # TODO: Implement for coordinate 'multi'
    for i, (coordinate_name, param_value) in enumerate(parameter_dict.items()):

        short_name: str = dimension_names[coordinate_name]

        #  assigning the right coordinates based on type
        if types[coordinate_name] == ParameterType.Simple:
            ds = ds.assign_coords(coords={short_name: param_value})
            ds = ds.expand_dims(dim=short_name)

        elif types[coordinate_name] == ParameterType.Multi:
            ds = ds.assign_coords({short_name: indices[i]})
            ds = ds.expand_dims(dim=short_name)

        else:
            raise NotImplementedError

    return ds


def compute_final_sequential_dataset(
    list_of_index_and_parameter: list,
    list_of_datasets: list,
    dimension_names: Mapping[str, str],
) -> Dict[str, "xr.Dataset"]:
    """Return a dictionary of result datasets where keys are different parameters.

    Parameters
    ----------
    list_of_index_and_parameter: list
    list_of_datasets: list
    dimension_names

    Returns
    -------
    final_datasets: dict
    """
    # Late import to speedup start-up time
    import xarray as xr

    final_dict: Dict[str, List[xr.Dataset]] = {}

    for _, parameter_dict, n in list_of_index_and_parameter:
        coordinate = str(list(parameter_dict)[0])
        coordinate_short: str = dimension_names[coordinate]

        if short(coordinate) not in final_dict:
            final_dict.update({coordinate_short: []})
            final_dict[coordinate_short].append(list_of_datasets[n])
        else:
            final_dict[coordinate_short].append(list_of_datasets[n])

    final_datasets: Dict[str, xr.Dataset] = {}
    for key, value in final_dict.items():
        ds = xr.combine_by_coords(value)
        # see issue #276
        if not isinstance(ds, xr.Dataset):
            raise TypeError("Expecting 'Dataset'.")

        final_datasets.update({key: ds})

    return final_datasets
