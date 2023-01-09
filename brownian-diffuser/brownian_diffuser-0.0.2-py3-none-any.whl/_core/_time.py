
__module_name__ = "_time.py"
__doc__ = """Time Module"""
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu"])
__version__ = "0.0.2"


# -- import packages: --------------------------------------------------------------------
import numpy as np
import torch


# -- code: -------------------------------------------------------------------------------
def timespan(t: (torch.Tensor or np.ndarray)):
    """Return the difference between the min and max time passed."""
    return (t.max() - t.min()).item()


# -- controller class: -------------------------------------------------------------------
class TimeConfiguration:
    def __parse__(self, kwargs, ignore=["self"]):

        for key, val in kwargs.items():
            if not key in ignore:
                setattr(self, key, val)

    def __init__(self, t: torch.Tensor, n_steps: int = 40):
        """
        
        Parameters:
        -----------
        t
            Unique time points.
            type: torch.Tensor
        
        n_steps
            Number of steps taken by generator.
            type: int
            default: 40
        """
        self.__parse__(locals())

    @property
    def timespan(self):
        """Return the difference between the min and max time passed."""
        return timespan(self.t)

    @property
    def dt(self):
        """Return uniform step size."""
        return self.timespan / self.n_steps

    @property
    def t0(self):
        """Initial time point"""
        return self.t[0].item()

    @property
    def tf(self):
        """Final time point"""
        return self.t[-1].item()
