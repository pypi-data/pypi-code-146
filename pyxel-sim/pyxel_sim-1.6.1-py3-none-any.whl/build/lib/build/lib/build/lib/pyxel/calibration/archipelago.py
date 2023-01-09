#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""Sub-package to create 'archipelagos'."""
import logging
from concurrent.futures.thread import ThreadPoolExecutor
from timeit import default_timer as timer
from typing import (
    TYPE_CHECKING,
    Callable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import dask.array as da
import numpy as np
import pandas as pd
import xarray as xr
from dask.delayed import Delayed
from tqdm.auto import tqdm

from pyxel.calibration import Algorithm, AlgorithmType, IslandProtocol
from pyxel.calibration.fitting import ModelFitting
from pyxel.calibration.util import slice_to_range

if TYPE_CHECKING:
    import pygmo as pg
    from numpy.typing import ArrayLike

    from pyxel.exposure import Readout


class ArchipelagoLogs:
    """Keep log information from all algorithms in an archipelago."""

    def __init__(self, algo_type: AlgorithmType, num_generations: int):
        try:
            import pygmo as pg
        except ImportError as exc:
            raise ImportError(
                "Missing optional package 'pygmo'.\n"
                "Please install it with 'pip install pyxel-sim[calibration]' "
                "or 'pip install pyxel-sim[all]'"
            ) from exc

        self._df = pd.DataFrame()
        self._num_generations = num_generations

        # Get logging's columns that will be extracted from the algorithm
        if algo_type is not AlgorithmType.Sade:
            raise NotImplementedError

        self._columns = (
            "num_generations",  # Generation number
            "num_evaluations",  # Number of functions evaluation made
            "best_fitness",  # The best fitness currently in the population
            "f",
            "cr",
            "dx",
            "df",
        )  # See: https://esa.github.io/pygmo2/algorithms.html#pygmo.sade.get_log
        self._algo_to_extract = pg.sade

    def _from_algo(self, algo: "pg.algorithm") -> pd.DataFrame:
        """Get logging information from an algorithm."""
        # Extract the Pygmo algorithm and its logging information
        algo_extracted = algo.extract(self._algo_to_extract)
        logs: list = algo_extracted.get_log()

        # Put the logging information from pygmo into a `DataFrame`
        df = pd.DataFrame(logs, columns=self._columns)

        return df

    def _from_archi(self, archi: "pg.archipelago") -> pd.DataFrame:
        """Get logging information from an archipelago."""
        lst: List[pd.DataFrame] = []

        for id_island, island in enumerate(archi):
            # Extract the Pygmo algorithm from an island
            df_island = self._from_algo(algo=island.get_algorithm())
            df_island["id_island"] = id_island + 1

            lst.append(df_island)

        df_archipelago = pd.concat(lst)
        return df_archipelago

    # TODO: Remove parameter 'id_evolution' ?
    def append(self, archi: "pg.archipelago", id_evolution: int) -> None:
        """Collect logging information from a archipelago for specified evolution id."""
        partial_df: pd.DataFrame = self._from_archi(archi=archi)
        partial_df["id_evolution"] = id_evolution

        self._df = pd.concat([self._df, partial_df])

    def get_full_total(self) -> pd.DataFrame:
        """TBW."""
        new_df = self._df.reset_index(drop=True)
        new_df["global_num_generations"] = (
            new_df["id_evolution"] - 1
        ) * self._num_generations + new_df["num_generations"]

        return new_df

    def get_total(self) -> pd.DataFrame:
        """TBW."""
        df: pd.DataFrame = self.get_full_total()
        return df[
            ["id_evolution", "id_island", "global_num_generations", "best_fitness"]
        ]


def extract_data_3d(
    df_results: pd.DataFrame,
    rows: int,
    cols: int,
    times: int,
    readout_times: np.ndarray,
) -> xr.Dataset:
    """Extract 'image', 'signal' and 'pixel' arrays from several delayed dynamic results."""
    lst: List[xr.Dataset] = []
    for _, row in df_results.iterrows():
        island: int = row["island"]
        id_processor: int = row["id_processor"]
        result: Mapping[str, Delayed] = row["processor"].result

        image_delayed: Delayed = result["image"]
        signal_delayed: Delayed = result["signal"]
        pixel_delayed: Delayed = result["pixel"]

        image_3d = da.from_delayed(
            image_delayed, shape=(times, rows, cols), dtype=float
        )
        signal_3d = da.from_delayed(
            signal_delayed, shape=(times, rows, cols), dtype=float
        )
        pixel_3d = da.from_delayed(
            pixel_delayed, shape=(times, rows, cols), dtype=float
        )

        partial_ds = xr.Dataset()
        partial_ds["simulated_image"] = xr.DataArray(
            image_3d, dims=["readout_time", "y", "x"]
        )
        partial_ds["simulated_signal"] = xr.DataArray(
            signal_3d, dims=["readout_time", "y", "x"]
        )
        partial_ds["simulated_pixel"] = xr.DataArray(
            pixel_3d, dims=["readout_time", "y", "x"]
        )

        lst.append(
            partial_ds.assign_coords(
                island=island,
                id_processor=id_processor,
            ).expand_dims(["island", "id_processor"])
        )

    ds: Union[xr.Dataset, xr.DataArray] = xr.combine_by_coords(lst).assign_coords(
        readout_time=readout_times,
        y=range(rows),
        x=range(cols),
    )

    if not isinstance(ds, xr.Dataset):
        raise TypeError("Expected a Dataset.")

    return ds


# TODO: Rename to PyxelArchipelago. See #335
class MyArchipelago:
    """User-defined Archipelago."""

    def __init__(
        self,
        num_islands: int,
        udi: IslandProtocol,
        algorithm: Algorithm,
        problem: ModelFitting,
        pop_size: int,
        bfe: Optional[Callable] = None,
        topology: Optional[Callable] = None,
        pygmo_seed: Optional[int] = None,
        parallel: bool = True,
        with_bar: bool = False,
    ):
        try:
            import pygmo as pg
        except ImportError as exc:
            raise ImportError(
                "Missing optional package 'pygmo'.\n"
                "Please install it with 'pip install pyxel-sim[calibration]' "
                "or 'pip install pyxel-sim[all]'"
            ) from exc

        self._log = logging.getLogger(__name__)

        self.num_islands = num_islands
        self.udi = udi
        self.algorithm: Algorithm = algorithm
        self.problem: ModelFitting = problem
        self.pop_size = pop_size
        self.bfe = bfe
        self.topology = topology
        self.pygmo_seed = pygmo_seed
        self.parallel = parallel
        self.with_bar = with_bar

        # Create a Pygmo archipelago
        self._pygmo_archi = pg.archipelago(t=self.topology)

        # Create a Pygmo algorithm
        verbosity_level: int = max(1, self.algorithm.population_size // 100)

        self._pygmo_algo: pg.algorithm = pg.algorithm(self.algorithm.get_algorithm())
        self._pygmo_algo.set_verbosity(verbosity_level)
        self._log.info(self._pygmo_algo)

        # Create a Pygmo problem
        self._pygmo_prob: pg.problem = pg.problem(self.problem)
        self._log.info(self._pygmo_prob)

        # Build the archipelago
        self._build()

    def _build(self) -> None:
        """Build the island(s) and populate them."""
        import pygmo as pg

        disable_bar: bool = not self.with_bar
        start_time: float = timer()

        def create_island(seed: Optional[int] = None) -> pg.island:
            """Create a new island."""
            return pg.island(
                udi=self.udi,
                algo=self._pygmo_algo,
                prob=self._pygmo_prob,
                b=self.bfe,
                size=self.pop_size,
                seed=seed,
            )

        # Create a seed for each island
        if self.pygmo_seed is None:
            seeds: Sequence[Optional[int]] = [None] * self.num_islands
        else:
            rng: np.random.Generator = np.random.default_rng(seed=self.pygmo_seed)
            max_value: int = np.iinfo(np.uint32).max
            seeds = [int(rng.integers(0, max_value)) for _ in range(self.num_islands)]

        # Create the islands and add them to this archipelago
        if self.parallel:
            # Create the islands in parallel with Threads
            with ThreadPoolExecutor(max_workers=self.num_islands) as executor:
                it = executor.map(create_island, seeds)

                for island in tqdm(
                    it,
                    desc="Create islands",
                    total=self.num_islands,
                    disable=disable_bar,
                ):
                    self._pygmo_archi.push_back(island)
        else:
            # Create the islands sequentially
            it = map(create_island, seeds)
            for island in tqdm(
                it, desc="Create islands", total=self.num_islands, disable=disable_bar
            ):
                self._pygmo_archi.push_back(island)

        stop_time = timer()
        logging.info("Create a new archipelago in %.2f s", stop_time - start_time)

    def run_evolve(
        self,
        readout: "Readout",
        num_evolutions: int = 1,
        num_best_decisions: Optional[int] = None,
    ) -> Tuple[xr.Dataset, pd.DataFrame, pd.DataFrame]:
        """Run evolution(s) several time.

        Parameters
        ----------
        sampling
        num_evolutions : int
            Number of time to run the evolutions.
        num_best_decisions : int or None, optional.
            Number of best individuals to extract. If this parameter is set to None then
            no individuals are extracted.

        Returns
        -------
        TBW.
        """
        self._log.info("Run %i evolutions", num_evolutions)
        logs = ArchipelagoLogs(
            algo_type=self.algorithm.type, num_generations=self.algorithm.generations
        )

        total_num_generations = num_evolutions * self.algorithm.generations

        with tqdm(
            total=total_num_generations,
            desc=f"Evolve with {self.num_islands} islands",
            unit=" generations",
            disable=not self.with_bar,
        ) as progress:

            champions_lst: List[xr.Dataset] = []
            # Run an evolution im the archipelago several times
            for id_evolution in range(num_evolutions):
                # If the evolution on this archipelago was already run before, then
                # the migration process between the islands is automatically executed
                # Call all 'evolve()' methods on all islands
                self._pygmo_archi.evolve()
                # self._log.info(self._pygmo_archi)  # TODO: Remove this

                # Block until all evolutions have finished and raise the first exception
                # that was encountered
                self._pygmo_archi.wait_check()

                # Collect logging information from the algorithms running in the
                # archipelago
                logs.append(archi=self._pygmo_archi, id_evolution=id_evolution + 1)

                progress.update(self.algorithm.generations)

                # Get partial champions for this evolution
                partial_champions: xr.Dataset = self._get_champions()

                # Get best population from the islands
                if num_best_decisions:
                    best_individuals: xr.Dataset = self.get_best_individuals(
                        num_best_decisions=num_best_decisions
                    )

                    all_champions = xr.merge([partial_champions, best_individuals])
                else:
                    all_champions = partial_champions

                champions_lst.append(
                    all_champions.assign_coords(evolution=id_evolution)
                )

        champions: xr.Dataset = xr.concat(champions_lst, dim="evolution")

        # Get logging information
        df_all_logs: pd.DataFrame = logs.get_full_total()

        # Get the champions in a `Dataset`
        last_champions = champions.isel(evolution=-1)

        # Get the processor(s) in a `DataFrame`
        df_results: pd.DataFrame = self.problem.apply_parameters_to_processors(
            parameters=last_champions["champion_parameters"],
        )

        assert isinstance(self.problem.sim_fit_range, tuple)
        slice_times, slice_rows, slice_cols = self.problem.sim_fit_range

        geometry = self.problem.processor.detector.geometry
        no_times = len(readout.times)

        # Extract simulated 'image', 'signal' and 'pixel' from the processors
        all_simulated_full = extract_data_3d(
            df_results=df_results,
            rows=geometry.row,
            cols=geometry.col,
            times=no_times,
            readout_times=readout.times,
        )

        # Get the target data
        all_data_fit_range = all_simulated_full.sel(
            y=slice_rows, x=slice_cols, readout_time=slice_times
        )
        if readout.time_domain_simulation:
            all_data_fit_range["target"] = xr.DataArray(
                self.problem.all_target_data,
                dims=["id_processor", "readout_time", "y", "x"],
                coords={
                    "id_processor": range(len(self.problem.all_target_data)),
                    "readout_time": slice_to_range(slice_times),
                    "y": slice_to_range(slice_rows),
                    "x": slice_to_range(slice_cols),
                },
            )
        else:
            all_data_fit_range["target"] = xr.DataArray(
                self.problem.all_target_data,
                dims=["id_processor", "y", "x"],
                coords={
                    "id_processor": range(len(self.problem.all_target_data)),
                    "y": slice_to_range(slice_rows),
                    "x": slice_to_range(slice_cols),
                },
            )

        ds: xr.Dataset = xr.merge([champions, all_data_fit_range])

        ds.attrs["num_islands"] = self.num_islands
        ds.attrs["population_size"] = self.algorithm.population_size
        ds.attrs["num_evolutions"] = num_evolutions
        ds.attrs["generations"] = self.algorithm.generations

        ds = ds.assign_coords({"param_id": range(ds.dims["param_id"])})

        return ds, df_results, df_all_logs

    def _get_champions(self) -> xr.Dataset:
        """Extract the champions.

        Returns
        -------
        Dataset
            A dataset containing the champions.

        Examples
        --------
        >>> self._get_champions()
        <xarray.Dataset>
        Dimensions:              (island: 2, param_id: 7)
        Dimensions without coordinates: island, param_id
        Data variables:
            champion_fitness     (island) float64 3.285e+04 4.102e+04
            champion_decision    (island, param_id) float64 0.1526 -1.977 ... 0.9329
            champion_parameters  (island, param_id) float64 0.1526 -1.977 ... 8.568
        """
        # Get fitness and decision vectors of the num_islands' champions
        champions_1d_fitness: ArrayLike = self._pygmo_archi.get_champions_f()

        champions_1d_decision: ArrayLike = self._pygmo_archi.get_champions_x()

        # Get the champions as a Dataset
        champions = xr.Dataset()
        champions["champion_fitness"] = xr.DataArray(
            np.ravel(champions_1d_fitness), dims="island"
        )
        champions["champion_decision"] = xr.DataArray(
            champions_1d_decision, dims=["island", "param_id"]
        )
        champions["champion_parameters"] = xr.DataArray(
            self.problem.convert_to_parameters(champions["champion_decision"]),
            dims=["island", "param_id"],
        )

        return champions

    def get_best_individuals(self, num_best_decisions: int) -> xr.Dataset:
        """Get the best decision vectors and fitness from the island of an archipelago.

        Parameters
        ----------
        num_best_decisions : int or None, optional.
            Number of best individuals to extract. If this parameter is set to None then
            no individuals are extracted.

        Returns
        -------
        Dataset
            A new dataset with two data arrays 'best_decision' and 'best_fitness'.

        Examples
        --------
        >>> archi = MyArchipelago(...)
        >>> archi.get_best_individuals(num_best_decisions=5)
        <xarray.Dataset>
        Dimensions:          (individual: 10, island: 2, param_id: 7)
        Coordinates:
          * island           (island) int64 0 1
          * individual       (individual) int64 0 1 2 3 4 5 6 7 8 9
        Dimensions without coordinates: param_id
        Data variables:
            best_decision    (island, individual, param_id) float64 0.1526 ... 0.1608
            best_parameters  (island, individual, param_id) float64 0.1526 ... 0.1608
            best_fitness     (island, individual) float64 3.285e+04 ... 5.732e+04

        Raises
        ------
        ValueError
            Raised if 'num_best_decisions' is a negative 'int' value.
        """
        if num_best_decisions < 0:
            raise ValueError(
                "'num_best_decisions' must be 'None' or a positive integer"
            )

        lst = []
        for island_idx, island in enumerate(self._pygmo_archi):
            population: pg.population = island.get_population()

            # Get the decision vectors: num_individuals x size_decision_vector
            decision_vectors_2d: np.ndarray = population.get_x()

            # Get the fitness vectors: num_individuals x 1
            fitness_vectors_2d: np.ndarray = population.get_f()

            # Convert the decision vectors to parameters:
            #   num_individuals x size_decision_vector
            parameters_2d = self.problem.convert_to_parameters(decision_vectors_2d)

            # Add the vectors into a Dataset
            island_population = xr.Dataset()
            island_population["best_decision"] = xr.DataArray(
                decision_vectors_2d, dims=["individual", "param_id"]
            )
            island_population["best_parameters"] = xr.DataArray(
                parameters_2d, dims=["individual", "param_id"]
            )
            island_population["best_fitness"] = xr.DataArray(
                fitness_vectors_2d.flatten(), dims=["individual"]
            )

            # Get the indexes for the best fitness vectors
            # and extract the 'num_besnum_best_decisionst_decisions' individuals
            all_indexes_sorted = island_population["best_fitness"].argsort()
            first_indexes_sorted = all_indexes_sorted[:num_best_decisions]

            # Use the indexes to get the best elements
            island_best_population = island_population.sel(
                individual=first_indexes_sorted
            )

            # Append the result and add a new coordinate 'island'
            lst.append(island_best_population.assign_coords(island=island_idx))

        # Create a new dataset
        best_individuals_no_coordinates = xr.concat(lst, dim="island")

        # Add coordinates
        num_individuals = len(best_individuals_no_coordinates["individual"])
        best_individuals: xr.Dataset = best_individuals_no_coordinates.assign_coords(
            individual=range(num_individuals),
            island=range(len(self._pygmo_archi)),
        )

        return best_individuals
