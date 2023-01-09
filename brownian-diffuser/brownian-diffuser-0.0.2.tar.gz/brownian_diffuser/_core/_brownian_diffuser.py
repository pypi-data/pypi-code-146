
__module_name__ = "_brownian_diffuser.py"
__doc__ = """BrownianDiffuser Module"""
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu"])
__version__ = "0.0.2"


# -- import packages: --------------------------------------------------------------------
from autodevice import AutoDevice
import numpy as np
import torch


# -- import local dependencies: ----------------------------------------------------------
from ._time import TimeConfiguration
from ._brownian_motion import BrownianMotion


# -- main BrownianDiffuser class: --------------------------------------------------------
class BrownianDiffuser(torch.nn.Module):
    """Class for manual drift functions"""

    def __init__(self):
        super(BrownianDiffuser, self).__init__()

    # -- configurations: -----------------------------------------------------------------
    def __repr__(self):
        return "Potential Drift Model"

    def __parse__(self, kwargs, ignore=["self"]):
        """parse passed keyword arguments"""
        for key, val in kwargs.items():
            if not key in ignore:
                setattr(self, key, val)

    def _configure_forward(self):
        """configure the forward function"""
        if self.is_potential_net:
            setattr(self, "forward", getattr(self, "potential_drift"))
        else:
            setattr(self, "forward", getattr(self, "forward_drift"))

    def _configure_brownian_motion(self, X_state):
        """
        Determine which function should be called for calculating drift.
        Should only called once - run once upon calling w.r.t. the data.
        """
        self._brownian_motion = BrownianMotion(
            X_state, n_steps=self.steps_to_take, stdev=self.stdev.to(self.device), device=self.device,
        )
        
    def __config__(self, X0, kwargs, ignore=["self", "X0"]):
        self.__parse__(kwargs, ignore)
        self._configure_forward()
        self.time = TimeConfiguration(self.t)
        self.device = AutoDevice()
        self._configure_brownian_motion(X0)

    # -- properties: ---------------------------------------------------------------------
    @property
    def t0(self):
        return self.time.t0

    @property
    def tf(self):
        return self.time.tf

    @property
    def dt(self):
        return self.time.dt

    @property
    def timespan(self):
        return self.time.timespan

    @property
    def brownian_motion(self):
        return self._brownian_motion()

    @property
    def sqrt_dt(self):
        return np.sqrt(self.dt)

    @property
    def n_forward_steps(self):
        return len(self.t[1:])

    @property
    def step_size(self):
        return int(self.n_steps / self.n_forward_steps)

    @property
    def is_potential_net(self):
        """Assumes potential is 1-D"""
        return list(self.net.parameters())[-1].shape[0] == 1

    @property
    def steps_to_take(self):
        """Return number of steps to take, accounting for breaking max."""
        if self.max_steps:
            return self.max_steps + 1
        return self.n_steps + 1

    # -- key functions: ------------------------------------------------------------------
    def potential_drift(self, X_state):
        """
        Return the drift position as the gradient of the potential.
        """
        X_psi = self.potential(X_state.requires_grad_())
        return torch.autograd.grad(
            X_psi, X_state, torch.ones_like(X_psi), create_graph=True
        )[0]

    def forward_drift(self, X_state):
        """
        If not a potential_net, simply pass the torch.nn.Module
        through the network.
        """
        return self.net(X_state)

    def potential(self, x):
        """Pass through potential net"""
        if self.is_potential_net:
            return self.net(x)
        else:
            raise ValueError("Not a potential net")

    def _brownian_step(self, X_state, Z_step):
        """
        Take a singular brownian step.
        """
        return X_state + self.forward(X_state) * self.dt + Z_step * self.sqrt_dt

    def _run_generator(self, X0):
        """
        Flat memory stepper. Generator to control / execute brownian stepping.

        Parameters:
        -----------
        X0
            type: torch.Tensor

        Returns:
        --------
        """

        current_step = 0
        X_state = X0
        Z = self.brownian_motion.to(self.device)
        
        while current_step < self.steps_to_take:
            if current_step == 0:
                yield X_state
            else:
                yield self._brownian_step(X_state, Z[current_step])
            current_step += 1

    # -- API-facing function call: -------------------------------------------------------
    def __call__(self, net, X0, t, n_steps=40, stdev=0.5, max_steps=None, return_all=False):
        """
        Parameters:
        -----------
        X0
            type: torch.Tensor

        Returns:
        --------
        X_pred
            type: torch.Tensor

        Notes:
        ------
        (1) Main API-facing function call.
        """
        
        self.__config__(X0, locals())
        X_pred = list(self._run_generator(X0))
        if not return_all:
            return torch.stack(X_pred[:: self.step_size])
        return torch.stack(X_pred)
