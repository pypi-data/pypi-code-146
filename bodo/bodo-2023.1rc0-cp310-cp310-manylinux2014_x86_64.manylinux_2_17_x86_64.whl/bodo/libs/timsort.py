import numba
import numpy as np
import pandas as pd
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    ixzs__khxqa = hi - lo
    if ixzs__khxqa < 2:
        return
    if ixzs__khxqa < MIN_MERGE:
        tkswy__uyqrz = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + tkswy__uyqrz, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    kwb__lzi = minRunLength(ixzs__khxqa)
    while True:
        glcri__ltajk = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if glcri__ltajk < kwb__lzi:
            ihv__ftmi = ixzs__khxqa if ixzs__khxqa <= kwb__lzi else kwb__lzi
            binarySort(key_arrs, lo, lo + ihv__ftmi, lo + glcri__ltajk, data)
            glcri__ltajk = ihv__ftmi
        stackSize = pushRun(stackSize, runBase, runLen, lo, glcri__ltajk)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += glcri__ltajk
        ixzs__khxqa -= glcri__ltajk
        if ixzs__khxqa == 0:
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
        obj__ofxxt = getitem_arr_tup(key_arrs, start)
        afzf__mxeg = getitem_arr_tup(data, start)
        gzx__wcyi = lo
        bbtp__qqnc = start
        assert gzx__wcyi <= bbtp__qqnc
        while gzx__wcyi < bbtp__qqnc:
            jsei__bcfd = gzx__wcyi + bbtp__qqnc >> 1
            if obj__ofxxt < getitem_arr_tup(key_arrs, jsei__bcfd):
                bbtp__qqnc = jsei__bcfd
            else:
                gzx__wcyi = jsei__bcfd + 1
        assert gzx__wcyi == bbtp__qqnc
        n = start - gzx__wcyi
        copyRange_tup(key_arrs, gzx__wcyi, key_arrs, gzx__wcyi + 1, n)
        copyRange_tup(data, gzx__wcyi, data, gzx__wcyi + 1, n)
        setitem_arr_tup(key_arrs, gzx__wcyi, obj__ofxxt)
        setitem_arr_tup(data, gzx__wcyi, afzf__mxeg)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    ahgm__wvrkr = lo + 1
    if ahgm__wvrkr == hi:
        return 1
    if getitem_arr_tup(key_arrs, ahgm__wvrkr) < getitem_arr_tup(key_arrs, lo):
        ahgm__wvrkr += 1
        while ahgm__wvrkr < hi and getitem_arr_tup(key_arrs, ahgm__wvrkr
            ) < getitem_arr_tup(key_arrs, ahgm__wvrkr - 1):
            ahgm__wvrkr += 1
        reverseRange(key_arrs, lo, ahgm__wvrkr, data)
    else:
        ahgm__wvrkr += 1
        while ahgm__wvrkr < hi and getitem_arr_tup(key_arrs, ahgm__wvrkr
            ) >= getitem_arr_tup(key_arrs, ahgm__wvrkr - 1):
            ahgm__wvrkr += 1
    return ahgm__wvrkr - lo


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
    wxvvp__sbmsm = 0
    while n >= MIN_MERGE:
        wxvvp__sbmsm |= n & 1
        n >>= 1
    return n + wxvvp__sbmsm


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    raux__iqom = len(key_arrs[0])
    tmpLength = (raux__iqom >> 1 if raux__iqom < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    aqzf__zgeke = (5 if raux__iqom < 120 else 10 if raux__iqom < 1542 else 
        19 if raux__iqom < 119151 else 40)
    runBase = np.empty(aqzf__zgeke, np.int64)
    runLen = np.empty(aqzf__zgeke, np.int64)
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
    xti__depgy = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert xti__depgy >= 0
    base1 += xti__depgy
    len1 -= xti__depgy
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
    fgr__upn = 0
    cnkhq__rvvdk = 1
    if key > getitem_arr_tup(arr, base + hint):
        hkxb__hekie = _len - hint
        while cnkhq__rvvdk < hkxb__hekie and key > getitem_arr_tup(arr, 
            base + hint + cnkhq__rvvdk):
            fgr__upn = cnkhq__rvvdk
            cnkhq__rvvdk = (cnkhq__rvvdk << 1) + 1
            if cnkhq__rvvdk <= 0:
                cnkhq__rvvdk = hkxb__hekie
        if cnkhq__rvvdk > hkxb__hekie:
            cnkhq__rvvdk = hkxb__hekie
        fgr__upn += hint
        cnkhq__rvvdk += hint
    else:
        hkxb__hekie = hint + 1
        while cnkhq__rvvdk < hkxb__hekie and key <= getitem_arr_tup(arr, 
            base + hint - cnkhq__rvvdk):
            fgr__upn = cnkhq__rvvdk
            cnkhq__rvvdk = (cnkhq__rvvdk << 1) + 1
            if cnkhq__rvvdk <= 0:
                cnkhq__rvvdk = hkxb__hekie
        if cnkhq__rvvdk > hkxb__hekie:
            cnkhq__rvvdk = hkxb__hekie
        tmp = fgr__upn
        fgr__upn = hint - cnkhq__rvvdk
        cnkhq__rvvdk = hint - tmp
    assert -1 <= fgr__upn and fgr__upn < cnkhq__rvvdk and cnkhq__rvvdk <= _len
    fgr__upn += 1
    while fgr__upn < cnkhq__rvvdk:
        kdw__bjztb = fgr__upn + (cnkhq__rvvdk - fgr__upn >> 1)
        if key > getitem_arr_tup(arr, base + kdw__bjztb):
            fgr__upn = kdw__bjztb + 1
        else:
            cnkhq__rvvdk = kdw__bjztb
    assert fgr__upn == cnkhq__rvvdk
    return cnkhq__rvvdk


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    cnkhq__rvvdk = 1
    fgr__upn = 0
    if key < getitem_arr_tup(arr, base + hint):
        hkxb__hekie = hint + 1
        while cnkhq__rvvdk < hkxb__hekie and key < getitem_arr_tup(arr, 
            base + hint - cnkhq__rvvdk):
            fgr__upn = cnkhq__rvvdk
            cnkhq__rvvdk = (cnkhq__rvvdk << 1) + 1
            if cnkhq__rvvdk <= 0:
                cnkhq__rvvdk = hkxb__hekie
        if cnkhq__rvvdk > hkxb__hekie:
            cnkhq__rvvdk = hkxb__hekie
        tmp = fgr__upn
        fgr__upn = hint - cnkhq__rvvdk
        cnkhq__rvvdk = hint - tmp
    else:
        hkxb__hekie = _len - hint
        while cnkhq__rvvdk < hkxb__hekie and key >= getitem_arr_tup(arr, 
            base + hint + cnkhq__rvvdk):
            fgr__upn = cnkhq__rvvdk
            cnkhq__rvvdk = (cnkhq__rvvdk << 1) + 1
            if cnkhq__rvvdk <= 0:
                cnkhq__rvvdk = hkxb__hekie
        if cnkhq__rvvdk > hkxb__hekie:
            cnkhq__rvvdk = hkxb__hekie
        fgr__upn += hint
        cnkhq__rvvdk += hint
    assert -1 <= fgr__upn and fgr__upn < cnkhq__rvvdk and cnkhq__rvvdk <= _len
    fgr__upn += 1
    while fgr__upn < cnkhq__rvvdk:
        kdw__bjztb = fgr__upn + (cnkhq__rvvdk - fgr__upn >> 1)
        if key < getitem_arr_tup(arr, base + kdw__bjztb):
            cnkhq__rvvdk = kdw__bjztb
        else:
            fgr__upn = kdw__bjztb + 1
    assert fgr__upn == cnkhq__rvvdk
    return cnkhq__rvvdk


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
        iuu__cjwtx = 0
        mpqu__xrd = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                mpqu__xrd += 1
                iuu__cjwtx = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                iuu__cjwtx += 1
                mpqu__xrd = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not iuu__cjwtx | mpqu__xrd < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            iuu__cjwtx = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if iuu__cjwtx != 0:
                copyRange_tup(tmp, cursor1, arr, dest, iuu__cjwtx)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, iuu__cjwtx)
                dest += iuu__cjwtx
                cursor1 += iuu__cjwtx
                len1 -= iuu__cjwtx
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            mpqu__xrd = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if mpqu__xrd != 0:
                copyRange_tup(arr, cursor2, arr, dest, mpqu__xrd)
                copyRange_tup(arr_data, cursor2, arr_data, dest, mpqu__xrd)
                dest += mpqu__xrd
                cursor2 += mpqu__xrd
                len2 -= mpqu__xrd
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
            if not iuu__cjwtx >= MIN_GALLOP | mpqu__xrd >= MIN_GALLOP:
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
        iuu__cjwtx = 0
        mpqu__xrd = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                iuu__cjwtx += 1
                mpqu__xrd = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                mpqu__xrd += 1
                iuu__cjwtx = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not iuu__cjwtx | mpqu__xrd < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            iuu__cjwtx = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if iuu__cjwtx != 0:
                dest -= iuu__cjwtx
                cursor1 -= iuu__cjwtx
                len1 -= iuu__cjwtx
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, iuu__cjwtx)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    iuu__cjwtx)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            mpqu__xrd = len2 - gallopLeft(getitem_arr_tup(arr, cursor1),
                tmp, 0, len2, len2 - 1)
            if mpqu__xrd != 0:
                dest -= mpqu__xrd
                cursor2 -= mpqu__xrd
                len2 -= mpqu__xrd
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, mpqu__xrd)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    mpqu__xrd)
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
            if not iuu__cjwtx >= MIN_GALLOP | mpqu__xrd >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    nfy__dlfdx = len(key_arrs[0])
    if tmpLength < minCapacity:
        jhn__xbdz = minCapacity
        jhn__xbdz |= jhn__xbdz >> 1
        jhn__xbdz |= jhn__xbdz >> 2
        jhn__xbdz |= jhn__xbdz >> 4
        jhn__xbdz |= jhn__xbdz >> 8
        jhn__xbdz |= jhn__xbdz >> 16
        jhn__xbdz += 1
        if jhn__xbdz < 0:
            jhn__xbdz = minCapacity
        else:
            jhn__xbdz = min(jhn__xbdz, nfy__dlfdx >> 1)
        tmp = alloc_arr_tup(jhn__xbdz, key_arrs)
        tmp_data = alloc_arr_tup(jhn__xbdz, data)
        tmpLength = jhn__xbdz
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        kyr__leky = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = kyr__leky


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    qxseh__ygq = arr_tup.count
    twog__qxhg = 'def f(arr_tup, lo, hi):\n'
    for i in range(qxseh__ygq):
        twog__qxhg += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        twog__qxhg += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        twog__qxhg += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    twog__qxhg += '  return\n'
    akpt__ewfi = {}
    exec(twog__qxhg, {}, akpt__ewfi)
    winc__ysuez = akpt__ewfi['f']
    return winc__ysuez


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    qxseh__ygq = src_arr_tup.count
    assert qxseh__ygq == dst_arr_tup.count
    twog__qxhg = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(qxseh__ygq):
        twog__qxhg += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    twog__qxhg += '  return\n'
    akpt__ewfi = {}
    exec(twog__qxhg, {'copyRange': copyRange}, akpt__ewfi)
    ovkc__bvk = akpt__ewfi['f']
    return ovkc__bvk


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    qxseh__ygq = src_arr_tup.count
    assert qxseh__ygq == dst_arr_tup.count
    twog__qxhg = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(qxseh__ygq):
        twog__qxhg += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    twog__qxhg += '  return\n'
    akpt__ewfi = {}
    exec(twog__qxhg, {'copyElement': copyElement}, akpt__ewfi)
    ovkc__bvk = akpt__ewfi['f']
    return ovkc__bvk


def getitem_arr_tup(arr_tup, ind):
    vtn__dmikz = [arr[ind] for arr in arr_tup]
    return tuple(vtn__dmikz)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    qxseh__ygq = arr_tup.count
    twog__qxhg = 'def f(arr_tup, ind):\n'
    twog__qxhg += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'.
        format(i) for i in range(qxseh__ygq)]), ',' if qxseh__ygq == 1 else '')
    akpt__ewfi = {}
    exec(twog__qxhg, {}, akpt__ewfi)
    vwz__qfsd = akpt__ewfi['f']
    return vwz__qfsd


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, qxrmd__cea in zip(arr_tup, val_tup):
        arr[ind] = qxrmd__cea


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    qxseh__ygq = arr_tup.count
    twog__qxhg = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(qxseh__ygq):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            twog__qxhg += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            twog__qxhg += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    twog__qxhg += '  return\n'
    akpt__ewfi = {}
    exec(twog__qxhg, {}, akpt__ewfi)
    vwz__qfsd = akpt__ewfi['f']
    return vwz__qfsd


def test():
    import time
    fyabf__tawm = time.time()
    vqugb__dsp = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((vqugb__dsp,), 0, 3, data)
    print('compile time', time.time() - fyabf__tawm)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    brum__mzi = np.random.ranf(n)
    kfoit__eirs = pd.DataFrame({'A': brum__mzi, 'B': data[0], 'C': data[1]})
    fyabf__tawm = time.time()
    npi__ckyib = kfoit__eirs.sort_values('A', inplace=False)
    mhdhw__lqq = time.time()
    sort((brum__mzi,), 0, n, data)
    print('Bodo', time.time() - mhdhw__lqq, 'Numpy', mhdhw__lqq - fyabf__tawm)
    np.testing.assert_almost_equal(data[0], npi__ckyib.B.values)
    np.testing.assert_almost_equal(data[1], npi__ckyib.C.values)


if __name__ == '__main__':
    test()
