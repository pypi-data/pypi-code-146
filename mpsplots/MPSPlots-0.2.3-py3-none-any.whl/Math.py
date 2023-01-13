import numpy
from scipy import ndimage

from MPSPlots.Utils import ToList


class Angle(object):
    def __init__(self, input, Unit='degree'):
        input = ToList(input)

        if Unit.lower() == 'degree':
            self.Degree = [i if i is not None else numpy.nan for i in input]
            self.Radian = [numpy.deg2rad(i) if i is not None else numpy.nan for i in input]

        if Unit.lower() == 'radian':
            self.Radian = [i if i is not None else numpy.nan for i in input]
            self.Degree = [numpy.rad2deg(i) if i is not None else numpy.nan for i in input]

        if len(self.Degree) == 1:
            self.Degree = [self.Degree[0]]
            self.Radian = [self.Radian[0]]


def Deg2Rad(Value):
    if Value is None:
        return numpy.nan
    else:
        return numpy.deg2rad(Value)


def Norm(Scalar):
    return numpy.sqrt(numpy.sum(numpy.abs(Scalar)**2))


def Normalize(Scalar):
    norm = Norm(Scalar)
    if norm == 0 or numpy.isnan(norm):
        return [0, 0, 0]
    else:
        return Scalar / norm


def InterpFull(Meshes, Scalar, Shape):

    phi, theta = numpy.mgrid[-numpy.pi / 2:numpy.pi / 2:complex(Shape[0]),
                          -numpy.pi:numpy.pi:complex(Shape[1])]

    Scalar = interp_at(Meshes.phi.Radian,
                       Meshes.theta.Radian,
                       Scalar.astype(numpy.complex).flatten(),
                       phi.flatten(),
                       theta.flatten(),
                       algorithm='linear',
                       extrapolate=True)

    return Scalar.reshape(Shape), phi, theta


def RescaleComplex(Input, Num):
    Scale = Num/Input.shape[0]
    InputReal = ndimage.interpolation.zoom(input=Input.real, zoom=(Scale), order=2)
    InputImag = ndimage.interpolation.zoom(input=Input.imag, zoom=(Scale), order=2)
    return InputReal + 1j * InputImag


def RotateComplex(Input, Rotation):
    InputReal = ndimage.rotate(Input.real, Rotation, reshape=False)
    InputImag = ndimage.rotate(Input.imag, Rotation, reshape=False)
    return InputReal + 1j * InputImag


def angle_space_to_direct(angle_space: numpy.ndarray, k: float,) -> numpy.ndarray:

    RadSpace = numpy.deg2rad(angle_space)

    fourier_space = numpy.sin(RadSpace) * k / (2 * numpy.pi)

    fourier_unit = numpy.abs(fourier_space[1] - fourier_space[0])

    DirectSpace = numpy.fft.fftshift(numpy.fft.fftfreq(angle_space.shape[0], d=fourier_unit))

    return DirectSpace


def direct_space_to_angle(direct_space: numpy.ndarray, k: float) -> numpy.ndarray:

    direct_unit = numpy.abs(direct_space[1] - direct_space[0])

    fourier_space = numpy.fft.fftshift(numpy.fft.fftfreq(direct_space.shape[0], d=direct_unit))

    angle_space = numpy.arcsin(2 * numpy.pi * fourier_space / k) # conversion spatial frequency to angular space

    if numpy.isnan(angle_space).any():
        raise Exception("Magnification too large.")

    return angle_space * 180 / numpy.pi


def NA_to_angle(NA: float) -> numpy.ndarray:
    if NA <= 1.0:
        return numpy.arcsin(NA)
    if NA >= 1.0:
        return numpy.arcsin(NA - 1) + numpy.pi / 2


def direct_space_to_spherical(x, y, max_angle):
    z = (x * 0.) + 50 / numpy.tan(max_angle)

    _, phi, theta = cartesian_to_spherical(x, y, z)

    return phi, theta


def angle_unit_to_direct_unit(angle, k):
    fourier_space = numpy.sin(angle) * k / (2 * numpy.pi)

    fourier_unit = numpy.abs(fourier_space[1] - fourier_space[0])

    DirectSpace = numpy.fft.fftshift(numpy.fft.fftfreq(angle.shape[0], d=fourier_unit))

    return DirectSpace


def cartesian_to_spherical(x, y, z):
    x = numpy.asarray(x)
    y = numpy.asarray(y)
    z = numpy.asarray(z)

    r = numpy.sqrt(x**2 + y**2 + z**2)
    phi = numpy.arcsin(z / r)
    theta = numpy.arctan2(y, x)
    return r, phi, theta


def spherical_to_cartesian(phi, theta, r=None):
    phi = numpy.asarray(phi)
    theta = numpy.asarray(theta)
    r = r if r is not None else numpy.ones(phi.shape)

    x = r * numpy.cos(phi) * numpy.cos(theta)
    y = r * numpy.cos(phi) * numpy.sin(theta)
    z = r * numpy.sin(phi)
    return x, y, z


def rotate_on_y(phi: numpy.ndarray, theta: numpy.ndarray, angle: float):
    x, y, z = spherical_to_cartesian(phi=phi, theta=theta)

    xp = x * numpy.cos(angle) + z * numpy.sin(angle)
    yp = y
    zp = z * numpy.cos(angle) - x * numpy.sin(angle)
    return cartesian_to_spherical(x=xp, y=yp, z=zp)


def rotate_on_z(phi: numpy.ndarray, theta: numpy.ndarray, angle: float):
    x, y, z = spherical_to_cartesian(phi=phi, theta=theta)

    xp = x * numpy.cos(angle) - y * numpy.sin(angle)
    yp = x * numpy.sin(angle) + y * numpy.cos(angle)
    zp = z
    return cartesian_to_spherical(x=xp, y=yp, z=zp)


def rotate_on_x(phi: numpy.ndarray, theta: numpy.ndarray, angle: float):
    x, y, z = spherical_to_cartesian(phi=phi, theta=theta)

    xp = x
    yp = y * numpy.cos(angle) - z * numpy.sin(angle)
    zp = y * numpy.sin(angle) + z * numpy.cos(angle)
    return cartesian_to_spherical(x=xp, y=yp, z=zp)


def get_spherical_mesh(sampling, max_angle):

    x, y = numpy.mgrid[-50: 50: complex(sampling), -50: 50: complex(sampling)]
    z = 50 / numpy.tan(max_angle)
    _, theta, phi = cartesian_to_spherical(x, y, x * 0 + z)

    return phi, theta


def angle2Jones(Delta):
    val = numpy.exp(1j * Delta) * 2
    JonesVector = numpy.array([1, val])
    Norm = (numpy.sqrt(1 + numpy.abs(val)**2))
    return JonesVector / Norm


def cart2sp(x, y, z):
    """Converts data from cartesian coordinates into spherical.

    Args:
        x (scalar or array_like): X-component of data.
        y (scalar or array_like): Y-component of data.
        z (scalar or array_like): Z-component of data.

    Returns:
        Tuple (r, theta, phi) of data in spherical coordinates.
    """
    x = numpy.asarray(x)
    y = numpy.asarray(y)
    z = numpy.asarray(z)
    scalar_input = False
    if x.ndim == 0 and y.ndim == 0 and z.ndim == 0:
        x = x[None]
        y = y[None]
        z = z[None]
        scalar_input = True
    r = numpy.sqrt(x**2 + y**2 + z**2)
    theta = numpy.arcsin(z / r)
    phi = numpy.arctan2(y, x)
    if scalar_input:
        return (r.squeeze(), theta.squeeze(), phi.squeeze())
    return (r, theta, phi)


def sp2cart(r, theta, phi):
    """Converts data in spherical coordinates into cartesian.

    Args:
        r (scalar or array_like): R-component of data.
        theta (scalar or array_like): theta-component of data.
        phi (scalar or array_like): phi-component of data.

    Returns:
        Tuple (x, y, z) of data in cartesian coordinates.
    """
    r = numpy.asarray(r)
    theta = numpy.asarray(theta)
    phi = numpy.asarray(phi)
    scalar_input = False
    if r.ndim == 0 and theta.ndim == 0 and phi.ndim == 0:
        r = r[None]
        theta = theta[None]
        phi = phi[None]
        scalar_input = True
    x = r * numpy.cos(theta) * numpy.cos(phi)
    y = r * numpy.cos(theta) * numpy.sin(phi)
    z = r * numpy.sin(theta)
    if scalar_input:
        return (x.squeeze(), y.squeeze(), z.squeeze())
    return (x, y, z)


def cart2cyl(x, y, z):
    """Converts data in cartesian coordinates into cylyndrical.

    Args:
        x (scalar or array_like): X-component of data.
        y (scalar or array_like): Y-component of data.
        z (scalar or array_like): Z-component of data.

    Returns:
        Tuple (r, phi, z) of data in cylindrical coordinates.
    """
    x = numpy.asarray(x)
    y = numpy.asarray(y)
    z = numpy.asarray(z)
    scalar_input = False
    if x.ndim == 0 and y.ndim == 0 and z.ndim == 0:
        x = x[None]
        y = y[None]
        z = z[None]
        scalar_input = True
    r = numpy.sqrt(x**2 + y**2)
    phi = numpy.arctan2(y, x)
    if scalar_input:
        return (r.squeeze(), phi.squeeze(), z.squeeze())
    return (r, phi, z)


def cyl2cart(r, phi, z):
    """Converts data in cylindrical coordinates into cartesian.

    Args:
        r (scalar or array_like): R-component of data.
        phi (scalar or array_like): phi-component of data.
        z (scalar or array_like): Z-component of data.

    Returns:
        Tuple (x, y, z) of data in cartesian coordinates.
    """
    r = numpy.asarray(r)
    phi = numpy.asarray(phi)
    z = numpy.asarray(z)
    scalar_input = False
    if r.ndim == 0 and phi.ndim == 0 and z.ndim == 0:
        r = r[None]
        phi = phi[None]
        z = z[None]
        scalar_input = True
    x = r * numpy.cos(phi)
    y = r * numpy.sin(phi)
    if scalar_input:
        return (x.squeeze(), y.squeeze(), z.squeeze())
    return (x, y, z)


# -
