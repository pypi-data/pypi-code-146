
__module_name__ = "_nn_int.py"
__doc__ = """Brownian Diffusion module formatted for standalone integration."""
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu"])
__version__ = "0.0.2"


# -- import local dependencies: ----------------------------------------------------------
from ._brownian_diffuser import BrownianDiffuser
from ._time import timespan


# -- code: -------------------------------------------------------------------------------
def nn_int(net, X0, t, dt=0.1, stdev=0.5, max_steps=None, return_all=False):

    n_steps = int(timespan(t) / dt)
    diffuser = BrownianDiffuser()
    return diffuser(
        net,
        X0,
        t,
        n_steps=n_steps,
        stdev=stdev,
        max_steps=max_steps,
        return_all=return_all,
    )
