#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0302
"""
LISA Orbits

This module implements orbit classes.

Authors:
    Jean-Baptiste Bayle <j2b.bayle@gmail.com>
    Marc Lilley <marc.lilley@gmail.com>
    Aurelien Hees <aurelien.hees@obspm.fr>
"""

import abc
import logging
import datetime
import h5py
import numpy as np
import scipy.interpolate
import importlib_resources
import importlib_metadata
import matplotlib.pyplot as plt
from oem import OrbitEphemerisMessage
from packaging.specifiers import SpecifierSet

from lisaconstants import c
from lisaconstants import ASTRONOMICAL_UNIT
from lisaconstants import ASTRONOMICAL_YEAR
from lisaconstants import SUN_SCHWARZSCHILD_RADIUS

from .utils import dot, norm, receiver, emitter
from .utils import arrayindex, atleast_2d

logger = logging.getLogger(__name__)


class Orbits(abc.ABC):
    """Abstract base class for concrete orbit classes.

    Use the sampling parameters ``dt``, ``size``, and ``t0`` arguments to define
    a regular default time grid. Use the ``t`` argument to define a custom
    (possibly irregular) default time vector. Note that doing so overrides the
    previously-described sampling parameters.

    The default time grid is used to sample the various orbital quantities when
    plotting or writing to an orbit file. The default time grid is also used
    if a :meth:`compute_...()` method is called without a time argument.

    Args:
        dt (float): sampling period [s]
        size (int): simulation size [samples]
        t0 (float): initial time [datetime.datetime]
        tt_method (str): light travel time computation method, one of 'analytic' or 'iterative'
        tt_order (int): light travel time series expansion order (0, 1 or 2)
        tt_niter (int): number of iterations for light travel times iterative procedure
        ignore_shapiro (bool): whether Shapiro delay are in light travel times
        t (array-like): list of UNIX timestamps defining a custom default time grid
    """

    #: ((3,) ndarray) Spacecraft indices.
    SC = np.array([1, 2, 3])

    #: ((6,) ndarray) Link (or MOSA) indices.
    LINKS = np.array([12, 23, 31, 13, 32, 21])

    #: (:obj:`datetime.datetime`) Default initial time for orbits, Jan. 1st 2034 at midnight.
    #: It is ``2019686400.0`` as a UNIX timestamp.
    DEFAULT_T0 = datetime.datetime.fromisoformat('2034-01-01 00:00:00')

    def __init__(self,
                 dt=100000,
                 size=316,
                 t0=DEFAULT_T0,
                 tt_method='analytic',
                 tt_order=2,
                 tt_niter=4,
                 ignore_shapiro=False,
                 t=None):
        # pylint: disable=too-many-arguments

        self.git_url = 'https://gitlab.in2p3.fr/lisa-simulation/orbits'
        self.version = importlib_metadata.version('lisaorbits')
        self.generator = self.__class__.__name__
        logger.info("Initializing orbits (lisaorbit verion %s)", self.version)

        #: str: Light travel time computation method.
        self.tt_method = str(tt_method)
        #: int: Maximum relativistic order for light travel time analytical
        #: expansion (use twice the half-integer order to make it an integer).
        self.tt_order = int(tt_order)
        #: int: Number of iterations for the light travel time iterative method.
        self.tt_niter = int(tt_niter)
        #: bool: Whether Shapiro delay is included in the computation
        # #: of light travel times.
        self.ignore_shapiro = bool(ignore_shapiro)

        if t is None:
            logger.debug("Using regular sampling (dt=%f, t0=%s, size=%d)", dt, t0, size)
            #: float: Sampling period [s].
            self.dt = float(dt)
            #: float: Initial time [s].
            self.t0 = t0.timestamp()
            #: int: Simulation size [samples].
            self.size = int(size)
            #: float: Sampling frequency [Hz].
            self.fs = 1 / self.dt
            #: float: Simulation duration [s].
            self.duration = self.size * self.dt
            #: array: Default time array [s].
            self.t = self.t0 + np.arange(self.size, dtype=np.float64) * self.dt
        else:
            logger.debug("Using custom sampling (size=%d)", len(t))
            if len(t) < 1:
                raise ValueError(f"Invalid custom sampling '{t}'.")
            self.dt = None
            self.fs = None
            self.t = np.sort(np.array(t, dtype=np.float64))
            self.t0 = self.t[0]
            self.size = len(t)
            self.duration = self.t[-1] - self.t[0]

    @abc.abstractmethod
    def compute_position(self, t, sc):
        r"""Compute the spacecraft position vector :math:`(\vb{x}, \vb{y}, \vb{z})`.

        The vector coordinates are given in the BCRS frame.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            sc ((M,) array-like): spacecraft indices

        Returns:
            (N, M, 3) ndarray: Spacecraft positions [m].
        """
        raise NotImplementedError

    @abc.abstractmethod
    def compute_velocity(self, t, sc):
        r"""Compute the spacecraft velocity vector :math:`(\vb{v}_x, \vb{v}_y, \vb{v}_z)`.

        The vector coordinates are given in the BCRS frame.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            sc ((M,) array-like): spacecraft indices

        Returns:
            (N, M, 3) ndarray: Spacecraft velocities [m/s].
        """
        raise NotImplementedError

    @abc.abstractmethod
    def compute_acceleration(self, t, sc):
        r"""Compute the spacecraft acceleration vector :math:`(\vb{a}_x, \vb{a}_y, \vb{a}_z)`.

        The vector coordinates are given in the BCRS frame.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            sc ((M,) array-like): spacecraft indices

        Returns:
            (N, M, 3) ndarray: Spacecraft accelerations [m/s2].
        """
        raise NotImplementedError

    @abc.abstractmethod
    def compute_tps_deviation(self, t, sc):
        r"""Compute spacecraft proper time (TPS) deviation as function of TCB.

        We compute the spacecraft proper time deviations, defined by

        .. math::
            \delta\tau(t) = \tau(t) - t \qc

        where :math:`\tau` is the spacecraft TPS and :math:`t` the associated TCB.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            sc ((M,) array-like): spacecraft indices

        Returns:
            (N, M) ndarray: Spacecraft proper time deviations [s].
        """
        raise NotImplementedError

    @abc.abstractmethod
    def compute_tps_deviation_derivative(self, t, sc):
        r"""Compute spacecraft proper time (TPS) deviation derivatives as function of TCB.

        We compute the time derivatives of the spacecraft proper time (TPS) deviations,
        defined by

        .. math::
            \dv{(\delta\tau)}{t} = \dv{(\tau - t)}{t} = \dv{\tau}{t} - 1 \qc

        where :math:`\tau` is the spacecraft TPS and :math:`t` the associated TCB.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            sc ((M,) array-like): spacecraft indices

        Returns:
            (N, M) ndarray: Spacecraft proper time deviation derivatives [s/s].
        """
        raise NotImplementedError

    def compute_tcb_deviation(self, tau, sc, order=1):
        r"""Compute coordinate time (TCB) deviation as function of TPS.

        We compute to a given order the coordinate time,

        .. math::
            \delta t(\tau) = t(\tau) - \tau \qc

        where :math:`\tau` is the spacecraft TPS and :math:`t` the associated TCB.

        Args:
            tau ((N,) or (N, M) array-like): TPS times [s]
            sc ((M,) array-like): spacecraft indices
            order (int): number of iterations

        Returns:
            (N, M) ndarray: Spacecraft coordinate time deviations [s].
        """
        # At zeroth order, there is no deviations
        tcb_deviation = 0
        for _ in range(order):
            tcb_deviation = -self.compute_tps_deviation(tcb_deviation + tau, sc) # (N, M)
        return tcb_deviation

    def compute_unit_vector(self, t, link):
        r"""Compute link unit vector.

        The unit vector points from the emitter spacecraft to the receiver spacecraft.

        The vector coordinates are given in the BCRS frame.

        We compute

        .. math::
           \vu{n} = \frac{\vb{x}_\text{rec}(t_\text{rec}) - \vb{x}_\text{emit}(t_\text{emit})}
           {\abs{\vb{x}_\text{rec}(t_\text{rec}) - \vb{x}_\text{emit}(t_\text{emit})}} \qs

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            link ((M,) array-like): link indices

        Returns:
            (N, M, 3) ndarray: Link unit vectors.
        """
        tt = self.compute_ltt(t, link) # (N, M)
        pos_rec = self.compute_position(t, receiver(link)) # (N, M, 3)
        t_em = atleast_2d(t) - tt # (N, M)
        pos_em = self.compute_position(t_em, emitter(link)) # (N, M, 3)
        return (pos_rec - pos_em) / norm(pos_rec - pos_em)[:, :, np.newaxis] # (N, M, 3)

    def compute_ltt(self, t, link):
        """Compute light travel times (LTTs).

        Light travel times are the differences between the TCB time of reception
        of a photon at one spacecraft, and the TCB time of emission of the same photon
        by another spacecraft.

        The default implementation calls :meth:`lisaorbits.Orbits._compute_ltt_analytic`
        or :meth:`lisaorbits.Orbits._compute_ltt_iterative` depending on the value
        of :attr:`lisaorbits.Orbits.tt_method`.

        Subclasses can override this method with custom implementations.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            link ((M,) array-like): link indices

        Returns:
            (N, M) ndarray: Light travel times [s].

        Raises:
            ValueError: if the computation method is invalid
        """
        if self.tt_method == 'analytic':
            return self._compute_ltt_analytic(t, link) # (N, M)
        if self.tt_method == 'iterative':
            return self._compute_ltt_iterative(t, link) # (N, M)
        raise ValueError(f"Invalid light travel time computation method '{self.tt_method}', "
                         "must be 'analytic' or 'iterative'.")

    def _compute_ltt_analytic(self, t, link):
        """Compute light travel times from a series expansion of the emitter trajectory.

        Refer to the model for more information.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            link ((M,) array-like): link indices

        Returns:
            (N, M) ndarray: Light travel times [s].

        Raises:
            ValueError: if expansion order is invalid
            ValueError: if Shapiro delay is on but expansion order is less than 2
        """
        if self.tt_order < 0 or self.tt_order > 2:
            raise ValueError(f"Invalid light travel time computation order '{self.tt_order}', "
                             "should be one of 0, 1, or 2 when computed with analytical expansion.")

        if self.tt_order < 2 and not self.ignore_shapiro:
            raise ValueError("Cannot include Shapiro delay for light travel times using an analytic "
                             f"expansion of order '{self.tt_order}' (must be greater than 2)")

        pos_em = self.compute_position(t, emitter(link)) # (N, M, 3)
        pos_rec = self.compute_position(t, receiver(link)) # (N, M, 3)

        # Order 0
        d_er = norm(pos_rec - pos_em) # (N, M)
        tt = d_er # (N, M)

        # Order 1
        if self.tt_order >= 1:
            vel_em = self.compute_velocity(t, emitter(link)) # (N, M, 3)
            r_er = (pos_rec - pos_em) # from emitter to receiver (N, M, 3)
            velem_rer = dot(vel_em, r_er) # (N, M)
            tt += velem_rer / c # (N, M)

        # Order 2
        if self.tt_order == 2:
            acc_em = self.compute_acceleration(t, emitter(link)) # (N, M, 3)
            # This part is a correction arising from emitter motion
            tt += 0.5 * (dot(vel_em, vel_em) + (velem_rer / d_er)**2 - dot(acc_em, r_er)) * d_er / c**2 # (N, M)
            # The following part is the Shapiro delay
            if not self.ignore_shapiro:
                r_em, r_rec = norm(pos_em), norm(pos_rec) # (N, M)
                tt += SUN_SCHWARZSCHILD_RADIUS * np.log((r_em + r_rec + d_er) / (r_em + r_rec - d_er)) # (N, M)

        return tt / c # (N, M)

    def _compute_ltt_iterative(self, t, link):
        """Compute light travel times using an iterative procedure.

        Refer to the model for more information.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            link ((M,) array-like): link indices

        Returns:
            (N, M) ndarray: Light travel times [s].

        Raises:
            ValueError: if the number of iterations is invalid
            ValueError: if Shapiro delay is on but the number of iterations is less than 2
        """
        if self.tt_niter < 0:
            raise ValueError(f"Invalid number of iterations '{self.tt_niter}' for iterative procedure when "
                             "computing the light travel times.")

        if self.tt_niter < 2 and not self.ignore_shapiro:
            raise ValueError("Cannot include Shapiro delay for light travel times using an iterative"
                             f"procedure with number of iterations '{self.tt_niter}' (must be greater than 2)")

        pos_em = self.compute_position(t, emitter(link)) # (N, M, 3)
        pos_rec = self.compute_position(t, receiver(link)) # (N, M, 3)

        # First the iteration to find the flat spacetime travel time
        tt = norm(pos_rec - pos_em) / c # (N, M)
        for _ in range(self.tt_niter):
            t_em = atleast_2d(t) - tt # (N, M)
            pos_em = self.compute_position(t_em, emitter(link)) # (N, M, 3)
            tt = norm(pos_rec - pos_em) / c # (N, M)

        # And the Shapiro time delay
        if not self.ignore_shapiro:
            r_em, r_rec = norm(pos_em), norm(pos_rec) # (N, M)
            d_er = c * tt # (N, M)
            tt += SUN_SCHWARZSCHILD_RADIUS * np.log((r_em + r_rec + d_er) / (r_em + r_rec - d_er)) / c # (N, M)

        return tt # (N, M)

    def compute_ltt_derivative(self, t, link):
        """Compute light travel time derivatives (LTTs).

        The default implementation uses an series expansion of the emitting spacecraft
        trajectory. Subclasses can override this method with custom implementations.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            link ((M,) array-like): link indices

        Returns:
            (N, M) ndarray: Light travel time derivatives [s/s].
        """
        pos_rec = self.compute_position(t, receiver(link)) # (N, M, 3)
        vel_rec = self.compute_velocity(t, receiver(link)) # (N, M, 3)
        ltt = self.compute_ltt(t, link) # (N, M)

        # Note that the position and velocity of the emitter are evaluated
        # at receiver time for order 0 and 1, but at emitter time for order 2
        if self.tt_order < 2 and self.tt_method == 'analytic':
            pos_em = self.compute_position(t, emitter(link)) # (N, M, 3)
            vel_em = self.compute_velocity(t, emitter(link)) # (N, M, 3)
        else:
            t_em = atleast_2d(t) - ltt # (N, M)
            pos_em = self.compute_position(t_em, emitter(link)) # (N, M, 3)
            vel_em = self.compute_velocity(t_em, emitter(link)) # (N, M, 3)

        r_er = pos_rec - pos_em # from emitter to receiver (N, M, 3)
        d_er = norm(pos_rec - pos_em) # (N, M)
        n_er = r_er / d_er[:, :, np.newaxis] # unit vector from emitter to receiver (N, M, 3)
        ner_vr = dot(n_er, vel_rec) # (N, M)
        ner_ve = dot(n_er, vel_em) # (N, M)

        if self.tt_order < 2 and self.tt_method == 'analytic':
            # This is the zeroth order term which contributes only
            # for order 0 or order 1
            # all quantities being evaluated at the receiver time
            d_tt = (ner_vr - ner_ve) / c # (N, M)
        else:
            # The derivation is different if one goes to 2nd order.
            # See Eq. 27 in Hees et al CQG 29(23):235027 (2012).
            r_em = norm(pos_em) # (N, M)
            r_rec = norm(pos_rec) # (N, M)
            den = (r_em + r_rec)**2 - d_er**2 # (N, M)
            dq_rec = ner_vr + 2 * SUN_SCHWARZSCHILD_RADIUS * \
                ((r_em + r_rec) * ner_vr - d_er * dot(pos_rec, vel_rec) / r_rec) / den # (N, M)
            dq_em = ner_ve + 2 * SUN_SCHWARZSCHILD_RADIUS * \
                ((r_em + r_rec) * ner_ve + d_er * dot(pos_em, vel_em) / r_em) / den # (N, M)
            d_tt = (dq_rec - dq_em) / (c - dq_em) # (N, M)

        if self.tt_order == 1 and self.tt_method == 'analytic':
            # This is the first order contribution, to be included only if
            # the order is strictly less than 2
            acc_em = self.compute_acceleration(t, emitter(link)) # (N, M, 3)
            d_tt += (dot(vel_rec - vel_em, vel_em) + dot(pos_rec - pos_em, acc_em)) / c**2 # (N, M)

        return d_tt # (N, M)

    def compute_ppr(self, t, link):
        """Compute proper pseudoranges (PPRs).

        Proper pseudoranges are the differences between the time of reception of a photon
        expressed in the TPS of the receiving spacecraft and the time of emission of the
        same photon expressed in the TPS of the emitting spacecraft.

        Note that they include information about the light travel times, as well as
        the conversion between TPSs and TCB.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            link ((M,) array-like): link indices

        Returns:
            (N, M) ndarray: Proper pseudoranges [s].
        """
        tau_receiver = self.compute_tps_deviation(t, receiver(link)) # (N, M)
        ltt = self.compute_ltt(t, link) # (N, M)
        t_em = atleast_2d(t) - ltt # (N, M)
        tps_deviations = self.compute_tps_deviation(t_em, emitter(link)) # (N, M)
        return ltt + tau_receiver - tps_deviations # (N, M)

    def compute_ppr_derivative(self, t, link):
        """Compute proper pseudorange (PPR) derivatives.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            link ((M,) array-like): link indices

        Returns:
            (N, M) ndarray: Proper pseudorange derivatives [s/s].
        """
        dtau_receiver = self.compute_tps_deviation_derivative(t, receiver(link)) # (N, M)
        d_tt = self.compute_ltt_derivative(t, link) # (N, M)
        ltt = self.compute_ltt(t, link) # (N, M)
        t_em = atleast_2d(t) - ltt # (N, M)
        dtau_emitter = self.compute_tps_deviation_derivative(t_em, emitter(link)) # (N, M)
        return (dtau_receiver - dtau_emitter + d_tt * (1 + dtau_emitter)) / (1 + dtau_receiver) # (N, M)

    def plot_spacecraft(self, sc, output=None):
        """Plot quantities associated with one spacecraft.

        Args:
            sc (int): spacecraft index, one of 1, 2, 3
            output (str): output filename, or ``None`` to show the plots
        """
        # Initialize the plot
        _, axes = plt.subplots(5, 1, figsize=(12, 20))
        axes[0].set_title(f"Spacecraft {sc}")
        axes[4].set_xlabel("Barycentric time (TCB) [s]")
        # Plot positions
        logger.info("Plotting positions for spacecraft %d", sc)
        axes[0].set_ylabel("Position [m]")
        positions = self.compute_position(self.t, [sc])[:, 0] # (N, 3)
        axes[0].plot(self.t, positions[:, 0], label=r'$x$')
        axes[0].plot(self.t, positions[:, 1], label=r'$y$')
        axes[0].plot(self.t, positions[:, 2], label=r'$z$')
        # Plot velocities
        logger.info("Plotting velocities for spacecraft %d", sc)
        axes[1].set_ylabel("Velocity [m/s]")
        velocities = self.compute_velocity(self.t, [sc])[:, 0] # (N, 3)
        axes[1].plot(self.t, velocities[:, 0], label=r'$v_x$')
        axes[1].plot(self.t, velocities[:, 1], label=r'$v_y$')
        axes[1].plot(self.t, velocities[:, 2], label=r'$v_z$')
        # Plot accelerations
        logger.info("Plotting accelerations for spacecraft %d", sc)
        axes[2].set_ylabel("Acceleration [m/s^2]")
        accelerations = self.compute_acceleration(self.t, [sc])[:, 0] # (N, 3)
        axes[2].plot(self.t, accelerations[:, 0], label=r'$a_x$')
        axes[2].plot(self.t, accelerations[:, 1], label=r'$a_y$')
        axes[2].plot(self.t, accelerations[:, 2], label=r'$a_z$')
        # Plot proper times
        logger.info("Plotting proper times for spacecraft %d", sc)
        axes[3].set_ylabel("Proper time deviation [s]")
        tps_deviations = self.compute_tps_deviation(self.t, [sc])[:, 0] # (N,)
        axes[3].plot(self.t, tps_deviations, label=r'$\delta \tau$')
        # Plot proper time derivatives
        logger.info("Plotting proper time derivatives for spacecraft %d", sc)
        axes[4].set_ylabel("Proper time deviation derivative [s/s]")
        tps_deviations_derivatives = self.compute_tps_deviation_derivative(self.t, [sc])[:, 0] # (N,)
        axes[4].plot(self.t, tps_deviations_derivatives, label=r'$\dot \delta \tau$')
        # Add legend and grid
        for axis in axes:
            axis.legend()
            axis.grid()
        # Show or save figure
        if output is not None:
            logger.info("Saving plots to %s", output)
            plt.savefig(output, bbox_inches='tight')
        else:
            logger.info("Showing plots")
            plt.show()

    def plot_links(self, output=None):
        """Plot quantities associated with the 6 links.

        Args:
            output: output filename, or ``None`` to show the plots
        """
        # Initialize the plot
        _, axes = plt.subplots(4, 1, figsize=(12, 16))
        axes[0].set_title("Light travel times, proper pseudorange and derivatives")
        axes[3].set_xlabel("Barycentric time (TCB) [s]")
        # Plot light travel times
        logger.info("Plotting light travel times")
        axes[0].set_ylabel("Light travel time [s]")
        ltts = self.compute_ltt(self.t, self.LINKS) # (N, M)
        for index, link in enumerate(self.LINKS):
            axes[0].plot(self.t, ltts[:, index], label=link)
        # Plot proper pseudoranges
        logger.info("Plotting proper pseudoranges")
        axes[1].set_ylabel("Proper pseudorange [s]")
        pprs = self.compute_ppr(self.t, self.LINKS) # (N, M)
        for index, link in enumerate(self.LINKS):
            axes[1].plot(self.t, pprs[:, index], label=link)
        # Plot light travel time derivatives
        logger.info("Plotting light travel time derivatives")
        axes[2].set_ylabel("Light travel time derivative [s/s]")
        ltt_derivatives = self.compute_ltt_derivative(self.t, self.LINKS) # (N, M)
        for index, link in enumerate(self.LINKS):
            axes[2].plot(self.t[:], ltt_derivatives[:, index], label=link)
        # Plot proper pseudorange derivatives
        logger.info("Plotting proper pseudorange derivatives")
        axes[3].set_ylabel("Proper pseudorange derivative [s/s]")
        ppr_derivatives = self.compute_ppr_derivative(self.t, self.LINKS) # (N, M)
        for index, link in enumerate(self.LINKS):
            axes[3].plot(self.t[:], ppr_derivatives[:, index], label=link)
        # Add legend and grid
        for axis in axes:
            axis.legend()
            axis.grid()
        # Show or save figure
        if output is not None:
            logger.info("Saving plots to %s", output)
            plt.savefig(output, bbox_inches='tight')
        else:
            logger.info("Showing plots")
            plt.show()

    def _write_attr(self, hdf5, *names):
        """Write a single object attribute as metadata on ``hdf5``.

        This method is used in :meth:`lisaorbits.Orbits._write_metadata`
        to write Python self's attributes as HDF5 attributes.

        >>> my_orbits = ConcreteOrbits()
        >>> my_orbits.parameter = 42
        >>> my_orbits._write_attr('parameter')

        Args:
            hdf5 (:obj:`h5py.Group`): an HDF5 file, or a dataset
            names* (str): attribute names
        """
        for name in names:
            hdf5.attrs[name] = getattr(self, name)

    def _write_metadata(self, hdf5):
        """Write relevant object's attributes as metadata on ``hdf5``.

        This is for tracability and reproducibility. All parameters
        necessary to re-instantiate the orbits object and reproduce the
        exact same simulation should be written to file.

        Use the :meth:`lisaorbits.Orbits._write_attr` method.

        .. admonition:: Suclassing notes
            This class is intended to be overloaded by subclasses to write
            additional attributes.

        .. important::
            You MUST call super implementation in subclasses.

        Args:
            hdf5 (:obj:`h5py.Group`): an HDF5 file, or a dataset
        """
        self._write_attr(hdf5,
            'git_url', 'version', 'generator',
            'tt_method', 'tt_order', 'tt_niter', 'ignore_shapiro',
            'dt', 't0', 'size', 'fs', 'duration',
        )

    def write(self, path='orbits.h5', mode='x'):
        """Generate an orbit file.

        Args:
            path (str): path to the generated orbit file
            mode (str): open mode, default ``'x'`` (create file, fail if exists)
        """
        # Open orbit file
        logger.info("Creating orbit file %s", path)
        with h5py.File(path, mode) as hdf5:

            logger.debug("Writing metadata")
            self._write_metadata(hdf5)

            logger.debug("Writing TCB spacecraft quantities")
            hdf5['tcb/x'] = self.compute_position(self.t, self.SC)
            hdf5['tcb/v'] = self.compute_velocity(self.t, self.SC)
            hdf5['tcb/a'] = self.compute_acceleration(self.t, self.SC)
            hdf5['tcb/delta_tau'] = self.compute_tps_deviation(self.t, self.SC)

            logger.debug("Writing TCB link quantities")
            hdf5['tcb/n'] = self.compute_unit_vector(self.t, self.LINKS)
            hdf5['tcb/ltt'] = self.compute_ltt(self.t, self.LINKS)
            hdf5['tcb/ppr'] = self.compute_ppr(self.t, self.LINKS)
            hdf5['tcb/d_ltt'] = self.compute_ltt_derivative(self.t, self.LINKS)
            hdf5['tcb/d_ppr'] = self.compute_ppr_derivative(self.t, self.LINKS)

            logger.debug("writing TPS spacecraft quantities")
            delta_t = self.compute_tcb_deviation(self.t, self.SC)
            hdf5['tps/delta_t'] = delta_t

            logger.debug("writing TPS link quantities")
            t = self.t[:, np.newaxis] + delta_t[:, arrayindex(self.SC, emitter(self.LINKS))]
            hdf5['tps/ppr'] = self.compute_ppr(t, self.LINKS)
            hdf5['tps/d_ppr'] = self.compute_ppr_derivative(t, self.LINKS)

            logger.info("Closing orbit file %s", path)


class StaticConstellation(Orbits):
    """Static constellation (fixed positions and constant armlengths).

    You can either initialize the orbits from a set of spacecraft positions,
    another instance of :class:`lisaorbits.Orbits`, or a set of armlengths.

    We assume that TPS deviations and derivatives thereof are vanishing.
    Similarly, velocities and accelerations are set to zero.

    Args:
        r_1 ((3,) array-like): position vector of spacecraft 1 in BCRS [m]
        r_2 ((3,) array-like): position vector of spacecraft 2 in BCRS [m]
        r_3 ((3,) array-like): position vector of spacecraft 3 in BCRS [m]
        **kwargs: all other args from :class:`lisaorbits.orbits.Orbits`
    """

    def __init__(self, r_1, r_2, r_3, tt_order=0, tt_niter=0, ignore_shapiro=True, **kwargs):

        # Update default args because we have a static constellation
        # and therefore do not need higher-order LTT computation
        super().__init__(
            tt_order=tt_order,
            tt_niter=tt_niter,
            ignore_shapiro=ignore_shapiro,
            **kwargs)

        #: (3, 3) ndarray: Spacecraft position vectors in BCRS [m].
        self.sc_positions = np.stack([r_1, r_2, r_3], axis=0) # (3 SC, 3 COORDS)
        if self.sc_positions.shape != (3, 3):
            raise TypeError("invalid shape '{self.sc_positions.shape}' for spacecraft positions")

    @classmethod
    def from_orbits(cls, orbits, t_freeze='t0', **kwargs):
        """Initialize a static constellation from other orbits.

        We compute spacecraft positions from ``orbits`` at ``t_freeze`` and
        use them as constant spacecraft positions for our static constellation.

        Args:
            orbits (:class:`lisaorbits.Orbits`): orbit instance
            t_freeze (float or str): time at which spacecraft positions are computed,
                or ``'t0'`` to use the orbits initial time [s]
            **kwargs: all other args from :class:`lisaorbits.orbits.StaticConstellation`
        """
        if not isinstance(orbits, Orbits):
            raise TypeError(f"orbits should be of type 'Orbits', got '{type(orbits)}'")
        if t_freeze == 't0':
            t_freeze = orbits.t0

        sc_positions = orbits.compute_position([t_freeze], [1, 2, 3])[0]
        return cls(sc_positions[0], sc_positions[1], sc_positions[2], **kwargs)

    @classmethod
    def from_armlengths(cls,
                        l_12=8.33242295*c,
                        l_23=8.30282196*c,
                        l_31=8.33242298*c,
                        barycenter=(0, 0, 0),
                        **kwargs):
        r"""Initialize a static constellation from armlengths.

        The default armlength values are based on the PPRs values for the first
        samples generated with :class:`lisaorbits.orbits.KeplerianOrbits`.

        The spacecraft are positioned such that spacecraft 1 lies on the x-axis,
        and the constellation is contained in the xy-plane.

        Args:
            l_12 (float): armlength between spacecraft 1 and 2 [m]
            l_23 (float): armlength between spacecraft 2 and 3 [m]
            l_31 (float): armlength between spacecraft 3 and 1 [m]
            barycenter ((3,) array-like): constellation's barycenter BCRS position [m]
            **kwargs: all other args from :class:`lisaorbits.orbits.StaticConstellation`
        """
        x_1 = np.sqrt(2 * l_12**2 - l_23**2 + 2 * l_31**2) / 3
        x_2 = (l_23**2 + l_31**2 - 5 * l_12**2) / (18 * x_1)
        x_3 = (l_12**2 + l_23**2 - 5 * l_31**2) / (18 * x_1)

        y_2 = -np.sqrt(-(l_12 - l_23 - l_31) * (l_12 + l_23 - l_31) \
            * (l_12 - l_23 + l_31) * (l_12 + l_23 + l_31)) / (6 * x_1)

        return cls(
            r_1=[x_1 + barycenter[0], barycenter[1], barycenter[2]],
            r_2=[x_2 + barycenter[0], y_2 + barycenter[1], barycenter[2]],
            r_3=[x_3 + barycenter[0], -y_2 + barycenter[1], barycenter[2]],
            **kwargs)

    def _write_metadata(self, hdf5):
        super()._write_metadata(hdf5)
        self._write_attr(hdf5, 'sc_positions')

    def compute_position(self, t, sc):
        sc_indices = arrayindex(self.SC, sc) # (M,)
        positions = self.sc_positions[sc_indices][np.newaxis]  # (1, M, 3)
        return np.repeat(positions, len(t), axis=0) # (N, M, 3)

    def compute_velocity(self, t, sc):
        return np.zeros((len(t), len(sc), 3)) # (N, M, 3)

    def compute_acceleration(self, t, sc):
        return np.zeros((len(t), len(sc), 3)) # (N, M, 3)

    def compute_tps_deviation(self, t, sc):
        return np.zeros((len(t), len(sc))) # (N, M)

    def compute_tps_deviation_derivative(self, t, sc):
        return np.zeros((len(t), len(sc))) # (N, M)


class EqualArmlengthOrbits(Orbits):
    r"""Keplerian orbits that minimize flexing to leading order in eccentricity.

    These orbits are the solution to the two-body problem in Newtonian gravity,
    optimized to leave inter-spacecraft distances constant to leading order in
    eccentricity.

    Args:
        L (float): mean inter-spacecraft distance [m]
        a (float): semi-major axis for an orbital period of 1 yr [m]
        lambda1 (float): spacecraft 1's longitude of periastron [rad]
        m_init1 (float): spacecraft 1's mean anomaly at initial time :math:`t_0` [rad]
        **kwargs: all other args from :class:`lisaorbits.orbits.Orbits`
    """

    def __init__(self, L=2.5E9, a=ASTRONOMICAL_UNIT, lambda1=0, m_init1=0, **kwargs):

        super().__init__(**kwargs)

        #: float: Semi-major axis for an orbital period of 1 yr [m].
        self.a = float(a)
        #: float: Mean inter-spacecraft distance [m].
        self.L = float(L)
        #: float: Spacecraft 1's mean anomaly at initial time [rad].
        self.m_init1 = float(m_init1)
        #: float: Spacecraft 1's longitude of periastron [rad].
        self.lambda1 = float(lambda1)
        #: float: Orbits eccentricity.
        self.e = self.L / (2 * self.a) / np.sqrt(3)

        self.n = 2 * np.pi / ASTRONOMICAL_YEAR
        self.theta = (self.SC - 1) * 2 * np.pi / 3 # (M,)
        self.beta = self.theta + self.lambda1 # (M,)
        self.cos_beta = np.cos(self.beta) # (M,)
        self.sin_beta = np.sin(self.beta) # (M,)

        self.gr_const = (self.n * self.a / c)**2

    def _write_metadata(self, hdf5):
        super()._write_metadata(hdf5)
        self._write_attr(hdf5, 'a', 'L', 'm_init1', 'lambda1')

    def _compute_mbar(self, t):
        """Computes the angle of the constellation center of mass.

        Args:
            t (array-like): TCB times [s]

        Returns:
            tuple: The 3-tuple ``(m_bar, cos(mbar), sin(mbar))`` of ndarrays
            with the same shape as ``t``.
        """
        t = np.atleast_1d(t)
        mbar = self.n * (t - self.t0) + self.m_init1 + self.lambda1 # (N,)
        return (mbar, np.cos(mbar), np.sin(mbar)) # (N,) for each element

    def compute_position(self, t, sc):
        sc_indices = arrayindex(self.SC, sc) # (M,)
        # Compute constellation angle
        mbar, cos_mbar, sin_mbar = self._compute_mbar(t) # (N,) or (N, M)
        mbar = atleast_2d(mbar) # (N, 1) or (N, M)
        cos_mbar = atleast_2d(cos_mbar) # (N, 1) or (N, M)
        sin_mbar = atleast_2d(sin_mbar) # (N, 1) or (N, M)
        # Compute positions
        sc_x = self.a * cos_mbar + self.a * self.e * (sin_mbar * cos_mbar * self.sin_beta[np.newaxis, sc_indices] \
                - (1 + sin_mbar**2) * self.cos_beta[np.newaxis, sc_indices]) # (N, M)
        sc_y = self.a * sin_mbar + self.a * self.e * (sin_mbar * cos_mbar * self.cos_beta[np.newaxis, sc_indices] \
                - (1 + cos_mbar**2) * self.sin_beta[np.newaxis, sc_indices]) # (N, M)
        sc_z = -self.a * self.e * np.sqrt(3) * np.cos(mbar - self.beta[np.newaxis, sc_indices]) # (N, M)
        # Stack coordinates
        return np.stack([sc_x, sc_y, sc_z], axis=-1) # (N, M, 3)

    def compute_velocity(self, t, sc):
        sc_indices = arrayindex(self.SC, sc) # (M,)
        # Compute constellation angle
        mbar, cos_mbar, sin_mbar = self._compute_mbar(t) # (N,) or (N, M)
        mbar = atleast_2d(mbar) # (N, 1) or (N, M)
        cos_mbar = atleast_2d(cos_mbar) # (N, 1) or (N, M)
        sin_mbar = atleast_2d(sin_mbar) # (N, 1) or (N, M)
        # Compute velocities
        sc_vx = -self.a * self.n * sin_mbar \
            + self.a * self.e * self.n * ((cos_mbar**2 - sin_mbar**2) * self.sin_beta[np.newaxis, sc_indices] \
            - 2 * sin_mbar * cos_mbar * self.cos_beta[np.newaxis, sc_indices]) # (N, M)
        sc_vy = self.a * self.n * cos_mbar \
            + self.a * self.e * self.n * ((cos_mbar**2 - sin_mbar**2) * self.cos_beta[np.newaxis, sc_indices] \
            + 2 * sin_mbar * cos_mbar * self.sin_beta[np.newaxis, sc_indices]) # (N, M)
        sc_vz = self.a * self.e * self.n * np.sqrt(3) * np.sin(mbar - self.beta[np.newaxis, sc_indices]) # (N, M)
        # Stack coordinates
        return np.stack([sc_vx, sc_vy, sc_vz], axis=-1) # (N, M, 3)

    def compute_acceleration(self, t, sc):
        sc_indices = arrayindex(self.SC, sc) # (M,)
        # Compute constellation angle
        mbar, cos_mbar, sin_mbar = self._compute_mbar(t) # (N,) or (N, M)
        mbar = atleast_2d(mbar) # (N, 1) or (N, M)
        cos_mbar = atleast_2d(cos_mbar) # (N, 1) or (N, M)
        sin_mbar = atleast_2d(sin_mbar) # (N, 1) or (N, M)
        # Compute velocities
        sc_ax = -self.a * self.n**2 * cos_mbar - 4 * self.a * self.e * self.n**2 \
            * (sin_mbar * cos_mbar * self.sin_beta[np.newaxis, sc_indices] \
            + (0.5 - sin_mbar**2) * self.cos_beta[np.newaxis, sc_indices]) # (N, M)
        sc_ay = -self.a * self.n**2 * sin_mbar - 4 * self.a * self.e * self.n**2 \
            * (sin_mbar * cos_mbar * self.cos_beta[np.newaxis, sc_indices] \
            + (0.5 - cos_mbar**2) * self.sin_beta[np.newaxis, sc_indices]) # (N, M)
        sc_az = self.a * self.e * self.n**2 * np.sqrt(3) \
            * np.cos(mbar - self.beta[np.newaxis, sc_indices]) # (N, M)
        # Stack coordinates
        return np.stack([sc_ax, sc_ay, sc_az], axis=-1) # (N, M, 3)

    def compute_tps_deviation(self, t, sc):
        sc_indices = arrayindex(self.SC, sc) # (M,)
        # Compute constellation angle
        mbar, _, _ = self._compute_mbar(t) # (N,) or (N, M)
        mbar = atleast_2d(mbar) # (N, 1) or (N, M)
        t = atleast_2d(t) # (N, 1) or (N, M)
        # Compute proper time deviation
        return -self.gr_const * (1.5 * (t - self.t0) \
            + 2 * self.e / self.n * (np.sin(mbar - self.beta[np.newaxis, sc_indices]) \
            - np.sin(self.m_init1 - self.theta[np.newaxis, sc_indices]))) # (N, M)

    def compute_tps_deviation_derivative(self, t, sc):
        sc_indices = arrayindex(self.SC, sc) # (M,)
        # Compute constellation angle
        mbar, _, _ = self._compute_mbar(t) # (N,) or (N, M)
        mbar = atleast_2d(mbar) # (N, 1) or (N, M)
        # Compute proper time deviation
        return -self.gr_const * (1.5 + 2 * self.e \
            * np.cos(mbar - self.beta[np.newaxis, sc_indices])) # (N, M)


class KeplerianOrbits(Orbits):
    """Keplerian orbits that minimize flexing to next-to leading order in eccentricity.

    These orbits are the solution to the two-body problem in Newtonian gravity,
    optimized to leave inter-spacecraft distances constant to second order in
    eccentricity.

    Args:
        L (float): mean inter-spacecraft distance [m]
        a (float): semi-major axis for an orbital period of 1 yr [m]
        lambda1 (float): spacecraft 1's longitude of periastron [rad]
        m_init1 (float): spacecraft 1's mean anomaly at initial time :math:`t_0` [rad]
        kepler_order (int): number of iterations in the Newton-Raphson procedure
        **kwargs: all other args from :class:`lisaorbits.Orbits`
    """

    def __init__(self, L=2.5E9, a=ASTRONOMICAL_UNIT, lambda1=0, m_init1=0, kepler_order=2, **kwargs):
        super().__init__(**kwargs)

        #: float: Semi-major axis for an orbital period of 1 yr [m].
        self.a = float(a)
        #: float: Mean inter-spacecraft distance [m].
        self.L = float(L)
        #: int: Number of iterations in the Newton-Raphson procedure.
        self.kepler_order = int(kepler_order)
        #: float: Spacecraft 1's mean anomaly at initial time [rad].
        self.m_init1 = float(m_init1)
        #: float: Spacecraft 1's longitude of periastron [rad].
        self.lambda1 = float(lambda1)

        #: float: Perturbation :math:`\delta` to tilt angle :math:`\nu`.
        self.delta = 5.0 / 8.0
        #: float: Orbital parameter (used for series expansions).
        self.alpha = self.L / (2 * self.a)
        #: float: Orbits tilt angle [rad].
        self.nu = np.pi / 3 + self.delta * self.alpha
        #: float: Orbits eccentricity.
        self.e = np.sqrt(1 + 4 * self.alpha * np.cos(self.nu) / np.sqrt(3) + 4 * self.alpha**2 / 3) - 1

        self.tan_i = self.alpha * np.sin(self.nu) / ((np.sqrt(3) / 2) + self.alpha * np.cos(self.nu))
        self.cos_i = 1 / np.sqrt(1 + self.tan_i**2)
        self.sin_i = self.tan_i * self.cos_i

        self.n = 2 * np.pi / ASTRONOMICAL_YEAR
        self.theta = (self.SC - 1) * 2 * np.pi / 3 # (3,)
        self.m_init = self.m_init1 - self.theta # (3,)
        self.lambda_k = self.lambda1 + self.theta # (3,)
        self.sin_lambda = np.sin(self.lambda_k) # (3,)
        self.cos_lambda = np.cos(self.lambda_k) # (3,)

        self.gr_const = (self.n * self.a / c)**2

    def _write_metadata(self, hdf5):
        super()._write_metadata(hdf5)
        self._write_attr(hdf5, 'a', 'L', 'kepler_order', 'm_init1', 'lambda1')

    def compute_eccentric_anomaly(self, t, sc):
        r"""Estimate the eccentric anomaly.

        This uses an iterative Newton-Raphson method to solve the Kepler equation,
        starting from a low eccentricity expansion of the solution.

        .. math::
            \psi_k - e \sin \psi_k = m_k(t) \qc

        with :math:`m_k(t)` the mean anomaly.

        We use ``kepler_order`` iterations. For low eccentricity, the convergence rate
        of this iterative scheme is of the order of :math:`e^2`. Typically for LISA
        spacecraft (characterized by a small eccentricity 0.005), the iterative
        procedure converges in one iteration using double precision.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            sc ((M,) array-like): spacecraft indices

        Returns:
            (N, M) ndarray: Eccentric anomalies [rad].
        """
        # Compute the mean anomaly
        logger.debug("Computing eccentric anomaly for spacecraft %s at time %s s", sc, t)
        sc_index = arrayindex(self.SC, sc) # (M,)
        m_init = self.m_init[sc_index] # (M,)
        m = m_init[np.newaxis] + self.n * (atleast_2d(t) - self.t0) # (N, M)
        # The following expression is valid up to e**4
        ecc_anomaly = m + (self.e - self.e**3/8) * np.sin(m) + 0.5 * self.e**2 * np.sin(2 * m) \
            + 3/8 * self.e**3 * np.sin(3 * m) # (N, M)
        # Standard Newton-Raphson iterative procedure
        for _ in range(self.kepler_order):
            error = ecc_anomaly - self.e * np.sin(ecc_anomaly) - m # (N, M)
            ecc_anomaly -= error / (1 - self.e * np.cos(ecc_anomaly)) # (N, M)
        return ecc_anomaly # (N, M)

    def compute_position(self, t, sc):
        sc_index = arrayindex(self.SC, sc)
        # Compute eccentric anomaly
        psi = self.compute_eccentric_anomaly(t, sc) # (N, M)
        cos_psi = np.cos(psi) # (N, M)
        sin_psi = np.sin(psi) # (N, M)
        # Reference position
        ref_x = self.a * self.cos_i * (cos_psi - self.e) # (N, M)
        ref_y = self.a * np.sqrt(1 - self.e**2) * sin_psi # (N, M)
        ref_z = -self.a * self.sin_i * (cos_psi - self.e) # (N, M)
        # Spacecraft position
        sc_x = self.cos_lambda[np.newaxis, sc_index] * ref_x \
            - self.sin_lambda[np.newaxis, sc_index] * ref_y # (N, M)
        sc_y = self.sin_lambda[np.newaxis, sc_index] * ref_x \
            + self.cos_lambda[np.newaxis, sc_index] * ref_y # (N, M)
        sc_z = ref_z # (N, M)
        # Stack coordinates
        return np.stack([sc_x, sc_y, sc_z], axis=-1) # (N, M, 3)

    def compute_velocity(self, t, sc):
        sc_index = arrayindex(self.SC, sc)
        # Compute eccentric anomaly
        psi = self.compute_eccentric_anomaly(t, sc) # (N, M)
        cos_psi = np.cos(psi) # (N, M)
        sin_psi = np.sin(psi) # (N, M)
        dpsi = self.n / (1 - self.e * cos_psi) # (N, M)
        # Reference velocity
        ref_vx = -self.a * dpsi * self.cos_i * sin_psi # (N, M)
        ref_vy = self.a * dpsi * np.sqrt(1 - self.e**2) * cos_psi # (N, M)
        ref_vz = self.a * self.sin_i * dpsi * sin_psi # (N, M)
        # Spacecraft velocity
        sc_vx = self.cos_lambda[np.newaxis, sc_index] * ref_vx \
            - self.sin_lambda[np.newaxis, sc_index] * ref_vy # (N, M)
        sc_vy = self.sin_lambda[np.newaxis, sc_index] * ref_vx \
            + self.cos_lambda[np.newaxis, sc_index] * ref_vy # (N, M)
        sc_vz = ref_vz # (N, M)
        # Stack coordinates
        return np.stack([sc_vx, sc_vy, sc_vz], axis=-1) # (N, M, 3)

    def compute_acceleration(self, t, sc):
        pos = self.compute_position(t, sc) # (N, M, 3)
        # Spacecraft acceleration
        a3_dist3 = float(self.a**3) / norm(pos)**3 # (N, M)
        return -self.n**2 * pos * a3_dist3[:, :, np.newaxis] # (N, M, 3)

    def compute_tps_deviation(self, t, sc):
        # Compute eccentric anomaly
        sin_psi = np.sin(self.compute_eccentric_anomaly(t, sc)) # (N, M)
        sin_psi_init = sin_psi[np.newaxis, 0] # (1, M)
        # Proper time deviation
        return -1.5 * self.gr_const * (atleast_2d(t) - self.t0) \
            - 2 * self.gr_const * (self.e / self.n) * (sin_psi - sin_psi_init) # (N, M)

    def compute_tps_deviation_derivative(self, t, sc):
        # Compute eccentric anomaly
        psi = self.compute_eccentric_anomaly(t, sc) # (N, M)
        cos_psi = np.cos(psi) # (N, M)
        dpsi = self.n / (1 - self.e * cos_psi) # (N, M)
        # Compute proper time deviation
        return -(3 + self.e * cos_psi) / (2 * self.n) * self.gr_const * dpsi # (N, M)


class InterpolatedOrbits(Orbits):
    """Interpolate an array of spacecraft positions.

    Splines are used to interpolate the spacecraft positions and velocities. The
    analytic derivatives of the splines are used to compute spacecraft velocities
    and accelerations if they are not provided.

    TPS deviations are numerically integrated.

    Args:
        t (array-like): array of UNIX timestamps [s]
        spacecraft_positions (array-like):
            array of spacecraft positions with dimension ``(t, sc, coordinate)`` [m]
        spacecraft_velocities (array-like or None):
            array of spacecraft velocities with dimension ``(t, sc, coordinate)``
            [m/s], or None to compute velocities as the derivatives of the
            interpolated positions
        interp_order (int): interpolation order to be used, 1 to 5
        ext (str): extrapolation mode for elements not in the interval defined by the knot sequence
        check_input (bool):
            whether to check that input contains only finite numbers -- disabling may give
            a performance gain, but may result in problems (crashes, non-termination or invalid results)
            if input file contains infinities or ``NaNs``
        **kwargs: all other args from :class:`lisaorbits.Orbits`
    """

    def __init__(self,
                 t,
                 spacecraft_positions,
                 spacecraft_velocities=None,
                 interp_order=5,
                 ext='extrapolate',
                 check_input=True,
                 **kwargs):

        super().__init__(**kwargs)

        #: array: Array of time knots [s].
        self.interp_t = np.sort(t)
        #: array: Spacecraft positions [m].
        self.spacecraft_positions = np.asarray(spacecraft_positions)
        #: array: Spacecraft velocities [m/s].
        self.spacecraft_velocities = np.asarray(spacecraft_velocities) \
            if spacecraft_velocities is not None \
            else None
        #: int: Spline interpolation order.
        self.interp_order = int(interp_order)
        #: str: Extrapolation mode for elements not in the interval defined by the knot sequence.
        self.ext = str(ext)
        #: bool: Whether to check that input contains only finite numbers.
        self.check_input = bool(check_input)

        # Check t, spacecraft_positions and spacecraft_velocities' shapes
        self._check_shapes()

        # pylint: disable=unnecessary-lambda-assignment
        interpolate = lambda x: scipy.interpolate.InterpolatedUnivariateSpline(
            self.interp_t, x,
            k=self.interp_order,
            ext=self.ext,
            check_finite=self.check_input
        )

        # Compute spline interpolation for positions
        logger.debug("Computing spline interpolation for spacecraft positions")
        self.interp_x = {sc: interpolate(self.spacecraft_positions[:, sc - 1, 0]) for sc in self.SC}
        self.interp_y = {sc: interpolate(self.spacecraft_positions[:, sc - 1, 1]) for sc in self.SC}
        self.interp_z = {sc: interpolate(self.spacecraft_positions[:, sc - 1, 2]) for sc in self.SC}

        if spacecraft_velocities is None:
            logger.debug("Computing spline derivatives for spacecraft velocities")
            # Compute derivatives of spline objects for spacecraft velocities
            self.interp_vx = {sc: self.interp_x[sc].derivative() for sc in self.SC}
            self.interp_vy = {sc: self.interp_y[sc].derivative() for sc in self.SC}
            self.interp_vz = {sc: self.interp_z[sc].derivative() for sc in self.SC}
        else:
            # Compute spline interpolation for velocities
            logger.debug("Computing spline interpolation for spacecraft velocities")
            self.interp_vx = {sc: interpolate(spacecraft_velocities[:, sc - 1, 0]) for sc in self.SC}
            self.interp_vy = {sc: interpolate(spacecraft_velocities[:, sc - 1, 1]) for sc in self.SC}
            self.interp_vz = {sc: interpolate(spacecraft_velocities[:, sc - 1, 2]) for sc in self.SC}

        # Compute derivatives of spline objects for spacecraft accelerations
        logger.debug("Computing spline derivatives for spacecraft accelerations")
        self.interp_ax = {sc: self.interp_vx[sc].derivative() for sc in self.SC}
        self.interp_ay = {sc: self.interp_vy[sc].derivative() for sc in self.SC}
        self.interp_az = {sc: self.interp_vz[sc].derivative() for sc in self.SC}

        logger.debug("Computing spline interpolation for spacecraft proper times")
        self.interp_dtau = {}
        self.interp_tau = {}
        for sc in self.SC:
            pos_norm = norm(self.spacecraft_positions[:, sc - 1])
            v_squared = self.interp_vx[sc](self.interp_t)**2 \
                + self.interp_vy[sc](self.interp_t)**2 \
                + self.interp_vz[sc](self.interp_t)**2
            dtau = -0.5 * (SUN_SCHWARZSCHILD_RADIUS / pos_norm + v_squared / c**2)
            self.interp_dtau[sc] = interpolate(dtau)
            self.interp_tau[sc] = self.interp_dtau[sc].antiderivative()

    def _write_metadata(self, hdf5):
        super()._write_metadata(hdf5)
        self._write_attr(hdf5, 'interp_order', 'ext', 'check_input')

    def _check_shapes(self):
        """Check array shapes.

        We check that ``t`` is of shape (N), and ``spacecraft_positions`` and
        ``spacecraft_velocities`` (if not None) are of shape (N, 3, 3).

        Raises:
            ValueError: if the shapes are invalid.
        """
        if len(self.interp_t.shape) != 1:
            raise ValueError(f"time array has shape {self.interp_t.shape}, must be (N).")

        size = self.interp_t.shape[0]
        if len(self.spacecraft_positions.shape) != 3 or \
           self.spacecraft_positions.shape[0] != size or \
           self.spacecraft_positions.shape[1] != 3 or \
           self.spacecraft_positions.shape[2] != 3:
            raise ValueError(
                f"spacecraft position array has shape "
                f"{self.spacecraft_positions.shape}, expected ({size}, 3, 3).")
        if self.spacecraft_velocities is not None and (
                len(self.spacecraft_velocities.shape) != 3 or \
                self.spacecraft_velocities.shape[0] != size or \
                self.spacecraft_velocities.shape[1] != 3 or \
                self.spacecraft_velocities.shape[2] != 3
            ):
            raise ValueError(
                f"spacecraft velocity array has shape "
                f"{self.spacecraft_velocities.shape}, expected ({size}, 3, 3).")

    @staticmethod
    def _broadcast_time(t, sc):
        """Broadcast time vector as a dictionary for each spacecraft in ``sc``.

        If ``t`` is of shape (N,), we use the array as-is as keys for all elements of ``sc``.
        If ``t`` is of shape (N, M) and ``sc`` is of shape (M,), then we return a dictionary
        with elements of ``sc`` as keys, and sliced (N,) arrays from ``t`` as values.

        Args:
            t ((N,) or (N, M) array-like): TCB times [s]
            sc ((M,) array-like): spacecraft indices

        Returns:
            dict of (N,) ndarrays: Dictionary of time arrays.

        Raises:
            ValueError: if the shapes of ``t`` and ``sc`` are incompatible.
        """
        logger.debug("Broadcasting time vector for spacecrast %s", sc)
        t = np.asarray(t)
        if t.ndim == 1:
            return {sc[i]: t for i in range(len(sc))}
        if t.shape[1] == sc.shape[0]:
            return {sc[i]: t[:, i] for i in range(len(sc))}
        raise ValueError("incompatible shapes for 't' and 'sc'")

    def compute_position(self, t, sc):
        t = self._broadcast_time(t, sc)
        # Interpolate state vector
        sc_x = np.stack([self.interp_x[a_sc](t[a_sc]) for a_sc in sc], axis=-1) # (N, M)
        sc_y = np.stack([self.interp_y[a_sc](t[a_sc]) for a_sc in sc], axis=-1) # (N, M)
        sc_z = np.stack([self.interp_z[a_sc](t[a_sc]) for a_sc in sc], axis=-1) # (N, M)
        return np.stack([sc_x, sc_y, sc_z], axis=-1) # (N, M, 3)

    def compute_velocity(self, t, sc):
        t = self._broadcast_time(t, sc)
        # Interpolate state vector
        sc_vx = np.stack([self.interp_vx[a_sc](t[a_sc]) for a_sc in sc], axis=-1) # (N, M)
        sc_vy = np.stack([self.interp_vy[a_sc](t[a_sc]) for a_sc in sc], axis=-1) # (N, M)
        sc_vz = np.stack([self.interp_vz[a_sc](t[a_sc]) for a_sc in sc], axis=-1) # (N, M)
        return np.stack([sc_vx, sc_vy, sc_vz], axis=-1) # (N, M, 3)

    def compute_acceleration(self, t, sc):
        t = self._broadcast_time(t, sc)
        # Interpolate state vector
        sc_ax = np.stack([self.interp_ax[a_sc](t[a_sc]) for a_sc in sc], axis=-1) # (N, M)
        sc_ay = np.stack([self.interp_ay[a_sc](t[a_sc]) for a_sc in sc], axis=-1) # (N, M)
        sc_az = np.stack([self.interp_az[a_sc](t[a_sc]) for a_sc in sc], axis=-1) # (N, M)
        return np.stack([sc_ax, sc_ay, sc_az], axis=-1) # (N, M, 3)

    def compute_tps_deviation(self, t, sc):
        t = self._broadcast_time(t, sc)
        return np.stack([self.interp_tau[a_sc](t[a_sc]) for a_sc in sc], axis=-1) # (N, M)

    def compute_tps_deviation_derivative(self, t, sc):
        t = self._broadcast_time(t, sc)
        return np.stack([self.interp_dtau[a_sc](t[a_sc]) for a_sc in sc], axis=-1) # (N, M)


class OEMFormatError(Exception):
    """Error in OEM format."""


class OEMOrbits(InterpolatedOrbits):
    """Reads orbits from three Orbit Ephemeris Message (OEM) files.

    Each OEM file describes the orbit of one spacecraft.

    The package includes some standard EOM files. Use {meth}`lisaorbits.EOMOrbits.
    from_included` to initialize an instance from those easily.

    Args:
        eom_1 (str): path to EOM file for spacecraft 1
        eom_2 (str): path to EOM file for spacecraft 2
        eom_3 (str): path to EOM file for spacecraft 3
        dt (float or str): sampling period [s], or ``'eom'`` to match EOM file's
        size (int or str): simulation size [samples], or ``'eom'`` to match EOM file's
        t0 (float or str): initial time [datetime], or ``'eom'`` to match EOM file's
        **kwargs: all other args from :class:`lisaorbits.InterpolatedOrbits`
    """

    def __init__(self, oem_1, oem_2, oem_3, dt='oem', size='oem', t0='oem', **kwargs):

        # Save file paths
        #: str: Path to EOM file for spacecraft 1.
        self.filename_1 = str(oem_1)
        #: str: Path to EOM file for spacecraft 2.
        self.filename_2 = str(oem_2)
        #: str: Path to EOM file for spacecraft 3.
        self.filename_3 = str(oem_3)

        # Read files
        epochs_1, positions_1 = self._read_oem(oem_1, 1)
        epochs_2, positions_2 = self._read_oem(oem_2, 2)
        epochs_3, positions_3 = self._read_oem(oem_3, 3)

        # Check time scales are identical
        if not np.all(epochs_1 == epochs_2) or not np.all(epochs_2 == epochs_3):
            raise ValueError("input files have different sampling")
        epochs = epochs_1
        positions = np.stack([positions_1, positions_2, positions_3], axis=1) # shape (t, sc, coord)

        # Replace sampling parameters that match EOM input files
        if len(epochs) <= 1:
            raise ValueError("input files must have at least two data points")
        dt = dt if dt != 'oem' else epochs[1] - epochs[0]
        size = size if size != 'oem' else len(epochs)
        t0 = t0 if t0 != 'oem' else datetime.datetime.fromtimestamp(epochs[0])

        # Convert from km (in OEM file) to meters
        positions *= 1E3
        # Convert from equatorial coordinates (in OEM file) to ecliptic coordinates
        # The conversion uses the obliquity of the ecliptic (84381".406 from IAU 2006)
        # To be changed to LISA Constant's `obliquity` constant when v1.2 is released
        obliquity = 84381.406 / (60 * 60) * (2 * np.pi / 360)
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(obliquity), -np.sin(obliquity)],
            [0, np.sin(obliquity), np.cos(obliquity)]
        ])
        ecliptic_positions = np.einsum('ijk,kl->ijl', positions, rotation_matrix)

        super().__init__(epochs, ecliptic_positions, dt=dt, size=size, t0=t0, **kwargs)

    @classmethod
    def from_included(cls, name, **kwargs):
        """Initialize an instance from EOM files included in the package.

        Args:
            name (str): 'esa-leading' or 'esa-trailing'
            **kwargs: all other args from :class:`lisaorbits.OEMOrbits`
        """
        data_dir = importlib_resources.files('lisaorbits') / 'data'
        if name == 'esa-trailing':
            oem_1 = data_dir / 'esa-trailing' / 'trajectory_out_mida-20deg_cw_sg-2nmss.oem1'
            oem_2 = data_dir / 'esa-trailing' / 'trajectory_out_mida-20deg_cw_sg-2nmss.oem2'
            oem_3 = data_dir / 'esa-trailing' / 'trajectory_out_mida-20deg_cw_sg-2nmss.oem3'
        elif name == 'esa-leading':
            oem_1 = data_dir / 'esa-leading' / 'trajectory_out_mida+20deg_cw_sg-2nmss.oem1'
            oem_2 = data_dir / 'esa-leading' / 'trajectory_out_mida+20deg_cw_sg-2nmss.oem2'
            oem_3 = data_dir / 'esa-leading' / 'trajectory_out_mida+20deg_cw_sg-2nmss.oem3'
        else:
            raise ValueError(f"unsupported included EOM files '{name}'")

        return cls(oem_1, oem_2, oem_3, **kwargs)

    def _write_metadata(self, hdf5):
        super()._write_metadata(hdf5)
        self._write_attr(hdf5, 'filename_1', 'filename_2', 'filename_3')

    def _read_oem(self, path, index):
        """Parse OEM file.

        We check structure and metadata, and return epochs and positions.

        Args:
            path (str): path to OEM file
            index (int): spacecraft index

        Returns:
            tuple: 2-tuple ``(epochs, positions)`` where `epochs` is a list of N UNIX timestamps,
            and ``positions`` is an array of shape (N, 3).
        """
        # pylint: disable=protected-access
        logger.info("Reading OEM file '%s'", path)
        ephemeris = OrbitEphemerisMessage.open(path)

        if ephemeris.version != '2.0':
            raise OEMFormatError(f"unsupported OEM version (got '{ephemeris.version}', expected '2.0')")
        if len(ephemeris._segments) != 1:
            raise OEMFormatError(f"invalid number of OEM segments (got {len(ephemeris._segments)}, expected 1)")

        header = {key: ephemeris.header[key] for key in ephemeris.header}
        setattr(self, f'header_{index}', header)

        segment = ephemeris._segments[0]
        metadata = segment.metadata
        if metadata['CENTER_NAME'] != 'SUN':
            raise OEMFormatError("invalid OEM metadata 'CENTER_NAME' (got '{metadata['CENTER_NAME']}', expected 'SUN')")
        if metadata['REF_FRAME'] != 'EME2000':
            raise OEMFormatError("invalid OEM metadata 'REF_FRAME' (got '{metadata['REF_FRAME']}', expected 'EME2000')")

        metadata_dict = {key: metadata[key] for key in metadata}
        setattr(self, f'metadata_{index}', metadata_dict)

        epochs = np.array([state.epoch.unix for state in segment])
        positions = np.stack([state.position for state in segment], axis=0)
        return (epochs, positions)


class ResampledOrbits(InterpolatedOrbits):
    """Resamples an existing orbit file to a new time grid.

    Splines are used to resample the spacecraft positions. All other quantities
    are deduced, as described in :class:`lisaorbits.InterpolatedOrbits`.

    Args:
        orbits (str): path to an existing orbit file
        **kwargs: all other args from :class:`lisaorbits.InterpolatedOrbits`
    """

    def __init__(self, orbits, **kwargs):

        #: str: Path to the original orbit file.
        self.orbits_path = str(orbits)

        # Load orbit file
        logger.info("Reading orbit file '%s'", self.orbits_path)
        t, spacecraft_positions = self._read_orbit_file()

        with h5py.File(self.orbits_path, 'r') as orbitf:
            self.original_attrs = dict(orbitf.attrs)

        super().__init__(t, spacecraft_positions, ext='extrapolate', **kwargs)

    def _write_metadata(self, hdf5):
        super()._write_metadata(hdf5)
        self._write_attr(hdf5, 'original_attrs')

    def _read_orbit_file(self):
        """Read the original orbit file.

        Returns:
            tuple: Tuple ``(t, spacecraft_positions)`` of arrays of times [s] and
            spacecraft positions [m] with dimension (t, sc, coordinate).

        Raises:
            ValueError: if the orbit file's version is not supported.
        """
        with h5py.File(self.orbits_path, 'r') as orbitf:
            version = orbitf.attrs['version']
            logger.debug("Using orbit file version %s", version)
            if version in SpecifierSet('~= 1.0'):
                sc_1 = np.stack((orbitf['tcb/sc_1'][coord] for coord in ['x', 'y', 'z']), axis=-1)
                sc_2 = np.stack((orbitf['tcb/sc_2'][coord] for coord in ['x', 'y', 'z']), axis=-1)
                sc_3 = np.stack((orbitf['tcb/sc_3'][coord] for coord in ['x', 'y', 'z']), axis=-1)
                spacecraft_positions = np.stack((sc_1, sc_2, sc_3), axis=1)
                return orbitf['tcb/t'], spacecraft_positions

            raise ValueError(f"unsupported orbit file version '{version}'")
