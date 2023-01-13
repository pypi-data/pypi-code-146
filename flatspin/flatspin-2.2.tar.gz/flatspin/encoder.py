"""
Input encoding
"""
import inspect
import numpy as np
import scipy.signal as signal
import copy

from .utils import get_default_kwargs

"""
Shapes of signals

(time,) -> (time, 1)
1D arrays are 1D signals

(time, D)
2D arrays are D-dimensional signals
With D=2 we have a vector signal

(time, H, W)
3D arrays are signals on a WxH grid

(time, H, W, D)
4D arrays are D-dimensional signals on a WxH grid
With D=2 we have a vector signal on a grid

In general signals can take any shape as part of the encoding process.
However, the last step must produce an output of either
(time, 2): a global vector signal
(time, H, W, 2): a local vector signal on a grid

"""

class Encoder:
    """
    Encoder base class

    An encoder translates logical input to an external field protocol.

    Input takes the form of arrays of shape (n_inputs, input_dim).
    1D input arrays may be used as a shorthand for (n_inputs, 1)

    The encoding process consists of one or more steps, where the output of one
    step is input to the next step:

    input -> step1 -> step2 -> ... -> h_ext

    In general, signals can take any shape as part of the encoding process.
    However, the last step must produce an output of either
    (time, 2): a global vector signal
    (time, H, W, 2): a local vector signal on a grid

    Each step is a simple function with optional parameters, e.g.:

    def step(input, param1=default1, param2=default2):
        ...

    The Encoder will inspect the signature of each step to discover the
    available parameters.  The parameters can then be set during encoder
    initialization, or afterwards via `set_params`. Note that parameter names
    may overlap, in which case all matching parameters will be set to the same
    value. """

    """ List of encoder steps. Subclasses must specify this list of steps. """
    steps = None

    def __init__(self, **params):
        self.params = [self._get_default_params(s) for s in self.steps]
        self.set_params(**params)

    def encode(self, input):
        """ Encode input as an external field

        Parameters
        ----------
        input : array_like
            Input shape should be (n_inputs, input_dim).
            1D input arrays may be used as a shorthand for (n_inputs, 1).

        Returns
        -------
        h_ext : ndarray
            The returned array is either:
            1. A global time-dependent field: ``h_ext.shape = (time, 2)``
            2. A spatial time-dependent field: ``h_ext.shape = (time, height, width, 2)``
        """
        input = check_input(input)
        #print(f'input {input.shape}', end=' ')
        for step, params in zip(self.steps, self.params):
            input = step(input, **params)
            #print(f'-> {step.__name__}({params})', end=' ')
            #print(f'-> {input.shape}', end=' ')
            #print(f'-> {input}', end=' ')
        #print('')
        return input

    def __call__(self, input):
        return self.encode(input)

    @classmethod
    def _get_default_params(cls, step):
        return dict(get_default_kwargs(step))

    @classmethod
    def get_default_params(cls):
        params = {}
        for s in cls.steps:
            params.update(cls._get_default_params(s))
        return params

    def get_params(self):
        """ Get available encoder parameters """
        params = {}
        for p in self.params:
            params.update(p)
        return params

    def set_param(self, name, value):
        """ Set encoder parameter name=value """
        for param in self.params:
            if name in param:
                param[name] = value

    def set_params(self, **params):
        """ Set encoder parameters """
        for k, v in params.items():
            self.set_param(k, v)

    def __repr__(self):
        params = {}
        for p in self.params:
            params.update(p)
        params = ", ".join(f"{k}={v}" for k,v in params.items())
        return f"{self.__class__.__name__}({params})"

#
# Encoder steps
#
def expand_dims(input):
    """ Ensure last dimension of input is single-dimensional """
    if input.shape[-1] != 1:
        return np.expand_dims(input, -1)
    return input

def check_input(input):
    input = np.array(input)
    if len(input.shape) == 1:
        return np.expand_dims(input, -1)
    return input

def scale(input, H0=0, H=1):
    """ Scale input to range [H0, H] """
    return H0 + input * (H - H0)

def multiply(input, H=1):
    """ Multiply input by H """
    return H * input

def angle(input, phi0=0, phi=360):
    """ Map input to angle in range [phi0, phi] -> vector components """
    input = check_input(input)
    theta0 = np.deg2rad(phi0)
    theta = np.deg2rad(phi)
    angles = theta0 + input * (theta - theta0)
    # add one dimension for vector
    out = expand_dims(angles)
    out = np.repeat(out, 2, axis=-1)
    out[...,0] = np.cos(out[...,0])
    out[...,1] = np.sin(out[...,1])
    return out

def angle_grid(input, phi0=0, phi=360, grid=None):
    """ Convenience function to offset all angles based on grid """
    input = expand_dims(check_input(input))
    if grid is not None:
        grid = np.atleast_2d(grid)
        phi0 = grid + phi0
        phi = phi0 + phi
    return angle(input, phi0, phi)

def sw(input, rotation=0):
    """ Multiply input vectors by SW astroid """
    input = check_input(input)
    angles = np.arctan2(input[...,1], input[...,0])
    angles = angles - np.deg2rad(rotation)

    Hs = (np.abs(np.sin(angles))**(2/3) + np.abs(np.cos(angles))**(2/3))**(-3/2)
    Hs.shape += (1,)

    return Hs * input

def broadcast_waveform(input, waveform):
    """ Broadcast waveform over input """
    input = check_input(input)
    # multiply input by waveform (broadcasting rules apply)
    out = input * waveform
    # roll last axis to the first (time)
    out = np.moveaxis(out, -1, 1)
    # finally concatenate it
    out = np.concatenate(out)
    return out

def repeat(input, timesteps=1):
    """ Repeat input a number of timesteps """
    return np.repeat(input, timesteps, axis=0)

def sin(input, timesteps=100, phase=0):
    """ Multiply input by sine wave """
    ph = np.deg2rad(phase)
    t = np.linspace(ph, 2 * np.pi + ph, timesteps, endpoint=False)
    waveform = np.sin(t)
    return broadcast_waveform(input, waveform)

def triangle(input, timesteps=100, phase=90):
    """ Multiply input by triangle wave """
    ph = np.deg2rad(phase)
    t = np.linspace(ph, 2 * np.pi + ph, timesteps, endpoint=False)
    waveform = signal.sawtooth(t, 0.5)
    return broadcast_waveform(input, waveform)

def rotate(input, timesteps=100, phase=0):
    """ Multiply input by rotation vector """
    ph = np.deg2rad(phase)
    t = np.linspace(ph, 2 * np.pi + ph, timesteps, endpoint=False)
    cos = broadcast_waveform(input, np.cos(t))
    sin = broadcast_waveform(input, np.sin(t))
    return np.stack([cos, sin], axis=-1)

def ppm(input, pos0=0, pos=1.0, timesteps=100):
    """ Pulse position modulation """
    input = check_input(input)

    # output shape
    shape = input.shape[:-1] if input.shape[-1] == 1 else input.shape
    shape = shape + (timesteps,)

    # calculate location of pulses
    pulse_inds = scale(input, pos0 * timesteps, pos * (timesteps-1)).round().astype(int)
    inds = tuple(np.array(list(np.ndindex(shape[:-1]))).T)
    inds += (pulse_inds.flatten(),)

    # make the pulses
    out = signal.unit_impulse(shape, inds)

    return out

def fixed_vector(input, phi=0):
    """ Convert scalar input to vectors at some angle phi """
    input = check_input(input)
    theta = np.deg2rad(phi)
    # add one dimension to broadcast vector
    input = expand_dims(input)
    vector = [np.cos(theta), np.sin(theta)]
    out = input * vector
    return out

def rotate_vector(input, phi=0):
    """ Rotate vector input by some angle phi """
    input = check_input(input)
    input_shape = input.shape
    theta = np.deg2rad(phi)
    rotation_matrix = np.array(
        [[np.cos(theta), -np.sin(theta)],
         [np.sin(theta),  np.cos(theta)]])
    input = input.reshape((-1,2)).T
    out = np.dot(rotation_matrix, input).T
    out = out.reshape(input_shape)
    return out

def ensure2d(input, fill=1.0):
    """ Convert scalar input to vectors """
    input = check_input(input)
    if input.shape[-1] == 1:
        input = np.column_stack([input, np.full(len(input), fill)])
    return input

# TODO: what's the point of grid_size? Wouldn't it always result in an
# effectively global field?
def grid(input, grid_size=(3,3), grid=None):
    """ Encode input onto grid

    Parameters
    ----------
    grid_size : tuple
        Create grid of fixed size (uniform weights)
        Ignored if grid is set
    grid : array
        Create grid of given size (non-uniform weights)
    """
    if grid is None:
        w, h = grid_size
        grid = np.ones((h, w))
    else:
        grid = np.atleast_2d(grid)

    input = check_input(input)

    # add dimensions to broadcast the grid
    shape = input.shape[:-1] if input.shape[-1] == 1 else input.shape
    input = input.reshape(shape + (1,) * grid.ndim)

    # broadcast the grid on each feature
    out = grid * input

    # now we have:
    # out.shape = (time,) + input.shape + grid.shape
    # shift axes to the end until we have the desired:
    # out.shape = (time,) + grid.shape + input.shape
    for i in range(out.ndim - grid.ndim - 1):
        out = np.moveaxis(out, 1, -1)

    return out

def onehot(input, nbits=2):
    input = check_input(input)

    # roll bit string 00..01 according to input
    out = np.zeros(input.shape + (nbits,))
    out[...,0] = 1
    for i, v in np.ndenumerate(input.astype(int)):
        out[i] = np.roll(out[i], v)

    # roll last axis to the first (time)
    out = np.moveaxis(out, -1, 1)

    # finally concatenate it
    out = np.concatenate(out)

    if input.shape[-1] == 1:
        return out.reshape(out.shape[:-1])
    return out


#
# Encoder definitions
#
class Constant(Encoder):
    """Encode input as the magnitude of a global field.

    Each field value is repeated `timesteps` times.
    The magnitude is scaled between `H0` and `H`.
    The field has a fixed angle `phi`."""

    steps = (repeat, scale, fixed_vector)

class Direct(Encoder):
    """Encode input directly as a global field.

    Note: input should already be in vector form.

    The input vectors are multiplied by `H`.
    """
    steps = (multiply,)

class Angle(Encoder):
    """Encode input as the angle of a global field.

    The angle is scaled between `phi0` and `phi`.
    The field has a fixed magnitude `H`."""

    steps = (angle, multiply)

class Sine(Encoder):
    """Encode input as the amplitude of a sinusoidal global field.

    The amplitude is scaled between `H0` and `H`.
    The field has a fixed angle of `phi` degrees.
    The sine wave has a resolution `timesteps` samples.
    The sine wave has a phase of `phase` degrees.
    """

    steps = (scale, sin, fixed_vector)

class Triangle(Encoder):
    """Encode input as the amplitude of a triangle wave global field.

    The amplitude is scaled between `H0` and `H`.
    The field has a fixed angle of `phi` degrees.
    The triangle wave has a resolution `timesteps` samples.
    The triangle wave has a phase of `phase` degrees.
    """

    steps = (scale, triangle, fixed_vector)

class Rotate(Encoder):
    """Encode input as the amplitude of a rotating global field.

    The amplitude is scaled between `H0` and `H`.
    The rotating field has a resolution `timesteps` samples.
    The rotating field has a phase of `phase` degrees.
    """

    steps = (scale, rotate)

class AngleSine(Encoder):
    """Encode input as the angle of a sinusoidal global field.

    The angle is scaled between `phi0` and `phi`.
    The field has a fixed amplitude `H`.
    The sine wave has a resolution `timesteps` samples.
    The sine wave has a phase of `phase` degrees.
    """

    steps = (angle, expand_dims, sin, multiply)

class AngleTriangle(Encoder):
    """Encode input as the angle of a triangle wave global field.

    The angle is scaled between `phi0` and `phi`.
    The field has a fixed amplitude `H`.
    The triangle wave has a resolution `timesteps` samples.
    The triangle wave has a phase of `phase` degrees.
    """

    steps = (angle, expand_dims, triangle, multiply)

class RotatePulse(Encoder):
    """Encode input as pulses along a rotating global field.

    Each input value is encoded as a pulse in a pulse train of `timesteps`
    samples. The position of the pulse will be between `pos0` and `pos`, where
    0 denotes the beginning of the pulse train and 1 denotes the end.
    The rotating field with have a base magnitude of `H0` and `H` when there is
    a pulse."""

    steps = (ppm, scale, rotate)

class Triangle2D(Encoder):
    """TODO: Please document me"""
    steps = (scale, ensure2d, triangle, rotate_vector)

class OneHot(Encoder):
    """TODO: Please document me"""
    steps = (onehot, scale, triangle, fixed_vector)

class ConstantGrid(Encoder):
    """Encode input as the magnitude of local fields on a grid.

    Each field value is repeated `timesteps` times.

    The grid is defined by `grid`, a 2D array whose values define the weights
    of the input for each grid cell. For example:

    grid = [[0, .5, 0],
            [.5, 1, .5],
            [0, .5, 0]]

    results in a 3x3 grid where the input is applied:
    * unmodified in the center cell (multiplied by 1)
    * halved in the edge cells (multiplied by 0.5)
    * discarded for the corner cells (multiplied by 0)

    After the input has been scaled by the grid weights, it is scaled to the
    range `H0` and `H`. Hence the magnitude of the field in a given cell is
    given by:

    h_ext[i,j] = H0 + grid[i,j] * input * (H - H0)

    For the above example grid, the field:
    * in the center cell will have magnitude H0 + 1 * input * (H - H0)
    * in the edge cells will have magnitude H0 + 0.5 * input * (H - H0)
    * in the corners will have a constant magnitude H0 (regardless of the input)

    Finally, the fields will have a fixed angle `phi`."""

    steps = (repeat, grid, scale, fixed_vector)

class SineGrid(Encoder):
    """Encode input as the amplitude of sinusoidal local fields on a grid.

    The parameters `grid`, `H0`, `H` and `phi` are the same as for `ConstantGrid`.
    The sine wave has a resolution `timesteps` samples and a phase of `phase`
    degrees.
    """
    steps = (grid, scale, expand_dims, sin, fixed_vector)

class TriangleGrid(Encoder):
    """Encode input as the amplitude of a triangle wave local fields on a grid.

    The parameters `grid`, `H0`, `H` and `phi` are the same as for `ConstantGrid`.
    The triangle wave has a resolution `timesteps` samples and a phase of
    `phase` degrees.
    """
    steps = (grid, scale, expand_dims, triangle, fixed_vector)

class AngleSineGrid(Encoder):
    """Encode input as the angle of sinusoidal local fields on a grid.

    The parameters `grid` and `H` are the same as for `ConstantGrid`.
    The grid weights scale the *amplitude* of the sine wave in each
    cell (angle is unaffected).

    The angle is scaled between `phi0` and `phi`.
    The sine wave has a resolution `timesteps` samples and a phase of `phase`
    degrees.
    """
    steps = (angle, expand_dims, sin, multiply, grid) # grid determines H

class AngleGridSine(Encoder):
    """Encode input as the angle of sinusoidal local fields on a grid.

    The parameters `grid` and `H` are the same as for `ConstantGrid`.
    The grid weights are used to offset the angle of each cell.
    The angle is scaled between `phi0` and `phi`.
    The field has a fixed amplitude `H`.
    The sine wave has a resolution `timesteps` samples.
    The sine wave has a phase of `phase` degrees.
    """
    steps = (angle_grid, expand_dims, sin, multiply) # grid adds angle offset

class RotatePulseGrid(Encoder):
    """Encode input as pulses along a rotating field """
    steps = (ppm, grid, scale, rotate)

'''
# TODO: Remove? Or generalize to ASW?
'sw-angle': Encoder(angle, sw, scale),
'sw-rotate': Encoder(scale, rotate, sw),
'sw-pulse': Encoder(ppm, scale, rotate, sw),
'sw-pulse-grid': Encoder(ppm, grid, scale, rotate, sw),
'''
