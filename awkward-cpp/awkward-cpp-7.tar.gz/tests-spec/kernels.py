
from numpy import uint8
kMaxInt64  = 9223372036854775806
kSliceNone = kMaxInt64 + 1
def awkward_BitMaskedArray_to_ByteMaskedArray(
    tobytemask, frombitmask, bitmasklength, validwhen, lsb_order
):
    if lsb_order:
        for i in range(bitmasklength):
            byte = frombitmask[i]
            tobytemask[(i * 8) + 0] = (byte & uint8(1)) != validwhen
            byte >>= 1
            tobytemask[(i * 8) + 1] = (byte & uint8(1)) != validwhen
            byte >>= 1
            tobytemask[(i * 8) + 2] = (byte & uint8(1)) != validwhen
            byte >>= 1
            tobytemask[(i * 8) + 3] = (byte & uint8(1)) != validwhen
            byte >>= 1
            tobytemask[(i * 8) + 4] = (byte & uint8(1)) != validwhen
            byte >>= 1
            tobytemask[(i * 8) + 5] = (byte & uint8(1)) != validwhen
            byte >>= 1
            tobytemask[(i * 8) + 6] = (byte & uint8(1)) != validwhen
            byte >>= 1
            tobytemask[(i * 8) + 7] = (byte & uint8(1)) != validwhen
    else:
        for i in range(bitmasklength):
            byte = frombitmask[i]
            tobytemask[(i * 8) + 0] = ((byte & uint8(128)) != 0) != validwhen
            byte <<= 1
            tobytemask[(i * 8) + 1] = ((byte & uint8(128)) != 0) != validwhen
            byte <<= 1
            tobytemask[(i * 8) + 2] = ((byte & uint8(128)) != 0) != validwhen
            byte <<= 1
            tobytemask[(i * 8) + 3] = ((byte & uint8(128)) != 0) != validwhen
            byte <<= 1
            tobytemask[(i * 8) + 4] = ((byte & uint8(128)) != 0) != validwhen
            byte <<= 1
            tobytemask[(i * 8) + 5] = ((byte & uint8(128)) != 0) != validwhen
            byte <<= 1
            tobytemask[(i * 8) + 6] = ((byte & uint8(128)) != 0) != validwhen
            byte <<= 1
            tobytemask[(i * 8) + 7] = ((byte & uint8(128)) != 0) != validwhen

awkward_BitMaskedArray_to_ByteMaskedArray = awkward_BitMaskedArray_to_ByteMaskedArray


def awkward_BitMaskedArray_to_IndexedOptionArray(
    toindex, frombitmask, bitmasklength, validwhen, lsb_order
):
    if lsb_order:
        for i in range(bitmasklength):
            byte = frombitmask[i]
            if (byte & uint8(1)) == validwhen:
                toindex[(i * 8) + 0] = (i * 8) + 0
            else:
                toindex[(i * 8) + 0] = -1
            byte >>= 1
            if (byte & uint8(1)) == validwhen:
                toindex[(i * 8) + 1] = (i * 8) + 1
            else:
                toindex[(i * 8) + 1] = -1
            byte >>= 1
            if (byte & uint8(1)) == validwhen:
                toindex[(i * 8) + 2] = (i * 8) + 2
            else:
                toindex[(i * 8) + 2] = -1
            byte >>= 1
            if (byte & uint8(1)) == validwhen:
                toindex[(i * 8) + 3] = (i * 8) + 3
            else:
                toindex[(i * 8) + 3] = -1
            byte >>= 1
            if (byte & uint8(1)) == validwhen:
                toindex[(i * 8) + 4] = (i * 8) + 4
            else:
                toindex[(i * 8) + 4] = -1
            byte >>= 1
            if (byte & uint8(1)) == validwhen:
                toindex[(i * 8) + 5] = (i * 8) + 5
            else:
                toindex[(i * 8) + 5] = -1
            byte >>= 1
            if (byte & uint8(1)) == validwhen:
                toindex[(i * 8) + 6] = (i * 8) + 6
            else:
                toindex[(i * 8) + 6] = -1
            byte >>= 1
            if (byte & uint8(1)) == validwhen:
                toindex[(i * 8) + 7] = (i * 8) + 7
            else:
                toindex[(i * 8) + 7] = -1
    else:
        for i in range(bitmasklength):
            byte = frombitmask[i]
            if ((byte & uint8(128)) != 0) == validwhen:
                toindex[(i * 8) + 0] = (i * 8) + 0
            else:
                toindex[(i * 8) + 0] = -1
            byte <<= 1
            if ((byte & uint8(128)) != 0) == validwhen:
                toindex[(i * 8) + 1] = (i * 8) + 1
            else:
                toindex[(i * 8) + 1] = -1
            byte <<= 1
            if ((byte & uint8(128)) != 0) == validwhen:
                toindex[(i * 8) + 2] = (i * 8) + 2
            else:
                toindex[(i * 8) + 2] = -1
            byte <<= 1
            if ((byte & uint8(128)) != 0) == validwhen:
                toindex[(i * 8) + 3] = (i * 8) + 3
            else:
                toindex[(i * 8) + 3] = -1
            byte <<= 1
            if ((byte & uint8(128)) != 0) == validwhen:
                toindex[(i * 8) + 4] = (i * 8) + 4
            else:
                toindex[(i * 8) + 4] = -1
            byte <<= 1
            if ((byte & uint8(128)) != 0) == validwhen:
                toindex[(i * 8) + 5] = (i * 8) + 5
            else:
                toindex[(i * 8) + 5] = -1
            byte <<= 1
            if ((byte & uint8(128)) != 0) == validwhen:
                toindex[(i * 8) + 6] = (i * 8) + 6
            else:
                toindex[(i * 8) + 6] = -1
            byte <<= 1
            if ((byte & uint8(128)) != 0) == validwhen:
                toindex[(i * 8) + 7] = (i * 8) + 7
            else:
                toindex[(i * 8) + 7] = -1

awkward_BitMaskedArray_to_IndexedOptionArray64 = awkward_BitMaskedArray_to_IndexedOptionArray


def awkward_ByteMaskedArray_getitem_nextcarry(tocarry, mask, length, validwhen):
    k = 0
    for i in range(length):
        if (mask[i] != 0) == validwhen:
            tocarry[k] = i
            k = k + 1

awkward_ByteMaskedArray_getitem_nextcarry_64 = awkward_ByteMaskedArray_getitem_nextcarry


def awkward_ByteMaskedArray_getitem_nextcarry_outindex(
    tocarry, outindex, mask, length, validwhen
):
    k = 0
    for i in range(length):
        if (mask[i] != 0) == validwhen:
            tocarry[k] = i
            outindex[i] = float(k)
            k = k + 1
        else:
            outindex[i] = -1

awkward_ByteMaskedArray_getitem_nextcarry_outindex_64 = awkward_ByteMaskedArray_getitem_nextcarry_outindex


def awkward_ByteMaskedArray_numnull(numnull, mask, length, validwhen):
    numnull[0] = 0
    for i in range(length):
        if (mask[i] != 0) != validwhen:
            numnull[0] = numnull[0] + 1

awkward_ByteMaskedArray_numnull = awkward_ByteMaskedArray_numnull


def awkward_ByteMaskedArray_overlay_mask(tomask, theirmask, mymask, length, validwhen):
    for i in range(length):
        theirs = theirmask[i]
        mine = (mymask[i] != 0) != validwhen
        tomask[i] = 1 if theirs | mine else 0

awkward_ByteMaskedArray_overlay_mask8 = awkward_ByteMaskedArray_overlay_mask


def awkward_ByteMaskedArray_reduce_next_64(
    nextcarry, nextparents, outindex, mask, parents, length, validwhen
):
    k = 0
    for i in range(length):
        if (mask[i] != 0) == validwhen:
            nextcarry[k] = i
            nextparents[k] = parents[i]
            outindex[i] = k
            k = k + 1
        else:
            outindex[i] = -1

awkward_ByteMaskedArray_reduce_next_64 = awkward_ByteMaskedArray_reduce_next_64


def awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64(
    nextshifts, mask, length, valid_when
):
    nullsum = 0
    k = 0
    for i in range(length):
        if (mask[i] != 0) == (valid_when != 0):
            nextshifts[k] = nullsum
            k = k + 1
        else:
            nullsum = nullsum + 1

awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64 = awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64


def awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_fromshifts_64(
    nextshifts, mask, length, valid_when, shifts
):
    nullsum = 0
    k = 0
    for i in range(length):
        if (mask[i] != 0) == (valid_when != 0):
            nextshifts[k] = shifts[i] + nullsum
            k = k + 1
        else:
            nullsum = nullsum + 1

awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_fromshifts_64 = awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_fromshifts_64


def awkward_ByteMaskedArray_toIndexedOptionArray(toindex, mask, length, validwhen):
    for i in range(length):
        toindex[i] = i if (mask[i] != 0) == validwhen else -1

awkward_ByteMaskedArray_toIndexedOptionArray64 = awkward_ByteMaskedArray_toIndexedOptionArray


def awkward_Content_getitem_next_missing_jagged_getmaskstartstop(
    index_in, offsets_in, mask_out, starts_out, stops_out, length
):
    k = 0
    for i in range(length):
        starts_out[i] = offsets_in[k]
        if index_in[i] < 0:
            mask_out[i] = -1
            stops_out[i] = offsets_in[k]
        else:
            mask_out[i] = i
            k = k + 1
            stops_out[i] = offsets_in[k]

awkward_Content_getitem_next_missing_jagged_getmaskstartstop = awkward_Content_getitem_next_missing_jagged_getmaskstartstop


def awkward_Index_iscontiguous(result, fromindex, length):
    result[0] = True
    expecting = 0
    for i in range(length):
        if fromindex[i] != expecting:
            result[0] = False
            return
        expecting += 1

awkward_Index32_iscontiguous = awkward_Index_iscontiguous
awkward_Index64_iscontiguous = awkward_Index_iscontiguous
awkward_Index8_iscontiguous = awkward_Index_iscontiguous
awkward_IndexU32_iscontiguous = awkward_Index_iscontiguous
awkward_IndexU8_iscontiguous = awkward_Index_iscontiguous


def awkward_IndexedArray_fill(toindex, toindexoffset, fromindex, length, base):
    for i in range(length):
        fromval = fromindex[i]
        toindex[toindexoffset + i] = -1 if fromval < 0 else float(fromval + base)

awkward_IndexedArray_fill_to64_from32 = awkward_IndexedArray_fill
awkward_IndexedArray_fill_to64_from64 = awkward_IndexedArray_fill
awkward_IndexedArray_fill_to64_fromU32 = awkward_IndexedArray_fill


def awkward_IndexedArray_fill_count(toindex, toindexoffset, length, base):
    for i in range(length):
        toindex[toindexoffset + i] = i + base

awkward_IndexedArray_fill_to64_count = awkward_IndexedArray_fill_count


def awkward_IndexedArray_flatten_nextcarry(tocarry, fromindex, lenindex, lencontent):
    k = 0
    for i in range(lenindex):
        j = fromindex[i]
        if j >= lencontent:
            raise ValueError("index out of range")
        else:
            if j >= 0:
                tocarry[k] = j
                k = k + 1

awkward_IndexedArray32_flatten_nextcarry_64 = awkward_IndexedArray_flatten_nextcarry
awkward_IndexedArray64_flatten_nextcarry_64 = awkward_IndexedArray_flatten_nextcarry
awkward_IndexedArrayU32_flatten_nextcarry_64 = awkward_IndexedArray_flatten_nextcarry


def awkward_IndexedArray_flatten_none2empty(
    outoffsets, outindex, outindexlength, offsets, offsetslength
):
    outoffsets[0] = offsets[0]
    k = 1
    for i in range(outindexlength):
        idx = outindex[i]
        if idx < 0:
            outoffsets[k] = outoffsets[k - 1]
            k = k + 1
        else:
            if (idx + 1) >= offsetslength:
                raise ValueError("flattening offset out of range")
            else:
                count = offsets[idx + 1] - offsets[idx]
                outoffsets[k] = outoffsets[k - 1] + count
                k = k + 1

awkward_IndexedArray32_flatten_none2empty_64 = awkward_IndexedArray_flatten_none2empty
awkward_IndexedArray64_flatten_none2empty_64 = awkward_IndexedArray_flatten_none2empty
awkward_IndexedArrayU32_flatten_none2empty_64 = awkward_IndexedArray_flatten_none2empty


def awkward_IndexedArray_getitem_nextcarry(tocarry, fromindex, lenindex, lencontent):
    k = 0
    for i in range(lenindex):
        j = fromindex[i]
        if (j < 0) or (j >= lencontent):
            raise ValueError("index out of range")
        else:
            tocarry[k] = j
            k = k + 1

awkward_IndexedArray32_getitem_nextcarry_64 = awkward_IndexedArray_getitem_nextcarry
awkward_IndexedArray64_getitem_nextcarry_64 = awkward_IndexedArray_getitem_nextcarry
awkward_IndexedArrayU32_getitem_nextcarry_64 = awkward_IndexedArray_getitem_nextcarry


def awkward_IndexedArray_getitem_nextcarry_outindex(
    tocarry, toindex, fromindex, lenindex, lencontent
):
    k = 0
    for i in range(lenindex):
        j = fromindex[i]
        if j >= lencontent:
            raise ValueError("index out of range")
        else:
            if j < 0:
                toindex[i] = -1
            else:
                tocarry[k] = j
                toindex[i] = float(k)
                k = k + 1

awkward_IndexedArray32_getitem_nextcarry_outindex_64 = awkward_IndexedArray_getitem_nextcarry_outindex
awkward_IndexedArray64_getitem_nextcarry_outindex_64 = awkward_IndexedArray_getitem_nextcarry_outindex
awkward_IndexedArrayU32_getitem_nextcarry_outindex_64 = awkward_IndexedArray_getitem_nextcarry_outindex


def awkward_IndexedArray_numnull(numnull, fromindex, lenindex):
    numnull[0] = 0
    for i in range(lenindex):
        if fromindex[i] < 0:
            numnull[0] = numnull[0] + 1

awkward_IndexedArray32_numnull = awkward_IndexedArray_numnull
awkward_IndexedArray64_numnull = awkward_IndexedArray_numnull
awkward_IndexedArrayU32_numnull = awkward_IndexedArray_numnull


def awkward_IndexedArray_numnull_parents(numnull, tolength, fromindex, lenindex):
    tolength[0] = 0
    for i in range(lenindex):
        if fromindex[i] < 0:
            numnull[i] = 1
            tolength[0] = tolength[0] + 1
        else:
            numnull[i] = 0

awkward_IndexedArray32_numnull_parents = awkward_IndexedArray_numnull_parents
awkward_IndexedArray64_numnull_parents = awkward_IndexedArray_numnull_parents
awkward_IndexedArrayU32_numnull_parents = awkward_IndexedArray_numnull_parents


def awkward_IndexedArray_numnull_unique_64(toindex, lenindex):
    for i in range(lenindex):
        toindex[i] = i
    toindex[-1] = -1

awkward_IndexedArray_numnull_unique_64 = awkward_IndexedArray_numnull_unique_64


def awkward_IndexedArray_index_of_nulls(toindex, fromindex, lenindex, parents, starts):
    j = 0
    for i in range(lenindex):
        if fromindex[i] < 0:
            parent = parents[i]
            start = starts[parent]
            toindex[j] = i - start
            j = j + 1

awkward_IndexedArray32_index_of_nulls = awkward_IndexedArray_index_of_nulls
awkward_IndexedArray64_index_of_nulls = awkward_IndexedArray_index_of_nulls
awkward_IndexedArrayU32_index_of_nulls = awkward_IndexedArray_index_of_nulls


def awkward_IndexedArray_overlay_mask(toindex, mask, fromindex, length):
    for i in range(length):
        m = mask[i]
        toindex[i] = -1 if m else fromindex[i]

awkward_IndexedArray32_overlay_mask8_to64 = awkward_IndexedArray_overlay_mask
awkward_IndexedArray64_overlay_mask8_to64 = awkward_IndexedArray_overlay_mask
awkward_IndexedArrayU32_overlay_mask8_to64 = awkward_IndexedArray_overlay_mask


def awkward_IndexedArray_reduce_next_64(
    nextcarry, nextparents, outindex, index, parents, length
):
    k = 0
    for i in range(length):
        if index[i] >= 0:
            nextcarry[k] = index[i]
            nextparents[k] = parents[i]
            outindex[i] = k
            k = k + 1
        else:
            outindex[i] = -1

awkward_IndexedArray32_reduce_next_64 = awkward_IndexedArray_reduce_next_64
awkward_IndexedArray64_reduce_next_64 = awkward_IndexedArray_reduce_next_64
awkward_IndexedArrayU32_reduce_next_64 = awkward_IndexedArray_reduce_next_64


def awkward_IndexedArray_reduce_next_fix_offsets_64(
    outoffsets, starts, startslength, outindexlength
):
    for i in range(startslength):
        outoffsets[i] = starts[i]
    outoffsets[startslength] = outindexlength

awkward_IndexedArray_reduce_next_fix_offsets_64 = awkward_IndexedArray_reduce_next_fix_offsets_64


def awkward_IndexedArray_unique_next_index_and_offsets_64(
    toindex, tooffsets, fromoffsets, fromnulls, startslength
):
    k = 0
    ll = 0
    shift = 0
    toindex[0] = ll
    tooffsets[0] = fromoffsets[0]
    for i in range(startslength):
        for _j in range(fromoffsets[i], fromoffsets[i + 1]):
            toindex[k] = ll
            k += 1
            ll += 1
            if fromnulls[k] == 1:
                toindex[k] = -1
                k += 1
                shift += 1
            tooffsets[i + 1] = fromoffsets[i + 1] + shift

awkward_IndexedArray_unique_next_index_and_offsets_64 = awkward_IndexedArray_unique_next_index_and_offsets_64


def awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64(nextshifts, index, length):
    nullsum = 0
    k = 0
    for i in range(length):
        if index[i] >= 0:
            nextshifts[k] = nullsum
            k = k + 1
        else:
            nullsum = nullsum + 1

awkward_IndexedArray32_reduce_next_nonlocal_nextshifts_64 = awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64
awkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64 = awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64
awkward_IndexedArrayU32_reduce_next_nonlocal_nextshifts_64 = awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64


def awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64(
    nextshifts, index, length, shifts
):
    nullsum = 0
    k = 0
    for i in range(length):
        if index[i] >= 0:
            nextshifts[k] = shifts[i] + nullsum
            k = k + 1
        else:
            nullsum = nullsum + 1

awkward_IndexedArray32_reduce_next_nonlocal_nextshifts_fromshifts_64 = awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64
awkward_IndexedArray64_reduce_next_nonlocal_nextshifts_fromshifts_64 = awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64
awkward_IndexedArrayU32_reduce_next_nonlocal_nextshifts_fromshifts_64 = awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64


def awkward_IndexedArray_simplify(
    toindex, outerindex, outerlength, innerindex, innerlength
):
    for i in range(outerlength):
        j = outerindex[i]
        if j < 0:
            toindex[i] = -1
        else:
            if j >= innerlength:
                raise ValueError("index out of range")
            else:
                toindex[i] = innerindex[j]

awkward_IndexedArray32_simplify32_to64 = awkward_IndexedArray_simplify
awkward_IndexedArray32_simplify64_to64 = awkward_IndexedArray_simplify
awkward_IndexedArray32_simplifyU32_to64 = awkward_IndexedArray_simplify
awkward_IndexedArray64_simplify32_to64 = awkward_IndexedArray_simplify
awkward_IndexedArray64_simplify64_to64 = awkward_IndexedArray_simplify
awkward_IndexedArray64_simplifyU32_to64 = awkward_IndexedArray_simplify
awkward_IndexedArrayU32_simplify32_to64 = awkward_IndexedArray_simplify
awkward_IndexedArrayU32_simplify64_to64 = awkward_IndexedArray_simplify
awkward_IndexedArrayU32_simplifyU32_to64 = awkward_IndexedArray_simplify


def awkward_IndexedArray_validity(index, length, lencontent, isoption):
    for i in range(length):
        idx = index[i]
        if not (isoption):
            if idx < 0:
                raise ValueError("index[i] < 0")
        if idx >= lencontent:
            raise ValueError("index[i] >= len(content)")

awkward_IndexedArray32_validity = awkward_IndexedArray_validity
awkward_IndexedArray64_validity = awkward_IndexedArray_validity
awkward_IndexedArrayU32_validity = awkward_IndexedArray_validity


def awkward_IndexedArray_ranges_next_64(
    index, fromstarts, fromstops, length, tostarts, tostops, tolength
):
    k = 0
    for i in range(length):
        stride = fromstops[i] - fromstarts[i]
        tostarts[i] = k
        for j in range(stride):
            if index[fromstarts[i] + j] > 0:
                k = k + 1
        tostops[i] = k
    tolength = k

awkward_IndexedArray32_ranges_next_64 = awkward_IndexedArray_ranges_next_64
awkward_IndexedArray64_ranges_next_64 = awkward_IndexedArray_ranges_next_64
awkward_IndexedArrayU32_ranges_next_64 = awkward_IndexedArray_ranges_next_64


def awkward_IndexedArray_ranges_carry_next_64(
    index, fromstarts, fromstops, length, tocarry
):
    k = 0
    for i in range(length):
        stride = fromstops[i] - fromstarts[i]
        for j in range(stride):
            if index[fromstarts[i] + j] > 0:
                tocarry[k] = index[fromstarts[i] + j]
                k = k + 1

awkward_IndexedArray32_ranges_carry_next_64 = awkward_IndexedArray_ranges_carry_next_64
awkward_IndexedArray64_ranges_carry_next_64 = awkward_IndexedArray_ranges_carry_next_64
awkward_IndexedArrayU32_ranges_carry_next_64 = awkward_IndexedArray_ranges_carry_next_64


def awkward_IndexedOptionArray_rpad_and_clip_mask_axis1(toindex, frommask, length):
    count = 0
    for i in range(length):
        if frommask[i]:
            toindex[i] = -1
        else:
            toindex[i] = count
            count = count + 1

awkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64 = awkward_IndexedOptionArray_rpad_and_clip_mask_axis1


def awkward_ListArray_broadcast_tooffsets(
    tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent
):
    k = 0
    for i in range(offsetslength - 1):
        start = int(fromstarts[i])
        stop = int(fromstops[i])
        if (start != stop) and (stop > lencontent):
            raise ValueError("stops[i] > len(content)")
        count = int(fromoffsets[i + 1] - fromoffsets[i])
        if count < 0:
            raise ValueError("broadcast's offsets must be monotonically increasing")
        if (stop - start) != count:
            raise ValueError("cannot broadcast nested list")
        for j in range(start, stop):
            tocarry[k] = float(j)
            k = k + 1

awkward_ListArray32_broadcast_tooffsets_64 = awkward_ListArray_broadcast_tooffsets
awkward_ListArray64_broadcast_tooffsets_64 = awkward_ListArray_broadcast_tooffsets
awkward_ListArrayU32_broadcast_tooffsets_64 = awkward_ListArray_broadcast_tooffsets


def awkward_ListArray_combinations_length(
    totallen, tooffsets, n, replacement, starts, stops, length
):
    totallen[0] = 0
    tooffsets[0] = 0
    for i in range(length):
        size = int(stops[i] - starts[i])
        if replacement:
            size += n - 1
        thisn = n

        if thisn > size:
            combinationslen = 0
        else:
            if thisn == size:
                combinationslen = 1
            else:
                if (thisn * 2) > size:
                    thisn = size - thisn
                combinationslen = size
                j = 2
                while j <= thisn:
                    combinationslen *= (size - j) + 1
                    combinationslen /= j
                    j = j + 1
        totallen[0] = totallen[0] + combinationslen
        tooffsets[i + 1] = tooffsets[i] + combinationslen

awkward_ListArray32_combinations_length_64 = awkward_ListArray_combinations_length
awkward_ListArray64_combinations_length_64 = awkward_ListArray_combinations_length
awkward_ListArrayU32_combinations_length_64 = awkward_ListArray_combinations_length


def awkward_ListArray_compact_offsets(tooffsets, fromstarts, fromstops, length):
    tooffsets[0] = 0
    for i in range(length):
        start = fromstarts[i]
        stop = fromstops[i]
        if stop < start:
            raise ValueError("stops[i] < starts[i]")
        tooffsets[i + 1] = tooffsets[i] + (stop - start)

awkward_ListArray32_compact_offsets_64 = awkward_ListArray_compact_offsets
awkward_ListArray64_compact_offsets_64 = awkward_ListArray_compact_offsets
awkward_ListArrayU32_compact_offsets_64 = awkward_ListArray_compact_offsets


def awkward_ListArray_fill(
    tostarts,
    tostartsoffset,
    tostops,
    tostopsoffset,
    fromstarts,
    fromstops,
    length,
    base,
):
    for i in range(length):
        tostarts[tostartsoffset + i] = float(fromstarts[i] + base)
        tostops[tostopsoffset + i] = float(fromstops[i] + base)

awkward_ListArray_fill_to64_from32 = awkward_ListArray_fill
awkward_ListArray_fill_to64_from64 = awkward_ListArray_fill
awkward_ListArray_fill_to64_fromU32 = awkward_ListArray_fill


def awkward_ListArray_getitem_jagged_apply(
    tooffsets,
    tocarry,
    slicestarts,
    slicestops,
    sliceouterlen,
    sliceindex,
    sliceinnerlen,
    fromstarts,
    fromstops,
    contentlen,
):
    k = 0
    for i in range(sliceouterlen):
        slicestart = slicestarts[i]
        slicestop = slicestops[i]
        tooffsets[i] = float(k)
        if slicestart != slicestop:
            if slicestop < slicestart:
                raise ValueError("jagged slice's stops[i] < starts[i]")
            if slicestop > sliceinnerlen:
                raise ValueError("jagged slice's offsets extend beyond its content")
            start = int(fromstarts[i])
            stop = int(fromstops[i])
            if stop < start:
                raise ValueError("stops[i] < starts[i]")
            if (start != stop) and (stop > contentlen):
                raise ValueError("stops[i] > len(content)")
            count = stop - start
            for j in range(slicestart, slicestop):
                index = int(sliceindex[j])
                if index < 0:
                    index += count
                if not ((0 <= index) and (index < count)):
                    raise ValueError("index out of range")
                tocarry[k] = start + index
                k = k + 1
        tooffsets[i + 1] = float(k)

awkward_ListArray32_getitem_jagged_apply_64 = awkward_ListArray_getitem_jagged_apply
awkward_ListArray64_getitem_jagged_apply_64 = awkward_ListArray_getitem_jagged_apply
awkward_ListArrayU32_getitem_jagged_apply_64 = awkward_ListArray_getitem_jagged_apply


def awkward_ListArray_getitem_jagged_carrylen(
    carrylen, slicestarts, slicestops, sliceouterlen
):
    carrylen[0] = 0
    for i in range(sliceouterlen):
        carrylen[0] = carrylen[0] + int(slicestops[i] - slicestarts[i])

awkward_ListArray_getitem_jagged_carrylen_64 = awkward_ListArray_getitem_jagged_carrylen


def awkward_ListArray_getitem_jagged_descend(
    tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops
):
    if sliceouterlen == 0:
        tooffsets[0] = 0
    else:
        tooffsets[0] = slicestarts[0]
    for i in range(sliceouterlen):
        slicecount = int(slicestops[i] - slicestarts[i])
        count = int(fromstops[i] - fromstarts[i])
        if slicecount != count:
            raise ValueError(
                "jagged slice inner length differs from array inner length"
            )
        tooffsets[i + 1] = tooffsets[i] + float(count)

awkward_ListArray32_getitem_jagged_descend_64 = awkward_ListArray_getitem_jagged_descend
awkward_ListArray64_getitem_jagged_descend_64 = awkward_ListArray_getitem_jagged_descend
awkward_ListArrayU32_getitem_jagged_descend_64 = awkward_ListArray_getitem_jagged_descend


def awkward_ListArray_getitem_jagged_expand(
    multistarts,
    multistops,
    singleoffsets,
    tocarry,
    fromstarts,
    fromstops,
    jaggedsize,
    length,
):
    for i in range(length):
        start = fromstarts[i]
        stop = fromstops[i]
        if stop < start:
            raise ValueError("stops[i] < starts[i]")
        if (stop - start) != jaggedsize:
            raise ValueError("cannot fit jagged slice into nested list")
        for j in range(jaggedsize):
            multistarts[(i * jaggedsize) + j] = singleoffsets[j]
            multistops[(i * jaggedsize) + j] = singleoffsets[j + 1]
            tocarry[(i * jaggedsize) + j] = start + j

awkward_ListArray32_getitem_jagged_expand_64 = awkward_ListArray_getitem_jagged_expand
awkward_ListArray64_getitem_jagged_expand_64 = awkward_ListArray_getitem_jagged_expand
awkward_ListArrayU32_getitem_jagged_expand_64 = awkward_ListArray_getitem_jagged_expand


def awkward_ListArray_getitem_jagged_numvalid(
    numvalid, slicestarts, slicestops, length, missing, missinglength
):
    numvalid[0] = 0
    for i in range(length):
        slicestart = slicestarts[i]
        slicestop = slicestops[i]
        if slicestart != slicestop:
            if slicestop < slicestart:
                raise ValueError("jagged slice's stops[i] < starts[i]")
            if slicestop > missinglength:
                raise ValueError("jagged slice's offsets extend beyond its content")
            for j in range(slicestart, slicestop):
                numvalid[0] = numvalid[0] + 1 if missing[j] >= 0 else 0

awkward_ListArray_getitem_jagged_numvalid_64 = awkward_ListArray_getitem_jagged_numvalid


def awkward_ListArray_getitem_jagged_shrink(
    tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing
):
    k = 0
    if length == 0:
        tosmalloffsets[0] = 0
        tolargeoffsets[0] = 0
    else:
        tosmalloffsets[0] = slicestarts[0]
        tolargeoffsets[0] = slicestarts[0]
    for i in range(length):
        slicestart = slicestarts[i]
        slicestop = slicestops[i]
        if slicestart != slicestop:
            smallcount = 0
            for j in range(slicestart, slicestop):
                if missing[j] >= 0:
                    tocarry[k] = j
                    k = k + 1
                    smallcount = smallcount + 1
            tosmalloffsets[i + 1] = tosmalloffsets[i] + smallcount
        else:
            tosmalloffsets[i + 1] = tosmalloffsets[i]
        tolargeoffsets[i + 1] = tolargeoffsets[i] + (slicestop - slicestart)

awkward_ListArray_getitem_jagged_shrink_64 = awkward_ListArray_getitem_jagged_shrink


def awkward_ListArray_getitem_next_array(
    tocarry,
    toadvanced,
    fromstarts,
    fromstops,
    fromarray,
    lenstarts,
    lenarray,
    lencontent,
):
    for i in range(lenstarts):
        if fromstops[i] < fromstarts[i]:
            raise ValueError("stops[i] < starts[i]")
        if (fromstarts[i] != fromstops[i]) and (fromstops[i] > lencontent):
            raise ValueError("stops[i] > len(content)")
        length = fromstops[i] - fromstarts[i]
        for j in range(lenarray):
            regular_at = fromarray[j]
            if regular_at < 0:
                regular_at += length
            if not ((0 <= regular_at) and (regular_at < length)):
                raise ValueError("index out of range")
            tocarry[(i * lenarray) + j] = fromstarts[i] + regular_at
            toadvanced[(i * lenarray) + j] = j

awkward_ListArray32_getitem_next_array_64 = awkward_ListArray_getitem_next_array
awkward_ListArray64_getitem_next_array_64 = awkward_ListArray_getitem_next_array
awkward_ListArrayU32_getitem_next_array_64 = awkward_ListArray_getitem_next_array


def awkward_ListArray_getitem_next_array_advanced(
    tocarry,
    toadvanced,
    fromstarts,
    fromstops,
    fromarray,
    fromadvanced,
    lenstarts,
    lenarray,
    lencontent,
):
    for i in range(lenstarts):
        if fromstops[i] < fromstarts[i]:
            raise ValueError("stops[i] < starts[i]")
        if (fromstarts[i] != fromstops[i]) and (fromstops[i] > lencontent):
            raise ValueError("stops[i] > len(content)")
        length = fromstops[i] - fromstarts[i]
        regular_at = fromarray[fromadvanced[i]]
        if regular_at < 0:
            regular_at += length
        if not ((0 <= regular_at) and (regular_at < length)):
            raise ValueError("index out of range")
        tocarry[i] = fromstarts[i] + regular_at
        toadvanced[i] = i

awkward_ListArray32_getitem_next_array_advanced_64 = awkward_ListArray_getitem_next_array_advanced
awkward_ListArray64_getitem_next_array_advanced_64 = awkward_ListArray_getitem_next_array_advanced
awkward_ListArrayU32_getitem_next_array_advanced_64 = awkward_ListArray_getitem_next_array_advanced


def awkward_ListArray_getitem_next_at(tocarry, fromstarts, fromstops, lenstarts, at):
    for i in range(lenstarts):
        length = fromstops[i] - fromstarts[i]
        regular_at = at
        if regular_at < 0:
            regular_at += length
        if not ((0 <= regular_at) and (regular_at < length)):
            raise ValueError("index out of range")
        tocarry[i] = fromstarts[i] + regular_at

awkward_ListArray32_getitem_next_at_64 = awkward_ListArray_getitem_next_at
awkward_ListArray64_getitem_next_at_64 = awkward_ListArray_getitem_next_at
awkward_ListArrayU32_getitem_next_at_64 = awkward_ListArray_getitem_next_at


def awkward_ListArray_getitem_next_range(
    tooffsets, tocarry, fromstarts, fromstops, lenstarts, start, stop, step
):
    k = 0
    tooffsets[0] = 0
    if step > 0:
        for i in range(lenstarts):
            length = fromstops[i] - fromstarts[i]
            regular_start = start
            regular_stop = stop
            awkward_regularize_rangeslice(
                regular_start,
                regular_stop,
                step > 0,
                start != kSliceNone,
                stop != kSliceNone,
                length,
            )
            j = regular_start
            while j < regular_stop:
                tocarry[k] = fromstarts[i] + j
                k = k + 1
                j += step
            tooffsets[i + 1] = float(k)
    else:
        for i in range(lenstarts):
            length = fromstops[i] - fromstarts[i]
            regular_start = start
            regular_stop = stop
            awkward_regularize_rangeslice(
                regular_start,
                regular_stop,
                step > 0,
                start != kSliceNone,
                stop != kSliceNone,
                length,
            )
            j = regular_start
            while j > regular_stop:
                tocarry[k] = fromstarts[i] + j
                k = k + 1
                j += step
            tooffsets[i + 1] = float(k)

awkward_ListArray32_getitem_next_range_64 = awkward_ListArray_getitem_next_range
awkward_ListArray64_getitem_next_range_64 = awkward_ListArray_getitem_next_range
awkward_ListArrayU32_getitem_next_range_64 = awkward_ListArray_getitem_next_range


def awkward_ListArray_getitem_next_range_carrylength(
    carrylength, fromstarts, fromstops, lenstarts, start, stop, step
):
    carrylength[0] = 0
    for i in range(lenstarts):
        length = fromstops[i] - fromstarts[i]
        regular_start = start
        regular_stop = stop
        awkward_regularize_rangeslice(
            regular_start,
            regular_stop,
            step > 0,
            start != kSliceNone,
            stop != kSliceNone,
            length,
        )
        if step > 0:
            j = regular_start
            while j < regular_stop:
                carrylength[0] = carrylength[0] + 1
                j += step
        else:
            j = regular_start
            while j > regular_stop:
                carrylength[0] = carrylength[0] + 1
                j += step

awkward_ListArray32_getitem_next_range_carrylength = awkward_ListArray_getitem_next_range_carrylength
awkward_ListArray64_getitem_next_range_carrylength = awkward_ListArray_getitem_next_range_carrylength
awkward_ListArrayU32_getitem_next_range_carrylength = awkward_ListArray_getitem_next_range_carrylength


def awkward_ListArray_getitem_next_range_counts(total, fromoffsets, lenstarts):
    total[0] = 0
    for i in range(lenstarts):
        total[0] = (total[0] + fromoffsets[i + 1]) - fromoffsets[i]

awkward_ListArray32_getitem_next_range_counts_64 = awkward_ListArray_getitem_next_range_counts
awkward_ListArray64_getitem_next_range_counts_64 = awkward_ListArray_getitem_next_range_counts
awkward_ListArrayU32_getitem_next_range_counts_64 = awkward_ListArray_getitem_next_range_counts


def awkward_ListArray_getitem_next_range_spreadadvanced(
    toadvanced, fromadvanced, fromoffsets, lenstarts
):
    for i in range(lenstarts):
        count = fromoffsets[i + 1] - fromoffsets[i]
        for j in range(count):
            toadvanced[fromoffsets[i] + j] = fromadvanced[i]

awkward_ListArray32_getitem_next_range_spreadadvanced_64 = awkward_ListArray_getitem_next_range_spreadadvanced
awkward_ListArray64_getitem_next_range_spreadadvanced_64 = awkward_ListArray_getitem_next_range_spreadadvanced
awkward_ListArrayU32_getitem_next_range_spreadadvanced_64 = awkward_ListArray_getitem_next_range_spreadadvanced


def awkward_ListArray_localindex(toindex, offsets, length):
    for i in range(length):
        start = int(offsets[i])
        stop = int(offsets[i + 1])
        for j in range(start, stop):
            toindex[j] = j - start

awkward_ListArray32_localindex_64 = awkward_ListArray_localindex
awkward_ListArray64_localindex_64 = awkward_ListArray_localindex
awkward_ListArrayU32_localindex_64 = awkward_ListArray_localindex


def awkward_ListArray_min_range(tomin, fromstarts, fromstops, lenstarts):
    shorter = fromstops[0] - fromstarts[0]
    for i in range(1, lenstarts):
        rangeval = fromstops[i] - fromstarts[i]
        shorter = shorter if shorter < rangeval else rangeval
    tomin[0] = shorter

awkward_ListArray32_min_range = awkward_ListArray_min_range
awkward_ListArray64_min_range = awkward_ListArray_min_range
awkward_ListArrayU32_min_range = awkward_ListArray_min_range


def awkward_ListArray_rpad_and_clip_length_axis1(
    tomin, fromstarts, fromstops, target, lenstarts
):
    length = 0
    for i in range(lenstarts):
        rangeval = fromstops[i] - fromstarts[i]
        length += target if target > rangeval else rangeval
    tomin[0] = length

awkward_ListArray32_rpad_and_clip_length_axis1 = awkward_ListArray_rpad_and_clip_length_axis1
awkward_ListArray64_rpad_and_clip_length_axis1 = awkward_ListArray_rpad_and_clip_length_axis1
awkward_ListArrayU32_rpad_and_clip_length_axis1 = awkward_ListArray_rpad_and_clip_length_axis1


def awkward_ListArray_rpad_axis1(
    toindex, fromstarts, fromstops, tostarts, tostops, target, length
):
    offset = 0
    for i in range(length):
        tostarts[i] = offset
        rangeval = fromstops[i] - fromstarts[i]
        for j in range(rangeval):
            toindex[offset + j] = fromstarts[i] + j
        for j in range(rangeval, target):
            toindex[offset + j] = -1
        offset = tostarts[i] + target if target > rangeval else tostarts[i] + rangeval
        tostops[i] = offset

awkward_ListArray32_rpad_axis1_64 = awkward_ListArray_rpad_axis1
awkward_ListArray64_rpad_axis1_64 = awkward_ListArray_rpad_axis1
awkward_ListArrayU32_rpad_axis1_64 = awkward_ListArray_rpad_axis1


def awkward_ListArray_validity(starts, stops, length, lencontent):
    for i in range(length):
        start = starts[i]
        stop = stops[i]
        if start != stop:
            if start > stop:
                raise ValueError("start[i] > stop[i]")
            if start < 0:
                raise ValueError("start[i] < 0")
            if stop > lencontent:
                raise ValueError("stop[i] > len(content)")

awkward_ListArray32_validity = awkward_ListArray_validity
awkward_ListArray64_validity = awkward_ListArray_validity
awkward_ListArrayU32_validity = awkward_ListArray_validity


def awkward_ListOffsetArray_compact_offsets(tooffsets, fromoffsets, length):
    diff = int(fromoffsets[0])
    tooffsets[0] = 0
    for i in range(length):
        tooffsets[i + 1] = fromoffsets[i + 1] - diff

awkward_ListOffsetArray32_compact_offsets_64 = awkward_ListOffsetArray_compact_offsets
awkward_ListOffsetArray64_compact_offsets_64 = awkward_ListOffsetArray_compact_offsets
awkward_ListOffsetArrayU32_compact_offsets_64 = awkward_ListOffsetArray_compact_offsets


def awkward_ListOffsetArray_drop_none_indexes(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes):
    nr_of_nones, offset1, offset2 = 0, 0, 0
    for i in range(length_offsets):
      offset2 = fromoffsets[i]
      for j in range(offset1, offset2):
        if (noneindexes[j] < 0):
          nr_of_nones+=1
      tooffsets[i] = fromoffsets[i] - nr_of_nones
      offset1 = offset2

awkward_ListOffsetArray_drop_none_indexes_32 = awkward_ListOffsetArray_drop_none_indexes
awkward_ListOffsetArray_drop_none_indexes_64 = awkward_ListOffsetArray_drop_none_indexes


def awkward_ListOffsetArray_flatten_offsets(
    tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen
):
    for i in range(outeroffsetslen):
        tooffsets[i] = inneroffsets[outeroffsets[i]]

awkward_ListOffsetArray32_flatten_offsets_64 = awkward_ListOffsetArray_flatten_offsets
awkward_ListOffsetArray64_flatten_offsets_64 = awkward_ListOffsetArray_flatten_offsets
awkward_ListOffsetArrayU32_flatten_offsets_64 = awkward_ListOffsetArray_flatten_offsets


def awkward_ListOffsetArray_reduce_local_nextparents_64(nextparents, offsets, length):
    initialoffset = offsets[0]
    for i in range(length):
        j = offsets[i] - initialoffset
        while j < (offsets[i + 1] - initialoffset):
            nextparents[j] = i
            j = j + 1

awkward_ListOffsetArray_reduce_local_nextparents_64 = awkward_ListOffsetArray_reduce_local_nextparents_64


def awkward_ListOffsetArray_reduce_local_outoffsets_64(
    outoffsets, parents, lenparents, outlength
):
    k = 0
    last = -1
    for i in range(lenparents):
        while last < parents[i]:
            outoffsets[k] = i
            k = k + 1
            last = last + 1

    while k <= outlength:
        outoffsets[k] = lenparents
        k = k + 1

awkward_ListOffsetArray_reduce_local_outoffsets_64 = awkward_ListOffsetArray_reduce_local_outoffsets_64


def awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64(
    maxcount, offsetscopy, offsets, length
):
    maxcount[0] = 0
    offsetscopy[0] = offsets[0]
    for i in range(length):
        count = offsets[i + 1] - offsets[i]
        if maxcount[0] < count:
            maxcount[0] = count
        offsetscopy[i + 1] = offsets[i + 1]

awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64 = awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64


def awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64(
    nummissing,
    missing,
    nextshifts,
    offsets,
    length,
    starts,
    parents,
    maxcount,
    nextlen,
    nextcarry,
):
    for i in range(length):
        start = offsets[i]
        stop = offsets[i + 1]
        count = stop - start
        if starts[parents[i]] == i:
            for k in range(maxcount):
                nummissing[k] = 0
        for k in range(count, maxcount):
            nummissing[k] = nummissing[k] + 1
        for j in range(count):
            missing[start + j] = nummissing[j]
    for j in range(nextlen):
        nextshifts[j] = missing[nextcarry[j]]

awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64 = awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64


def awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64(
    nextstarts, nextparents, nextlen
):
    lastnextparent = -1
    for i in range(nextlen):
        if nextparents[i] != lastnextparent:
            nextstarts[nextparents[i]] = i
        lastnextparent = nextparents[i]

awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64 = awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64


def awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64(
    outstarts, outstops, distincts, lendistincts, outlength
):
    maxcount = lendistincts if (outlength == 0) else int(lendistincts // outlength)
    if outlength > 0 and lendistincts > 0:
        # The sublist index
        k = 0
        i_next_sublist = 0
        for i in range(lendistincts):
            # Are we now in the next sublist?
            if i == i_next_sublist:
                # Advance counter
                i_next_sublist += maxcount

                # Add a new sublist
                outstarts[k] = i
                outstops[k] = i

                k += 1

            # Expand stop index of previous list
            if distincts[i] != -1:
                outstops[k - 1] = i + 1
    else:
        for k in range(outlength):
          outstarts[k] = 0
          outstops[k] = 0

awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64 = awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64


def awkward_ListOffsetArray_rpad_and_clip_axis1(toindex, fromoffsets, length, target):
    for i in range(length):
        rangeval = float(fromoffsets[i + 1] - fromoffsets[i])
        shorter = target if target < rangeval else rangeval
        for j in range(shorter):
            toindex[(i * target) + j] = float(fromoffsets[i]) + j
        for j in range(shorter, target):
            toindex[(i * target) + j] = -1

awkward_ListOffsetArray32_rpad_and_clip_axis1_64 = awkward_ListOffsetArray_rpad_and_clip_axis1
awkward_ListOffsetArray64_rpad_and_clip_axis1_64 = awkward_ListOffsetArray_rpad_and_clip_axis1
awkward_ListOffsetArrayU32_rpad_and_clip_axis1_64 = awkward_ListOffsetArray_rpad_and_clip_axis1


def awkward_ListOffsetArray_rpad_axis1(toindex, fromoffsets, fromlength, target):
    count = 0
    for i in range(fromlength):
        rangeval = float(fromoffsets[i + 1] - fromoffsets[i])
        for j in range(rangeval):
            toindex[count] = float(fromoffsets[i]) + j
            count = count + 1
        for j in range(rangeval, target):
            toindex[count] = -1
            count = count + 1

awkward_ListOffsetArray32_rpad_axis1_64 = awkward_ListOffsetArray_rpad_axis1
awkward_ListOffsetArray64_rpad_axis1_64 = awkward_ListOffsetArray_rpad_axis1
awkward_ListOffsetArrayU32_rpad_axis1_64 = awkward_ListOffsetArray_rpad_axis1


def awkward_ListOffsetArray_rpad_length_axis1(
    tooffsets, fromoffsets, fromlength, target, tolength
):
    length = 0
    tooffsets[0] = 0
    for i in range(fromlength):
        rangeval = fromoffsets[i + 1] - fromoffsets[i]
        longer = rangeval if target < rangeval else target
        length = length + longer
        tooffsets[i + 1] = tooffsets[i] + longer
    tolength[0] = length

awkward_ListOffsetArray32_rpad_length_axis1 = awkward_ListOffsetArray_rpad_length_axis1
awkward_ListOffsetArray64_rpad_length_axis1 = awkward_ListOffsetArray_rpad_length_axis1
awkward_ListOffsetArrayU32_rpad_length_axis1 = awkward_ListOffsetArray_rpad_length_axis1


def awkward_ListOffsetArray_toRegularArray(size, fromoffsets, offsetslength):
    size[0] = -1
    for i in range(offsetslength - 1):
        count = int(fromoffsets[i + 1]) - int(fromoffsets[i])
        if count < 0:
            raise ValueError("offsets must be monotonically increasing")
        if size[0] == -1:
            size[0] = count
        else:
            if size[0] != count:
                raise ValueError(
                    "cannot convert to RegularArray because subarray lengths are not regular"
                )
    if size[0] == -1:
        size[0] = 0

awkward_ListOffsetArray32_toRegularArray = awkward_ListOffsetArray_toRegularArray
awkward_ListOffsetArray64_toRegularArray = awkward_ListOffsetArray_toRegularArray
awkward_ListOffsetArrayU32_toRegularArray = awkward_ListOffsetArray_toRegularArray


def awkward_MaskedArray_getitem_next_jagged_project(
    index, starts_in, stops_in, starts_out, stops_out, length
):
    k = 0
    for i in range(length):
        if index[i] >= 0:
            starts_out[k] = starts_in[i]
            stops_out[k] = stops_in[i]
            k = k + 1

awkward_MaskedArray32_getitem_next_jagged_project = awkward_MaskedArray_getitem_next_jagged_project
awkward_MaskedArray64_getitem_next_jagged_project = awkward_MaskedArray_getitem_next_jagged_project
awkward_MaskedArrayU32_getitem_next_jagged_project = awkward_MaskedArray_getitem_next_jagged_project


def awkward_NumpyArray_fill(toptr, tooffset, fromptr, length):
    for i in range(length):
        toptr[tooffset + i] = float(fromptr[i])

awkward_NumpyArray_fill_toint8_fromint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint8_fromint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint8_fromint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint8_fromint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint8_fromuint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint8_fromuint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint8_fromuint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint8_fromuint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint8_fromfloat32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint8_fromfloat64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint16_fromint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint16_fromint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint16_fromint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint16_fromint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint16_fromuint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint16_fromuint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint16_fromuint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint16_fromuint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint16_fromfloat32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint16_fromfloat64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint32_fromint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint32_fromint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint32_fromint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint32_fromint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint32_fromuint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint32_fromuint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint32_fromuint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint32_fromuint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint32_fromfloat32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint32_fromfloat64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint64_fromint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint64_fromint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint64_fromint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint64_fromint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint64_fromuint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint64_fromuint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint64_fromuint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint64_fromuint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint64_fromfloat32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_toint64_fromfloat64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint8_fromint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint8_fromint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint8_fromint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint8_fromint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint8_fromuint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint8_fromuint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint8_fromuint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint8_fromuint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint8_fromfloat32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint8_fromfloat64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint16_fromint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint16_fromint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint16_fromint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint16_fromint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint16_fromuint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint16_fromuint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint16_fromuint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint16_fromuint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint16_fromfloat32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint16_fromfloat64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint32_fromint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint32_fromint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint32_fromint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint32_fromint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint32_fromuint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint32_fromuint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint32_fromuint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint32_fromuint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint32_fromfloat32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint32_fromfloat64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint64_fromint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint64_fromint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint64_fromint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint64_fromint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint64_fromuint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint64_fromuint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint64_fromuint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint64_fromuint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint64_fromfloat32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_touint64_fromfloat64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat32_fromint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat32_fromint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat32_fromint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat32_fromint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat32_fromuint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat32_fromuint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat32_fromuint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat32_fromuint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat32_fromfloat32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat32_fromfloat64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat64_fromint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat64_fromint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat64_fromint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat64_fromint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat64_fromuint8 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat64_fromuint16 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat64_fromuint32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat64_fromuint64 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat64_fromfloat32 = awkward_NumpyArray_fill
awkward_NumpyArray_fill_tofloat64_fromfloat64 = awkward_NumpyArray_fill


def awkward_NumpyArray_rearrange_shifted(toptr, fromshifts, length, fromoffsets, offsetslength, fromparents, parentslength):
    k = 0
    for i in range(offsetslength - 1):
        for j in rage(fromoffsets[i + 1] - fromoffsets[i]):
            toptr[k] = toptr[k] + fromoffsets[i]
            k = k + 1

    for i in range(length):
        parent = fromparents[i]
        start = fromstarts[parent]
        toptr[i] = toptr[i] + fromshifts[toptr[i]] - start

awkward_NumpyArray_rearrange_shifted_toint64_fromint64 = awkward_NumpyArray_rearrange_shifted


def awkward_NumpyArray_reduce_adjust_starts_64(toptr, outlength, parents, starts):
    for k in range(outlength):
        i = toptr[k]
        if i >= 0:
            parent = parents[i]
            start = starts[parent]
            toptr[k] += -start

awkward_NumpyArray_reduce_adjust_starts_64 = awkward_NumpyArray_reduce_adjust_starts_64


def awkward_NumpyArray_reduce_adjust_starts_shifts_64(
    toptr, outlength, parents, starts, shifts
):
    for k in range(outlength):
        i = toptr[k]
        if i >= 0:
            parent = parents[i]
            start = starts[parent]
            toptr[k] += shifts[i] - start

awkward_NumpyArray_reduce_adjust_starts_shifts_64 = awkward_NumpyArray_reduce_adjust_starts_shifts_64


def awkward_NumpyArray_reduce_mask_ByteMaskedArray_64(
    toptr, parents, lenparents, outlength
):
    for i in range(outlength):
        toptr[i] = 1
    for i in range(lenparents):
        toptr[parents[i]] = 0

awkward_NumpyArray_reduce_mask_ByteMaskedArray_64 = awkward_NumpyArray_reduce_mask_ByteMaskedArray_64


def awkward_RegularArray_broadcast_tooffsets(fromoffsets, offsetslength, size):
    for i in range(offsetslength - 1):
        count = int(fromoffsets[i + 1] - fromoffsets[i])
        if count < 0:
            raise ValueError("broadcast's offsets must be monotonically increasing")
        if size != count:
            raise ValueError("cannot broadcast nested list")

awkward_RegularArray_broadcast_tooffsets_64 = awkward_RegularArray_broadcast_tooffsets


def awkward_RegularArray_broadcast_tooffsets_size1(tocarry, fromoffsets, offsetslength):
    k = 0
    for i in range(offsetslength - 1):
        count = int(fromoffsets[i + 1] - fromoffsets[i])
        if count < 0:
            raise ValueError("broadcast's offsets must be monotonically increasing")
        for j in range(count):
            tocarry[k] = float(i)
            k = k + 1

awkward_RegularArray_broadcast_tooffsets_size1_64 = awkward_RegularArray_broadcast_tooffsets_size1


def awkward_RegularArray_compact_offsets(tooffsets, length, size):
    tooffsets[0] = 0
    for i in range(length):
        tooffsets[i + 1] = (i + 1) * size

awkward_RegularArray_compact_offsets64 = awkward_RegularArray_compact_offsets


def awkward_RegularArray_getitem_carry(tocarry, fromcarry, lencarry, size):
    for i in range(lencarry):
        for j in range(size):
            tocarry[(i * size) + j] = (fromcarry[i] * size) + j

awkward_RegularArray_getitem_carry_64 = awkward_RegularArray_getitem_carry


def awkward_RegularArray_getitem_jagged_expand(
    multistarts, multistops, singleoffsets, regularsize, regularlength
):
    for i in range(regularlength):
        for j in range(regularsize):
            multistarts[(i * regularsize) + j] = singleoffsets[j]
            multistops[(i * regularsize) + j] = singleoffsets[j + 1]

awkward_RegularArray_getitem_jagged_expand_64 = awkward_RegularArray_getitem_jagged_expand


def awkward_RegularArray_getitem_next_array(
    tocarry, toadvanced, fromarray, length, lenarray, size
):
    for i in range(length):
        for j in range(lenarray):
            tocarry[(i * lenarray) + j] = (i * size) + fromarray[j]
            toadvanced[(i * lenarray) + j] = j

awkward_RegularArray_getitem_next_array_64 = awkward_RegularArray_getitem_next_array


def awkward_RegularArray_getitem_next_array_advanced(
    tocarry, toadvanced, fromadvanced, fromarray, length, lenarray, size
):
    for i in range(length):
        tocarry[i] = (i * size) + fromarray[fromadvanced[i]]
        toadvanced[i] = i

awkward_RegularArray_getitem_next_array_advanced_64 = awkward_RegularArray_getitem_next_array_advanced


def awkward_RegularArray_getitem_next_array_regularize(
    toarray, fromarray, lenarray, size
):
    for j in range(lenarray):
        toarray[j] = fromarray[j]
        if toarray[j] < 0:
            toarray[j] += size
        if not ((0 <= toarray[j]) and (toarray[j] < size)):
            raise ValueError("index out of range")

awkward_RegularArray_getitem_next_array_regularize_64 = awkward_RegularArray_getitem_next_array_regularize


def awkward_RegularArray_getitem_next_at(tocarry, at, length, size):
    regular_at = at
    if regular_at < 0:
        regular_at += size
    if not ((0 <= regular_at) and (regular_at < size)):
        raise ValueError("index out of range")
    for i in range(length):
        tocarry[i] = (i * size) + regular_at

awkward_RegularArray_getitem_next_at_64 = awkward_RegularArray_getitem_next_at


def awkward_RegularArray_getitem_next_range(
    tocarry, regular_start, step, length, size, nextsize
):
    for i in range(length):
        for j in range(nextsize):
            tocarry[(i * nextsize) + j] = ((i * size) + regular_start) + (j * step)

awkward_RegularArray_getitem_next_range_64 = awkward_RegularArray_getitem_next_range


def awkward_RegularArray_getitem_next_range_spreadadvanced(
    toadvanced, fromadvanced, length, nextsize
):
    for i in range(length):
        for j in range(nextsize):
            toadvanced[(i * nextsize) + j] = fromadvanced[i]

awkward_RegularArray_getitem_next_range_spreadadvanced_64 = awkward_RegularArray_getitem_next_range_spreadadvanced


def awkward_RegularArray_localindex(toindex, size, length):
    for i in range(length):
        for j in range(size):
            toindex[(i * size) + j] = j

awkward_RegularArray_localindex_64 = awkward_RegularArray_localindex


def awkward_RegularArray_reduce_local_nextparents(nextparents, size, length):
    k = 0
    for i in range(length):
        for _ in range(size):
            # nextparents should contain the row index
            nextparents[k] = i
            k += 1

awkward_RegularArray_reduce_local_nextparents_64 = awkward_RegularArray_reduce_local_nextparents


def awkward_RegularArray_reduce_nonlocal_preparenext(nextcarry, nextparents, parents, size, length):
    k = 0
    for j in range(size):
        for i in range(length):
            # nextparents needs to be locally contiguous
            # so order our arrays by the transpose
            nextcarry[k] = i * size + j
            nextparents[k] = parents[i] * size + j
            k += 1

awkward_RegularArray_reduce_nonlocal_preparenext_64 = awkward_RegularArray_reduce_nonlocal_preparenext


def awkward_RegularArray_rpad_and_clip_axis1(toindex, target, size, length):
    shorter = target if target < size else size
    for i in range(length):
        for j in range(shorter):
            toindex[(i * target) + j] = (i * size) + j
        for j in range(shorter, target):
            toindex[(i * target) + j] = -1

awkward_RegularArray_rpad_and_clip_axis1_64 = awkward_RegularArray_rpad_and_clip_axis1


def awkward_UnionArray_fillindex(toindex, toindexoffset, fromindex, length):
    for i in range(length):
        toindex[toindexoffset + i] = float(fromindex[i])

awkward_UnionArray_fillindex_to64_from32 = awkward_UnionArray_fillindex
awkward_UnionArray_fillindex_to64_from64 = awkward_UnionArray_fillindex
awkward_UnionArray_fillindex_to64_fromU32 = awkward_UnionArray_fillindex


def awkward_UnionArray_fillindex_count(toindex, toindexoffset, length):
    for i in range(length):
        toindex[toindexoffset + i] = float(i)

awkward_UnionArray_fillindex_to64_count = awkward_UnionArray_fillindex_count


def awkward_UnionArray_fillna(toindex, fromindex, length):
    for i in range(length):
        toindex[i] = fromindex[i] if fromindex[i] >= 0 else 0

awkward_UnionArray_fillna_from32_to64 = awkward_UnionArray_fillna
awkward_UnionArray_fillna_from64_to64 = awkward_UnionArray_fillna
awkward_UnionArray_fillna_fromU32_to64 = awkward_UnionArray_fillna


def awkward_UnionArray_filltags(totags, totagsoffset, fromtags, length, base):
    for i in range(length):
        totags[totagsoffset + i] = float(fromtags[i] + base)

awkward_UnionArray_filltags_to8_from8 = awkward_UnionArray_filltags


def awkward_UnionArray_filltags_const(totags, totagsoffset, length, base):
    for i in range(length):
        totags[totagsoffset + i] = float(base)

awkward_UnionArray_filltags_to8_const = awkward_UnionArray_filltags_const


def awkward_UnionArray_flatten_combine(
    totags, toindex, tooffsets, fromtags, fromindex, length, offsetsraws
):
    tooffsets[0] = 0
    k = 0
    for i in range(length):
        tag = fromtags[i]
        idx = fromindex[i]
        start = offsetsraws[tag][idx]
        stop = offsetsraws[tag][idx + 1]
        tooffsets[i + 1] = tooffsets[i] + (stop - start)
        for j in range(start, stop):
            totags[k] = tag
            toindex[k] = j
            k = k + 1

awkward_UnionArray32_flatten_combine_64 = awkward_UnionArray_flatten_combine
awkward_UnionArray64_flatten_combine_64 = awkward_UnionArray_flatten_combine
awkward_UnionArrayU32_flatten_combine_64 = awkward_UnionArray_flatten_combine


def awkward_UnionArray_flatten_length(
    total_length, fromtags, fromindex, length, offsetsraws
):
    total_length[0] = 0
    for i in range(length):
        tag = fromtags[i]
        idx = fromindex[i]
        start = offsetsraws[tag][idx]
        stop = offsetsraws[tag][idx + 1]
        total_length[0] = total_length[0] + (stop - start)

awkward_UnionArray32_flatten_length_64 = awkward_UnionArray_flatten_length
awkward_UnionArray64_flatten_length_64 = awkward_UnionArray_flatten_length
awkward_UnionArrayU32_flatten_length_64 = awkward_UnionArray_flatten_length


def awkward_UnionArray_nestedfill_tags_index(
    totags, toindex, tmpstarts, tag, fromcounts, length
):
    k = 0
    for i in range(length):
        start = tmpstarts[i]
        stop = start + fromcounts[i]
        for j in range(start, stop):
            totags[j] = tag
            toindex[j] = k
            k += 1
        tmpstarts[i] = stop

awkward_UnionArray8_32_nestedfill_tags_index_64 = awkward_UnionArray_nestedfill_tags_index
awkward_UnionArray8_64_nestedfill_tags_index_64 = awkward_UnionArray_nestedfill_tags_index
awkward_UnionArray8_U32_nestedfill_tags_index_64 = awkward_UnionArray_nestedfill_tags_index


def awkward_UnionArray_project(lenout, tocarry, fromtags, fromindex, length, which):
    lenout[0] = 0
    for i in range(length):
        if fromtags[i] == which:
            tocarry[lenout[0]] = fromindex[i]
            lenout[0] = lenout[0] + 1

awkward_UnionArray8_32_project_64 = awkward_UnionArray_project
awkward_UnionArray8_64_project_64 = awkward_UnionArray_project
awkward_UnionArray8_U32_project_64 = awkward_UnionArray_project


def awkward_UnionArray_regular_index(toindex, current, size, fromtags, length):
    count = 0
    for k in range(size):
        current[k] = 0
    for i in range(length):
        tag = fromtags[i]
        toindex[i] = current[tag]
        current[tag] = current[tag] + 1

awkward_UnionArray8_32_regular_index = awkward_UnionArray_regular_index
awkward_UnionArray8_64_regular_index = awkward_UnionArray_regular_index
awkward_UnionArray8_U32_regular_index = awkward_UnionArray_regular_index


def awkward_UnionArray_regular_index_getsize(size, fromtags, length):
    size[0] = 0
    for i in range(length):
        tag = int(fromtags[i])
        if size[0] < tag:
            size[0] = tag
    size[0] = size[0] + 1

awkward_UnionArray8_regular_index_getsize = awkward_UnionArray_regular_index_getsize


def awkward_UnionArray_simplify(
    totags,
    toindex,
    outertags,
    outerindex,
    innertags,
    innerindex,
    towhich,
    innerwhich,
    outerwhich,
    length,
    base,
):
    for i in range(length):
        if outertags[i] == outerwhich:
            j = outerindex[i]
            if innertags[j] == innerwhich:
                totags[i] = float(towhich)
                toindex[i] = float(innerindex[j] + base)

awkward_UnionArray8_32_simplify8_32_to8_64 = awkward_UnionArray_simplify
awkward_UnionArray8_32_simplify8_64_to8_64 = awkward_UnionArray_simplify
awkward_UnionArray8_32_simplify8_U32_to8_64 = awkward_UnionArray_simplify
awkward_UnionArray8_64_simplify8_32_to8_64 = awkward_UnionArray_simplify
awkward_UnionArray8_64_simplify8_64_to8_64 = awkward_UnionArray_simplify
awkward_UnionArray8_64_simplify8_U32_to8_64 = awkward_UnionArray_simplify
awkward_UnionArray8_U32_simplify8_32_to8_64 = awkward_UnionArray_simplify
awkward_UnionArray8_U32_simplify8_64_to8_64 = awkward_UnionArray_simplify
awkward_UnionArray8_U32_simplify8_U32_to8_64 = awkward_UnionArray_simplify


def awkward_UnionArray_simplify_one(
    totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base
):
    for i in range(length):
        if fromtags[i] == fromwhich:
            totags[i] = float(towhich)
            toindex[i] = float(fromindex[i] + base)

awkward_UnionArray8_32_simplify_one_to8_64 = awkward_UnionArray_simplify_one
awkward_UnionArray8_64_simplify_one_to8_64 = awkward_UnionArray_simplify_one
awkward_UnionArray8_U32_simplify_one_to8_64 = awkward_UnionArray_simplify_one


def awkward_UnionArray_validity(tags, index, length, numcontents, lencontents):
    for i in range(length):
        tag = tags[i]
        idx = index[i]
        if tag < 0:
            raise ValueError("tags[i] < 0")
        if idx < 0:
            raise ValueError("index[i] < 0")
        if tag >= numcontents:
            raise ValueError("tags[i] >= len(contents)")
        lencontent = lencontents[tag]
        if idx >= lencontent:
            raise ValueError("index[i] >= len(content[tags[i]])")

awkward_UnionArray8_32_validity = awkward_UnionArray_validity
awkward_UnionArray8_64_validity = awkward_UnionArray_validity
awkward_UnionArray8_U32_validity = awkward_UnionArray_validity


def awkward_index_rpad_and_clip_axis0(toindex, target, length):
    shorter = target if target < length else length
    for i in range(shorter):
        toindex[i] = i
    for i in range(shorter, target):
        toindex[i] = -1

awkward_index_rpad_and_clip_axis0_64 = awkward_index_rpad_and_clip_axis0


def awkward_index_rpad_and_clip_axis1(tostarts, tostops, target, length):
    offset = 0
    for i in range(length):
        tostarts[i] = offset
        offset = offset + target
        tostops[i] = offset

awkward_index_rpad_and_clip_axis1_64 = awkward_index_rpad_and_clip_axis1


def awkward_Index_nones_as_index(toindex, length):
    last_index = 0
    for i in range(length):
        if toindex[i] > last_index:
            last_index = toindex[i]
    for i in range(length):
        if toindex[i] == -1:
            last_index = last_index + 1
            toindex[i] = last_index

awkward_Index_nones_as_index_64 = awkward_Index_nones_as_index


def awkward_localindex(toindex, length):
    for i in range(length):
        toindex[i] = i

awkward_localindex_64 = awkward_localindex


def awkward_missing_repeat(outindex, index, indexlength, repetitions, regularsize):
    for i in range(repetitions):
        for j in range(indexlength):
            base = index[j]
            outindex[(i * indexlength) + j] = base + i * regularsize if base >= 0 else 0

awkward_missing_repeat_64 = awkward_missing_repeat


def awkward_reduce_argmax(toptr, fromptr, parents, lenparents, outlength):
    for k in range(outlength):
        toptr[k] = -1
    for i in range(lenparents):
        parent = parents[i]
        if (toptr[parent] == -1) or (fromptr[i] > fromptr[toptr[parent]]):
            toptr[parent] = i

awkward_reduce_argmax_int8_64 = awkward_reduce_argmax
awkward_reduce_argmax_int16_64 = awkward_reduce_argmax
awkward_reduce_argmax_int32_64 = awkward_reduce_argmax
awkward_reduce_argmax_int64_64 = awkward_reduce_argmax
awkward_reduce_argmax_uint8_64 = awkward_reduce_argmax
awkward_reduce_argmax_uint16_64 = awkward_reduce_argmax
awkward_reduce_argmax_uint32_64 = awkward_reduce_argmax
awkward_reduce_argmax_uint64_64 = awkward_reduce_argmax
awkward_reduce_argmax_float32_64 = awkward_reduce_argmax
awkward_reduce_argmax_float64_64 = awkward_reduce_argmax


def awkward_reduce_argmin(toptr, fromptr, parents, lenparents, outlength):
    for k in range(outlength):
        toptr[k] = -1
    for i in range(lenparents):
        parent = parents[i]
        if (toptr[parent] == -1) or (fromptr[i] < fromptr[toptr[parent]]):
            toptr[parent] = i

awkward_reduce_argmin_int8_64 = awkward_reduce_argmin
awkward_reduce_argmin_int16_64 = awkward_reduce_argmin
awkward_reduce_argmin_int32_64 = awkward_reduce_argmin
awkward_reduce_argmin_int64_64 = awkward_reduce_argmin
awkward_reduce_argmin_uint8_64 = awkward_reduce_argmin
awkward_reduce_argmin_uint16_64 = awkward_reduce_argmin
awkward_reduce_argmin_uint32_64 = awkward_reduce_argmin
awkward_reduce_argmin_uint64_64 = awkward_reduce_argmin
awkward_reduce_argmin_float32_64 = awkward_reduce_argmin
awkward_reduce_argmin_float64_64 = awkward_reduce_argmin


def awkward_reduce_count_64(toptr, parents, lenparents, outlength):
    for i in range(outlength):
        toptr[i] = 0
    for i in range(lenparents):
        toptr[parents[i]] = toptr[parents[i]] + 1

awkward_reduce_count_64 = awkward_reduce_count_64


def awkward_reduce_countnonzero(toptr, fromptr, parents, lenparents, outlength):
    for i in range(outlength):
        toptr[i] = 0
    for i in range(lenparents):
        toptr[parents[i]] += fromptr[i] != 0

awkward_reduce_countnonzero_bool_64 = awkward_reduce_countnonzero
awkward_reduce_countnonzero_int8_64 = awkward_reduce_countnonzero
awkward_reduce_countnonzero_int16_64 = awkward_reduce_countnonzero
awkward_reduce_countnonzero_int32_64 = awkward_reduce_countnonzero
awkward_reduce_countnonzero_int64_64 = awkward_reduce_countnonzero
awkward_reduce_countnonzero_uint8_64 = awkward_reduce_countnonzero
awkward_reduce_countnonzero_uint16_64 = awkward_reduce_countnonzero
awkward_reduce_countnonzero_uint32_64 = awkward_reduce_countnonzero
awkward_reduce_countnonzero_uint64_64 = awkward_reduce_countnonzero
awkward_reduce_countnonzero_float32_64 = awkward_reduce_countnonzero
awkward_reduce_countnonzero_float64_64 = awkward_reduce_countnonzero


def awkward_reduce_max(toptr, fromptr, parents, lenparents, outlength, identity):
    for i in range(outlength):
        toptr[i] = identity
    for i in range(lenparents):
        x = fromptr[i]
        toptr[parents[i]] = x if x > toptr[parents[i]] else toptr[parents[i]]

awkward_reduce_max_int8_int8_64 = awkward_reduce_max
awkward_reduce_max_int16_int16_64 = awkward_reduce_max
awkward_reduce_max_int32_int32_64 = awkward_reduce_max
awkward_reduce_max_int64_int64_64 = awkward_reduce_max
awkward_reduce_max_uint8_uint8_64 = awkward_reduce_max
awkward_reduce_max_uint16_uint16_64 = awkward_reduce_max
awkward_reduce_max_uint32_uint32_64 = awkward_reduce_max
awkward_reduce_max_uint64_uint64_64 = awkward_reduce_max
awkward_reduce_max_float32_float32_64 = awkward_reduce_max
awkward_reduce_max_float64_float64_64 = awkward_reduce_max


def awkward_reduce_min(toptr, fromptr, parents, lenparents, outlength, identity):
    for i in range(outlength):
        toptr[i] = identity
    for i in range(lenparents):
        x = fromptr[i]
        toptr[parents[i]] = x if x < toptr[parents[i]] else toptr[parents[i]]

awkward_reduce_min_int8_int8_64 = awkward_reduce_min
awkward_reduce_min_int16_int16_64 = awkward_reduce_min
awkward_reduce_min_int32_int32_64 = awkward_reduce_min
awkward_reduce_min_int64_int64_64 = awkward_reduce_min
awkward_reduce_min_uint8_uint8_64 = awkward_reduce_min
awkward_reduce_min_uint16_uint16_64 = awkward_reduce_min
awkward_reduce_min_uint32_uint32_64 = awkward_reduce_min
awkward_reduce_min_uint64_uint64_64 = awkward_reduce_min
awkward_reduce_min_float32_float32_64 = awkward_reduce_min
awkward_reduce_min_float64_float64_64 = awkward_reduce_min


def awkward_reduce_prod(toptr, fromptr, parents, lenparents, outlength):
    for i in range(outlength):
        toptr[i] = float(1)
    for i in range(lenparents):
        toptr[parents[i]] *= float(fromptr[i])

awkward_reduce_prod_int32_int8_64 = awkward_reduce_prod
awkward_reduce_prod_int32_int16_64 = awkward_reduce_prod
awkward_reduce_prod_int32_int32_64 = awkward_reduce_prod
awkward_reduce_prod_int64_int8_64 = awkward_reduce_prod
awkward_reduce_prod_int64_int16_64 = awkward_reduce_prod
awkward_reduce_prod_int64_int32_64 = awkward_reduce_prod
awkward_reduce_prod_int64_int64_64 = awkward_reduce_prod
awkward_reduce_prod_uint32_uint8_64 = awkward_reduce_prod
awkward_reduce_prod_uint32_uint16_64 = awkward_reduce_prod
awkward_reduce_prod_uint32_uint32_64 = awkward_reduce_prod
awkward_reduce_prod_uint64_uint8_64 = awkward_reduce_prod
awkward_reduce_prod_uint64_uint16_64 = awkward_reduce_prod
awkward_reduce_prod_uint64_uint32_64 = awkward_reduce_prod
awkward_reduce_prod_uint64_uint64_64 = awkward_reduce_prod
awkward_reduce_prod_float32_float32_64 = awkward_reduce_prod
awkward_reduce_prod_float64_float64_64 = awkward_reduce_prod


def awkward_reduce_prod_bool(toptr, fromptr, parents, lenparents, outlength):
    for i in range(outlength):
        toptr[i] = True
    for i in range(lenparents):
        toptr[parents[i]] &= fromptr[i] != 0

awkward_reduce_prod_bool_bool_64 = awkward_reduce_prod_bool
awkward_reduce_prod_bool_int8_64 = awkward_reduce_prod_bool
awkward_reduce_prod_bool_int16_64 = awkward_reduce_prod_bool
awkward_reduce_prod_bool_int32_64 = awkward_reduce_prod_bool
awkward_reduce_prod_bool_int64_64 = awkward_reduce_prod_bool
awkward_reduce_prod_bool_uint8_64 = awkward_reduce_prod_bool
awkward_reduce_prod_bool_uint16_64 = awkward_reduce_prod_bool
awkward_reduce_prod_bool_uint32_64 = awkward_reduce_prod_bool
awkward_reduce_prod_bool_uint64_64 = awkward_reduce_prod_bool
awkward_reduce_prod_bool_float32_64 = awkward_reduce_prod_bool
awkward_reduce_prod_bool_float64_64 = awkward_reduce_prod_bool


def awkward_reduce_sum(toptr, fromptr, parents, lenparents, outlength):
    for i in range(outlength):
        toptr[i] = float(0)
    for i in range(lenparents):
        toptr[parents[i]] += float(fromptr[i])

awkward_reduce_sum_int32_int8_64 = awkward_reduce_sum
awkward_reduce_sum_int32_int16_64 = awkward_reduce_sum
awkward_reduce_sum_int32_int32_64 = awkward_reduce_sum
awkward_reduce_sum_int64_int8_64 = awkward_reduce_sum
awkward_reduce_sum_int64_int16_64 = awkward_reduce_sum
awkward_reduce_sum_int64_int32_64 = awkward_reduce_sum
awkward_reduce_sum_int64_int64_64 = awkward_reduce_sum
awkward_reduce_sum_uint32_uint8_64 = awkward_reduce_sum
awkward_reduce_sum_uint32_uint16_64 = awkward_reduce_sum
awkward_reduce_sum_uint32_uint32_64 = awkward_reduce_sum
awkward_reduce_sum_uint64_uint8_64 = awkward_reduce_sum
awkward_reduce_sum_uint64_uint16_64 = awkward_reduce_sum
awkward_reduce_sum_uint64_uint32_64 = awkward_reduce_sum
awkward_reduce_sum_uint64_uint64_64 = awkward_reduce_sum
awkward_reduce_sum_float32_float32_64 = awkward_reduce_sum
awkward_reduce_sum_float64_float64_64 = awkward_reduce_sum


def awkward_reduce_sum_bool(toptr, fromptr, parents, lenparents, outlength):
    for i in range(outlength):
        toptr[i] = False
    for i in range(lenparents):
        toptr[parents[i]] |= fromptr[i] != 0

awkward_reduce_sum_bool_bool_64 = awkward_reduce_sum_bool
awkward_reduce_sum_bool_int8_64 = awkward_reduce_sum_bool
awkward_reduce_sum_bool_int16_64 = awkward_reduce_sum_bool
awkward_reduce_sum_bool_int32_64 = awkward_reduce_sum_bool
awkward_reduce_sum_bool_int64_64 = awkward_reduce_sum_bool
awkward_reduce_sum_bool_uint8_64 = awkward_reduce_sum_bool
awkward_reduce_sum_bool_uint16_64 = awkward_reduce_sum_bool
awkward_reduce_sum_bool_uint32_64 = awkward_reduce_sum_bool
awkward_reduce_sum_bool_uint64_64 = awkward_reduce_sum_bool
awkward_reduce_sum_bool_float32_64 = awkward_reduce_sum_bool
awkward_reduce_sum_bool_float64_64 = awkward_reduce_sum_bool


def awkward_reduce_sum_int32_bool_64(toptr, fromptr, parents, lenparents, outlength):
    for i in range(outlength):
        toptr[i] = 0
    for i in range(lenparents):
        toptr[parents[i]] += fromptr[i] != 0

awkward_reduce_sum_int32_bool_64 = awkward_reduce_sum_int32_bool_64


def awkward_reduce_sum_int64_bool_64(toptr, fromptr, parents, lenparents, outlength):
    for i in range(outlength):
        toptr[i] = 0
    for i in range(lenparents):
        toptr[parents[i]] += fromptr[i] != 0

awkward_reduce_sum_int64_bool_64 = awkward_reduce_sum_int64_bool_64


