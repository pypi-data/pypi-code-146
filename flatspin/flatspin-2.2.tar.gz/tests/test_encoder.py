import numpy as np
import pandas as pd
import pytest
from .utils import approx, assert_allclose
from numpy.testing import assert_array_equal

from flatspin.encoder import *

def test_scale():
    input = np.array([0, 0.5, 1])
    out = scale(input, 0.5, 1)
    assert_array_equal(out, [0.5, 0.75, 1.0])

def test_broadcast_waveform():
    # 1d input
    input = [0, 1, 2]
    waveform = [0, 1, 0]
    out = broadcast_waveform(input, waveform)
    assert_array_equal(out, [0, 0, 0, 0, 1, 0, 0, 2, 0])

    # single 1d input
    input = [2]
    waveform = [0, 1, 0]
    out = broadcast_waveform(input, waveform)
    assert_array_equal(out, [0, 2, 0])

    # 2d input
    input = [[[0], [1]],
             [[2], [3]]]
    out = broadcast_waveform(input, waveform)
    expect = [[0, 0],
              [0, 1],
              [0, 0],
              [0, 0],
              [2, 3],
              [0, 0]]
    assert_array_equal(out, expect)

    # 1d input signal
    input = [[0, 1, 2],
             [3, 4, 5]]
    out = broadcast_waveform(input, waveform)
    assert_array_equal(out, [0, 1, 0, 0, 4, 0])

    # 2d input signal
    input = [[[0, 1, 2], [3, 4, 5]],
             [[6, 7, 8], [9, 10, 11]]]
    out = broadcast_waveform(input, waveform)
    expect = [[0, 0],
              [1, 4],
              [0, 0],
              [0, 0],
              [7, 10],
              [0, 0]]
    assert_array_equal(out, expect)

def test_sin():
    s = np.sin(np.linspace(0, 2 * np.pi, 100, endpoint=False))

    # 3 inputs, each with single feature
    input = np.array([1, 2, 3])
    input.shape += (1,)
    out = sin(input, 100)
    assert out.shape == (300,)
    expect = np.concatenate([1*s, 2*s, 3*s])
    assert_array_equal(out, expect)

    # 2 inputs, each with 3 features
    input = np.array([[1, 2, 3],
                      [4, 5, 6]])
    input.shape += (1,)
    out = sin(input, 100)
    assert out.shape == (200, 3)
    expect = [np.transpose([1*s, 2*s, 3*s]),
              np.transpose([4*s, 5*s, 6*s])]
    expect = np.concatenate(expect)
    assert_array_equal(out, expect)

    # 2 inputs, each with 2x2 features
    input = np.array([[[1, 2],
                       [3, 4]],
                      [[5, 6],
                       [7, 8]]])
    input.shape += (1,)
    out = sin(input, 100)
    assert out.shape == (200, 2, 2)
    expect = [[[1*s, 2*s],
               [3*s, 4*s]],
              [[5*s, 6*s],
               [7*s, 8*s]]]
    expect = np.rollaxis(np.array(expect), -1, 1)
    expect = np.concatenate(expect)
    assert_array_equal(out, expect)

def test_rotate():
    c = np.cos(np.linspace(0, 2 * np.pi, 100, endpoint=False))
    s = np.sin(np.linspace(0, 2 * np.pi, 100, endpoint=False))

    # 1d input
    input = [1, 2, 3]
    out = rotate(input, 100)
    assert out.shape == (300, 2)
    expect1 = np.concatenate([1*c, 2*c, 3*c])
    expect2 = np.concatenate([1*s, 2*s, 3*s])
    expect = np.column_stack([expect1, expect2])
    assert_array_equal(out, expect)

    # 2 inputs, each with 3 features
    input = np.array([[1, 2, 3],
                      [4, 5, 6]])
    input.shape += (1,)
    out = rotate(input, 100)
    assert out.shape == (200, 3, 2)
    expect0 = [np.concatenate([1*c, 4*c]), np.concatenate([1*s, 4*s])]
    assert_array_equal(out[:,0], np.column_stack(expect0))
    expect1 = [np.concatenate([2*c, 5*c]), np.concatenate([2*s, 5*s])]
    assert_array_equal(out[:,1], np.column_stack(expect1))
    expect2 = [np.concatenate([3*c, 6*c]), np.concatenate([3*s, 6*s])]
    assert_array_equal(out[:,2], np.column_stack(expect2))

    # 2 inputs, each with 2x2 features
    input = np.array([[[1, 2],
                       [3, 4]],
                      [[5, 6],
                       [7, 8]]])
    input.shape += (1,)
    out = rotate(input, 100)
    assert out.shape == (200, 2, 2, 2)
    expect00 = [np.concatenate([1*c, 5*c]), np.concatenate([1*s, 5*s])]
    assert_array_equal(out[:,0,0], np.column_stack(expect00))
    expect11 = [np.concatenate([4*c, 8*c]), np.concatenate([4*s, 8*s])]
    assert_array_equal(out[:,1,1], np.column_stack(expect11))

def test_angle():
    # 3 inputs, each with single feature
    input = np.array([0, 0.25, 0.5, 0.75, 1])
    out = angle(input)
    assert out.shape == (5, 2)
    expect = [[1, 0],
              [0, 1],
              [-1, 0],
              [0, -1],
              [1, 0]]
    assert_allclose(out, expect)

    # 2 inputs, each with 3 features
    input = np.array([[0, 0.25, 0.5],
                      [0.75, 1.0, 0.5]])
    out = angle(input)
    assert out.shape == (2, 3, 2)
    expect = [[[1, 0], [0, 1], [-1, 0]],
              [[0, -1], [1, 0], [-1, 0]]]
    assert_allclose(out, expect)

def test_fixed_vector():
    # 3 inputs, each with single feature
    input = np.array([1, 2, 3])
    c = np.cos(np.deg2rad(30))
    s = np.sin(np.deg2rad(30))
    out = fixed_vector(input, 30)
    assert out.shape == (3, 2)
    expect = [[1*c, 1*s],
              [2*c, 2*s],
              [3*c, 3*s]]
    assert_array_equal(out, expect)

    # 2 inputs, each with 3 features
    input = np.array([[1, 2, 3],
                      [4, 5, 6]])
    out = fixed_vector(input, 30)
    assert out.shape == (2, 3, 2)
    expect = [[[1*c, 1*s], [2*c, 2*s], [3*c, 3*s]],
              [[4*c, 4*s], [5*c, 5*s], [6*c, 6*s]]]
    assert_array_equal(out, expect)

def test_rotate_vector():
    def v(deg):
        rad = np.deg2rad(deg)
        return np.column_stack([np.cos(rad), np.sin(rad)])

    #
    # 1d array of vectors
    #
    degs = np.linspace(0, 360, 5*5)
    input = np.array(v(degs))

    # 0 deg rotation -> no change
    out = rotate_vector(input, 0)
    assert_array_equal(out, input)

    # 90 deg rotation
    out = rotate_vector(input, 90)
    expect = v(degs + 90)
    assert_allclose(out, expect)

    # -90 deg rotation
    out = rotate_vector(input, -90)
    expect = v(degs - 90)
    assert_allclose(out, expect)

    # 60 deg rotation
    out = rotate_vector(input, 60)
    expect = v(degs + 60)
    assert_allclose(out, expect)

    # 360 + 60 deg rotation
    out = rotate_vector(input, 360+60)
    expect = v(degs + 60)
    assert_allclose(out, expect)

    #
    # 2d array of vectors
    #
    input = input.reshape((5,5,2))

    # 0 deg rotation -> no change
    out = rotate_vector(input, 0)
    assert_array_equal(out, input)

    # 90 deg rotation
    out = rotate_vector(input, 90)
    expect = v(degs + 90).reshape(input.shape)
    assert_allclose(out, expect)

    # -90 deg rotation
    out = rotate_vector(input, -90)
    expect = v(degs - 90).reshape(input.shape)
    assert_allclose(out, expect)

    # 60 deg rotation
    out = rotate_vector(input, 60)
    expect = v(degs + 60).reshape(input.shape)
    assert_allclose(out, expect)

    # 360 + 60 deg rotation
    out = rotate_vector(input, 360+60)
    expect = v(degs + 60).reshape(input.shape)
    assert_allclose(out, expect)


def test_ensure2d():
    #
    # 1d scalar inputs -> vectors
    #
    input = np.array([0,1,2,3])

    # default: fill y component with 1
    out = ensure2d(input)
    expect = [[0,1], [1,1], [2,1], [3,1]]
    assert_array_equal(out, expect)

    # fill y component with 5
    out = ensure2d(input, fill=5)
    expect = [[0,5], [1,5], [2,5], [3,5]]
    assert_array_equal(out, expect)

    # vector inputs -> unchanged
    input = np.array([[0,1],[2,3]])
    out = ensure2d(input)
    expect = [[0,1], [2,3]]
    assert_array_equal(out, expect)

def test_grid():
    # 2 inputs, each with single feature
    input = np.array([1, 2])
    out = grid(input, (3, 2))
    assert out.shape == (2, 2, 3)
    expect = [[[1,1,1],
               [1,1,1]],
              [[2,2,2],
               [2,2,2]]]
    assert_array_equal(out, expect)

    # 2 inputs, each with 2 features
    input = np.array([[1, 2], [3, 4]])
    out = grid(input, (3, 2))
    assert out.shape == (2, 2, 3, 2)
    expect = [[[[1,2],[1,2],[1,2]],
               [[1,2],[1,2],[1,2]]],
              [[[3,4],[3,4],[3,4]],
               [[3,4],[3,4],[3,4]]]]
    assert_array_equal(out, expect)

    # 1D grid
    input = np.array([1, 2])
    out = grid(input, (3, 1))
    assert out.shape == (2, 1, 3)
    expect = [[[1,1,1]],
              [[2,2,2]]]
    assert_array_equal(out, expect)

    input = np.array([1, 2])
    out = grid(input, (1, 3))
    assert out.shape == (2, 3, 1)
    expect = [[[1],
               [1],
               [1]],
              [[2],
               [2],
               [2]]]
    assert_array_equal(out, expect)

def test_onehot():
    # single feature
    input = np.array([0, 1])
    out = onehot(input, nbits=2)
    assert_array_equal(out, [1, 0, 0, 1])

    input = np.array([0, 1])
    out = onehot(input, nbits=3)
    assert_array_equal(out, [1, 0, 0, 0, 1, 0])

    input = np.array([0, 1, 2])
    out = onehot(input, nbits=3)
    assert_array_equal(out, [1, 0, 0, 0, 1, 0, 0, 0, 1])

    # 2 inputs, each with 2 features
    input = np.array([[0, 1], [2, 0]])
    out = onehot(input, nbits=3)

             # 0, 1
    expect = [[1, 0],
              [0, 1],
              [0, 0],

             # 2, 0
              [0, 1],
              [0, 0],
              [1, 0]]
    assert_array_equal(out, expect)

def test_ppm():
    # single feature
    input = np.array([0, 0.5, 1])
    out = ppm(input, timesteps=3)
    expect = [[1,0,0],
              [0,1,0],
              [0,0,1]]
    assert_array_equal(out, expect)

    out = ppm(input, timesteps=6, pos=0.5)
    expect = [[1,0,0,0,0,0],
              [0,1,0,0,0,0],
              [0,0,1,0,0,0]]
    assert_array_equal(out, expect)

    out = ppm(input, timesteps=6, pos0=0.5)
    expect = [[0,0,0,1,0,0],
              [0,0,0,0,1,0],
              [0,0,0,0,0,1]]
    assert_array_equal(out, expect)

    # 2 inputs, each with 2 features
    input = np.array([[0, 0.5], [0.5, 1.0]])
    out = ppm(input, timesteps=3)
    expect = [[[1,0,0],[0,1,0]],
              [[0,1,0],[0,0,1]]]
    assert_array_equal(out, expect)

def test_constant_encoder():
    input = np.array([[0,.5,1]]).T
    encoder = Constant()

    out = encoder(input)
    expect = np.array([[0,0],[.5,0],[1,0]])
    assert_array_equal(out, expect)

    encoder.set_params(H=3)
    out = encoder(input)
    expect = np.array([[0,0],[1.5,0],[3,0]])
    assert_array_equal(out, expect)

    encoder.set_params(H0=1)
    out = encoder(input)
    expect = np.array([[1,0],[2,0],[3,0]])
    assert_array_equal(out, expect)

    encoder.set_params(phi=90)
    out = encoder(input)
    expect = np.array([[0,1],[0,2],[0,3]])
    assert_allclose(out, expect)

    encoder.set_params(timesteps=2)
    out = encoder(input)
    expect = np.array([[0,1],[0,1],[0,2],[0,2],[0,3],[0,3]])
    assert_allclose(out, expect)

def test_sin_encoder():
    input = np.array([[0,.5,1]]).T
    encoder = Sine()

    out = encoder(input)
    s = np.sin(np.linspace(0, 2*np.pi, 100, endpoint=False))
    expect = np.concatenate([0*s, .5*s, 1*s])
    assert_array_equal(out[:,0], expect)
    assert_array_equal(out[:,1], np.zeros(len(expect)))

    encoder.set_params(H=10)
    out = encoder(input)
    assert_array_equal(out[:,0], 10 * expect)
    assert_array_equal(out[:,1], np.zeros(len(expect)))

    encoder.set_params(H0=5)
    out = encoder(input)
    expect = np.concatenate([5*s, 7.5*s, 10*s])
    assert_array_equal(out[:,0], expect)
    assert_array_equal(out[:,1], np.zeros(len(expect)))

    encoder.set_params(phi=90)
    out = encoder(input)
    assert_allclose(out[:,0], np.zeros(len(expect)))
    assert_array_equal(out[:,1], expect)

def test_triangle_encoder():
    input = np.array([[0,.5,1]]).T
    encoder = Triangle(timesteps=8)

    out = encoder(input)
    s = np.array([0, 0.5, 1, 0.5, 0, -0.5, -1, -0.5])
    expect = np.concatenate([0*s, .5*s, 1*s])
    assert_array_equal(out[:,0], expect)
    assert_array_equal(out[:,1], np.zeros(len(expect)))

    encoder.set_params(H=10)
    out = encoder(input)
    assert_array_equal(out[:,0], 10 * expect)
    assert_array_equal(out[:,1], np.zeros(len(expect)))

    encoder.set_params(H0=5)
    out = encoder(input)
    expect = np.concatenate([5*s, 7.5*s, 10*s])
    assert_array_equal(out[:,0], expect)
    assert_array_equal(out[:,1], np.zeros(len(expect)))

    encoder.set_params(phi=90)
    out = encoder(input)
    assert_allclose(out[:,0], np.zeros(len(expect)))
    assert_array_equal(out[:,1], expect)

def test_constant_grid_encoder():
    input = np.array([[0,.5,1]]).T
    encoder = ConstantGrid(grid_size=(3,3))

    out = encoder(input)
    s = np.ones((3,3))
    expect = np.concatenate([[0*s], [.5*s], [1*s]])
    assert_array_equal(out[...,0], expect)
    assert_array_equal(out[...,1], 0*expect)

    encoder.set_params(H=10)
    out = encoder(input)
    assert_array_equal(out[...,0], 10*expect)
    assert_array_equal(out[...,1], 0*expect)

    encoder.set_params(H0=5)
    out = encoder(input)
    expect = np.concatenate([[5*s], [7.5*s], [10*s]])
    assert_array_equal(out[...,0], expect)
    assert_array_equal(out[...,1], 0*expect)

    encoder.set_params(phi=90)
    out = encoder(input)
    assert_allclose(out[...,0], 0*expect)
    assert_array_equal(out[...,1], expect)

    encoder.set_params(timesteps=2)
    out = encoder(input)
    rexpect = np.repeat(expect, 2, axis=0)
    assert_allclose(out[...,0], 0*rexpect)
    assert_array_equal(out[...,1], rexpect)

    # custom grid weights
    grid = np.array([[0,1],[.5,0]])
    encoder.set_params(grid=grid, H0=0, H=1, phi=0, timesteps=1)

    out = encoder(input)
    expect = np.concatenate([[0*grid], [.5*grid], [1*grid]])
    assert_array_equal(out[...,0], expect)
    assert_array_equal(out[...,1], 0*expect)

    # scaling happens after the grid
    encoder.set_params(H0=5, H=10)
    out = encoder(input)
    expect = np.array([[[5,5],[5,5]],
                       [[5,7.5],[6.25,5]],
                       [[5,10],[7.5,5]]])
    assert_array_equal(out[...,0], expect)
    assert_array_equal(out[...,1], 0*expect)

    encoder.set_params(timesteps=2)
    out = encoder(input)
    rexpect = np.repeat(expect, 2, axis=0)
    assert_array_equal(out[...,0], rexpect)
    assert_array_equal(out[...,1], 0*rexpect)
