import numba
import numpy as np
import pandas as pd
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    zobnj__oqnae = hi - lo
    if zobnj__oqnae < 2:
        return
    if zobnj__oqnae < MIN_MERGE:
        larz__llwz = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + larz__llwz, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    lwksw__cjb = minRunLength(zobnj__oqnae)
    while True:
        fsxt__fbz = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if fsxt__fbz < lwksw__cjb:
            cmpak__gzmq = (zobnj__oqnae if zobnj__oqnae <= lwksw__cjb else
                lwksw__cjb)
            binarySort(key_arrs, lo, lo + cmpak__gzmq, lo + fsxt__fbz, data)
            fsxt__fbz = cmpak__gzmq
        stackSize = pushRun(stackSize, runBase, runLen, lo, fsxt__fbz)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += fsxt__fbz
        zobnj__oqnae -= fsxt__fbz
        if zobnj__oqnae == 0:
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
        aay__dlza = getitem_arr_tup(key_arrs, start)
        iufqb__sjhf = getitem_arr_tup(data, start)
        dcfvk__hnocv = lo
        cjw__ctg = start
        assert dcfvk__hnocv <= cjw__ctg
        while dcfvk__hnocv < cjw__ctg:
            basxj__ped = dcfvk__hnocv + cjw__ctg >> 1
            if aay__dlza < getitem_arr_tup(key_arrs, basxj__ped):
                cjw__ctg = basxj__ped
            else:
                dcfvk__hnocv = basxj__ped + 1
        assert dcfvk__hnocv == cjw__ctg
        n = start - dcfvk__hnocv
        copyRange_tup(key_arrs, dcfvk__hnocv, key_arrs, dcfvk__hnocv + 1, n)
        copyRange_tup(data, dcfvk__hnocv, data, dcfvk__hnocv + 1, n)
        setitem_arr_tup(key_arrs, dcfvk__hnocv, aay__dlza)
        setitem_arr_tup(data, dcfvk__hnocv, iufqb__sjhf)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    npiia__wpqbk = lo + 1
    if npiia__wpqbk == hi:
        return 1
    if getitem_arr_tup(key_arrs, npiia__wpqbk) < getitem_arr_tup(key_arrs, lo):
        npiia__wpqbk += 1
        while npiia__wpqbk < hi and getitem_arr_tup(key_arrs, npiia__wpqbk
            ) < getitem_arr_tup(key_arrs, npiia__wpqbk - 1):
            npiia__wpqbk += 1
        reverseRange(key_arrs, lo, npiia__wpqbk, data)
    else:
        npiia__wpqbk += 1
        while npiia__wpqbk < hi and getitem_arr_tup(key_arrs, npiia__wpqbk
            ) >= getitem_arr_tup(key_arrs, npiia__wpqbk - 1):
            npiia__wpqbk += 1
    return npiia__wpqbk - lo


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
    zwjo__loxp = 0
    while n >= MIN_MERGE:
        zwjo__loxp |= n & 1
        n >>= 1
    return n + zwjo__loxp


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    odij__urby = len(key_arrs[0])
    tmpLength = (odij__urby >> 1 if odij__urby < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    utf__scwib = (5 if odij__urby < 120 else 10 if odij__urby < 1542 else 
        19 if odij__urby < 119151 else 40)
    runBase = np.empty(utf__scwib, np.int64)
    runLen = np.empty(utf__scwib, np.int64)
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
    vjzi__oud = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert vjzi__oud >= 0
    base1 += vjzi__oud
    len1 -= vjzi__oud
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
    nxpc__vevjb = 0
    lxd__lcc = 1
    if key > getitem_arr_tup(arr, base + hint):
        sjzn__iuoq = _len - hint
        while lxd__lcc < sjzn__iuoq and key > getitem_arr_tup(arr, base +
            hint + lxd__lcc):
            nxpc__vevjb = lxd__lcc
            lxd__lcc = (lxd__lcc << 1) + 1
            if lxd__lcc <= 0:
                lxd__lcc = sjzn__iuoq
        if lxd__lcc > sjzn__iuoq:
            lxd__lcc = sjzn__iuoq
        nxpc__vevjb += hint
        lxd__lcc += hint
    else:
        sjzn__iuoq = hint + 1
        while lxd__lcc < sjzn__iuoq and key <= getitem_arr_tup(arr, base +
            hint - lxd__lcc):
            nxpc__vevjb = lxd__lcc
            lxd__lcc = (lxd__lcc << 1) + 1
            if lxd__lcc <= 0:
                lxd__lcc = sjzn__iuoq
        if lxd__lcc > sjzn__iuoq:
            lxd__lcc = sjzn__iuoq
        tmp = nxpc__vevjb
        nxpc__vevjb = hint - lxd__lcc
        lxd__lcc = hint - tmp
    assert -1 <= nxpc__vevjb and nxpc__vevjb < lxd__lcc and lxd__lcc <= _len
    nxpc__vevjb += 1
    while nxpc__vevjb < lxd__lcc:
        cmnl__uct = nxpc__vevjb + (lxd__lcc - nxpc__vevjb >> 1)
        if key > getitem_arr_tup(arr, base + cmnl__uct):
            nxpc__vevjb = cmnl__uct + 1
        else:
            lxd__lcc = cmnl__uct
    assert nxpc__vevjb == lxd__lcc
    return lxd__lcc


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    lxd__lcc = 1
    nxpc__vevjb = 0
    if key < getitem_arr_tup(arr, base + hint):
        sjzn__iuoq = hint + 1
        while lxd__lcc < sjzn__iuoq and key < getitem_arr_tup(arr, base +
            hint - lxd__lcc):
            nxpc__vevjb = lxd__lcc
            lxd__lcc = (lxd__lcc << 1) + 1
            if lxd__lcc <= 0:
                lxd__lcc = sjzn__iuoq
        if lxd__lcc > sjzn__iuoq:
            lxd__lcc = sjzn__iuoq
        tmp = nxpc__vevjb
        nxpc__vevjb = hint - lxd__lcc
        lxd__lcc = hint - tmp
    else:
        sjzn__iuoq = _len - hint
        while lxd__lcc < sjzn__iuoq and key >= getitem_arr_tup(arr, base +
            hint + lxd__lcc):
            nxpc__vevjb = lxd__lcc
            lxd__lcc = (lxd__lcc << 1) + 1
            if lxd__lcc <= 0:
                lxd__lcc = sjzn__iuoq
        if lxd__lcc > sjzn__iuoq:
            lxd__lcc = sjzn__iuoq
        nxpc__vevjb += hint
        lxd__lcc += hint
    assert -1 <= nxpc__vevjb and nxpc__vevjb < lxd__lcc and lxd__lcc <= _len
    nxpc__vevjb += 1
    while nxpc__vevjb < lxd__lcc:
        cmnl__uct = nxpc__vevjb + (lxd__lcc - nxpc__vevjb >> 1)
        if key < getitem_arr_tup(arr, base + cmnl__uct):
            lxd__lcc = cmnl__uct
        else:
            nxpc__vevjb = cmnl__uct + 1
    assert nxpc__vevjb == lxd__lcc
    return lxd__lcc


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
        oozy__stsxw = 0
        eqmx__mtkbp = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                eqmx__mtkbp += 1
                oozy__stsxw = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                oozy__stsxw += 1
                eqmx__mtkbp = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not oozy__stsxw | eqmx__mtkbp < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            oozy__stsxw = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if oozy__stsxw != 0:
                copyRange_tup(tmp, cursor1, arr, dest, oozy__stsxw)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, oozy__stsxw)
                dest += oozy__stsxw
                cursor1 += oozy__stsxw
                len1 -= oozy__stsxw
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            eqmx__mtkbp = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if eqmx__mtkbp != 0:
                copyRange_tup(arr, cursor2, arr, dest, eqmx__mtkbp)
                copyRange_tup(arr_data, cursor2, arr_data, dest, eqmx__mtkbp)
                dest += eqmx__mtkbp
                cursor2 += eqmx__mtkbp
                len2 -= eqmx__mtkbp
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
            if not oozy__stsxw >= MIN_GALLOP | eqmx__mtkbp >= MIN_GALLOP:
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
        oozy__stsxw = 0
        eqmx__mtkbp = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                oozy__stsxw += 1
                eqmx__mtkbp = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                eqmx__mtkbp += 1
                oozy__stsxw = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not oozy__stsxw | eqmx__mtkbp < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            oozy__stsxw = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if oozy__stsxw != 0:
                dest -= oozy__stsxw
                cursor1 -= oozy__stsxw
                len1 -= oozy__stsxw
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, oozy__stsxw)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    oozy__stsxw)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            eqmx__mtkbp = len2 - gallopLeft(getitem_arr_tup(arr, cursor1),
                tmp, 0, len2, len2 - 1)
            if eqmx__mtkbp != 0:
                dest -= eqmx__mtkbp
                cursor2 -= eqmx__mtkbp
                len2 -= eqmx__mtkbp
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, eqmx__mtkbp)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    eqmx__mtkbp)
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
            if not oozy__stsxw >= MIN_GALLOP | eqmx__mtkbp >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    afa__gmt = len(key_arrs[0])
    if tmpLength < minCapacity:
        lyl__rphcb = minCapacity
        lyl__rphcb |= lyl__rphcb >> 1
        lyl__rphcb |= lyl__rphcb >> 2
        lyl__rphcb |= lyl__rphcb >> 4
        lyl__rphcb |= lyl__rphcb >> 8
        lyl__rphcb |= lyl__rphcb >> 16
        lyl__rphcb += 1
        if lyl__rphcb < 0:
            lyl__rphcb = minCapacity
        else:
            lyl__rphcb = min(lyl__rphcb, afa__gmt >> 1)
        tmp = alloc_arr_tup(lyl__rphcb, key_arrs)
        tmp_data = alloc_arr_tup(lyl__rphcb, data)
        tmpLength = lyl__rphcb
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        pbr__wtrfk = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = pbr__wtrfk


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    snjy__smd = arr_tup.count
    jmglv__nzj = 'def f(arr_tup, lo, hi):\n'
    for i in range(snjy__smd):
        jmglv__nzj += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        jmglv__nzj += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        jmglv__nzj += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    jmglv__nzj += '  return\n'
    afo__tglzz = {}
    exec(jmglv__nzj, {}, afo__tglzz)
    kefef__dqcb = afo__tglzz['f']
    return kefef__dqcb


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    snjy__smd = src_arr_tup.count
    assert snjy__smd == dst_arr_tup.count
    jmglv__nzj = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(snjy__smd):
        jmglv__nzj += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    jmglv__nzj += '  return\n'
    afo__tglzz = {}
    exec(jmglv__nzj, {'copyRange': copyRange}, afo__tglzz)
    objs__ehah = afo__tglzz['f']
    return objs__ehah


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    snjy__smd = src_arr_tup.count
    assert snjy__smd == dst_arr_tup.count
    jmglv__nzj = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(snjy__smd):
        jmglv__nzj += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    jmglv__nzj += '  return\n'
    afo__tglzz = {}
    exec(jmglv__nzj, {'copyElement': copyElement}, afo__tglzz)
    objs__ehah = afo__tglzz['f']
    return objs__ehah


def getitem_arr_tup(arr_tup, ind):
    iswc__pjctl = [arr[ind] for arr in arr_tup]
    return tuple(iswc__pjctl)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    snjy__smd = arr_tup.count
    jmglv__nzj = 'def f(arr_tup, ind):\n'
    jmglv__nzj += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'.
        format(i) for i in range(snjy__smd)]), ',' if snjy__smd == 1 else '')
    afo__tglzz = {}
    exec(jmglv__nzj, {}, afo__tglzz)
    jceee__dweax = afo__tglzz['f']
    return jceee__dweax


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, xry__izh in zip(arr_tup, val_tup):
        arr[ind] = xry__izh


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    snjy__smd = arr_tup.count
    jmglv__nzj = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(snjy__smd):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            jmglv__nzj += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            jmglv__nzj += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    jmglv__nzj += '  return\n'
    afo__tglzz = {}
    exec(jmglv__nzj, {}, afo__tglzz)
    jceee__dweax = afo__tglzz['f']
    return jceee__dweax


def test():
    import time
    ipmha__uihfh = time.time()
    ule__jiisc = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((ule__jiisc,), 0, 3, data)
    print('compile time', time.time() - ipmha__uihfh)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    rhofa__jit = np.random.ranf(n)
    tqrhr__tcpcl = pd.DataFrame({'A': rhofa__jit, 'B': data[0], 'C': data[1]})
    ipmha__uihfh = time.time()
    lfm__tbke = tqrhr__tcpcl.sort_values('A', inplace=False)
    lexxr__bnp = time.time()
    sort((rhofa__jit,), 0, n, data)
    print('Bodo', time.time() - lexxr__bnp, 'Numpy', lexxr__bnp - ipmha__uihfh)
    np.testing.assert_almost_equal(data[0], lfm__tbke.B.values)
    np.testing.assert_almost_equal(data[1], lfm__tbke.C.values)


if __name__ == '__main__':
    test()
