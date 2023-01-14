import numpy as np

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def test_numpy():
    assert isfloat(np.pi)