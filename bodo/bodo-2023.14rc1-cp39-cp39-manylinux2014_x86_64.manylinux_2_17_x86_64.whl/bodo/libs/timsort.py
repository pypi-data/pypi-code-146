import numba
import numpy as np
import pandas as pd
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    qjuxf__uahwu = hi - lo
    if qjuxf__uahwu < 2:
        return
    if qjuxf__uahwu < MIN_MERGE:
        wee__djws = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + wee__djws, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    sie__chrca = minRunLength(qjuxf__uahwu)
    while True:
        paa__vppfb = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if paa__vppfb < sie__chrca:
            lzl__qsdkv = (qjuxf__uahwu if qjuxf__uahwu <= sie__chrca else
                sie__chrca)
            binarySort(key_arrs, lo, lo + lzl__qsdkv, lo + paa__vppfb, data)
            paa__vppfb = lzl__qsdkv
        stackSize = pushRun(stackSize, runBase, runLen, lo, paa__vppfb)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += paa__vppfb
        qjuxf__uahwu -= paa__vppfb
        if qjuxf__uahwu == 0:
            break
    assert lo == hi
    stackSize, tmpLength, tmp, tmp_data, minGallop = mergeForceCollapse(
        stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
        tmp_data, minGallop)
    assert stackSize == 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def binarySort(key_arrs, lo, hi, start, data):
    assert lo <= start and start <= hi
    if start == lo:
        start += 1
    while start < hi:
        ryhnt__jyzq = getitem_arr_tup(key_arrs, start)
        pnwkt__tnl = getitem_arr_tup(data, start)
        uld__zqvyt = lo
        msyf__lqcps = start
        assert uld__zqvyt <= msyf__lqcps
        while uld__zqvyt < msyf__lqcps:
            nap__gmt = uld__zqvyt + msyf__lqcps >> 1
            if ryhnt__jyzq < getitem_arr_tup(key_arrs, nap__gmt):
                msyf__lqcps = nap__gmt
            else:
                uld__zqvyt = nap__gmt + 1
        assert uld__zqvyt == msyf__lqcps
        n = start - uld__zqvyt
        copyRange_tup(key_arrs, uld__zqvyt, key_arrs, uld__zqvyt + 1, n)
        copyRange_tup(data, uld__zqvyt, data, uld__zqvyt + 1, n)
        setitem_arr_tup(key_arrs, uld__zqvyt, ryhnt__jyzq)
        setitem_arr_tup(data, uld__zqvyt, pnwkt__tnl)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    hiynd__ntkyj = lo + 1
    if hiynd__ntkyj == hi:
        return 1
    if getitem_arr_tup(key_arrs, hiynd__ntkyj) < getitem_arr_tup(key_arrs, lo):
        hiynd__ntkyj += 1
        while hiynd__ntkyj < hi and getitem_arr_tup(key_arrs, hiynd__ntkyj
            ) < getitem_arr_tup(key_arrs, hiynd__ntkyj - 1):
            hiynd__ntkyj += 1
        reverseRange(key_arrs, lo, hiynd__ntkyj, data)
    else:
        hiynd__ntkyj += 1
        while hiynd__ntkyj < hi and getitem_arr_tup(key_arrs, hiynd__ntkyj
            ) >= getitem_arr_tup(key_arrs, hiynd__ntkyj - 1):
            hiynd__ntkyj += 1
    return hiynd__ntkyj - lo


@numba.njit(no_cpython_wrapper=True, cache=True)
def reverseRange(key_arrs, lo, hi, data):
    hi -= 1
    while lo < hi:
        swap_arrs(key_arrs, lo, hi)
        swap_arrs(data, lo, hi)
        lo += 1
        hi -= 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def minRunLength(n):
    assert n >= 0
    sai__mqh = 0
    while n >= MIN_MERGE:
        sai__mqh |= n & 1
        n >>= 1
    return n + sai__mqh


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    dycg__wfplt = len(key_arrs[0])
    tmpLength = (dycg__wfplt >> 1 if dycg__wfplt < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    bha__odw = (5 if dycg__wfplt < 120 else 10 if dycg__wfplt < 1542 else 
        19 if dycg__wfplt < 119151 else 40)
    runBase = np.empty(bha__odw, np.int64)
    runLen = np.empty(bha__odw, np.int64)
    return stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def pushRun(stackSize, runBase, runLen, runBase_val, runLen_val):
    runBase[stackSize] = runBase_val
    runLen[stackSize] = runLen_val
    stackSize += 1
    return stackSize


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeCollapse(stackSize, runBase, runLen, key_arrs, data, tmpLength,
    tmp, tmp_data, minGallop):
    while stackSize > 1:
        n = stackSize - 2
        if n >= 1 and runLen[n - 1] <= runLen[n] + runLen[n + 1
            ] or n >= 2 and runLen[n - 2] <= runLen[n] + runLen[n - 1]:
            if runLen[n - 1] < runLen[n + 1]:
                n -= 1
        elif runLen[n] > runLen[n + 1]:
            break
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeAt(stackSize,
            runBase, runLen, key_arrs, data, tmpLength, tmp, tmp_data,
            minGallop, n)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeForceCollapse(stackSize, runBase, runLen, key_arrs, data,
    tmpLength, tmp, tmp_data, minGallop):
    while stackSize > 1:
        n = stackSize - 2
        if n > 0 and runLen[n - 1] < runLen[n + 1]:
            n -= 1
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeAt(stackSize,
            runBase, runLen, key_arrs, data, tmpLength, tmp, tmp_data,
            minGallop, n)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeAt(stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
    tmp_data, minGallop, i):
    assert stackSize >= 2
    assert i >= 0
    assert i == stackSize - 2 or i == stackSize - 3
    base1 = runBase[i]
    len1 = runLen[i]
    base2 = runBase[i + 1]
    len2 = runLen[i + 1]
    assert len1 > 0 and len2 > 0
    assert base1 + len1 == base2
    runLen[i] = len1 + len2
    if i == stackSize - 3:
        runBase[i + 1] = runBase[i + 2]
        runLen[i + 1] = runLen[i + 2]
    stackSize -= 1
    oywsl__tgx = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert oywsl__tgx >= 0
    base1 += oywsl__tgx
    len1 -= oywsl__tgx
    if len1 == 0:
        return stackSize, tmpLength, tmp, tmp_data, minGallop
    len2 = gallopLeft(getitem_arr_tup(key_arrs, base1 + len1 - 1), key_arrs,
        base2, len2, len2 - 1)
    assert len2 >= 0
    if len2 == 0:
        return stackSize, tmpLength, tmp, tmp_data, minGallop
    if len1 <= len2:
        tmpLength, tmp, tmp_data = ensureCapacity(tmpLength, tmp, tmp_data,
            key_arrs, data, len1)
        minGallop = mergeLo(key_arrs, data, tmp, tmp_data, minGallop, base1,
            len1, base2, len2)
    else:
        tmpLength, tmp, tmp_data = ensureCapacity(tmpLength, tmp, tmp_data,
            key_arrs, data, len2)
        minGallop = mergeHi(key_arrs, data, tmp, tmp_data, minGallop, base1,
            len1, base2, len2)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopLeft(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    xlrd__sok = 0
    otmi__oyjui = 1
    if key > getitem_arr_tup(arr, base + hint):
        elbpn__tms = _len - hint
        while otmi__oyjui < elbpn__tms and key > getitem_arr_tup(arr, base +
            hint + otmi__oyjui):
            xlrd__sok = otmi__oyjui
            otmi__oyjui = (otmi__oyjui << 1) + 1
            if otmi__oyjui <= 0:
                otmi__oyjui = elbpn__tms
        if otmi__oyjui > elbpn__tms:
            otmi__oyjui = elbpn__tms
        xlrd__sok += hint
        otmi__oyjui += hint
    else:
        elbpn__tms = hint + 1
        while otmi__oyjui < elbpn__tms and key <= getitem_arr_tup(arr, base +
            hint - otmi__oyjui):
            xlrd__sok = otmi__oyjui
            otmi__oyjui = (otmi__oyjui << 1) + 1
            if otmi__oyjui <= 0:
                otmi__oyjui = elbpn__tms
        if otmi__oyjui > elbpn__tms:
            otmi__oyjui = elbpn__tms
        tmp = xlrd__sok
        xlrd__sok = hint - otmi__oyjui
        otmi__oyjui = hint - tmp
    assert -1 <= xlrd__sok and xlrd__sok < otmi__oyjui and otmi__oyjui <= _len
    xlrd__sok += 1
    while xlrd__sok < otmi__oyjui:
        wdqkl__txl = xlrd__sok + (otmi__oyjui - xlrd__sok >> 1)
        if key > getitem_arr_tup(arr, base + wdqkl__txl):
            xlrd__sok = wdqkl__txl + 1
        else:
            otmi__oyjui = wdqkl__txl
    assert xlrd__sok == otmi__oyjui
    return otmi__oyjui


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    otmi__oyjui = 1
    xlrd__sok = 0
    if key < getitem_arr_tup(arr, base + hint):
        elbpn__tms = hint + 1
        while otmi__oyjui < elbpn__tms and key < getitem_arr_tup(arr, base +
            hint - otmi__oyjui):
            xlrd__sok = otmi__oyjui
            otmi__oyjui = (otmi__oyjui << 1) + 1
            if otmi__oyjui <= 0:
                otmi__oyjui = elbpn__tms
        if otmi__oyjui > elbpn__tms:
            otmi__oyjui = elbpn__tms
        tmp = xlrd__sok
        xlrd__sok = hint - otmi__oyjui
        otmi__oyjui = hint - tmp
    else:
        elbpn__tms = _len - hint
        while otmi__oyjui < elbpn__tms and key >= getitem_arr_tup(arr, base +
            hint + otmi__oyjui):
            xlrd__sok = otmi__oyjui
            otmi__oyjui = (otmi__oyjui << 1) + 1
            if otmi__oyjui <= 0:
                otmi__oyjui = elbpn__tms
        if otmi__oyjui > elbpn__tms:
            otmi__oyjui = elbpn__tms
        xlrd__sok += hint
        otmi__oyjui += hint
    assert -1 <= xlrd__sok and xlrd__sok < otmi__oyjui and otmi__oyjui <= _len
    xlrd__sok += 1
    while xlrd__sok < otmi__oyjui:
        wdqkl__txl = xlrd__sok + (otmi__oyjui - xlrd__sok >> 1)
        if key < getitem_arr_tup(arr, base + wdqkl__txl):
            otmi__oyjui = wdqkl__txl
        else:
            xlrd__sok = wdqkl__txl + 1
    assert xlrd__sok == otmi__oyjui
    return otmi__oyjui


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeLo(key_arrs, data, tmp, tmp_data, minGallop, base1, len1, base2, len2
    ):
    assert len1 > 0 and len2 > 0 and base1 + len1 == base2
    arr = key_arrs
    arr_data = data
    copyRange_tup(arr, base1, tmp, 0, len1)
    copyRange_tup(arr_data, base1, tmp_data, 0, len1)
    cursor1 = 0
    cursor2 = base2
    dest = base1
    setitem_arr_tup(arr, dest, getitem_arr_tup(arr, cursor2))
    copyElement_tup(arr_data, cursor2, arr_data, dest)
    cursor2 += 1
    dest += 1
    len2 -= 1
    if len2 == 0:
        copyRange_tup(tmp, cursor1, arr, dest, len1)
        copyRange_tup(tmp_data, cursor1, arr_data, dest, len1)
        return minGallop
    if len1 == 1:
        copyRange_tup(arr, cursor2, arr, dest, len2)
        copyRange_tup(arr_data, cursor2, arr_data, dest, len2)
        copyElement_tup(tmp, cursor1, arr, dest + len2)
        copyElement_tup(tmp_data, cursor1, arr_data, dest + len2)
        return minGallop
    len1, len2, cursor1, cursor2, dest, minGallop = mergeLo_inner(key_arrs,
        data, tmp_data, len1, len2, tmp, cursor1, cursor2, dest, minGallop)
    minGallop = 1 if minGallop < 1 else minGallop
    if len1 == 1:
        assert len2 > 0
        copyRange_tup(arr, cursor2, arr, dest, len2)
        copyRange_tup(arr_data, cursor2, arr_data, dest, len2)
        copyElement_tup(tmp, cursor1, arr, dest + len2)
        copyElement_tup(tmp_data, cursor1, arr_data, dest + len2)
    elif len1 == 0:
        raise ValueError('Comparison method violates its general contract!')
    else:
        assert len2 == 0
        assert len1 > 1
        copyRange_tup(tmp, cursor1, arr, dest, len1)
        copyRange_tup(tmp_data, cursor1, arr_data, dest, len1)
    return minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeLo_inner(arr, arr_data, tmp_data, len1, len2, tmp, cursor1,
    cursor2, dest, minGallop):
    while True:
        xsj__jcs = 0
        bmu__mykeo = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                bmu__mykeo += 1
                xsj__jcs = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                xsj__jcs += 1
                bmu__mykeo = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not xsj__jcs | bmu__mykeo < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            xsj__jcs = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if xsj__jcs != 0:
                copyRange_tup(tmp, cursor1, arr, dest, xsj__jcs)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, xsj__jcs)
                dest += xsj__jcs
                cursor1 += xsj__jcs
                len1 -= xsj__jcs
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            bmu__mykeo = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if bmu__mykeo != 0:
                copyRange_tup(arr, cursor2, arr, dest, bmu__mykeo)
                copyRange_tup(arr_data, cursor2, arr_data, dest, bmu__mykeo)
                dest += bmu__mykeo
                cursor2 += bmu__mykeo
                len2 -= bmu__mykeo
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor1, arr, dest)
            copyElement_tup(tmp_data, cursor1, arr_data, dest)
            cursor1 += 1
            dest += 1
            len1 -= 1
            if len1 == 1:
                return len1, len2, cursor1, cursor2, dest, minGallop
            minGallop -= 1
            if not xsj__jcs >= MIN_GALLOP | bmu__mykeo >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeHi(key_arrs, data, tmp, tmp_data, minGallop, base1, len1, base2, len2
    ):
    assert len1 > 0 and len2 > 0 and base1 + len1 == base2
    arr = key_arrs
    arr_data = data
    copyRange_tup(arr, base2, tmp, 0, len2)
    copyRange_tup(arr_data, base2, tmp_data, 0, len2)
    cursor1 = base1 + len1 - 1
    cursor2 = len2 - 1
    dest = base2 + len2 - 1
    copyElement_tup(arr, cursor1, arr, dest)
    copyElement_tup(arr_data, cursor1, arr_data, dest)
    cursor1 -= 1
    dest -= 1
    len1 -= 1
    if len1 == 0:
        copyRange_tup(tmp, 0, arr, dest - (len2 - 1), len2)
        copyRange_tup(tmp_data, 0, arr_data, dest - (len2 - 1), len2)
        return minGallop
    if len2 == 1:
        dest -= len1
        cursor1 -= len1
        copyRange_tup(arr, cursor1 + 1, arr, dest + 1, len1)
        copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1, len1)
        copyElement_tup(tmp, cursor2, arr, dest)
        copyElement_tup(tmp_data, cursor2, arr_data, dest)
        return minGallop
    len1, len2, tmp, cursor1, cursor2, dest, minGallop = mergeHi_inner(key_arrs
        , data, tmp_data, base1, len1, len2, tmp, cursor1, cursor2, dest,
        minGallop)
    minGallop = 1 if minGallop < 1 else minGallop
    if len2 == 1:
        assert len1 > 0
        dest -= len1
        cursor1 -= len1
        copyRange_tup(arr, cursor1 + 1, arr, dest + 1, len1)
        copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1, len1)
        copyElement_tup(tmp, cursor2, arr, dest)
        copyElement_tup(tmp_data, cursor2, arr_data, dest)
    elif len2 == 0:
        raise ValueError('Comparison method violates its general contract!')
    else:
        assert len1 == 0
        assert len2 > 0
        copyRange_tup(tmp, 0, arr, dest - (len2 - 1), len2)
        copyRange_tup(tmp_data, 0, arr_data, dest - (len2 - 1), len2)
    return minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeHi_inner(arr, arr_data, tmp_data, base1, len1, len2, tmp, cursor1,
    cursor2, dest, minGallop):
    while True:
        xsj__jcs = 0
        bmu__mykeo = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                xsj__jcs += 1
                bmu__mykeo = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                bmu__mykeo += 1
                xsj__jcs = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not xsj__jcs | bmu__mykeo < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            xsj__jcs = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if xsj__jcs != 0:
                dest -= xsj__jcs
                cursor1 -= xsj__jcs
                len1 -= xsj__jcs
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, xsj__jcs)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    xsj__jcs)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            bmu__mykeo = len2 - gallopLeft(getitem_arr_tup(arr, cursor1),
                tmp, 0, len2, len2 - 1)
            if bmu__mykeo != 0:
                dest -= bmu__mykeo
                cursor2 -= bmu__mykeo
                len2 -= bmu__mykeo
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, bmu__mykeo)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    bmu__mykeo)
                if len2 <= 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor1, arr, dest)
            copyElement_tup(arr_data, cursor1, arr_data, dest)
            cursor1 -= 1
            dest -= 1
            len1 -= 1
            if len1 == 0:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            minGallop -= 1
            if not xsj__jcs >= MIN_GALLOP | bmu__mykeo >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    dgu__dir = len(key_arrs[0])
    if tmpLength < minCapacity:
        lrrey__dxx = minCapacity
        lrrey__dxx |= lrrey__dxx >> 1
        lrrey__dxx |= lrrey__dxx >> 2
        lrrey__dxx |= lrrey__dxx >> 4
        lrrey__dxx |= lrrey__dxx >> 8
        lrrey__dxx |= lrrey__dxx >> 16
        lrrey__dxx += 1
        if lrrey__dxx < 0:
            lrrey__dxx = minCapacity
        else:
            lrrey__dxx = min(lrrey__dxx, dgu__dir >> 1)
        tmp = alloc_arr_tup(lrrey__dxx, key_arrs)
        tmp_data = alloc_arr_tup(lrrey__dxx, data)
        tmpLength = lrrey__dxx
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        jbjz__hlmp = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = jbjz__hlmp


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    sbe__uju = arr_tup.count
    vfq__znpb = 'def f(arr_tup, lo, hi):\n'
    for i in range(sbe__uju):
        vfq__znpb += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        vfq__znpb += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        vfq__znpb += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    vfq__znpb += '  return\n'
    tawfj__mgn = {}
    exec(vfq__znpb, {}, tawfj__mgn)
    pgql__jlzm = tawfj__mgn['f']
    return pgql__jlzm


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    sbe__uju = src_arr_tup.count
    assert sbe__uju == dst_arr_tup.count
    vfq__znpb = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(sbe__uju):
        vfq__znpb += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    vfq__znpb += '  return\n'
    tawfj__mgn = {}
    exec(vfq__znpb, {'copyRange': copyRange}, tawfj__mgn)
    letm__wftw = tawfj__mgn['f']
    return letm__wftw


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    sbe__uju = src_arr_tup.count
    assert sbe__uju == dst_arr_tup.count
    vfq__znpb = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(sbe__uju):
        vfq__znpb += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    vfq__znpb += '  return\n'
    tawfj__mgn = {}
    exec(vfq__znpb, {'copyElement': copyElement}, tawfj__mgn)
    letm__wftw = tawfj__mgn['f']
    return letm__wftw


def getitem_arr_tup(arr_tup, ind):
    yrksh__shcf = [arr[ind] for arr in arr_tup]
    return tuple(yrksh__shcf)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    sbe__uju = arr_tup.count
    vfq__znpb = 'def f(arr_tup, ind):\n'
    vfq__znpb += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'.
        format(i) for i in range(sbe__uju)]), ',' if sbe__uju == 1 else '')
    tawfj__mgn = {}
    exec(vfq__znpb, {}, tawfj__mgn)
    entu__foafy = tawfj__mgn['f']
    return entu__foafy


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, bzx__aum in zip(arr_tup, val_tup):
        arr[ind] = bzx__aum


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    sbe__uju = arr_tup.count
    vfq__znpb = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(sbe__uju):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            vfq__znpb += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            vfq__znpb += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    vfq__znpb += '  return\n'
    tawfj__mgn = {}
    exec(vfq__znpb, {}, tawfj__mgn)
    entu__foafy = tawfj__mgn['f']
    return entu__foafy


def test():
    import time
    mws__bjdnm = time.time()
    orlw__ipb = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((orlw__ipb,), 0, 3, data)
    print('compile time', time.time() - mws__bjdnm)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    bzfua__lozz = np.random.ranf(n)
    zisqi__hcrz = pd.DataFrame({'A': bzfua__lozz, 'B': data[0], 'C': data[1]})
    mws__bjdnm = time.time()
    lalzi__hywag = zisqi__hcrz.sort_values('A', inplace=False)
    wkyey__bum = time.time()
    sort((bzfua__lozz,), 0, n, data)
    print('Bodo', time.time() - wkyey__bum, 'Numpy', wkyey__bum - mws__bjdnm)
    np.testing.assert_almost_equal(data[0], lalzi__hywag.B.values)
    np.testing.assert_almost_equal(data[1], lalzi__hywag.C.values)


if __name__ == '__main__':
    test()
