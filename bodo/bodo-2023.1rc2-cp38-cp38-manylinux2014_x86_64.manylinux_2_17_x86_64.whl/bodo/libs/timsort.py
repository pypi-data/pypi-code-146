import numba
import numpy as np
import pandas as pd
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    caw__phb = hi - lo
    if caw__phb < 2:
        return
    if caw__phb < MIN_MERGE:
        aqsuc__ejsgn = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + aqsuc__ejsgn, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    tuncg__iym = minRunLength(caw__phb)
    while True:
        muvpj__pmlqb = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if muvpj__pmlqb < tuncg__iym:
            hdgl__bvhv = caw__phb if caw__phb <= tuncg__iym else tuncg__iym
            binarySort(key_arrs, lo, lo + hdgl__bvhv, lo + muvpj__pmlqb, data)
            muvpj__pmlqb = hdgl__bvhv
        stackSize = pushRun(stackSize, runBase, runLen, lo, muvpj__pmlqb)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += muvpj__pmlqb
        caw__phb -= muvpj__pmlqb
        if caw__phb == 0:
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
        fvelk__ypphk = getitem_arr_tup(key_arrs, start)
        ufrcg__isrhk = getitem_arr_tup(data, start)
        hbe__ugvdq = lo
        dgo__jgpz = start
        assert hbe__ugvdq <= dgo__jgpz
        while hbe__ugvdq < dgo__jgpz:
            xlq__pjls = hbe__ugvdq + dgo__jgpz >> 1
            if fvelk__ypphk < getitem_arr_tup(key_arrs, xlq__pjls):
                dgo__jgpz = xlq__pjls
            else:
                hbe__ugvdq = xlq__pjls + 1
        assert hbe__ugvdq == dgo__jgpz
        n = start - hbe__ugvdq
        copyRange_tup(key_arrs, hbe__ugvdq, key_arrs, hbe__ugvdq + 1, n)
        copyRange_tup(data, hbe__ugvdq, data, hbe__ugvdq + 1, n)
        setitem_arr_tup(key_arrs, hbe__ugvdq, fvelk__ypphk)
        setitem_arr_tup(data, hbe__ugvdq, ufrcg__isrhk)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    wllj__knjt = lo + 1
    if wllj__knjt == hi:
        return 1
    if getitem_arr_tup(key_arrs, wllj__knjt) < getitem_arr_tup(key_arrs, lo):
        wllj__knjt += 1
        while wllj__knjt < hi and getitem_arr_tup(key_arrs, wllj__knjt
            ) < getitem_arr_tup(key_arrs, wllj__knjt - 1):
            wllj__knjt += 1
        reverseRange(key_arrs, lo, wllj__knjt, data)
    else:
        wllj__knjt += 1
        while wllj__knjt < hi and getitem_arr_tup(key_arrs, wllj__knjt
            ) >= getitem_arr_tup(key_arrs, wllj__knjt - 1):
            wllj__knjt += 1
    return wllj__knjt - lo


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
    ppqi__ictzg = 0
    while n >= MIN_MERGE:
        ppqi__ictzg |= n & 1
        n >>= 1
    return n + ppqi__ictzg


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    zon__xuywy = len(key_arrs[0])
    tmpLength = (zon__xuywy >> 1 if zon__xuywy < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    ckbak__rgcf = (5 if zon__xuywy < 120 else 10 if zon__xuywy < 1542 else 
        19 if zon__xuywy < 119151 else 40)
    runBase = np.empty(ckbak__rgcf, np.int64)
    runLen = np.empty(ckbak__rgcf, np.int64)
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
    ibd__iyqai = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert ibd__iyqai >= 0
    base1 += ibd__iyqai
    len1 -= ibd__iyqai
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
    svzr__oijgu = 0
    xwd__rab = 1
    if key > getitem_arr_tup(arr, base + hint):
        hhow__iirx = _len - hint
        while xwd__rab < hhow__iirx and key > getitem_arr_tup(arr, base +
            hint + xwd__rab):
            svzr__oijgu = xwd__rab
            xwd__rab = (xwd__rab << 1) + 1
            if xwd__rab <= 0:
                xwd__rab = hhow__iirx
        if xwd__rab > hhow__iirx:
            xwd__rab = hhow__iirx
        svzr__oijgu += hint
        xwd__rab += hint
    else:
        hhow__iirx = hint + 1
        while xwd__rab < hhow__iirx and key <= getitem_arr_tup(arr, base +
            hint - xwd__rab):
            svzr__oijgu = xwd__rab
            xwd__rab = (xwd__rab << 1) + 1
            if xwd__rab <= 0:
                xwd__rab = hhow__iirx
        if xwd__rab > hhow__iirx:
            xwd__rab = hhow__iirx
        tmp = svzr__oijgu
        svzr__oijgu = hint - xwd__rab
        xwd__rab = hint - tmp
    assert -1 <= svzr__oijgu and svzr__oijgu < xwd__rab and xwd__rab <= _len
    svzr__oijgu += 1
    while svzr__oijgu < xwd__rab:
        val__kqnd = svzr__oijgu + (xwd__rab - svzr__oijgu >> 1)
        if key > getitem_arr_tup(arr, base + val__kqnd):
            svzr__oijgu = val__kqnd + 1
        else:
            xwd__rab = val__kqnd
    assert svzr__oijgu == xwd__rab
    return xwd__rab


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    xwd__rab = 1
    svzr__oijgu = 0
    if key < getitem_arr_tup(arr, base + hint):
        hhow__iirx = hint + 1
        while xwd__rab < hhow__iirx and key < getitem_arr_tup(arr, base +
            hint - xwd__rab):
            svzr__oijgu = xwd__rab
            xwd__rab = (xwd__rab << 1) + 1
            if xwd__rab <= 0:
                xwd__rab = hhow__iirx
        if xwd__rab > hhow__iirx:
            xwd__rab = hhow__iirx
        tmp = svzr__oijgu
        svzr__oijgu = hint - xwd__rab
        xwd__rab = hint - tmp
    else:
        hhow__iirx = _len - hint
        while xwd__rab < hhow__iirx and key >= getitem_arr_tup(arr, base +
            hint + xwd__rab):
            svzr__oijgu = xwd__rab
            xwd__rab = (xwd__rab << 1) + 1
            if xwd__rab <= 0:
                xwd__rab = hhow__iirx
        if xwd__rab > hhow__iirx:
            xwd__rab = hhow__iirx
        svzr__oijgu += hint
        xwd__rab += hint
    assert -1 <= svzr__oijgu and svzr__oijgu < xwd__rab and xwd__rab <= _len
    svzr__oijgu += 1
    while svzr__oijgu < xwd__rab:
        val__kqnd = svzr__oijgu + (xwd__rab - svzr__oijgu >> 1)
        if key < getitem_arr_tup(arr, base + val__kqnd):
            xwd__rab = val__kqnd
        else:
            svzr__oijgu = val__kqnd + 1
    assert svzr__oijgu == xwd__rab
    return xwd__rab


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
        zsbqk__hsfje = 0
        plsft__epi = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                plsft__epi += 1
                zsbqk__hsfje = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                zsbqk__hsfje += 1
                plsft__epi = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not zsbqk__hsfje | plsft__epi < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            zsbqk__hsfje = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if zsbqk__hsfje != 0:
                copyRange_tup(tmp, cursor1, arr, dest, zsbqk__hsfje)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, zsbqk__hsfje)
                dest += zsbqk__hsfje
                cursor1 += zsbqk__hsfje
                len1 -= zsbqk__hsfje
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            plsft__epi = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if plsft__epi != 0:
                copyRange_tup(arr, cursor2, arr, dest, plsft__epi)
                copyRange_tup(arr_data, cursor2, arr_data, dest, plsft__epi)
                dest += plsft__epi
                cursor2 += plsft__epi
                len2 -= plsft__epi
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
            if not zsbqk__hsfje >= MIN_GALLOP | plsft__epi >= MIN_GALLOP:
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
        zsbqk__hsfje = 0
        plsft__epi = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                zsbqk__hsfje += 1
                plsft__epi = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                plsft__epi += 1
                zsbqk__hsfje = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not zsbqk__hsfje | plsft__epi < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            zsbqk__hsfje = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if zsbqk__hsfje != 0:
                dest -= zsbqk__hsfje
                cursor1 -= zsbqk__hsfje
                len1 -= zsbqk__hsfje
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, zsbqk__hsfje)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    zsbqk__hsfje)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            plsft__epi = len2 - gallopLeft(getitem_arr_tup(arr, cursor1),
                tmp, 0, len2, len2 - 1)
            if plsft__epi != 0:
                dest -= plsft__epi
                cursor2 -= plsft__epi
                len2 -= plsft__epi
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, plsft__epi)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    plsft__epi)
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
            if not zsbqk__hsfje >= MIN_GALLOP | plsft__epi >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    mvzno__kryk = len(key_arrs[0])
    if tmpLength < minCapacity:
        rphzk__ooh = minCapacity
        rphzk__ooh |= rphzk__ooh >> 1
        rphzk__ooh |= rphzk__ooh >> 2
        rphzk__ooh |= rphzk__ooh >> 4
        rphzk__ooh |= rphzk__ooh >> 8
        rphzk__ooh |= rphzk__ooh >> 16
        rphzk__ooh += 1
        if rphzk__ooh < 0:
            rphzk__ooh = minCapacity
        else:
            rphzk__ooh = min(rphzk__ooh, mvzno__kryk >> 1)
        tmp = alloc_arr_tup(rphzk__ooh, key_arrs)
        tmp_data = alloc_arr_tup(rphzk__ooh, data)
        tmpLength = rphzk__ooh
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        dgvi__qvm = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = dgvi__qvm


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    ucnjk__wrts = arr_tup.count
    hhj__plc = 'def f(arr_tup, lo, hi):\n'
    for i in range(ucnjk__wrts):
        hhj__plc += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        hhj__plc += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        hhj__plc += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    hhj__plc += '  return\n'
    tseb__xmhf = {}
    exec(hhj__plc, {}, tseb__xmhf)
    gpn__irmxa = tseb__xmhf['f']
    return gpn__irmxa


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    ucnjk__wrts = src_arr_tup.count
    assert ucnjk__wrts == dst_arr_tup.count
    hhj__plc = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(ucnjk__wrts):
        hhj__plc += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    hhj__plc += '  return\n'
    tseb__xmhf = {}
    exec(hhj__plc, {'copyRange': copyRange}, tseb__xmhf)
    aoica__abfr = tseb__xmhf['f']
    return aoica__abfr


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    ucnjk__wrts = src_arr_tup.count
    assert ucnjk__wrts == dst_arr_tup.count
    hhj__plc = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(ucnjk__wrts):
        hhj__plc += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    hhj__plc += '  return\n'
    tseb__xmhf = {}
    exec(hhj__plc, {'copyElement': copyElement}, tseb__xmhf)
    aoica__abfr = tseb__xmhf['f']
    return aoica__abfr


def getitem_arr_tup(arr_tup, ind):
    nng__pzq = [arr[ind] for arr in arr_tup]
    return tuple(nng__pzq)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    ucnjk__wrts = arr_tup.count
    hhj__plc = 'def f(arr_tup, ind):\n'
    hhj__plc += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'.
        format(i) for i in range(ucnjk__wrts)]), ',' if ucnjk__wrts == 1 else
        '')
    tseb__xmhf = {}
    exec(hhj__plc, {}, tseb__xmhf)
    mewim__odr = tseb__xmhf['f']
    return mewim__odr


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, cka__lcmn in zip(arr_tup, val_tup):
        arr[ind] = cka__lcmn


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    ucnjk__wrts = arr_tup.count
    hhj__plc = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(ucnjk__wrts):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            hhj__plc += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            hhj__plc += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    hhj__plc += '  return\n'
    tseb__xmhf = {}
    exec(hhj__plc, {}, tseb__xmhf)
    mewim__odr = tseb__xmhf['f']
    return mewim__odr


def test():
    import time
    rocvy__rvle = time.time()
    shh__ovucw = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((shh__ovucw,), 0, 3, data)
    print('compile time', time.time() - rocvy__rvle)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    haqaa__nhd = np.random.ranf(n)
    odwq__eemn = pd.DataFrame({'A': haqaa__nhd, 'B': data[0], 'C': data[1]})
    rocvy__rvle = time.time()
    pcrsk__wzf = odwq__eemn.sort_values('A', inplace=False)
    zlei__ammhn = time.time()
    sort((haqaa__nhd,), 0, n, data)
    print('Bodo', time.time() - zlei__ammhn, 'Numpy', zlei__ammhn - rocvy__rvle
        )
    np.testing.assert_almost_equal(data[0], pcrsk__wzf.B.values)
    np.testing.assert_almost_equal(data[1], pcrsk__wzf.C.values)


if __name__ == '__main__':
    test()
