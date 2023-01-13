import numpy as np
from numpy.linalg import norm
import pytest
from .utils import approx

from flatspin import IsingSpinIce
from numpy.testing import assert_array_equal, assert_allclose

def ASW(h_par, h_perp, b=1, beta=3, c=1, gamma=3):
    sw = b*(1 - ((h_perp/c)**2)**(1/beta))**(gamma/2)
    sw[h_par<0] *= -1
    return sw

def test_init_no_temp(opencl):
    si = IsingSpinIce(temperature=0, **opencl)

    assert si.h_therm.shape == (si.spin_count, 2)
    assert si.h_therm == approx(0)

    tf = si.thermal_fields()
    assert tf.shape == (si.spin_count, 2)
    assert tf == approx(0)

def test_init_temp(opencl):
    si = IsingSpinIce(temperature=100, **opencl)

    assert si.h_therm.shape == (si.spin_count, 2)
    assert not si.h_therm == approx(0)

    tf = si.thermal_fields()
    assert tf.shape == (si.spin_count, 2)
    assert not tf == approx(0)

    # thermal_fields is in local per-spin reference, while h_therm is global
    assert np.all(tf != si.h_therm)

def test_flip(opencl):
    si = IsingSpinIce(temperature=100, **opencl)

    h_therm1 = si.h_therm.copy()
    tf1 = si.thermal_fields()

    si.flip(0)

    # h_therm unchanged
    assert_array_equal(si.h_therm, h_therm1)

    # thermal_fields for spin 0 should have flipped
    tf1[0] *= -1
    assert_array_equal(si.thermal_fields(), tf1)

def test_relax(opencl):
    si = IsingSpinIce(temperature=300, **opencl)
    tf1 = si.thermal_fields()
    si.relax()

    # relax() updates thermal fields
    assert si.thermal_fields() != approx(tf1)


def test_set_temperature(opencl):
    si = IsingSpinIce(alpha=0,
            hc=0.02, sw_b=1, sw_c=1, sw_beta=3, sw_gamma=3,
            m_therm=860e3 * 1.5e-23, therm_timescale=1, **opencl)

    assert si.temperature == 0
    si.set_temperature(400)
    assert si.temperature == 400

    steps1 = si.relax()
    h_therm1 = si.h_therm.copy()
    assert steps1 > 0

    old_temperature = si.temperature
    si.set_temperature(500)
    assert si.temperature > old_temperature

    steps2 = si.relax()
    h_therm2 = si.h_therm.copy()
    assert steps2 > 0
    assert steps2 > steps1
    assert not np.array_equal(h_therm1, h_therm2)

@pytest.mark.parametrize("temperature", [0, 100, 270, 300, 478])
def test_uniform_to_htherm(temperature):
    si = IsingSpinIce(spin_angle=0, alpha=0, temperature=temperature)
    kB = 1.38064852e-23
    T = si.temperature
    m_therm = si.m_therm
    c = kB * T / m_therm
    attempt_freq = si.attempt_freq
    dt = si.therm_timescale

    def cdf_inv(x):
        return -c*np.log(np.log(x)/(-dt * attempt_freq))

    u = np.random.uniform(size=100)
    assert_array_equal(si._uniform_to_htherm(u), cdf_inv(u))

def test_htherm_magnitude():
    temperature = 300
    si = IsingSpinIce(size=(10,10), spin_angle=0, alpha=0, temperature=300, sw_b=1, sw_c=1, sw_beta=3, sw_gamma=3, hc=0.001, m_therm=860e3 * 1e-24)
    kB = 1.38064852e-23
    T = si.temperature
    m_therm = si.m_therm
    c = kB * T / m_therm
    attempt_freq = si.attempt_freq
    dt = si.therm_timescale

    si.set_random_seed(0x12340)
    si.update_thermal_noise()

    si.set_random_seed(0x12340)
    draw_uniform = si.rng.uniform(size = si.spin_count)
    h_len = si._uniform_to_htherm(draw_uniform)
    #h_therm = si._field_astroid_direction(h_len)

    assert_allclose(norm(si.h_therm, axis=1), h_len)

@pytest.mark.parametrize("magnitude", [0, 1/3, 1])
def test_field_astroid_direction_sw(magnitude):
    si = IsingSpinIce(size=(1,1), spin_angle=0, alpha=0, sw_b=1, sw_c=1, sw_beta=3, sw_gamma=3, hc=1)

    # Zero field should point at either 90+45 or 180+45 degrees
    # h_ext in q2
    si.set_h_ext([-1e-9, 1e-9])
    #magnitude = 1
    hdir = si._field_astroid_direction(magnitude)[0]
    expect = magnitude * np.array([np.cos(3*np.pi/4), np.sin(3*np.pi/4)])
    assert_allclose(hdir, expect, atol=1e-03, rtol=1e-03)

    # h_ext in q3
    si.set_h_ext([-1e-9, -1e-9])
    hdir = si._field_astroid_direction(magnitude)[0]
    expect = magnitude * np.array([np.cos(5*np.pi/4), np.sin(5*np.pi/4)])
    assert_allclose(hdir, expect, atol=1e-03, rtol=1e-03)

def test_field_astroid_direction_outside():
    si = IsingSpinIce(size=(1,1), spin_angle=0, alpha=0, sw_b=1, sw_c=1, sw_beta=3, sw_gamma=3, hc=1)

    # h_ext outside of astroid, should still point out
    si.set_h_ext([-.9, -.9])
    hdir = si._field_astroid_direction(1)[0]
    expect = np.array([np.cos(5*np.pi/4), np.sin(5*np.pi/4)])
    assert_allclose(hdir, expect, atol=1e-03, rtol=1e-03)

def test_field_astroid_direction_asw():
    # beta=gamma=2 and c=.5 gives an astroid with linear shape
    # where distance to astroid can be found analytically
    c = 0.5
    si = IsingSpinIce(size=(1,1), spin_angle=0, alpha=0, sw_b=1, sw_c=c, sw_beta=2, sw_gamma=2, hc=1)

    si.set_h_ext([0, 0.01])
    hdir = si._field_astroid_direction(1)[0]
    x = -2*c**2/(2+2*c**2)
    y = c * (x+1)
    expect = np.array([x, y])
    expect /= norm(expect)
    assert_allclose(hdir, expect, atol=1e-03, rtol=1e-03)

@pytest.mark.parametrize("angle", [0, 20, 30, 45, 60, 90, 112, 120, 135, 160, 180])
def test_field_astroid_direction_circle(angle):
    # Circular astroid should always yield direction radially along h_ext
    si = IsingSpinIce(size=(1,1), spin_angle=0, alpha=0, sw_b=1, sw_c=1, sw_beta=1, sw_gamma=1, hc=1)

    angle = np.deg2rad(angle)

    hpar = np.cos(np.pi/2+angle)
    hperp = np.sin(np.pi/2+angle)
    si.set_h_ext([.1*hpar, .1*hperp])
    hdir = si._field_astroid_direction(1)[0]
    expect = np.array([hpar, hperp])
    assert_allclose(hdir, expect, rtol=1e-03, atol=1e-03)

def test_field_astroid_direction_boundary():
    # Test when h_ext is exactly at the astroid boundary
    hc = 0.02
    #hc = 1
    b = 1
    c = 1
    beta = 3
    gamma = 3
    res = 101
    si = IsingSpinIce(size=(1,1), spin_angle=0, alpha=0, sw_b=b, sw_c=c, sw_beta=beta, sw_gamma=gamma, hc=hc, astroid_resolution=res)

    thetas = np.linspace(np.pi, 2*np.pi, res)

    h_perp = c * np.cos(thetas)
    h_par = np.sin(thetas)
    astroid = ASW(h_par, h_perp, b=b, c=c, beta=beta, gamma=gamma)

    for i in range(len(astroid)):
        h = np.array([hc * astroid[i], hc * h_perp[i]])
        si.set_h_ext(h)

        # Positive magnitude should always point out of astroid (towards switching)
        hdir = si._field_astroid_direction(1)[0]
        assert hdir[0] < 0, f"Failed for i={i} h={h/hc} {si.astroid_resolution} {astroid[i], h_perp[i]}"

        # Negative magnitude should always point into astroid (against switching)
        hdir = si._field_astroid_direction(-1)[0]
        assert hdir[0] > 0, f"Failed for i={i} h={h/hc}"

@pytest.mark.parametrize("magnitude", [1.01, 0.99])
def test_field_astroid_direction_flippable(magnitude):
    hc = 0.02
    b = 1
    c = 1
    beta = 3
    gamma = 3
    H = magnitude * hc
    res = 101
    si = IsingSpinIce(size=(1,1), spin_angle=0, alpha=0, sw_b=b, sw_c=c, sw_beta=beta, sw_gamma=gamma, hc=hc, astroid_resolution=res)

    assert len(si.flippable()) == 0

    dtheta = np.pi / 1024
    thetas = np.arange(np.pi + dtheta, 2*np.pi, dtheta)
    degs = np.rad2deg(thetas)

    h_perp = c * np.cos(thetas)
    h_par = np.sin(thetas)
    astroid = ASW(h_par, h_perp, b=b, c=c, beta=beta, gamma=gamma)

    for i in range(len(astroid)):
        h = np.array([H * astroid[i], H * h_perp[i]])

        si.set_h_ext(h)
        assert len(si.flippable()) == (1 if magnitude > 1 else 0)
        hdir = si._field_astroid_direction(hc)[0]
        assert hdir[0] < 0, f"Expected negative hdir for i={i} deg={degs[i]} h={h} hdir={hdir} h_ext={si.h_ext}"
        si.set_h_ext(h + hdir)
        assert len(si.flippable()) == 1, f"Should flip for i={i} deg={degs[i]} h={h} hdir={hdir} h_ext={si.h_ext}"

        si.set_h_ext(h)
        assert len(si.flippable()) == (1 if magnitude > 1 else 0)
        hdir = si._field_astroid_direction(-hc)[0]
        assert hdir[0] > 0, f"Expected positive hdir for i={i} deg={degs[i]} h={h} hdir={hdir} h_ext={si.h_ext}"
        si.set_h_ext(h + hdir)
        assert len(si.flippable()) == 0, f"Should not flip for i={i} theta={np.rad2deg(thetas[i])} h={h/hc} hdir={hdir} h_ext={si.h_ext/hc}"

def test_field_astroid_direction_negative():
    hc = 1
    si = IsingSpinIce(size=(1,1), spin_angle=0, alpha=0, sw_b=1, sw_c=1, sw_beta=3, sw_gamma=3, hc=hc)

    # External field is strong enough to switch
    phis = np.arange(90+1, 270-1, 1)
    rads = np.deg2rad(phis)
    H = 1.4 * hc
    hs = np.column_stack([H * np.cos(rads), H * np.sin(rads)])
    for phi, h in zip(phis, hs):
        si.set_h_ext(h)
        E = si.switching_energy()[0]
        assert len(si.flippable()) == 1
        assert E > 1e-10

        # A large negative thermal magnitude should prevent switching
        hdir = si._field_astroid_direction(-2)[0]
        si.set_h_ext(h + hdir)
        E = si.switching_energy()[0]
        assert len(si.flippable()) == 0, f"Flippable for phi={phi}"
        # Avoid numerical instability
        assert E < -1e-10, f"Numerical instability for phi={phi}"

def test_h_therm(opencl):
    si = IsingSpinIce(size=(10,10), spin_angle=0, temperature=300,
            hc=0.02, sw_b=1, sw_c=1, sw_beta=3, sw_gamma=3,
            m_therm=860e3 * 1e-23, therm_timescale=0.1, **opencl)

    assert si.temperature == 300

    h_therm1 = si.h_therm.copy()
    h_therm1_magnitude = norm(h_therm1, axis=1)
    n_flippable1 = len(si.flippable())
    assert n_flippable1 > 0

    assert_array_equal(si.total_fields(), h_therm1 + si.dipolar_fields())

    assert si.step() == 1

    assert_array_equal(si.h_therm, h_therm1)

    # Increase temperature
    si.set_temperature(320)
    assert si.temperature == 320

    for i in range(10):
        si.update_thermal_noise()
        h_therm2 = si.h_therm.copy()
        h_therm2_magnitude = norm(h_therm2, axis=1)
        n_flippable2 = len(si.flippable())

        assert not np.array_equal(h_therm1, h_therm2)
        # Magnitude of h_therm should be greater at higher temperatures
        assert np.sum(h_therm1_magnitude) < np.sum(h_therm2_magnitude)
        assert n_flippable1 < n_flippable2
