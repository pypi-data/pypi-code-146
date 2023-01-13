import sys

import numpy
import pytest

sys.path.append("./")
sys.path.append("./test")
import synth_datagen

import orientationpy

VERBOSE = 0


# --- Generate 2D test angles from -90 to 90
@pytest.mark.parametrize("angleDeg", numpy.random.rand(10) * 180 - 90)
def test_2D_synth(angleDeg):
    sigma = 2
    boxSize = 3
    # Check that gaussian and splines are accurate enough per pixel
    im = synth_datagen.generate_synthetic_data([100, 100], angleDeg, smooth=2)[25:75, 25:75]
    for mode, angular_tolerance_2D in [["gaussian", 0.5], ["splines", 0.5], ["finite_difference", 5]]:
        structureTensor = orientationpy.computeGradientStructureTensor(im, sigma, mode=mode)
        orientations = orientationpy.computeOrientation(structureTensor)
        assert numpy.isclose(orientations["theta"].mean(), angleDeg, atol=angular_tolerance_2D)

    # Check that gaussian and splines are accurate enough in small boxes
    for mode in ["gaussian", "splines"]:
        structureTensor = orientationpy.computeGradientStructureTensorBoxes(im, boxSize, mode=mode)
        orientations = orientationpy.computeOrientation(structureTensor, computeEnergy=True, computeCoherency=True)
        assert orientations["energy"].mean() > 0
        assert orientations["coherency"].mean() > 0.8
        assert numpy.isclose(orientations["theta"].mean(), angleDeg, atol=angular_tolerance_2D)

        vectors = orientationpy.anglesToVectors(orientations).reshape(2, -1).T
        norms = numpy.linalg.norm(vectors, axis=1)
        assert numpy.allclose(norms, 1.0, atol=0.01)

    # Check that energy and coherency are OK, let's just do it for the pixel-level
    # Let's also check for non-square crops...
    # im = synth_datagen.generate_synthetic_data([100, 100], angleDeg, smooth=2)[35:65, 25:75]
    # gradients = orientationpy.computeGradient(im, mode="finite_difference")
    # structureTensor = orientationpy.computeStructureTensor(gradients, 2)
    # orientation, energy, coherency = orientationpy.computeOrientation(structureTensor, computeEnergy=True, computeCoherency=True)

    ## Check membrane is rejected in 2D
    # orientations = orientationpy.computeOrientation(structureTensor, mode="membrane")
    # assert orientation is None

    ## Check wrong mode is also rejected
    # orientations = orientationpy.computeOrientation(structureTensor, mode="froop")
    # assert orientation is None


def test_edge_cases():
    # Edge case 1: the 2D image detector for 1-padded 2D images
    im = synth_datagen.generate_synthetic_data([100, 100], 33, smooth=2)[25:75, 25:75]
    im = im[numpy.newaxis, ...]
    structureTensor = orientationpy.computeGradientStructureTensor(im, 2, mode="gaussian")
    print(structureTensor.shape)
    assert structureTensor.shape == (3, im.shape[-2], im.shape[-1])

    orientations = orientationpy.computeOrientation(
        structureTensor,
    )
    print(orientations["theta"].mean())
    assert numpy.allclose(numpy.mean(orientations["theta"]), 33.0, atol=0.1)
    with pytest.raises(KeyError):
        print(orientations["phi"])

    # Edge case 2: bad gradient mode
    with pytest.raises(ValueError):
        orientationpy.computeGradient(im, mode="BadMode")

    # Edge case 3: bad orientation mode
    with pytest.raises(ValueError):
        orientationpy.computeOrientation(structureTensor, mode="BadMode")

    # Edge case 4: ask for membrane mode in 2d in computeOrientation
    with pytest.raises(ValueError):
        orientationpy.computeOrientation(structureTensor, mode="membrane")

    # Edge case 5: len(structureTensor.shape) != 3 or 4 in computeOrientation
    with pytest.raises(ValueError):
        orientationpy.computeOrientation(numpy.array([1, 1, 1, 1, 1, 1]), mode="membrane")

    # Edge case 6: len(structureTensor.shape) != 3 or 4
    with pytest.raises(ValueError):
        orientationpy.computeOrientation(numpy.array([1, 1, 1, 1, 1, 1]), mode="membrane")

    # Edge case 7: non 2D or 3D case in anglesToVectors
    with pytest.raises(KeyError):
        orientationpy.anglesToVectors({"empty": "dict"})

    # Edge case 8: not-a-dict
    with pytest.raises(TypeError):
        orientationpy.anglesToVectors(structureTensor)


def test_3D_fibres():
    def genThetaPhi(rot):
        # --- Generate 3D image
        im = synth_datagen.generate_synthetic_data([100, 100, 100], rot)[25:-25, 25:-25, 25:-25]
        structureTensor = orientationpy.computeGradientStructureTensor(im, sigma=1, mode="gaussian")
        orientations = orientationpy.computeOrientation(structureTensor, mode="fiber")
        return orientations["theta"], orientations["phi"]

    def genThetaPhiBoxes(rot, boxSize):
        # --- Generate 3D image
        im = synth_datagen.generate_synthetic_data([100, 100, 100], rot)[25:-25, 25:-25, 25:-25]
        structureTensor = orientationpy.computeGradientStructureTensorBoxes(im, boxSize, mode="splines")
        orientations = orientationpy.computeOrientation(structureTensor, mode="fiber", computeEnergy=True, computeCoherency=True)
        return orientations["theta"], orientations["phi"]

    # Pointing along Z
    theta, phi = genThetaPhi([0, 0, 0])
    assert numpy.allclose(theta.mean(), 0, 0.1)
    vecZYX = orientationpy.anglesToVectors({"theta": theta, "phi": phi})
    vecZYXnorm = numpy.linalg.norm(vecZYX, axis=0)
    print(vecZYXnorm)
    assert vecZYXnorm.shape == (50, 50, 50)
    assert numpy.allclose(vecZYXnorm, 1.0, atol=0.01)
    assert numpy.allclose(vecZYX[0, :, :, :], 1.0, atol=0.01)
    assert numpy.allclose(vecZYX[1, :, :, :], 0.0, atol=0.01)
    assert numpy.allclose(vecZYX[2, :, :, :], 0.0, atol=0.01)

    # Pointing along Y
    theta, phi = genThetaPhi([0, 0, 90])
    assert numpy.allclose(theta.mean(), 90, 0.1)
    # In the XY plane they are ambiguous
    phi[phi > 180] -= 180
    assert numpy.allclose(phi.mean(), 90, 0.1)

    # Pointing along X
    theta, phi = genThetaPhi([0, 90, 0])
    # In the XY plane they are ambiguous
    phi[phi >= 270] -= 360
    phi[phi >= 90] -= 180
    assert numpy.allclose(theta.mean(), 90, atol=0.1)
    assert numpy.allclose(phi.mean(), 0, atol=0.1)

    theta, phi = genThetaPhi([0, 0, 45])
    assert numpy.allclose(theta.mean(), 45, atol=0.1)
    assert numpy.allclose(phi.mean(), 90, atol=0.5)

    theta, phi = genThetaPhi([0, 0, -45])
    assert numpy.allclose(theta.mean(), 45, atol=0.1)
    assert numpy.allclose(phi.mean(), 270, atol=0.5)

    theta, phi = genThetaPhi([0, 45, 0])
    assert numpy.allclose(theta.mean(), 45, atol=0.1)
    assert numpy.allclose(phi.mean(), 180, atol=0.5)

    theta, phi = genThetaPhi([0, -45, 0])
    assert numpy.allclose(theta.mean(), 45, atol=0.1)
    assert numpy.allclose(numpy.cos(numpy.deg2rad(phi.ravel())).mean(), 1, atol=0.01)

    theta, phi = genThetaPhiBoxes([0, 0, -45], 5)
    assert numpy.allclose(theta.mean(), 45, atol=0.1)
    assert numpy.allclose(phi.mean(), 270, atol=0.5)

    # for the last case, ensure vectors are normed
    vectors = orientationpy.anglesToVectors({"theta": theta, "phi": phi}).reshape(3, -1).T
    norms = numpy.linalg.norm(vectors, axis=1)
    assert numpy.allclose(norms, 1.0, atol=0.01)

    # Bonus finite_difference for Z-aligned
    # Pointing along Z
    im = synth_datagen.generate_synthetic_data([100, 100, 100], [0, 0, 0])[25:-25, 25:-25, 25:-25]
    structureTensor = orientationpy.computeGradientStructureTensor(im, sigma=1, mode="finite_difference")
    orientations = orientationpy.computeOrientation(structureTensor, mode="fiber")
    assert numpy.allclose(orientations["theta"], 0, 1)
