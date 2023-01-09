from datetime import timedelta
from math import floor

from tqdm.auto import tqdm


def swmm5_run_progress(fn_inp, fn_rpt=None, fn_out=None, n_total=100, swmm_lib_path=None):
    """
    Run a simulation with OWA-SWMM (PySWMM package) and adding a progress bar.

    Args:
        fn_inp (str): pointer to name of input file (must exist)
        fn_rpt (str): pointer to name of report file (to be created)
        fn_out (str): pointer to name of binary output file (to be created)
        n_total (int): Number of progress bar iterations.
        swmm_lib_path: User-specified SWMM library path (default None).
    """
    from pyswmm import Simulation

    with Simulation(inputfile=fn_inp, reportfile=fn_rpt, outputfile=fn_out, swmm_lib_path=swmm_lib_path) as sim:
        total_time_seconds = (sim.end_time - sim.start_time) / timedelta(seconds=1)
        sim.step_advance(floor(total_time_seconds / n_total))

        with tqdm(total=n_total, desc=f'swmm5 {fn_inp}') as progress:
            for _ in sim:
                progress.update(1)
                progress.postfix = f'{sim.current_time}'
            progress.update(progress.total - progress.n)
            progress.postfix = f'{sim.current_time}'
