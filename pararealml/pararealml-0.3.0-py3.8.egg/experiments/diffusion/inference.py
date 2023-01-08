import warnings
from typing import Sequence

import numpy as np
from mpi4py import MPI

from pararealml.operators.parareal import PararealOperator
from pararealml.utils.tf import use_cpu
from pararealml.utils.time import mpi_time, time


def print_execution_time_stats(execution_times: Sequence[float], name: str):
    print(
        f"{name} execution time - "
        f"mean: {np.mean(execution_times)}s; sd: {np.std(execution_times)}s"
    )


def parareal_termination_condition(
    _: np.ndarray, new_y_end_points: np.ndarray
) -> bool:
    y_dim = ivp.constrained_problem.differential_equation.y_dimension
    fine_fdm_discrete_sol = fine_fdm_sol.discrete_y()
    max_diff_norms = np.empty(y_dim)
    for y_ind in range(y_dim):
        diff_norms = np.empty(len(new_y_end_points))
        for i, new_y_end_point in enumerate(new_y_end_points[..., y_ind]):
            fine_y_end_point = fine_fdm_discrete_sol[
                (i + 1) * len(fine_fdm_discrete_sol) // len(new_y_end_points)
                - 1,
                ...,
                y_ind,
            ]
            diff_norms[i] = np.sqrt(
                np.square(new_y_end_point - fine_y_end_point).mean()
            )

        max_diff_norms[y_ind] = np.max(diff_norms)

    return all(max_diff_norms < parareal_tol)


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.rank

    use_cpu()

    warnings.filterwarnings("ignore", category=RuntimeWarning)

    from experiments.diffusion.ivp import ivp
    from experiments.diffusion.operators import (
        coarse_ar,
        coarse_fast_fdm,
        coarse_fdm,
        coarse_pidon,
        fine_fdm,
    )

    coarse_ar.model.model.load_weights("weights/ar").expect_partial()
    coarse_pidon.model.load_weights("weights/pidon").expect_partial()

    parareal_tol = np.array([3.49572636e-05])
    parareal_fdm = PararealOperator(
        fine_fdm, coarse_fdm, parareal_termination_condition
    )
    parareal_fast_fdm = PararealOperator(
        fine_fdm, coarse_fast_fdm, parareal_termination_condition
    )
    parareal_ar = PararealOperator(
        fine_fdm, coarse_ar, parareal_termination_condition
    )
    parareal_pidon = PararealOperator(
        fine_fdm, coarse_pidon, parareal_termination_condition
    )

    n_warmup_runs = 5
    n_real_runs = 50

    fine_fdm_sol = None
    coarse_fdm_sol = None
    coarse_fast_fdm_sol = None
    coarse_ar_sol = None
    coarse_pidon_sol = None

    parareal_fdm_sol = None
    parareal_fast_fdm_sol = None
    parareal_ar_sol = None
    parareal_pidon_sol = None

    fine_fdm_times = []
    coarse_fdm_times = []
    coarse_fast_fdm_times = []
    coarse_ar_times = []
    coarse_pidon_times = []

    parareal_fdm_times = []
    parareal_fast_fdm_times = []
    parareal_ar_times = []
    parareal_pidon_times = []

    for run_ind in range(n_warmup_runs + n_real_runs):
        fine_fdm_sol, fine_fdm_time = time(f"rank {rank} fine fdm")(
            fine_fdm.solve
        )(ivp)
        coarse_fdm_sol, coarse_fdm_time = time(f"rank {rank} coarse fdm")(
            coarse_fdm.solve
        )(ivp)
        coarse_fast_fdm_sol, coarse_fast_fdm_time = time(
            f"rank {rank} coarse fast fdm"
        )(coarse_fast_fdm.solve)(ivp)
        coarse_ar_sol, coarse_ar_time = time(f"rank {rank} coarse ar")(
            coarse_ar.solve
        )(ivp)
        coarse_pidon_sol, coarse_pidon_time = time(
            f"rank {rank} coarse pidon"
        )(coarse_pidon.solve)(ivp)

        parareal_fdm_sol, parareal_fdm_time = mpi_time("parareal fdm")(
            parareal_fdm.solve
        )(ivp)
        parareal_fast_fdm_sol, parareal_fast_fdm_time = mpi_time(
            "parareal fast fdm"
        )(parareal_fast_fdm.solve)(ivp)
        parareal_ar_sol, parareal_ar_time = mpi_time("parareal ar")(
            parareal_ar.solve
        )(ivp)
        parareal_pidon_sol, parareal_pidon_time = mpi_time("parareal pidon")(
            parareal_pidon.solve
        )(ivp)

        if run_ind >= n_warmup_runs:
            fine_fdm_times.append(fine_fdm_time)
            coarse_fdm_times.append(coarse_fdm_time)
            coarse_fast_fdm_times.append(coarse_fast_fdm_time)
            coarse_ar_times.append(coarse_ar_time)
            coarse_pidon_times.append(coarse_pidon_time)

            parareal_fdm_times.append(parareal_fdm_time)
            parareal_fast_fdm_times.append(parareal_fast_fdm_time)
            parareal_ar_times.append(parareal_ar_time)
            parareal_pidon_times.append(parareal_pidon_time)

    if rank == 0:
        print_execution_time_stats(fine_fdm_times, "fine fdm")
        print_execution_time_stats(coarse_fdm_times, "coarse fdm")
        print_execution_time_stats(coarse_fast_fdm_times, "coarse fast fdm")
        print_execution_time_stats(coarse_ar_times, "coarse ar")
        print_execution_time_stats(coarse_pidon_times, "coarse pidon")

        print_execution_time_stats(parareal_fdm_times, "parareal fdm")
        print_execution_time_stats(
            parareal_fast_fdm_times, "parareal fast fdm"
        )
        print_execution_time_stats(parareal_ar_times, "parareal ar")
        print_execution_time_stats(parareal_pidon_times, "parareal pidon")
