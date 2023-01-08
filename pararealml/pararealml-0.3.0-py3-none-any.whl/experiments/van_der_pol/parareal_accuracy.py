import numpy as np
from mpi4py import MPI

from pararealml.operators.parareal import PararealOperator
from pararealml.utils.tf import use_cpu

if __name__ == "__main__":
    use_cpu()

    comm = MPI.COMM_WORLD
    rank = comm.rank
    size = comm.size

    from experiments.van_der_pol.ivp import ivp
    from experiments.van_der_pol.operators import (
        coarse_ar,
        coarse_fast_fdm,
        coarse_fdm,
        coarse_pidon,
        fine_fdm,
    )

    coarse_ar.model.model.load_weights("weights/ar").expect_partial()
    coarse_pidon.model.load_weights("weights/pidon").expect_partial()

    fine_fdm_sol = fine_fdm.solve(ivp)
    coarse_fdm_sol = coarse_fdm.solve(ivp)
    coarse_fast_fdm_sol = coarse_fast_fdm.solve(ivp)
    coarse_ar_sol = coarse_ar.solve(ivp)
    coarse_pidon_sol = coarse_pidon.solve(ivp)

    if rank == 0:
        coarse_end_point_diff = fine_fdm_sol.diff(
            [
                coarse_fdm_sol,
                coarse_fast_fdm_sol,
                coarse_ar_sol,
                coarse_pidon_sol,
            ]
        )
        coarse_end_point_rms_diffs = np.sqrt(
            np.square(np.stack(coarse_end_point_diff.differences))
        )
        print(
            "Coarse - sub-solution end-point RMS differences:\n"
            f"{coarse_end_point_rms_diffs}\n"
        )

    for n_parareal_iterations in range(1, size + 1):
        parareal_fdm = PararealOperator(
            fine_fdm, coarse_fdm, 0.0, n_parareal_iterations
        )
        parareal_fast_fdm = PararealOperator(
            fine_fdm, coarse_fast_fdm, 0.0, n_parareal_iterations
        )
        parareal_ar = PararealOperator(
            fine_fdm, coarse_ar, 0.0, n_parareal_iterations
        )
        parareal_pidon = PararealOperator(
            fine_fdm, coarse_pidon, 0.0, n_parareal_iterations
        )

        parareal_fdm_sol = parareal_fdm.solve(ivp)
        parareal_fast_fdm_sol = parareal_fast_fdm.solve(ivp)
        parareal_ar_sol = parareal_ar.solve(ivp)
        parareal_pidon_sol = parareal_pidon.solve(ivp)

        if rank == 0:
            parareal_end_point_diff = fine_fdm_sol.diff(
                [
                    coarse_fdm_sol,
                    coarse_fast_fdm_sol,
                    coarse_ar_sol,
                    coarse_pidon_sol,
                    parareal_fdm_sol,
                    parareal_fast_fdm_sol,
                    parareal_ar_sol,
                    parareal_pidon_sol,
                ]
            )
            parareal_end_point_rms_diffs = np.sqrt(
                np.square(np.stack(parareal_end_point_diff.differences[4:]))
            )
            print(
                f"Parareal iterations {n_parareal_iterations} - "
                "sub-solution end-point RMS differences:\n"
                f"{parareal_end_point_rms_diffs}\n"
            )

            parareal_full_rms_diffs = np.array(
                [
                    np.sqrt(
                        np.square(
                            fine_fdm_sol.discrete_y() - sol.discrete_y()
                        ).mean(axis=0)
                    )
                    for sol in [
                        parareal_fdm_sol,
                        parareal_fast_fdm_sol,
                        parareal_ar_sol,
                        parareal_pidon_sol,
                    ]
                ]
            )
            print(
                f"Parareal iterations {n_parareal_iterations} - "
                "full solution RMS differences:\n"
                f"{parareal_full_rms_diffs}\n"
            )
