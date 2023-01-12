from tomwer.core.process.reconstruction.paramsbase import _ReconsParam, _get_db_fromstr
from tomwer.core.process.reconstruction.darkref.params import DKRFRP


def test_paramsbase():
    """
    Test _ReconsParam class
    """
    params = _ReconsParam()
    assert isinstance(params.all_params, list)


def test_get_db_fromstr():
    """
    test '_get_db_fromstr' function
    """
    assert _get_db_fromstr(vals="12") == 12.0
    assert _get_db_fromstr(vals="12.0") == 12.0
    assert _get_db_fromstr(vals="(12.0, )") == 12.0
    assert _get_db_fromstr(vals="(12.0, 13.5)") == (12.0, 13.5)
    assert _get_db_fromstr(vals="[12.0, 13.5]") == (12.0, 13.5)


def test_basic_DKRFRP():
    """
    dummy test for DKRFRP
    """
    recons_params = DKRFRP()
    ddict = recons_params.to_dict()
    DKRFRP.from_dict(ddict)
    assert isinstance(
        recons_params.to_unique_recons_set(),
        tuple,
    )
