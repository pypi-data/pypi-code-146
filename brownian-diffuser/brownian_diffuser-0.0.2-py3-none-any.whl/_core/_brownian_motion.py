
__module_name__ = "_brownian_motion.py"
__doc__ = """Brownian Motion Module"""
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu"])
__version__ = "0.0.2"


# -- import packages: --------------------------------------------------------------------
import torch
from autodevice import AutoDevice


# -- main module class: ------------------------------------------------------------------
class BrownianMotion:
    def __parse__(self, kwargs, ignore=["self"]):

        for key, val in kwargs.items():
            if not key in ignore:
                setattr(self, key, val)

    def __init__(self, X_state: torch.Tensor, stdev: float, n_steps: int, device = AutoDevice()) -> None:

        """
        Brownian Motion class

        Parameters:
        -----------
        X_state
            Representative cell state of shape: (n_cells, n_dim)
            type: torch.Tensor
        stdev
            parameter specifying the magnitude of brownian motion
        n_steps
            Number of brownian "steps" to be generated

        Returns:
        --------
        z
            Brownian motion tensor of size: (n_steps, n_cells, n_dim)
            type: torch.Tensor
        """

        self.__parse__(locals())

    @property
    def state_shape(self) -> list:
        """
        State shape.
        
        Parameters:
        -----------
        None
        
        Returns:
        --------
        state_shape
            type: list
        """
        return list(self.X_state.shape)

    @property
    def temporal_state_shape(self) -> list:
        """
        Temporal state shape. n_steps x state_shape.
        
        Parameters:
        -----------
        None
        
        Returns:
        --------
        temporal_state_shape
            type: list
        """
        return [self.n_steps] + self.state_shape

    def __call__(self):
        """Create brownian motion Tensor."""
        return torch.randn(self.temporal_state_shape, requires_grad=True).to(
            self.device
        ) * self.stdev.to(self.device)

    def __repr__(self):
        return "Brownian Motion Generator"
