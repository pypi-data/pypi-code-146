import numba
import numpy as np
import pandas as pd
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    ife__ttcus = hi - lo
    if ife__ttcus < 2:
        return
    if ife__ttcus < MIN_MERGE:
        foodh__ycsnp = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + foodh__ycsnp, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    ocagp__fuuu = minRunLength(ife__ttcus)
    while True:
        vvjc__mwmx = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if vvjc__mwmx < ocagp__fuuu:
            rkg__wtvj = (ife__ttcus if ife__ttcus <= ocagp__fuuu else
                ocagp__fuuu)
            binarySort(key_arrs, lo, lo + rkg__wtvj, lo + vvjc__mwmx, data)
            vvjc__mwmx = rkg__wtvj
        stackSize = pushRun(stackSize, runBase, runLen, lo, vvjc__mwmx)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += vvjc__mwmx
        ife__ttcus -= vvjc__mwmx
        if ife__ttcus == 0:
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
        qsbhu__hpazv = getitem_arr_tup(key_arrs, start)
        gpig__fvg = getitem_arr_tup(data, start)
        lyc__vrhtd = lo
        cezb__iyzb = start
        assert lyc__vrhtd <= cezb__iyzb
        while lyc__vrhtd < cezb__iyzb:
            bqozs__soamf = lyc__vrhtd + cezb__iyzb >> 1
            if qsbhu__hpazv < getitem_arr_tup(key_arrs, bqozs__soamf):
                cezb__iyzb = bqozs__soamf
            else:
                lyc__vrhtd = bqozs__soamf + 1
        assert lyc__vrhtd == cezb__iyzb
        n = start - lyc__vrhtd
        copyRange_tup(key_arrs, lyc__vrhtd, key_arrs, lyc__vrhtd + 1, n)
        copyRange_tup(data, lyc__vrhtd, data, lyc__vrhtd + 1, n)
        setitem_arr_tup(key_arrs, lyc__vrhtd, qsbhu__hpazv)
        setitem_arr_tup(data, lyc__vrhtd, gpig__fvg)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    zhv__stbvg = lo + 1
    if zhv__stbvg == hi:
        return 1
    if getitem_arr_tup(key_arrs, zhv__stbvg) < getitem_arr_tup(key_arrs, lo):
        zhv__stbvg += 1
        while zhv__stbvg < hi and getitem_arr_tup(key_arrs, zhv__stbvg
            ) < getitem_arr_tup(key_arrs, zhv__stbvg - 1):
            zhv__stbvg += 1
        reverseRange(key_arrs, lo, zhv__stbvg, data)
    else:
        zhv__stbvg += 1
        while zhv__stbvg < hi and getitem_arr_tup(key_arrs, zhv__stbvg
            ) >= getitem_arr_tup(key_arrs, zhv__stbvg - 1):
            zhv__stbvg += 1
    return zhv__stbvg - lo


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
    urj__ejp = 0
    while n >= MIN_MERGE:
        urj__ejp |= n & 1
        n >>= 1
    return n + urj__ejp


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    pjut__duh = len(key_arrs[0])
    tmpLength = (pjut__duh >> 1 if pjut__duh < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    umcp__ksj = (5 if pjut__duh < 120 else 10 if pjut__duh < 1542 else 19 if
        pjut__duh < 119151 else 40)
    runBase = np.empty(umcp__ksj, np.int64)
    runLen = np.empty(umcp__ksj, np.int64)
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
    exwe__bglqp = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert exwe__bglqp >= 0
    base1 += exwe__bglqp
    len1 -= exwe__bglqp
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
    iqz__fbn = 0
    taw__ecw = 1
    if key > getitem_arr_tup(arr, base + hint):
        mlopf__ytf = _len - hint
        while taw__ecw < mlopf__ytf and key > getitem_arr_tup(arr, base +
            hint + taw__ecw):
            iqz__fbn = taw__ecw
            taw__ecw = (taw__ecw << 1) + 1
            if taw__ecw <= 0:
                taw__ecw = mlopf__ytf
        if taw__ecw > mlopf__ytf:
            taw__ecw = mlopf__ytf
        iqz__fbn += hint
        taw__ecw += hint
    else:
        mlopf__ytf = hint + 1
        while taw__ecw < mlopf__ytf and key <= getitem_arr_tup(arr, base +
            hint - taw__ecw):
            iqz__fbn = taw__ecw
            taw__ecw = (taw__ecw << 1) + 1
            if taw__ecw <= 0:
                taw__ecw = mlopf__ytf
        if taw__ecw > mlopf__ytf:
            taw__ecw = mlopf__ytf
        tmp = iqz__fbn
        iqz__fbn = hint - taw__ecw
        taw__ecw = hint - tmp
    assert -1 <= iqz__fbn and iqz__fbn < taw__ecw and taw__ecw <= _len
    iqz__fbn += 1
    while iqz__fbn < taw__ecw:
        aaek__gzmx = iqz__fbn + (taw__ecw - iqz__fbn >> 1)
        if key > getitem_arr_tup(arr, base + aaek__gzmx):
            iqz__fbn = aaek__gzmx + 1
        else:
            taw__ecw = aaek__gzmx
    assert iqz__fbn == taw__ecw
    return taw__ecw


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    taw__ecw = 1
    iqz__fbn = 0
    if key < getitem_arr_tup(arr, base + hint):
        mlopf__ytf = hint + 1
        while taw__ecw < mlopf__ytf and key < getitem_arr_tup(arr, base +
            hint - taw__ecw):
            iqz__fbn = taw__ecw
            taw__ecw = (taw__ecw << 1) + 1
            if taw__ecw <= 0:
                taw__ecw = mlopf__ytf
        if taw__ecw > mlopf__ytf:
            taw__ecw = mlopf__ytf
        tmp = iqz__fbn
        iqz__fbn = hint - taw__ecw
        taw__ecw = hint - tmp
    else:
        mlopf__ytf = _len - hint
        while taw__ecw < mlopf__ytf and key >= getitem_arr_tup(arr, base +
            hint + taw__ecw):
            iqz__fbn = taw__ecw
            taw__ecw = (taw__ecw << 1) + 1
            if taw__ecw <= 0:
                taw__ecw = mlopf__ytf
        if taw__ecw > mlopf__ytf:
            taw__ecw = mlopf__ytf
        iqz__fbn += hint
        taw__ecw += hint
    assert -1 <= iqz__fbn and iqz__fbn < taw__ecw and taw__ecw <= _len
    iqz__fbn += 1
    while iqz__fbn < taw__ecw:
        aaek__gzmx = iqz__fbn + (taw__ecw - iqz__fbn >> 1)
        if key < getitem_arr_tup(arr, base + aaek__gzmx):
            taw__ecw = aaek__gzmx
        else:
            iqz__fbn = aaek__gzmx + 1
    assert iqz__fbn == taw__ecw
    return taw__ecw


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
        qmq__rgmz = 0
        znhp__zcv = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                znhp__zcv += 1
                qmq__rgmz = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                qmq__rgmz += 1
                znhp__zcv = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not qmq__rgmz | znhp__zcv < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            qmq__rgmz = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if qmq__rgmz != 0:
                copyRange_tup(tmp, cursor1, arr, dest, qmq__rgmz)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, qmq__rgmz)
                dest += qmq__rgmz
                cursor1 += qmq__rgmz
                len1 -= qmq__rgmz
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            znhp__zcv = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if znhp__zcv != 0:
                copyRange_tup(arr, cursor2, arr, dest, znhp__zcv)
                copyRange_tup(arr_data, cursor2, arr_data, dest, znhp__zcv)
                dest += znhp__zcv
                cursor2 += znhp__zcv
                len2 -= znhp__zcv
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
            if not qmq__rgmz >= MIN_GALLOP | znhp__zcv >= MIN_GALLOP:
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
        qmq__rgmz = 0
        znhp__zcv = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                qmq__rgmz += 1
                znhp__zcv = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                znhp__zcv += 1
                qmq__rgmz = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not qmq__rgmz | znhp__zcv < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            qmq__rgmz = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if qmq__rgmz != 0:
                dest -= qmq__rgmz
                cursor1 -= qmq__rgmz
                len1 -= qmq__rgmz
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, qmq__rgmz)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    qmq__rgmz)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            znhp__zcv = len2 - gallopLeft(getitem_arr_tup(arr, cursor1),
                tmp, 0, len2, len2 - 1)
            if znhp__zcv != 0:
                dest -= znhp__zcv
                cursor2 -= znhp__zcv
                len2 -= znhp__zcv
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, znhp__zcv)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    znhp__zcv)
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
            if not qmq__rgmz >= MIN_GALLOP | znhp__zcv >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    dwq__sfipb = len(key_arrs[0])
    if tmpLength < minCapacity:
        ishdg__dlm = minCapacity
        ishdg__dlm |= ishdg__dlm >> 1
        ishdg__dlm |= ishdg__dlm >> 2
        ishdg__dlm |= ishdg__dlm >> 4
        ishdg__dlm |= ishdg__dlm >> 8
        ishdg__dlm |= ishdg__dlm >> 16
        ishdg__dlm += 1
        if ishdg__dlm < 0:
            ishdg__dlm = minCapacity
        else:
            ishdg__dlm = min(ishdg__dlm, dwq__sfipb >> 1)
        tmp = alloc_arr_tup(ishdg__dlm, key_arrs)
        tmp_data = alloc_arr_tup(ishdg__dlm, data)
        tmpLength = ishdg__dlm
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        vdpuw__fgs = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = vdpuw__fgs


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    psnj__vzgik = arr_tup.count
    mjc__trd = 'def f(arr_tup, lo, hi):\n'
    for i in range(psnj__vzgik):
        mjc__trd += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        mjc__trd += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        mjc__trd += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    mjc__trd += '  return\n'
    hjj__owfs = {}
    exec(mjc__trd, {}, hjj__owfs)
    zlc__kbc = hjj__owfs['f']
    return zlc__kbc


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    psnj__vzgik = src_arr_tup.count
    assert psnj__vzgik == dst_arr_tup.count
    mjc__trd = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(psnj__vzgik):
        mjc__trd += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    mjc__trd += '  return\n'
    hjj__owfs = {}
    exec(mjc__trd, {'copyRange': copyRange}, hjj__owfs)
    prb__xow = hjj__owfs['f']
    return prb__xow


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    psnj__vzgik = src_arr_tup.count
    assert psnj__vzgik == dst_arr_tup.count
    mjc__trd = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(psnj__vzgik):
        mjc__trd += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    mjc__trd += '  return\n'
    hjj__owfs = {}
    exec(mjc__trd, {'copyElement': copyElement}, hjj__owfs)
    prb__xow = hjj__owfs['f']
    return prb__xow


def getitem_arr_tup(arr_tup, ind):
    gqkxm__kvt = [arr[ind] for arr in arr_tup]
    return tuple(gqkxm__kvt)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    psnj__vzgik = arr_tup.count
    mjc__trd = 'def f(arr_tup, ind):\n'
    mjc__trd += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'.
        format(i) for i in range(psnj__vzgik)]), ',' if psnj__vzgik == 1 else
        '')
    hjj__owfs = {}
    exec(mjc__trd, {}, hjj__owfs)
    kyn__dtr = hjj__owfs['f']
    return kyn__dtr


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, ihn__prezh in zip(arr_tup, val_tup):
        arr[ind] = ihn__prezh


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    psnj__vzgik = arr_tup.count
    mjc__trd = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(psnj__vzgik):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            mjc__trd += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            mjc__trd += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    mjc__trd += '  return\n'
    hjj__owfs = {}
    exec(mjc__trd, {}, hjj__owfs)
    kyn__dtr = hjj__owfs['f']
    return kyn__dtr


def test():
    import time
    ccp__xine = time.time()
    ahsf__wmlzj = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((ahsf__wmlzj,), 0, 3, data)
    print('compile time', time.time() - ccp__xine)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    wfxu__gtqrp = np.random.ranf(n)
    poe__nste = pd.DataFrame({'A': wfxu__gtqrp, 'B': data[0], 'C': data[1]})
    ccp__xine = time.time()
    tvc__hvrlh = poe__nste.sort_values('A', inplace=False)
    vuzl__qjjp = time.time()
    sort((wfxu__gtqrp,), 0, n, data)
    print('Bodo', time.time() - vuzl__qjjp, 'Numpy', vuzl__qjjp - ccp__xine)
    np.testing.assert_almost_equal(data[0], tvc__hvrlh.B.values)
    np.testing.assert_almost_equal(data[1], tvc__hvrlh.C.values)


if __name__ == '__main__':
    test()
