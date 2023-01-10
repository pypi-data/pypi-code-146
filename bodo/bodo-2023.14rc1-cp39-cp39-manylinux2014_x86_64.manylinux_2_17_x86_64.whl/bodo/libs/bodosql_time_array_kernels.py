"""
Implements time array kernels that are specific to BodoSQL
"""
import numba
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import raise_bodo_error


def make_time_to_time_util(name):

    @numba.generated_jit(nopython=True)
    def util(arr):
        ncypr__lis = ['arr']
        msal__vua = [arr]
        wofsy__zle = [True]
        if is_valid_int_arg(arr):
            vcr__fobd = 'res[i] = bodo.Time(0, 0, arg0)'
        elif is_valid_string_arg(arr):
            vcr__fobd = 'res[i] = bodo.time_from_str(arg0)'
        else:
            raise_bodo_error(
                f'{name} argument must be an integer, string, integer or string column, or null'
                )
        rzpa__vvtb = bodo.TimeArrayType(9)
        return gen_vectorized(ncypr__lis, msal__vua, wofsy__zle, vcr__fobd,
            rzpa__vvtb)
    return util


time_util = make_time_to_time_util('TIME')
to_time_util = make_time_to_time_util('TO_TIME')


@numba.generated_jit(nopython=True)
def time_from_parts_util(hour, minute, second, nanosecond):
    verify_int_arg(hour, 'TIME_FROM_PARTS', 'hour')
    verify_int_arg(minute, 'TIME_FROM_PARTS', 'minute')
    verify_int_arg(second, 'TIME_FROM_PARTS', 'second')
    verify_int_arg(nanosecond, 'TIME_FROM_PARTS', 'nanosecond')
    ncypr__lis = ['hour', 'minute', 'second', 'nanosecond']
    msal__vua = [hour, minute, second, nanosecond]
    wofsy__zle = [True] * 4
    vcr__fobd = 'res[i] = bodo.Time(arg0, arg1, arg2, arg3)'
    rzpa__vvtb = bodo.TimeType(9)
    return gen_vectorized(ncypr__lis, msal__vua, wofsy__zle, vcr__fobd,
        rzpa__vvtb)
