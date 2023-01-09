from lnbfx import lookup


def test_lookup():
    cr_700 = lookup.pipeline.cell_ranger_v7_0_0
    assert list(cr_700.keys()) == ["id", "v", "name", "reference"]
    assert all([isinstance(v, str) for v in cr_700.values()])

    cr_701 = lookup.pipeline.cell_ranger_v7_0_1
    assert list(cr_701.keys()) == ["id", "v", "name", "reference"]
    assert all([isinstance(v, str) for v in cr_701.values()])
