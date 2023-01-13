"""
Flatspin model
"""
#!/usr/bin/env python3
import sys
import os
import numpy as np
from numpy.linalg import norm
from math import ceil, sqrt
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap
from matplotlib.collections import PatchCollection
import time
import itertools
from datetime import timedelta
from copy import copy
from PIL import Image
import pkg_resources
from abc import ABC, abstractmethod
import warnings

from flatspin.grid import Grid
from flatspin.vertices import find_vertices, vertex_type
from flatspin.utils import get_default_params
from flatspin.plotting import plot_vectors, plot_astroid
from flatspin.data import read_table

# TODO: Only import pycuda of use_cuda=1
normalize_rad = Normalize(vmin=0, vmax=2*np.pi)
normalize_vertex_type = Normalize(vmin=1, vmax=4)

kB = 1.38064852e-23 # m^2 kg s^-2 K^-1

class LabelIndexer:
    """ Lookup table of labels to spin index

    Supports standard numpy indexing such as slices etc.
    """
    def __init__(self, labels):
        labels = np.array(labels)
        if len(labels.shape) == 1:
            labels.shape += (1,)

        shape = tuple(np.max(labels, axis=0) + 1)
        # Empty slots in the lookup table are -1
        self.index = np.full(shape, -1, dtype=int)
        # Populate table with labels
        self.index[tuple(labels.T)] = np.arange(len(labels), dtype=int)

    def __getitem__(self, label):
        indices = self.index[label]
        indices = indices[indices >= 0]
        if len(indices) == 1:
            indices = indices[0]
        return indices

    def __repr__(self):
        return repr(self.index)

class SpinIce(ABC):
    """ Spin ice abstract base class

    The :class:`SpinIce` class contains the core implementation
    of the :ref:`flatspin model <model>`. It is an abstract base class, and
    cannot be instantiated directly. Subclasses of this class define the
    geometry, by implementing :func:`_init_geometry`.
    """
    def __init__(self, *, size=(4,4), lattice_spacing=1, hc=0.2, alpha=0.001,
            disorder=0, h_ext=(0,0), neighbor_distance=1, switching='sw',
            sw_b=0.41, sw_c=1, sw_beta=1.5, sw_gamma=3.9,
            temperature=0, therm_timescale=1, m_therm=.2*860e3*220e-9*80e-9*25e-9,
            attempt_freq=1e9, flip_mode='max', init='polarized',
            random_prob=0.5, random_seed=0,
            use_opencl=False, opencl_platform=0, opencl_device=0,
            use_cuda=False, astroid_resolution=1801):
        """
        Parameters
        ----------
        size : tuple of int
            The size of the spin ice (width, height).
            Note that the size is geometry specific.
        lattice_spacing : float
            Spacing between each spin.
        hc : float
            Mean switching threshold.
        alpha : float
            Coupling strength alpha = u_0 * M / (4 * pi * a^3), where a is the
            lattice spacing and M is the net magneticmoment of a single magnet.
        disorder : float
            Switching threshold disorder as percentage of hc. If non-zero,
            sample switching from a normal distribution with mean hc and
            standard deviation hc * disorder.
        h_ext : tuple of float
            External field (h_extx, h_exty).
        neighbor_distance : float
            Neighborhood to consider when calculating dipole interactions.
            All spins within lattice_spacing * neighbor_distance are considered
            neighbors. Set neighbor_distance=np.inf for a global neighborhood.
        switching : {'sw', 'budrikis'}
            Magnetic switching model:
                - 'sw': Extended Stoner-Wohlfarth model
                - 'budrikis': switching based on the parallel field component
        sw_b : float
            Height of the Stoner-Wohlfarth astroid (parallel axis).
        sw_c : float
            Width of the Stoner-Wohlfarth astroid (perpendicular axis).
        sw_beta : float
            Pointiness of the top/bottom of the Stoner-Wohlfarth astroid
            (parallel axis).
        sw_gamma : float
            Pointiness of the left/right of the Stoner-Wohlfarth astroid
            (perpendicular axis).
        temperature : float (positive)
            Absolute temperature in Kelvin.
        therm_timescale : float
            The thermal time scale (length in seconds of each simulated timestep).
            When temperature > 0, the thermal activity per timestep increases
            with therm_timescale. See also set_temperature().
        m_therm : float
            Thermal nucleation moment (thermal nucleation volume * magnetic moment).
            See also set_temperature().
        attempt_freq : float
            Attempt frequency (1/s).
            Only used for temperature calculations, see set_temperature().
        flip_mode : {'single', 'max', 'max-rand', 'all'}
            Flip mode strategy:
                - 'single': single uniform random flip (Budrikis Monte Carlo)
                - 'max': flip the spin with maximum energy, break ties by index
                - 'max-rand': flip the spin with maximum energy, break ties randomly
                - 'all': flip all flippable spins
        init : {1, -1, 'random', 'image.png'} or ndarray
            Initial spin state.
        use_opencl : bool
            Use OpenCL acceleration.
        opencl_platform : int
            Select OpenCL platform (if multiple GPUs of different families are installed).
        opencl_device : int
            Select OpenCL device (if multiple GPUs of the same family are installed).
        use_cuda : bool
            Use CUDA acceleration. NB! Requires compute platform 10 and above.
        astroid_resolution : number of polar points in one rotation to resolve
            astroid shape for h_dist calculcations

        """
        self.size = size
        self.lattice_spacing = lattice_spacing
        self.hc = hc
        self.alpha = alpha
        self.disorder = disorder
        self.switching = switching
        self.sw_params = (sw_b, sw_c, sw_beta, sw_gamma)
        self.m_therm = m_therm
        self.therm_timescale = therm_timescale
        self.attempt_freq = attempt_freq
        self.astroid_resolution = astroid_resolution
        self.flip_mode = flip_mode
        self.neighbor_distance = neighbor_distance
        self.random_prob = random_prob
        assert switching in ('budrikis', 'sw')
        assert flip_mode in ('single', 'max', 'max-rand', 'all')
        assert neighbor_distance > 0

        self.labels = None

        self.cl = use_opencl
        self.cl_device = opencl_device
        self.cl_platform = opencl_platform
        self._cl_context = None

        self.cuda = use_cuda
        self._cuda_relax_kernel = None

        self.set_random_seed(random_seed)

        # geometry
        pos, angle = self._init_geometry()
        self.pos = pos.astype(float, order='C')
        self.angle = angle.astype(float)
        self.m = np.column_stack([np.cos(self.angle), np.sin(self.angle)])
        self.spin_count = len(self.pos)

        if self.labels is None:
            # No labels, labels = indices
            self.labels = np.arange(self.spin_count)

        self.L = LabelIndexer(self.labels)

        # astroid tree
        self._init_astroid_tree()

        # spin flip threshold
        self.threshold = np.zeros(self.spin_count)
        self._init_threshold()

        # spin state
        self.spin = np.ones(self.spin_count, dtype=np.int8)
        self._init_spin(init)

        # flat neighbor list (computed once)
        self._neighbor_list = self._init_neighbor_list()
        self.num_neighbors = self._neighbor_list.shape[-1]

        # dipolar fields between each spin and its neighbors
        # precomputed on demand by _h_dip/_init_cl
        self._h_dip_cache = None

        self.set_h_ext(h_ext)

        # minimum threshold from origo
        self._zero_to_astroid = self.astroid_tree.query([(0,0)], k=1)[0][0]
        self._multiflip_warn = 0.05

        # thermal noise
        self.temperature = 0
        self.set_temperature(temperature)
        self.update_thermal_noise()

    @property
    def N(self):
        """ Alias for self.spin_count """
        return self.spin_count

    def label(self, i):
        """ Get the label of a given spin index or list of indices """
        return tuple(self.labels[i])

    def indexof(self, label):
        """ Get the spin index of a given label or range of labels

        Alias for self.L[label]
        """
        return self.L[label]

    def indices(self):
        """ Get all spin indices """
        return range(self.spin_count)

    def all_indices(self):
        """ Get all spin indices as numpy integer array index
        See https://docs.scipy.org/doc/numpy/reference/arrays.indexing.html#integer-array-indexing
        """
        return list(self.indices())

    def _init_spin(self, init):
        if isinstance(init, str) and init == 'random':
            self.randomize(self.random_prob)

        if isinstance(init, str) and init.endswith('png'):
            self.set_spin_image(init)

        if isinstance(init, np.ndarray):
            self.set_spin(init)

        if isinstance(init, int) and init in (-1, 1):
            self.polarize(init)

    @abstractmethod
    def _init_geometry(self):
        """ Initialize the geometry

        Subclasses should override this method and return a tuple (pos, angle),
        where pos is an array with the (x, y) positions of the spins, while
        angle is an array with the rotations of the spins.

        The base class implementation may be invoked to generate an Ising
        geometry.
        """
        nx, ny = self.size
        spin_count = nx * ny
        pos = np.zeros((spin_count, 2), dtype=float)
        angle = np.zeros(spin_count, dtype=float)

        # rotation of each spin: zero by default

        # positions of each spin
        rows = np.arange(ny, dtype=int)
        cols = np.arange(nx, dtype=int)
        grid = np.array(np.meshgrid(rows, cols))
        grid = grid.T.reshape((-1, 2))
        pos = self.lattice_spacing * np.flip(grid.astype(float), axis=-1)
        pos[:] = pos
        self.labels = grid

        return pos, angle

    def _init_threshold(self):
        # spin flip threshold
        if np.array(self.hc).size > 1:
           self._init_threshold_grid()
        else:
            if self.disorder:
                std = self.hc * self.disorder
                self.threshold = self.rng.normal(self.hc, std, self.threshold.shape)
            else:
                self.threshold[:] = self.hc

        if self.disorder:
            # all thresholds should be positive
            self.threshold = np.abs(self.threshold)

    def _init_threshold_grid(self):
        hc = np.atleast_2d(self.hc)
        G = self.fixed_grid((hc.shape[1], hc.shape[0]))

        if self.disorder:
            for i in np.ndindex(G.size):
                std = hc[i] * self.disorder
                spin_inds = G.point_index(i)
                self.threshold[spin_inds] = self.rng.normal(hc[i], std, len(spin_inds))
        else:
            spin_inds = self.all_indices()
            grid_inds = G.grid_index(spin_inds)
            self.threshold[spin_inds] = hc[grid_inds]

    def _init_neighbor_list(self):
        # Calculate neighborhood matrix
        # print(f'_init_neighbor_list(size={self.size})')
        neighbors = []
        num_neighbors = 0

        # Construct KDTree for every position
        tree = cKDTree(self.pos)

        nd = self.lattice_spacing * self.neighbor_distance
        nd += 1e-5 # pad to avoid rounding errors

        for i in self.indices():
            p = self.pos[i]
            n = tree.query_ball_point([p], nd)[0]
            n.remove(i)
            neighbors.append(n)
            num_neighbors = max(num_neighbors, len(n))

        # print(f'num_neighbors={num_neighbors}')

        # Neighborhood list, -1 marks end of each list
        neighbor_list = np.full((self.spin_count, num_neighbors), -1, dtype=np.int32)
        for i, neighs in enumerate(neighbors):
            neighbor_list[i,:len(neighs)] = neighs

        return neighbor_list

    def _init_h_dip(self):
        # when use_opencl=1, the hdip cache is initialized by _init_cl()
        assert (not self.cl) and (not self.cuda)

        # cache dipolar fields for the neighborhood of all magnets
        _h_dip = np.zeros((self.spin_count, self.num_neighbors, 2), dtype=np.float64)
        for i in self.indices():
            for jj, j in enumerate(self.neighbors(i)):
                # print(f'i={i} jj={jj} j={j}')
                _h_dip[i][jj] = np.array(self.spin_dipolar_field(i, j))

        return _h_dip

    def _init_astroid_tree(self):
        # Switching astroid shape in units hk (self.threshold)
        b, c, beta, gamma = self.sw_params

        # Due to the two-fold symmetry of the astroid, we only need to consider
        # one quadrant where h_par <= 0 and h_perp >= 0
        # Note: the first element is top of astroid, while last element is the apex
        thetas = np.linspace(0, -np.pi/2, self.astroid_resolution)

        # h_par, h_perp are created from calculating h_par(h_perp) from SW-
        # curve, over thetas coresponding to negative h_pars
        h_perp = c * np.cos(thetas)
        h_par = -b * (1 - ((h_perp/c)**2)**(1/beta))**(gamma/2)

        # Construct cKDTree of astroid to quickly look up nearest point
        astroid_points = np.column_stack((h_par, h_perp))
        self.astroid_tree = cKDTree(astroid_points)

        # Calculate astroid normals based on left/right neighbor
        p0 = astroid_points[0:-2]
        p2 = astroid_points[2:]
        delta = p2 - p0
        dx = delta[:,0]
        dy = delta[:,1]
        normals = np.column_stack([dy, -dx])

        # Normalize to unit length
        lens = norm(normals, axis=1).reshape((-1, 1))
        normals /= lens

        # For edges of the astroid (top/bottom and apex), simply use the
        # normals of the next neighbor
        normals = np.pad(normals, ((1, 1), (0, 0)), 'edge')

        self.astroid_normals = normals

    def __getstate__(self):
        odict = copy(self.__dict__)
        # Don't pickle _cl attributes. They will be automatically
        # re-initialized by _init_cl() when needed
        for k in list(filter(lambda k: k.startswith('_cl'), odict)):
            odict[k] = None
        return odict

    def __eq__(self, other):
        state = self.__getstate__()
        other_state = other.__getstate__()
        for k in state:
            if np.any(state[k] != other_state[k]):
                return False
        return True

    @property
    def width(self):
        x = self.pos[:, 0]
        xmin, xmax = np.min(x), np.max(x)
        return xmax - xmin

    @property
    def height(self):
        y = self.pos[:, 1]
        ymin, ymax = np.min(y), np.max(y)
        return ymax - ymin

    @property
    def vectors(self):
        """ Spin vectors """
        spin = np.array(self.spin, dtype=float)
        spin.shape += (1,)
        mag = self.m * spin
        return mag

    def set_spin(self, spin):
        spin = np.array(spin, dtype=np.int8)
        assert spin.shape == (self.spin_count,)
        assert np.all(np.logical_or(spin == 1, spin == -1))
        self.spin = spin

    def set_spin_image(self, filename):
        """ Set spin state from image

        The image is resized to fit the default spin grid. Then the grayscale
        image is used to set spin state:
        * black maps to spin -1
        * non-black maps to spin 1
        """
        # Use default grid
        G = self.grid()
        # calculate size of grid
        height, width = G.size

        # load image
        img = Image.open(filename)
        img = img.convert('L') # convert to grayscale

        # flip it since (0,0) is top left in the image but (0,0) is bottom left
        # in our spin geometry
        img = img.transpose(Image.FLIP_TOP_BOTTOM)

        # resize image to the default grid size
        img = img.resize((width, height))
        img = np.array(img)

        img[img != 0] = 1  # map non-black to spin 1
        img[img == 0] = -1 # map black to spin -1

        # finally set all the spins
        self.set_grid('spin', np.array(img))

    def set_threshold(self, threshold):
        """
        Set switching thresholds manually.

        NB: this method does not update self.hc
        """
        assert threshold.shape == (self.spin_count,)
        self.threshold = np.array(threshold)

    def set_hc(self, hc):
        """
        Set mean switching threshold hc.

        Rescales existing thresholds to have new mean hc and standard
        devication hc * disorder.
        """
        if np.array(hc).size > 1 or np.array(self.hc).size > 1:
            # old or new hc were grid based
            return self._set_hc_grid(hc)

        self.threshold *= hc / self.hc
        self.hc = hc

    def _set_hc_grid(self, hc):
        spin_inds = self.all_indices()

        # Determine the old hc values based on self.hc
        # which may or may not have been a grid based thing
        values = np.atleast_2d(self.hc)
        G = self.fixed_grid((values.shape[1], values.shape[0]))

        # Map old hc values onto spins
        old_hc = np.zeros(self.spin_count)
        grid_inds = G.grid_index(spin_inds)
        old_hc[spin_inds] = values[grid_inds]

        # Similarly, map new hc values onto spins
        values = np.atleast_2d(hc)
        G = self.fixed_grid((values.shape[1], values.shape[0]))
        grid_inds = G.grid_index(spin_inds)
        new_hc = np.zeros(self.spin_count)
        new_hc[spin_inds] = values[grid_inds]

        # Finally, rescale existing thresholds to have new mean hc from grid
        self.threshold *= new_hc / old_hc
        self.hc = hc

    def set_h_ext(self, h_ext):
        """
        Set external field to h_ext

        h_ext can either be a single vector for a uniform field (h_ext.shape==(2,))
        or a 2D array of vectors for a non-uniform field (h_ext.shape==(self.spin_count, 2))
        """
        h_ext = np.array(h_ext, dtype=np.float64, order='C')
        assert h_ext.shape == (2,) or h_ext.shape == (self.spin_count, 2)
        if h_ext.shape == (2,):
            h_ext = np.tile(h_ext, (self.spin_count, 1))
        self.h_ext = h_ext

    def set_h_ext_grid(self, h_ext):
        if h_ext.shape == (2,):
            # global
            self.set_h_ext(h_ext)
        else:
            # grid
            self.set_grid('h_ext', h_ext)

    def set_alpha(self, alpha):
        """ Set coupling strength alpha = u_0 * M / (4 * pi * a^3), where a is the
            lattice spacing and M is the net magneticmoment of a single magnet."""
        self.alpha = alpha

    def set_therm_timescale(self, therm_timescale):
        """ Set thermal time scale (length in seconds of each simulated timestep).
            When temperature > 0, the thermal activity per timestep increases
            with therm_timescale. See also set_temperature(). """
        self.therm_timescale = therm_timescale

    def set_m_therm(self, m_therm):
        """ Thermal nucleation moment (thermal nucleation volume * magnetic moment).
            See also set_temperature(). """
        self.m_therm = m_therm

    def set_temperature(self, temperature):
        """ Set temperature for the thermal field

        The random thermal field depends on temperature, as well as the
        parameters m_therm, therm_timescale and attempt_freq.

        Note: flatspin does not account for the temperature dependence of the
        parameters.  If these parameters are expected to vary significantly in
        the temperature range of interest, this has to be explicitly accounted
        for by the user.
        """
        assert self.m_therm > 0
        assert self.therm_timescale > 0
        assert self.attempt_freq > 0
        assert temperature >= 0

        # multiflip warning
        if self.temperature < temperature:
            # If the new temperature is higher, warn if multiflip is likely
            threshold_zero = np.mean(self.threshold) * self._zero_to_astroid
            f = self.attempt_freq * np.exp(-self.m_therm * \
                threshold_zero / (kB * temperature))
            P_flip_zero = np.exp(-f * self.therm_timescale)
            P_flip_once = f * self.therm_timescale * np.exp(-f * self.therm_timescale)
            P_multiflip = 1 - P_flip_zero - P_flip_once
            #print(f"P_flip_once={P_flip_once} P_multiflip={P_multiflip}")
            if P_multiflip > self._multiflip_warn:
                warnings.warn(f"Probability of multiflip, {P_multiflip:.3f}, "
                    + f"exceeds {self._multiflip_warn} for temperature={temperature}. "
                    + "Reduce therm_timescale or temperature.")

        self.temperature = temperature

    def set_random_seed(self, seed):
        """ Seed the random number generator used in the model. """
        self.random_seed = seed
        self.rng = np.random.default_rng(seed)

    def set_angle(self, angle):
        """ Change the angles of the spins.

        angle is an array of new angles in radians.
        The number of new angles must match the spin count.
        """
        angle = np.array(angle, dtype=float)
        assert angle.shape == (self.spin_count,)
        self.angle = angle
        self.m = np.column_stack([np.cos(angle), np.sin(angle)])

        # Invalidate the h_dip cache
        self._h_dip_cache = None
        if self.cl:
            self._init_cl_geometry()
        if self.cuda:
            self._init_cuda_geometry()

    def set_pos(self, pos):
        """ Change the positions of the spins.

        pos is an array of new positions.
        The number of new positions must match the spin count.
        """
        pos = np.array(pos, dtype=float, order='C')
        assert pos.shape == (self.spin_count, 2)
        self.pos = pos

        # Invalidate the h_dip cache
        self._h_dip_cache = None

        # Re-initialize neighbor list
        self._neighbor_list = self._init_neighbor_list()
        self.num_neighbors = self._neighbor_list.shape[-1]

        if self.cl:
            self._init_cl_geometry()
        if self.cuda:
            self._init_cuda_geometry()

    def set_geometry(self, pos, angle):
        """ Change the geometry.

        angle is an array of new angles in radians.
        pos is an array of new positions.
        The number of new positions and angles must match the spin count.
        """
        pos = np.array(pos, dtype=float, order='C')
        assert pos.shape == (self.spin_count, 2)
        angle = np.array(angle, dtype=float)
        assert angle.shape == (self.spin_count,)

        self.pos = pos
        self.angle = angle
        self.m = np.column_stack([np.cos(angle), np.sin(angle)])

        # Invalidate the h_dip cache
        self._h_dip_cache = None

        # Re-initialize neighbor list
        self._neighbor_list = self._init_neighbor_list()
        self.num_neighbors = self._neighbor_list.shape[-1]

        if self.cl:
            self._init_cl_geometry()
        if self.cuda:
            self._init_cuda_geometry()

    def randomize(self, prob=0.5, seed=None):
        """ Randomize spins.

        Spins take the value -1 with probability prob.
        If seed is not None, re-seed the model RNG prior to randomizing spins.
        """
        if seed is not None:
            self.set_random_seed(seed)

        self.spin = -1 + 2 * self.rng.binomial(1, 1 - prob, self.spin_count)
        self.spin = self.spin.astype(np.int8)

    def polarize(self, spin=1):
        assert spin in (1, -1)
        self.spin[:] = spin

    def update_thermal_noise(self):
        """ Resamples thermal noise.
        Samples a field magnitude matching probability of switching from
        Poisson(arrhenius_rate(Zeeman/kB*T)*timestep) and returns field vector
        directed along minimal distance to astroid"""

        if self.temperature:
            draw_uniform = self.rng.uniform(size=self.spin_count)
            h_len = self._uniform_to_htherm(draw_uniform)
            self._h_therm_cache = self._field_astroid_direction(h_len)
            # _h_therm_cache is wrt spin direction (h_par, h_perp),
            # so convert to global reference frame to yield h_therm
            m = self.m * self.spin.reshape((-1, 1))
            m_x = np.column_stack([m[:,0], -m[:,1]])
            m_y = np.column_stack([m[:,1], m[:,0]])
            h_therm_x = np.sum(self._h_therm_cache * m_x, axis=1)
            h_therm_y = np.sum(self._h_therm_cache * m_y, axis=1)
            self.h_therm = np.column_stack([h_therm_x, h_therm_y])
        elif self.cuda:
            self._h_therm_cache = np.zeros((self.spin_count,2))
            self.h_therm = np.zeros((self.spin_count, 2))
        else:
            self._h_therm_cache = None
            self.h_therm = np.zeros((self.spin_count, 2))

    def neighbors(self, i):
        neighs = self._neighbor_list[i]
        return neighs[neighs >= 0]

    def spin_dipolar_field(self, i, j):
        """ Calculate dipolar field between spin i and j relative to positive spin """
        r = self.pos[j] - self.pos[i]
        m = self.m
        dist = norm(r)
        h_dip_1 = -m[j] / dist**3
        h_dip_2 = 3 * r * m[j].dot(r) / dist**5
        h_dip = h_dip_1 + h_dip_2

        m_angle = np.arctan2(m[i][1], m[i][0])
        h_angle = np.arctan2(h_dip[1], h_dip[0])
        h = norm(h_dip)
        theta = h_angle - m_angle
        h_par = h*np.cos(theta)
        h_perp = h*np.sin(theta)
        return np.array([h_par, h_perp], dtype=float)

    def dipolar_field(self, i):
        """ Calculate total dipolar field parallell to spin i """
        if self.cl:
            # path only for testing
            return self._h_dip_local_cl()[i]
        if self.cuda:
            return self._h_dip_local_cuda()[i]
        return self._h_dip_local(i)

    def dipolar_fields(self):
        if self.cl:
            return self._h_dip_local_cl()

        if self.cuda:
            return self._h_dip_local_cuda()

        h_dip = np.zeros((self.spin_count, 2))
        for i in self.indices():
            h_dip[i] = self.dipolar_field(i)
        return h_dip

    @property
    def _h_dip(self):
        if self._h_dip_cache is None:
            self._h_dip_cache = self._init_h_dip()
        return self._h_dip_cache

    def _h_dip_local(self, i):
        hdip = np.zeros(2) # h_par, h_perp
        for jj, j in enumerate(self.neighbors(i)):
            # print("h_dip", jj, j)
            hdip += self._h_dip[i][jj] * self.spin[i] * self.spin[j]
        return self.alpha * hdip

    def external_field(self, i):
        """ Calculate external field parallel and perpendicular to spin i """
        if self.cl:
            # path only for testing
            return tuple(self._external_fields_cl()[i])

        if self.cuda:
            return tuple(self._external_fields_cuda()[i])

        m = self.spin[i] * self.m[i]
        h_ext = self.h_ext[i]
        h_par = np.dot(h_ext, m)
        m_perp = [-m[1], m[0]]
        h_perp = np.dot(h_ext, m_perp)
        return np.array([h_par, h_perp], dtype=np.float64)

    def external_fields(self):
        """ Calculate external fields parallel and perpendicular to all spins """
        if self.cl:
            return self._external_fields_cl()

        if self.cuda:
            return self._external_fields_cuda()

        m = self.m * self.spin.reshape((-1, 1))
        h_par = np.sum(self.h_ext * m, axis=1)
        m_perp = np.column_stack([-m[:,1], m[:,0]])
        h_perp = np.sum(self.h_ext * m_perp, axis=1)
        return np.column_stack([h_par, h_perp])

    def thermal_field(self, i):
        """ Calculate thermal field parallel and perpendicular to spin i """
        if self._h_therm_cache is None:
            return np.zeros(2)
        # thermal field is already computerd in _h_therm_cache
        return (self._h_therm_cache[i])

    def thermal_fields(self):
        """ Calculate thermal fields parallel and perpendicular to all spins """
        if self._h_therm_cache is None:
            return np.zeros((self.spin_count, 2))
        # thermal field is already computerd in _h_therm_cache
        return self._h_therm_cache

    def total_field(self, i):
        """ Calculate the total field parallel to spin i """
        if self.cl:
            return self._total_fields_cl()[i] + self.thermal_field(i)

        if self.cuda:
            return self._total_fields_cuda()[i] + self.thermal_field(i)

        return self.dipolar_field(i) + self.external_field(i) + self.thermal_field(i)

    def total_fields(self):
        h_therm = self.thermal_fields() if self.temperature > 0 else 0
        if self.cl:
            # TODO: make thermal_fields_cl
            return self._total_fields_cl() + h_therm
        return self.dipolar_fields() + self.external_fields() + h_therm

    def total_non_thermal_fields(self):
        if self.cl:
            return self._total_fields_cl()
        return self.dipolar_fields() + self.external_fields()

    def flip(self, i):
        self.spin[i] *= -1
        if self._h_therm_cache is not None:
            # Flipping a spin effectively flips its thermal field
            self._h_therm_cache[i] *= -1

    # TODO: rename / discard?
    def _switching_energy_budrikis(self):
        h_tot = self.total_fields()
        h_par = h_tot[..., 0] # parallel components only
        E = -(h_par + self.threshold)
        return E

    def _switching_energy_sw(self):
        b, c, beta, gamma = self.sw_params

        h_tot = self.total_fields()
        h_par = h_tot[..., 0] / (b * self.threshold)
        h_perp = h_tot[..., 1] / (c * self.threshold)

        # Switching criteria 1: h_par**(2/3) + h_perp**(2/3) > hc**(2/3)
        # E > 0: switching is possible
        E = (h_par**2)**(1/gamma) + (h_perp**2)**(1/beta) - 1

        # Switching criteria 2: h_par < 0
        # make E negative when h_par >= 0
        # Use a very small number here instead of zero to avoid a corner case:
        # when the field is perfectly perpendicular to the magnet, rounding
        # errors can cause h_par to always be negative regardless of the spin,
        # resulting in an infinite switching loop.
        cond = h_par >= -1e-12
        E[cond] = -np.abs(E[cond])
        return E

    def switching_energy(self):
        if self.switching == 'budrikis':
            E = self._switching_energy_budrikis()
        else:
            E = self._switching_energy_sw()

        return E

    def flippable_energy(self):
        flippable = []
        energy = self.switching_energy()
        flippable = np.nonzero(energy > 0)
        energy = energy[flippable]
        flippable = flippable[0]
        return flippable, energy

    def flippable(self):
        return self.flippable_energy()[0]

    def _field_astroid_direction(self, magnitude):
        """ Return a vector in the direction of shortest path to astroid """
        if self.switching == 'budrikis':
            return self._field_astroid_direction_budrikis(magnitude)

        return self._field_astroid_direction_sw(magnitude)

    def _field_astroid_direction_budrikis(self, magnitude):
        """ Return a vector in the direction of shortest path to astroid """
        ones = np.ones(self.spin_count)
        h_therm = np.column_stack([-magnitude * ones, 0 * ones])
        return h_therm

    def _field_astroid_direction_sw(self, magnitude):
        """ Return a vector in the direction of shortest path to astroid """
        b, c, beta, gamma = self.sw_params

        # Calculate h_par / h_perp
        h_tot = self.total_non_thermal_fields()

        # Normalize to astroid units
        h_tot /= self.threshold.reshape((-1, 1))

        # Astroid is symmetric, and we only sample the quadrant where h_perp is
        # positive.  When h_perp is negative, we reflect around the h_par axis,
        # and flip the corresponding directions back later.
        h_perp_negative = h_tot[:,1] < 0
        h_tot[:,1] = np.abs(h_tot[:,1])

        h_par = h_tot[..., 0]
        h_perp = h_tot[..., 1]

        # Magnitude is also normalized to astroid units
        if np.isscalar(magnitude):
            magnitude = magnitude * np.ones(self.spin_count)
        else:
            magnitude = np.array(magnitude)
        magnitude /= self.threshold

        # Look up nearest point on astroid
        astroid_points = self.astroid_tree.data
        distances, indices = self.astroid_tree.query(h_tot, k=1)
        nearest = astroid_points[indices]

        # The normal of the nearest point is the direction towards the shortest
        # path out of the astroid... except for a few corner cases, which are
        # handled below.
        normals = self.astroid_normals[indices]

        #
        # When the astroid is not smooth, we cannot rely on the normal.
        # For these cases, we calculate the direction manually.
        #

        # When beta > 2, the astroid is not smooth at the apex
        if beta > 2:
            # If the nearest point is the apex...
            apex_index = len(self.astroid_tree.data) - 1
            cond = (indices == apex_index)

            # Only consider the case where we are on the left side of the apex.
            # The approximation is good enough close to the apex, and this
            # avoids the possibility of crossing the astroid twice when
            # calculating the direction manually, below.  If we didn't ignore
            # this case, it's possible to cross the astroid twice without also
            # crossing the h_perp=0 axis, which would circumvent our
            # double-crossing avoidance code (later).
            cond[cond] = h_par[cond] < nearest[cond,0]

            # Calculate the direction manually based on the next nearest point.
            # We use the next nearest point instead of the apex to ensure the
            # perpendicular component is never zero, which would cause trouble
            # in the double-crossing avoidance code (later).
            next_point = astroid_points[apex_index - 1]
            new_normals = h_tot[cond] - next_point
            lens = norm(new_normals, axis=1).reshape((-1, 1))
            new_normals /= lens
            normals[cond] = new_normals

        # The top/bottom of the astroid is not smooth: it is effectively a
        # corner between the astroid and the h_par=0 axis.

        # If the nearest point is at the top (or bottom)...
        index_top = 0
        cond = indices == index_top
        # ... and h_par is positive (we're inside the astroid, in all other
        # cases the direction based on the normal is fine)
        cond[cond] = h_par[cond] > 0

        # Calculate the direction manually towards the top astroid point
        new_normals = astroid_points[index_top] - h_tot[cond]
        lens = norm(new_normals, axis=1).reshape((-1, 1))
        new_normals /= lens
        normals[cond] = new_normals

        #
        # End of special cases where the astroid is non-smooth
        #

        # If we are above/below the astroid, the shortest distance might be
        # horizontally until we cross the h_par = 0 axis
        cond = h_perp > c
        cond[cond] = distances[cond] > np.abs(h_par[cond])
        normals[cond] = [-1, 0]

        # Direction out of astroid is simply the normals scaled with the magnitudes
        h_dir = normals * magnitude.reshape((-1, 1))

        # Ensure we cannot cross astroid boundary more than once.
        # Negative magnitudes represent thermal energy which counteracts
        # field-based switching, i.e., starting outside the astroid, a thermal
        # field can enter the astroid again.
        # If the magnitude is negative and sufficiently strong, a thermal field may
        # first bring us into the astroid (correct), but then out again (incorrect).
        # Prevent this from happening by calculating the distance to the
        # h_perp=0 axis and make sure it is never crossed.
        #cond = magnitude < 0 and np.abs(h_dir[:,1]) > 1e-5

        # Where do we end up after the thermal field is applied?
        dest = h_perp + h_dir[:,1]
        # Check whether we cross the h_perp=0 axis
        # Due to symmetry, we always start above the axis
        #cond = np.logical_and(np.sign(h_perp) != 0, np.sign(h_perp) != np.sign(dest))
        cond = np.sign(dest) < 0
        # ... and that magnitude is negative
        cond = np.logical_and(cond, magnitude < 0)
        # Reduce the magnitude of h_dir until we hit the h_perp=0 axis
        scale = -h_perp[cond] / h_dir[cond,1]
        h_dir[cond] *= scale.reshape((-1, 1))

        # Flip any vectors with negative h_perp
        h_dir[h_perp_negative,1] *= -1

        # Finally, convert back to h_ext units
        h_dir *= self.threshold.reshape((-1, 1))

        return h_dir

    def _uniform_to_htherm(self, u):
        ''' Transform a random uniform variable to a thermal field magnitude
        '''

        T = self.temperature
        m_therm = self.m_therm
        attempt_freq = self.attempt_freq
        dt = self.therm_timescale

        return (-kB*T / m_therm) * np.log(np.log(u) / (-dt * attempt_freq))

    def step(self):
        """ Perform a flip of one or more flippable spins """
        flip, energy = self.flippable_energy()
        # print("flippable:", len(flip))
        if len(flip) == 0:
            return False

        # TODO: rename / parameterize?
        if self.flip_mode == 'single':
            # Flip a single random spin
            i = self.rng.choice(flip)
            self.flip(i)

        elif self.flip_mode == 'max':
            # Flip the spin with maximum energy
            i = flip[np.argmax(energy)]
            self.flip(i)

        elif self.flip_mode == 'max-rand':
            # Flip the spin with maximum energy, ties broken by random choice
            # Break ties by random choice
            i = np.argmax(energy)
            ties, = np.nonzero(energy == energy[i])
            j = flip[self.rng.choice(ties)]
            self.flip(j)

        # TODO: drop?
        elif self.flip_mode == 'all':
            for i in flip:
                self.flip(i)

        return True

    def relax(self):
        """ Flip spins until equilibrium, return number of calls to step() """
        return self._relax(True, True)

    def _relax(self, copy_cpu_to_gpu=True, copy_gpu_to_cpu=True):
        """ Optimized relax() to avoid unnecessary copying """
        self.update_thermal_noise()

        if self.cuda:
            return self._relax_cuda(copy_cpu_to_gpu, copy_gpu_to_cpu)

        steps = 0

        while self.step():
            steps += 1

        return steps

    def _relax_cuda(self, copy_cpu_to_gpu=True, copy_gpu_to_cpu=True):
        """ Flip spins until equilibrium, return number of calls to step() """
        if not self._cuda_relax_kernel:
            self._init_cuda()

        #hack to avoid copying data if we're not using thermal fields
        if self._h_therm_cache is not None:
            cuda.memcpy_htod(self._cuda_tmp_temp_field, self._h_therm_cache)

        if copy_cpu_to_gpu:
            cuda.memcpy_htod(self._cuda_spin, self.spin)

        cuda.memcpy_htod(self._cuda_h_ext, self.h_ext)

        b, c, beta, gamma = self.sw_params

        self._cuda_relax_kernel(
                (1,1),
                (1,1,1),
                self._cuda_h_dip_cache,
                self._cuda_m,
                self._cuda_h_ext,
                self._cuda_tmp_dip_field,
                self._cuda_tmp_ext_field,
                self._cuda_tmp_temp_field,
                self._cuda_threshold,
                self._cuda_tmp_switching_energies,
                self._cuda_spin,
                self._cuda_neighbor_list,
                self._cuda_num_steps,
                self.alpha,
                b, c, beta, gamma,
                self.num_neighbors,
                self.spin_count,
                self._cuda_done)

        #cuda.memcpy_dtoh(self.spin, self._cuda_spin)
        if (copy_gpu_to_cpu):
            cuda.memcpy_dtoh(self.spin, self._cuda_spin)

        _cuda_returned_num_steps = np.array([0], dtype=np.int32)
        cuda.memcpy_dtoh(_cuda_returned_num_steps, self._cuda_num_steps)

        return _cuda_returned_num_steps[0]

    def energy(self):
        """ Calculate energy per spin

        The energy is the component of the total field directed
        anti-parallel to the spin magnetization """

        h_tot = self.total_fields()
        h_par = h_tot[..., 0] # parallel components only
        E = -h_par
        return E

    def dipolar_energy(self):
        """ Calculate the dipolar energy per spin

        The dipolar energy is the component of the dipolar field directed
        anti-parallel to the spin magnetization """
        h_dip = self.dipolar_fields()
        h_par = h_dip[..., 0] # parallel components only
        E = -h_par
        return E

    def external_energy(self):
        """ Calculate the external energy per spin

        The external energy is the component of the external field directed
        anti-parallel to the spin magnetization """
        h_ext = self.external_fields()
        h_par = h_ext[..., 0] # parallel components only
        E = -h_par
        return E

    def thermal_energy(self):
        """ Calculate the thermal energy per spin

        The thermal energy is the component of the thermal field directed
        anti-parallel to the spin magnetization """
        h_therm = self.thermal_fields()
        h_par = h_therm[..., 0] # parallel components only
        E = -h_par
        return E

    def total_energy(self):
        """ Calculate the total energy """
        return np.sum(self.energy())

    def total_dipolar_energy(self):
        """ Calculate the total dipolar energy """
        return np.sum(self.dipolar_energy())

    def total_external_energy(self):
        """ Calculate the total external energy """
        return np.sum(self.external_energy())

    def total_thermal_energy(self):
        """ Calculate the total thermal energy """
        return np.sum(self.thermal_energy())

    def total_energies(self):
        dip = self.total_dipolar_energy()
        ext = self.total_external_energy()
        therm = self.total_thermal_energy()
        total = np.sum((dip, therm, ext))
        return [dip, ext, therm, total]

    def total_magnetization(self):
        mag = self.vectors
        return np.array(np.sum(mag, axis=0))

    # sub-classes can override this to specify the size of the vertex window
    # (see find_vertices)
    _vertex_size = (2, 1)

    def find_vertices(self):
        """ Find the vertices in this geometry

        Returns a tuple (vi, vj, indices) where vi, vj are the vertex indices
        and indices is a list of spin indices corresponding to each vertex
        index.
        """
        return find_vertices(self.grid(), self.pos, self.angle, self._vertex_size)

    def vertices(self):
        """ Get the spin indices of all vertices """
        vi, vj, indices = self.find_vertices()
        return indices

    def vertex_indices(self):
        """ Get all vertex indices """
        vi, vj, indices = self.find_vertices()
        return vi, vj

    def vertex_type(self, v):
        """ Get the vertex type for a vertex where v are the spin indices
        of the vertex """
        return vertex_type(self.spin[v], self.pos[v], self.angle[v])

    def vertex_count(self):
        """ Count the number of vertices of each type

        Returns a tuple (types, counts) where types are the different vertex
        types and counts are the corresponding counts. """
        vertex_types = [self.vertex_type(v) for v in self.vertices()]
        types, counts = np.unique(vertex_types, return_counts=True)
        return tuple(types), tuple(counts)

    def vertex_population(self):
        """ Calculate the vertex type population as a fraction of all vertices

        Returns a tuple (types, pops) where types are the different vertex
        types and pops are the corresponding fractions. """
        types, counts = self.vertex_count()
        counts = np.array(counts)
        pops = counts / np.sum(counts)
        return types, tuple(pops)

    def vertex_pos(self, v):
        """ Get the position of a vertex where v are the spin indices of the
        vertex """
        return np.mean(self.pos[v], axis=0)

    def vertex_mag(self, v):
        """ Get the direction of a vertex v """
        spin = self.spin[v]
        spin.shape += (1,)
        m = self.m[v]
        mag = m * spin
        return np.sum(mag, axis=0)

    @property
    def _default_cell_size(self):
        return (self.lattice_spacing, self.lattice_spacing)

    def grid(self, cell_size=None):
        """ Map spin indices onto a regular grid

        The spacing between each grid point is given by cell_size.
        If cell_size <= lattice_spacing, each grid cell will contain at
        most one spin.
        If cell_size > lattice_spacing, each grid cell may contain more
        than one spin.
        If cell_size is None, an optimal (geometry dependent) cell size is used

        Returns a Grid object which allows quick lookup of spin index to
        grid index
        """
        if cell_size is None:
            cell_size = self._default_cell_size
        if np.isscalar(cell_size):
            cell_size = (cell_size, cell_size)

        # Calculate optimal padding
        padx = min(self._default_cell_size[0]/2, cell_size[0]/2)
        pady = min(self._default_cell_size[1]/2, cell_size[1]/2)
        padding = (padx, pady)

        grid = Grid(self.pos, cell_size, padding)

        return grid

    def fixed_grid(self, grid_size):
        """ Map spin indices onto a regular grid of fixed size

        Like grid() but takes grid size (number of cells) as parameter
        instead of cell size.
        """
        return Grid.fixed_grid(self.pos, grid_size)

    def set_grid(self, attr, values):
        """ Map grid values onto some spin attribute.

        Valid attributes: spin, h_ext, threshold
        """
        values = np.array(values)
        G = self.fixed_grid((values.shape[1], values.shape[0]))

        # spin indices as numpy integer array index
        spin_inds = self.all_indices()

        # map all spin indices to grid index
        grid_inds = G.grid_index(spin_inds)

        # determine shape of attr and the corresponding set-function
        set_attr = getattr(self, 'set_' + attr)
        oldattr = getattr(self, attr)
        newattr = oldattr.copy()
        newattr[spin_inds] = values[grid_inds]
        set_attr(newattr)

    def view_grid(self, attr, cell_size=None, method='sum'):
        """ Project some spin attribute onto a grid.

        Valid attributes: spin, vectors, h_ext, threshold, pos

        The spacing between each grid cell is given by cell_size.
        If cell_size <= lattice_spacing, each grid cell will contain at
        most one spin attribute.
        If cell_size > lattice_spacing, each grid cell will contain the
        sum of several spin attributes.
        """

        # make the grid
        G = self.grid(cell_size)

        # get the values we wish to view on the grid
        values = getattr(self, attr)

        return G.add_values(values, method=method)

    # TODO: return spin instead of vectors
    def spin_grid(self, cell_size=None):
        """ Project the spin vectors onto a grid.

        See view_grid() for information about cell_size
        """
        return self.view_grid('vectors', cell_size)

    def plot(self, arrows=True, **kwargs):
        return plot_vectors(self.pos, self.vectors, arrows=arrows, **kwargs)

    def plot_energy(self, **kwargs):
        E = self.energy()
        kwargs.setdefault('cmap', 'bwr')
        return self.plot(C=E, **kwargs)

    def plot_vertices(self, **kwargs):
        size = self.lattice_spacing * 0.15
        vertices = self.vertices()
        circles = [plt.Circle(self.vertex_pos(v), size) for v in vertices]
        colors = np.array([self.vertex_type(v) for v in vertices])
        col = PatchCollection(circles, cmap='vertex-type', norm=normalize_vertex_type, **kwargs)
        col.set_array(colors)
        ax = plt.gca()
        ax.add_collection(col)
        ax.autoscale_view()
        return col

    def plot_vertex_mag(self, arrows=True, **kwargs):
        vertices = self.vertices()
        XY = np.array([self.vertex_pos(v) for v in vertices])
        UV = np.array([self.vertex_mag(v) for v in vertices])

        # Normalize vectors to unit length
        nmax = norm(UV, axis=-1).max()
        if nmax != 0:
            UV = UV / nmax

        return plot_vectors(XY, UV, arrows=arrows, **kwargs)

    def plot_astroid(self, rotation=0, **kwargs):
        b, c, beta, gamma = self.sw_params
        return plot_astroid(b, c, beta, gamma, rotation=rotation, **kwargs)

    def plot_astroids(self, **kwargs):
        angles = np.unique(self.angle)
        b, c, beta, gamma = self.sw_params
        for a in angles:
            rotation = np.rad2deg(a)
            kwargs['label'] = f"{rotation:.1f}°"
            plot_astroid(b, c, beta, gamma, rotation=rotation, **kwargs)
        plt.legend()

    def _init_h_dip_cl(self):
        # Only called by _init_cl()
        assert self.cl

        posr = self.pos.ravel()
        pos_g = cl.Buffer(self._cl_context, clmf.READ_ONLY | clmf.COPY_HOST_PTR, hostbuf=posr)
        nn = max(1, self.num_neighbors)
        res_g = cl.Buffer(self._cl_context, clmf.WRITE_ONLY, 2 * self.spin_count * nn * np.dtype(np.float64).itemsize)
        self._cl_prg.spin_dipolar_field(
                self._cl_queue,
                (self.spin_count, nn),
                None,
                pos_g,
                res_g,
                self._cl_neighbors_g,
                self._cl_n_neighbors_g,
                self._cl_m_g
                )


        res = np.empty((self.spin_count, nn, 2), dtype=np.float64)

        cl.enqueue_copy(self._cl_queue, res, res_g)

        return res

    def _init_h_dip_cuda(self):
        # Only called by _init_cuda()
        assert self.cuda

        self._cuda_spin_dipolar_field = self.mod.get_function('spin_dipolar_field').prepare("PPPiP").prepared_call

        nn = max(1, self.num_neighbors)
        posr = self.pos.ravel()
        _cuda_pos_g = cuda.mem_alloc(posr.nbytes)
        _cuda_res_g = cuda.mem_alloc(2 * self.spin_count * nn * np.dtype(np.float64).itemsize)

        cuda.memcpy_htod(_cuda_pos_g, posr)
        #cuda.memcpy_htod(_cuda_res_g,

        #blocksize = 1024;
        #grid_x_dim = np.ceil(self.spin_count/blocksize);
        #grid_y_dim = np.ceil(self.num_neighbors/blocksize);
        grid_x_dim = self.spin_count
        grid_y_dim = nn

        self._cuda_spin_dipolar_field(
                (grid_x_dim, grid_y_dim),
                (1,1,1),
                _cuda_pos_g,
                _cuda_res_g,
                self._cuda_neighbor_list,
                self.num_neighbors,
                self._cuda_m
                )

        res = np.zeros((self.spin_count, nn, 2), dtype=np.float64)

        cuda.memcpy_dtoh(res, _cuda_res_g)

        return res



    def _init_cl(self):
        assert self.cl
        if self._cl_context:
            # already initialized
            return

        global cl, clmf
        cl = __import__("pyopencl")
        clmf = cl.mem_flags

        platforms = cl.get_platforms()
        assert(len(platforms) > 0), "Couldn't find any platforms! Driver installed?"
        platform = platforms[self.cl_platform]

        devices = platform.get_devices()
        assert(len(devices) > 0), "No devices in platform"
        device = devices[self.cl_device]
        # print("Using device {} on {}".format(device.name, platform.name))

        self._cl_context = cl.Context([device])
        self._cl_queue = cl.CommandQueue(self._cl_context)

        src = pkg_resources.resource_string(__name__, "flatspin_cl_kernels.c")
        src = src.decode("utf-8")

        self._cl_prg = cl.Program(self._cl_context, src).build(options=[])

        #preload some of the buffers.
        self._cl_spin_g = cl.Buffer(self._cl_context, clmf.READ_ONLY | clmf.COPY_HOST_PTR, hostbuf=self.spin)
        self._cl_res_g = cl.Buffer(self._cl_context, clmf.WRITE_ONLY,
                np.prod((self.spin_count, 2)) * np.dtype(np.float64).itemsize)
        self._cl_alpha_g = cl.Buffer(self._cl_context, clmf.READ_ONLY | clmf.COPY_HOST_PTR, hostbuf=np.float64(self.alpha))
        self._cl_h_ext_g = cl.Buffer(self._cl_context, clmf.READ_ONLY | clmf.COPY_HOST_PTR, hostbuf=self.h_ext)

        self._init_cl_geometry()

    def _init_cl_geometry(self):
        """ (Re-)initialize cl buffers that depend on geometry """
        global cl, clmf
        assert self.cl
        if not self._cl_context:
            # CL not yet initialized, nothing to do
            return

        if self.num_neighbors < 1:
            self._cl_neighbors_g = cl.Buffer(self._cl_context, clmf.READ_ONLY, size=1)
        else:
            self._cl_neighbors_g = cl.Buffer(self._cl_context, clmf.READ_ONLY | clmf.COPY_HOST_PTR, hostbuf=self._neighbor_list)
        self._cl_n_neighbors_g = cl.Buffer(self._cl_context, clmf.READ_ONLY | clmf.COPY_HOST_PTR, hostbuf=np.int32(self.num_neighbors))

        self._cl_m_g = cl.Buffer(self._cl_context, clmf.READ_ONLY | clmf.COPY_HOST_PTR, hostbuf=np.float64(self.m))
        # we are now ready to calculate h_dip cache on the GPU
        if self._h_dip_cache is None:
            self._h_dip_cache = self._init_h_dip_cl()

        self._cl_hdip_cache_g = cl.Buffer(self._cl_context, clmf.READ_ONLY | clmf.COPY_HOST_PTR, hostbuf=self._h_dip_cache)


    def _init_cuda(self):
        assert self.cuda
        if self._cuda_relax_kernel:
            return

        import pycuda.autoinit
        import pycuda
        from pycuda.compiler import DynamicSourceModule
        global cuda
        cuda = pycuda.driver

        # print("Initializing CUDA")
        src = pkg_resources.resource_string(__name__, "flatspin_cuda_kernels.cu")
        src = src.decode("utf-8")
        self.mod = DynamicSourceModule(src)
        self._cuda_relax_kernel = self.mod.get_function('relax').prepare("PPPPPPPPPPPdddddiiP").prepared_call

        self._cuda_spin = cuda.mem_alloc(self.spin_count * np.dtype('int8').itemsize)
        cuda.memcpy_htod(self._cuda_spin, self.spin)

        self._cuda_tmp_dip_field = cuda.mem_alloc(int(2 * self.spin_count * np.dtype('double').itemsize))
        self._cuda_tmp_ext_field = cuda.mem_alloc(int(2 * self.spin_count * np.dtype('double').itemsize))
        self._cuda_tmp_temp_field = cuda.mem_alloc(int(2 * self.spin_count * np.dtype('double').itemsize))

        #transfer 0's to the card
        cuda.memcpy_htod(self._cuda_tmp_temp_field, np.zeros((self.spin_count, 2), dtype=np.float64))

        self._cuda_h_ext = cuda.mem_alloc(self.h_ext.nbytes)
        cuda.memcpy_htod(self._cuda_h_ext, self.h_ext)

        self._cuda_threshold = cuda.mem_alloc(self.threshold.nbytes)
        cuda.memcpy_htod(self._cuda_threshold, self.threshold)

        self._cuda_num_steps = cuda.mem_alloc(4) #np.array([0], dtype=np.int32)

        self._cuda_tmp_switching_energies = cuda.mem_alloc(self.spin_count * np.dtype('double').itemsize)

        self._cuda_done = cuda.mem_alloc(np.dtype('int').itemsize)

        self._init_cuda_geometry()

    def _init_cuda_geometry(self):
        """ (Re-)initialize cuda buffers that depend on geometry """
        global cuda
        assert self.cuda
        if not self._cuda_relax_kernel:
            # CUDA not yet initialized, nothing to do
            return

        if self.num_neighbors < 1:
            self._cuda_neighbor_list = cuda.mem_alloc(1)
        else:
            self._cuda_neighbor_list = cuda.mem_alloc(self._neighbor_list.nbytes)
        cuda.memcpy_htod(self._cuda_neighbor_list, self._neighbor_list)

        self._cuda_m = cuda.mem_alloc(self.m.nbytes)
        cuda.memcpy_htod(self._cuda_m, self.m)

        if self._h_dip_cache is None:
            self._h_dip_cache = self._init_h_dip_cuda()

        self._cuda_h_dip_cache = cuda.mem_alloc(self._h_dip_cache.nbytes)
        cuda.memcpy_htod(self._cuda_h_dip_cache, self._h_dip_cache)

    def _total_fields_cl(self):
        self._init_cl()

        #this will calcualte for all indices
        #copy the updated data to the device
        #print(self.spin.shape)

        cl.enqueue_copy(self._cl_queue, self._cl_spin_g, self.spin)
        cl.enqueue_copy(self._cl_queue, self._cl_h_ext_g, self.h_ext)
        cl.enqueue_copy(self._cl_queue, self._cl_alpha_g, np.float64(self.alpha))

        self._cl_prg.total_fields(self._cl_queue, (self.spin_count,), None,
                self._cl_spin_g,
                self._cl_hdip_cache_g,
                self._cl_alpha_g,
                self._cl_res_g,
                self._cl_neighbors_g,
                self._cl_n_neighbors_g,
                self._cl_m_g,
                self._cl_h_ext_g
        )

        res = np.empty((self.spin_count, 2), dtype=np.float64)
        cl.enqueue_copy(self._cl_queue, res, self._cl_res_g)

        return res

    #Eh, it's just the two calls isolated anyway.
    def _total_fields_cuda(self):
        self._init_cuda()
        return self._h_dip_local_cuda() + self._external_fields_cuda()

    def _h_dip_local_cl(self):
        self._init_cl()

        #this will calcualte for all indices
        cl.enqueue_copy(self._cl_queue, self._cl_spin_g, self.spin)
        cl.enqueue_copy(self._cl_queue, self._cl_alpha_g, np.float64(self.alpha))


        self._cl_prg.test_h_dip_local(self._cl_queue, (self.spin_count,), None,
                self._cl_spin_g,
                self._cl_hdip_cache_g,
                self._cl_alpha_g,
                self._cl_res_g,
                self._cl_neighbors_g,
                self._cl_n_neighbors_g
        )

        res = np.empty((self.spin_count, 2), dtype=np.float64)
        cl.enqueue_copy(self._cl_queue, res, self._cl_res_g)

        return res

    def _external_fields_cl(self):
        self._init_cl()

        #this will calcualte for all indices
        spin_g = cl.Buffer(self._cl_context, clmf.READ_ONLY | clmf.COPY_HOST_PTR, hostbuf=self.spin)

        cl.enqueue_copy(self._cl_queue, self._cl_spin_g, self.spin)
        cl.enqueue_copy(self._cl_queue, self._cl_h_ext_g, self.h_ext)


        self._cl_prg.test_h_ext(self._cl_queue, (self.spin_count,), None,
                self._cl_spin_g,
                self._cl_m_g,
                self._cl_h_ext_g,
                self._cl_res_g,
        )

        res = np.empty((self.spin_count, 2), dtype=np.float64)
        cl.enqueue_copy(self._cl_queue, res, self._cl_res_g)

        return res

    def _external_fields_cuda(self):
        self._init_cuda()
        external_field_kernel = self.mod.get_function('external_field').prepare("PPPPi").prepared_call
        cuda.memcpy_htod(self._cuda_spin, self.spin)
        cuda.memcpy_htod(self._cuda_h_ext, self.h_ext)
        external_field_kernel(
                                (self.spin_count, 1),
                                (1,1,1),
                                self._cuda_spin,
                                self._cuda_m,
                                self._cuda_h_ext,
                                self._cuda_tmp_ext_field,
                                self.spin_count)

        res = np.zeros((self.spin_count, 2), dtype=np.float64)
        cuda.memcpy_dtoh(res, self._cuda_tmp_ext_field)
        return res


    def _h_dip_local_cuda(self):
        self._init_cuda()
        dipolar_field_kernel = self.mod.get_function('h_dip_local').prepare("PdPPiPi").prepared_call
        cuda.memcpy_htod(self._cuda_spin, self.spin)
        cuda.memcpy_htod(self._cuda_h_ext, self.h_ext)

        dipolar_field_kernel(
                                (self.spin_count, 1),
                                (1,1,1),
                                self._cuda_h_dip_cache,
                                self.alpha,
                                self._cuda_spin,
                                self._cuda_neighbor_list,
                                self.num_neighbors,
                                self._cuda_tmp_dip_field,
                                self.spin_count)

        res = np.zeros((self.spin_count, 2), dtype=np.float64)
        cuda.memcpy_dtoh(res, self._cuda_tmp_dip_field)
        return res


class IsingSpinIce(SpinIce):
    def __init__(self, *, spin_angle=90, **kwargs):
        self.spin_angle = spin_angle

        super().__init__(**kwargs)

    def _init_geometry(self):
        pos, angle = super()._init_geometry()

        angle[:] = np.deg2rad(self.spin_angle)

        return pos, angle


class SquareSpinIce(SpinIce):
    pass

class SquareSpinIceClosed(SquareSpinIce):
    def __init__(self, *, edge="symmetric", **kwargs):
        assert edge in ("symmetric", "asymmetric")
        self.edge = edge

        super().__init__(**kwargs)

    def _init_geometry(self):
        nx, ny = self.size
        sym = 1 if self.edge == "symmetric" else 0
        spin_count = (ny + sym) * nx + ny * (nx + sym)
        pos = np.zeros((spin_count, 2), dtype=float)
        angle = np.zeros(spin_count, dtype=float)

        labels = []

        a = self.lattice_spacing
        y = 0
        i = 0
        for row in range(0, 2 * ny + sym):
            is_vert = row % 2 # 1 for vert, 0 for horiz
            ncols = nx
            x = 0

            if is_vert:
                # vertical row
                ncols += sym
            else:
                # horizontal row
                x += a/2

            for col in range(0, ncols):
                if is_vert:
                    angle[i] = np.pi/2
                pos[i] = [x, y]

                label = (row, col)
                labels.append(label)

                x += a
                i += 1

            y += a / 2

        self.labels = np.array(labels)

        return pos, angle

    def _init_spin(self, init):
        if isinstance(init, str) and init == 'ground':
            for row, col in self.labels:
                i = self.L[row, col]
                if row % 4 == 0 and col % 2 == 1:
                    self.spin[i] = -1
                elif row % 4 == 2 and col % 2 == 0:
                    self.spin[i] = -1
                elif row % 4 == 1 and col % 2 == 0:
                    self.spin[i] = -1
                elif row % 4 == 3 and col % 2 == 1:
                    self.spin[i] = -1
        else:
            super()._init_spin(init)

    _vertex_size = (3, 3)

    @property
    def _default_cell_size(self):
        return (self.lattice_spacing/2, self.lattice_spacing/2)

class SquareSpinIceOpen(SquareSpinIce):
    def __init__(self, *, neighbor_distance=sqrt(2), **kwargs):
        kwargs['neighbor_distance'] = neighbor_distance

        super().__init__(**kwargs)

    def _init_geometry(self):
        pos, angle = super()._init_geometry()

        angle[:] = np.pi/4

        for i in range(len(pos)):
            row, col = self.labels[i]
            if row % 2 == 0 and col % 2 == 1:
                angle[i] += np.pi/2
            elif row % 2 == 1 and col % 2 == 0:
                angle[i] += np.pi/2

        return pos, angle

    _vertex_size = (2, 2)

class PinwheelSpinIceDiamond(SquareSpinIceClosed):
    def __init__(self, *, spin_angle=45, neighbor_distance=10, **kwargs):
        self.spin_angle = spin_angle
        kwargs['neighbor_distance'] = neighbor_distance

        super().__init__(**kwargs)

    def _init_geometry(self):
        pos, angle = super()._init_geometry()

        # rotate each island by spin_angle
        angle[:] -= np.deg2rad(self.spin_angle)

        return pos, angle

class PinwheelSpinIceLuckyKnot(SquareSpinIceOpen):
    def __init__(self, *, spin_angle=45, neighbor_distance=10*sqrt(2), **kwargs):
        self.spin_angle = spin_angle
        kwargs['neighbor_distance'] = neighbor_distance

        super().__init__(**kwargs)

    def _init_geometry(self):
        pos, angle = super()._init_geometry()

        # rotate each island by spin_angle
        angle[:] -= np.deg2rad(self.spin_angle)

        return pos, angle

class PinwheelSpinIceRandom(PinwheelSpinIceDiamond):
    def __init__(self, *, spin_angle_disorder=0, **kwargs):
        self.spin_angle_disorder = spin_angle_disorder

        super().__init__(**kwargs)

    def _init_geometry(self):
        pos, angle = super()._init_geometry()

        # rotate each island by spin_angle
        std = self.spin_angle_disorder
        angle[:] += np.deg2rad(self.rng.normal(0, std, angle.shape))

        return pos, angle

class KagomeSpinIce(SpinIce):
    def _init_geometry(self):
        labels = []

        nx, ny = self.size

        n_top_bot = (2 * nx * 2)
        n_mid = (2 * nx + 1) * (ny - 1)
        n_vert = (nx + 1) * ny
        spin_count = n_top_bot + n_mid + n_vert

        pos = np.zeros((spin_count, 2), dtype=float)
        angle = np.zeros(spin_count, dtype=float)

        n_rows = 2 * ny + 1
        last_row = n_rows - 1

        a = self.lattice_spacing
        y = 0
        i = 0
        for row in range(0, n_rows):
            if row % 2 == 0:
                # "horizontal" magnets (+/-30 degree)
                n_cols = 2 * nx + 1
                if row == 0 or row == last_row:
                    # first and last row has 1 less element
                    n_cols -= 1

                x = a/2
                col0 = 0
                if ny % 2 == 0 and row == last_row:
                    # even number of magnets, skip first magnet
                    x += a
                    col0 += 1

                for col in range(col0, col0 + n_cols):
                    pos[i] = [x, y]
                    angle[i] = np.deg2rad(30)
                    if row % 4 == 0 and col % 2 == 0:
                        angle[i] *= -1
                    if row % 4 == 2 and col % 2 == 1:
                        angle[i] *= -1

                    label = (row, col)
                    labels.append(label)

                    x += a
                    i += 1
            else:
                # vertical magnets (90 degrees)
                n_cols = nx + 1
                x = 0
                if row % 4 == 3:
                    x += a
                for col in range(0, n_cols):
                    pos[i] = [x, y]
                    angle[i] = np.deg2rad(90)

                    label = (row, col)
                    labels.append(label)

                    x += 2 * a
                    i += 1

            y += a * sqrt(3) / 2

        self.labels = np.array(labels)

        return pos, angle

    _vertex_size = (2,3)

    @property
    def _default_cell_size(self):
        sizex = self.lattice_spacing/2
        sizey = sqrt(3)*self.lattice_spacing/2
        return (sizex, sizey)

    def _init_spin(self, init):
        if isinstance(init, str) and init == 'ground':
            for row, col in self.labels:
                i = self.L[row, col]
                if row % 4 == 0 and(col-1)%6 < 3:
                    self.spin[i] = -1
                elif row % 4 == 2 and (col-1)%6 >=3:
                    self.spin[i] = -1
                elif row % 4 == 1 and col % 3 == 2:
                    self.spin[i] = -1
                elif row % 4 == 3 and col % 3 == 0:
                    self.spin[i] = -1

        else:
            super()._init_spin(init)

class KagomeSpinIceRotated(SpinIce):
    def _init_geometry(self):
        labels = []

        nx, ny = self.size

        n_top_bot = (2 * nx * 2)
        n_mid = (2 * nx + 1) * (ny - 1)
        n_vert = (nx + 1) * ny
        spin_count = n_top_bot + n_mid + n_vert

        pos = np.zeros((spin_count, 2), dtype=float)
        angle = np.zeros(spin_count, dtype=float)

        n_cols = 2 * nx + 1
        last_col = n_cols - 1

        a = self.lattice_spacing
        x = 0
        i = 0
        for col in range(0, n_cols):
            if col % 2 == 0:
                # "horizontal" magnets (+/-30 degree)
                n_rows = 2 * ny + 1
                if col == 0 or col == last_col:
                    # first and last col has 1 less element
                    n_rows -= 1

                y = a/2
                row0 = 0
                if nx % 2 == 0 and col == last_col:
                    # even number of magnets, skip first magnet
                    y += a
                    row0 += 1

                for row in range(row0, row0 + n_rows):
                    pos[i] = [x, y]
                    angle[i] = np.deg2rad(60)
                    if col % 4 == 0 and row % 2 == 0:
                        angle[i] *= -1
                    if col % 4 == 2 and row % 2 == 1:
                        angle[i] *= -1

                    label = (col, row)
                    labels.append(label)

                    y += a
                    i += 1
            else:
                # vertical magnets (90 degrees)
                n_rows = ny + 1
                y = 0
                if col % 4 == 3:
                    y += a
                for row in range(0, n_rows):
                    pos[i] = [x, y]
                    angle[i] = np.deg2rad(0)

                    label = (col, row)
                    labels.append(label)

                    y += 2 * a
                    i += 1

            x += a * sqrt(3) / 2

        self.labels = np.array(labels)

        return pos, angle

    _vertex_size = (3,2)

    @property
    def _default_cell_size(self):
        sizex = sqrt(3)*self.lattice_spacing/2
        sizey = self.lattice_spacing/2
        return (sizex, sizey)

    def _init_spin(self, init):
        if isinstance(init, str) and init == 'ground':
            for col, row in self.labels:
                i = self.L[col, row]
                if col % 2 == 0 and row % 3 == 2:
                    self.spin[i] = -1
                elif col % 4 == 1 and row % 3 != 2:
                    self.spin[i] = -1
                elif col % 4 == 3 and row % 3 != 0:
                    self.spin[i] = -1

        else:
            super()._init_spin(init)

class CustomSpinIce(SpinIce):
    def __init__(self, *, magnet_coords=[[1,1],[1,2]], magnet_angles=[0,90],
                 radians=False, coords_as_labels=False, labels=None, **kwargs):
        # load values from file
        if isinstance(magnet_coords, str):
            magnet_coords = np.array(read_table(magnet_coords))
        if isinstance(magnet_angles, str):
            magnet_angles = np.array(read_table(magnet_angles))
        if isinstance(labels, str):
            labels = np.array(read_table(labels))

        self.magnet_coords = magnet_coords
        if radians:
            self.magnet_angles = magnet_angles
        else:
            self.magnet_angles = np.deg2rad(magnet_angles)

        self.coords_as_labels = coords_as_labels
        self.custom_labels = labels

        super().__init__(**kwargs)

    def _init_geometry(self):
        pos = np.array(self.magnet_coords, dtype=float)
        angle = np.atleast_1d(np.array(self.magnet_angles, dtype=float).squeeze())

        assert pos.ndim == 2
        assert angle.ndim == 1
        assert pos.shape[0] == angle.shape[0], "unequal number of coordinates and angles"
        assert len(np.unique(pos,axis=0)) == len(pos), "magnet coordinates cannot be repeated"

        pos *= self.lattice_spacing

        if self.coords_as_labels:
            self.labels = self.magnet_coords.copy()
        else:
            self.labels = self.custom_labels

        return pos, angle

class LatticeSpinIce(SpinIce):
    def __init__(self, *, basis0=(1,0), basis1=(0,1), const_angle=0, radians=False, **kwargs):
        self.basis0 = basis0
        self.basis1 = basis1

        if not radians:
            const_angle = np.deg2rad(const_angle)
        self.const_angle = const_angle

        super().__init__(**kwargs)

    def _init_geometry(self):
        b0 = np.array(self.basis0)
        b1 = np.array(self.basis1)

        grid = np.array(np.meshgrid(np.arange(self.size[1]), np.arange(self.size[0]))).T.reshape(-1, 2)
        grid = np.fliplr(grid) #flip x and y so labels will be (row, col) or (b0, b1)
        pos = np.dot(grid, np.array([b0, b1]))
        angle = np.full(len(pos), self.const_angle)
        self.labels = grid

        pos = pos * self.lattice_spacing
        return pos, angle

    def set_basis(self, basis0=None, basis1=None):
        if basis0 is not None:
            self.basis0 = basis0
        if basis1 is not None:
            self.basis1 = basis1

        b0 = self.basis0
        b1 = self.basis1

        grid = self.labels
        pos = np.dot(grid, np.array([b0, b1]))
        pos = pos * self.lattice_spacing

        self.set_pos(pos)

class TileLatticeSpinIce(LatticeSpinIce):
    def __init__(self, *, angle_tile=((90,0),(0,90)), hole_tile=None, radians=False, **kwargs):
        if not radians:
            angle_tile = np.deg2rad(angle_tile)
        self.angle_tile = np.atleast_2d(angle_tile).T

        if hole_tile is not None:
            hole_tile = np.atleast_2d(hole_tile).T
            assert np.any(hole_tile), "Your hole_tile is all holes and no magnets!"
        self.hole_tile = hole_tile
        super().__init__(radians=radians, **kwargs)

    def _init_geometry(self):
        pos, angle = super()._init_geometry()

        if self.hole_tile is not None:
            grid = self.labels
            m, n = self.hole_tile.shape
            holes = self.hole_tile[np.mod(grid[:, 0], m), np.mod(grid[:, 1], n)]
            not_holes = np.nonzero(holes)
            pos = pos[not_holes]
            angle = angle[not_holes]
            self.labels = self.labels[not_holes]

        if self.angle_tile is not None:
            grid = self.labels
            m, n = self.angle_tile.shape
            angle = self.angle_tile[np.mod(grid[:, 0], m), np.mod(grid[:, 1], n)]

        return pos, angle

    def set_angle_tile(self, angle_tile, radians=True):
        grid = self.labels

        if angle_tile is not None:
            if not radians:
                angle_tile = np.deg2rad(angle_tile)
            self.angle_tile = np.atleast_2d(angle_tile).T
            m, n = self.angle_tile.shape
            angle = self.angle_tile[np.mod(grid[:, 0], m), np.mod(grid[:, 1], n)]
        else:
            self.angle_tile = angle_tile
            angle = np.full(self.spin_count, self.const_angle)

        self.set_angle(angle)
