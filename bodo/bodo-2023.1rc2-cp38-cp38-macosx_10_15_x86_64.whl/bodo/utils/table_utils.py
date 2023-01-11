"""File containing utility functions for supporting DataFrame operations with Table Format."""
from collections import defaultdict
from typing import Any, Dict, Set
import numba
import numpy as np
from numba.core import types
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.table import TableType
from bodo.utils.typing import get_castable_arr_dtype, get_overload_const_bool, get_overload_const_str, is_overload_constant_bool, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, raise_bodo_error


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_mappable_table_func(table, func_name, out_arr_typ, is_method,
    used_cols=None):
    if not is_overload_constant_str(func_name) and not is_overload_none(
        func_name):
        raise_bodo_error(
            'generate_mappable_table_func(): func_name must be a constant string'
            )
    if not is_overload_constant_bool(is_method):
        raise_bodo_error(
            'generate_mappable_table_func(): is_method must be a constant boolean'
            )
    ekcdk__ywrn = not is_overload_none(func_name)
    if ekcdk__ywrn:
        func_name = get_overload_const_str(func_name)
        cwc__kuq = get_overload_const_bool(is_method)
    fdibh__djax = out_arr_typ.instance_type if isinstance(out_arr_typ,
        types.TypeRef) else out_arr_typ
    ubzdn__zissv = fdibh__djax == types.none
    vvz__wehaa = len(table.arr_types)
    if ubzdn__zissv:
        jgzb__hhdux = table
    else:
        ryr__wpj = tuple([fdibh__djax] * vvz__wehaa)
        jgzb__hhdux = TableType(ryr__wpj)
    bqxbc__loptt = {'bodo': bodo, 'lst_dtype': fdibh__djax, 'table_typ':
        jgzb__hhdux}
    dmkmw__fmys = (
        'def impl(table, func_name, out_arr_typ, is_method, used_cols=None):\n'
        )
    if ubzdn__zissv:
        dmkmw__fmys += (
            f'  out_table = bodo.hiframes.table.init_table(table, False)\n')
        dmkmw__fmys += f'  l = len(table)\n'
    else:
        dmkmw__fmys += f"""  out_list = bodo.hiframes.table.alloc_empty_list_type({vvz__wehaa}, lst_dtype)
"""
    if not is_overload_none(used_cols):
        psm__dhql = used_cols.instance_type
        bxbn__mqsft = np.array(psm__dhql.meta, dtype=np.int64)
        bqxbc__loptt['used_cols_glbl'] = bxbn__mqsft
        hbz__ytml = set([table.block_nums[cakya__cqch] for cakya__cqch in
            bxbn__mqsft])
        dmkmw__fmys += f'  used_cols_set = set(used_cols_glbl)\n'
    else:
        dmkmw__fmys += f'  used_cols_set = None\n'
        bxbn__mqsft = None
    dmkmw__fmys += (
        f'  bodo.hiframes.table.ensure_table_unboxed(table, used_cols_set)\n')
    for vfsik__vol in table.type_to_blk.values():
        dmkmw__fmys += f"""  blk_{vfsik__vol} = bodo.hiframes.table.get_table_block(table, {vfsik__vol})
"""
        if ubzdn__zissv:
            dmkmw__fmys += f"""  out_list_{vfsik__vol} = bodo.hiframes.table.alloc_list_like(blk_{vfsik__vol}, len(blk_{vfsik__vol}), False)
"""
            hefke__ltba = f'out_list_{vfsik__vol}'
        else:
            hefke__ltba = 'out_list'
        if bxbn__mqsft is None or vfsik__vol in hbz__ytml:
            dmkmw__fmys += f'  for i in range(len(blk_{vfsik__vol})):\n'
            bqxbc__loptt[f'col_indices_{vfsik__vol}'] = np.array(table.
                block_to_arr_ind[vfsik__vol], dtype=np.int64)
            dmkmw__fmys += f'    col_loc = col_indices_{vfsik__vol}[i]\n'
            if bxbn__mqsft is not None:
                dmkmw__fmys += f'    if col_loc not in used_cols_set:\n'
                dmkmw__fmys += f'        continue\n'
            if ubzdn__zissv:
                msv__yttx = 'i'
            else:
                msv__yttx = 'col_loc'
            if not ekcdk__ywrn:
                dmkmw__fmys += (
                    f'    {hefke__ltba}[{msv__yttx}] = blk_{vfsik__vol}[i]\n')
            elif cwc__kuq:
                dmkmw__fmys += f"""    {hefke__ltba}[{msv__yttx}] = blk_{vfsik__vol}[i].{func_name}()
"""
            else:
                dmkmw__fmys += f"""    {hefke__ltba}[{msv__yttx}] = {func_name}(blk_{vfsik__vol}[i])
"""
        if ubzdn__zissv:
            dmkmw__fmys += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, {hefke__ltba}, {vfsik__vol})
"""
    if ubzdn__zissv:
        dmkmw__fmys += (
            f'  out_table = bodo.hiframes.table.set_table_len(out_table, l)\n')
        dmkmw__fmys += '  return out_table\n'
    else:
        dmkmw__fmys += """  return bodo.hiframes.table.init_table_from_lists((out_list,), table_typ)
"""
    vmbf__feqzu = {}
    exec(dmkmw__fmys, bqxbc__loptt, vmbf__feqzu)
    return vmbf__feqzu['impl']


def generate_mappable_table_func_equiv(self, scope, equiv_set, loc, args, kws):
    ahmd__flm = args[0]
    if equiv_set.has_shape(ahmd__flm):
        return ArrayAnalysis.AnalyzeResult(shape=ahmd__flm, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_utils_table_utils_generate_mappable_table_func
    ) = generate_mappable_table_func_equiv


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_table_nbytes(table, out_arr, start_offset, parallel=False):
    bqxbc__loptt = {'bodo': bodo, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value)}
    dmkmw__fmys = 'def impl(table, out_arr, start_offset, parallel=False):\n'
    dmkmw__fmys += '  bodo.hiframes.table.ensure_table_unboxed(table, None)\n'
    for vfsik__vol in table.type_to_blk.values():
        dmkmw__fmys += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {vfsik__vol})\n'
            )
        bqxbc__loptt[f'col_indices_{vfsik__vol}'] = np.array(table.
            block_to_arr_ind[vfsik__vol], dtype=np.int64)
        dmkmw__fmys += '  for i in range(len(blk)):\n'
        dmkmw__fmys += f'    col_loc = col_indices_{vfsik__vol}[i]\n'
        dmkmw__fmys += '    out_arr[col_loc + start_offset] = blk[i].nbytes\n'
    dmkmw__fmys += '  if parallel:\n'
    dmkmw__fmys += '    for i in range(start_offset, len(out_arr)):\n'
    dmkmw__fmys += (
        '      out_arr[i] = bodo.libs.distributed_api.dist_reduce(out_arr[i], sum_op)\n'
        )
    vmbf__feqzu = {}
    exec(dmkmw__fmys, bqxbc__loptt, vmbf__feqzu)
    return vmbf__feqzu['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_concat(table, col_nums_meta, arr_type):
    arr_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type
    yrfos__mnx = table.type_to_blk[arr_type]
    bqxbc__loptt: Dict[str, Any] = {'bodo': bodo}
    bqxbc__loptt['col_indices'] = np.array(table.block_to_arr_ind[
        yrfos__mnx], dtype=np.int64)
    may__ariax = col_nums_meta.instance_type
    bqxbc__loptt['col_nums'] = np.array(may__ariax.meta, np.int64)
    dmkmw__fmys = 'def impl(table, col_nums_meta, arr_type):\n'
    dmkmw__fmys += (
        f'  blk = bodo.hiframes.table.get_table_block(table, {yrfos__mnx})\n')
    dmkmw__fmys += (
        '  col_num_to_ind_in_blk = {c : i for i, c in enumerate(col_indices)}\n'
        )
    dmkmw__fmys += '  n = len(table)\n'
    nbark__tafq = arr_type == bodo.string_array_type
    if nbark__tafq:
        dmkmw__fmys += '  total_chars = 0\n'
        dmkmw__fmys += '  for c in col_nums:\n'
        dmkmw__fmys += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
        dmkmw__fmys += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
        dmkmw__fmys += (
            '    total_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n')
        dmkmw__fmys += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n * len(col_nums), total_chars)
"""
    else:
        dmkmw__fmys += """  out_arr = bodo.utils.utils.alloc_type(n * len(col_nums), arr_type, (-1,))
"""
    dmkmw__fmys += '  for i in range(len(col_nums)):\n'
    dmkmw__fmys += '    c = col_nums[i]\n'
    if not nbark__tafq:
        dmkmw__fmys += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
    dmkmw__fmys += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
    dmkmw__fmys += '    off = i * n\n'
    dmkmw__fmys += '    for j in range(len(arr)):\n'
    dmkmw__fmys += '      if bodo.libs.array_kernels.isna(arr, j):\n'
    dmkmw__fmys += '        bodo.libs.array_kernels.setna(out_arr, off+j)\n'
    dmkmw__fmys += '      else:\n'
    dmkmw__fmys += '        out_arr[off+j] = arr[j]\n'
    dmkmw__fmys += '  return out_arr\n'
    cpj__gfrhq = {}
    exec(dmkmw__fmys, bqxbc__loptt, cpj__gfrhq)
    rvx__scvv = cpj__gfrhq['impl']
    return rvx__scvv


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_astype(table, new_table_typ, copy, _bodo_nan_to_str, used_cols=None):
    new_table_typ = new_table_typ.instance_type
    ccxp__iilh = not is_overload_false(copy)
    vyhed__dzh = is_overload_true(copy)
    bqxbc__loptt: Dict[str, Any] = {'bodo': bodo}
    jqrh__ces = table.arr_types
    qzuz__hbglk = new_table_typ.arr_types
    uwo__lpn: Set[int] = set()
    qhzg__bamik: Dict[types.Type, Set[types.Type]] = defaultdict(set)
    tohzc__psa: Set[types.Type] = set()
    for cakya__cqch, zom__qot in enumerate(jqrh__ces):
        ogbmz__grjgy = qzuz__hbglk[cakya__cqch]
        if zom__qot == ogbmz__grjgy:
            tohzc__psa.add(zom__qot)
        else:
            uwo__lpn.add(cakya__cqch)
            qhzg__bamik[ogbmz__grjgy].add(zom__qot)
    dmkmw__fmys = (
        'def impl(table, new_table_typ, copy, _bodo_nan_to_str, used_cols=None):\n'
        )
    dmkmw__fmys += (
        f'  out_table = bodo.hiframes.table.init_table(new_table_typ, False)\n'
        )
    dmkmw__fmys += (
        f'  out_table = bodo.hiframes.table.set_table_len(out_table, len(table))\n'
        )
    zgvc__gatru = set(range(len(jqrh__ces)))
    wwqrg__nmjcb = zgvc__gatru - uwo__lpn
    if not is_overload_none(used_cols):
        psm__dhql = used_cols.instance_type
        rlpk__errtc = set(psm__dhql.meta)
        uwo__lpn = uwo__lpn & rlpk__errtc
        wwqrg__nmjcb = wwqrg__nmjcb & rlpk__errtc
        hbz__ytml = set([table.block_nums[cakya__cqch] for cakya__cqch in
            rlpk__errtc])
    else:
        rlpk__errtc = None
    xzg__yoo = dict()
    for bxpq__czqo in uwo__lpn:
        cmf__zxlg = table.block_nums[bxpq__czqo]
        olxs__amu = new_table_typ.block_nums[bxpq__czqo]
        if f'cast_cols_{cmf__zxlg}_{olxs__amu}' in xzg__yoo:
            xzg__yoo[f'cast_cols_{cmf__zxlg}_{olxs__amu}'].append(bxpq__czqo)
        else:
            xzg__yoo[f'cast_cols_{cmf__zxlg}_{olxs__amu}'] = [bxpq__czqo]
    for aaxsj__wbi in table.blk_to_type:
        for olxs__amu in new_table_typ.blk_to_type:
            mgrs__nij = xzg__yoo.get(f'cast_cols_{aaxsj__wbi}_{olxs__amu}', [])
            bqxbc__loptt[f'cast_cols_{aaxsj__wbi}_{olxs__amu}'] = np.array(list
                (mgrs__nij), dtype=np.int64)
            dmkmw__fmys += f"""  cast_cols_{aaxsj__wbi}_{olxs__amu}_set = set(cast_cols_{aaxsj__wbi}_{olxs__amu})
"""
    bqxbc__loptt['copied_cols'] = np.array(list(wwqrg__nmjcb), dtype=np.int64)
    dmkmw__fmys += f'  copied_cols_set = set(copied_cols)\n'
    for fnl__nio, paos__omxa in new_table_typ.type_to_blk.items():
        bqxbc__loptt[f'typ_list_{paos__omxa}'] = types.List(fnl__nio)
        dmkmw__fmys += f"""  out_arr_list_{paos__omxa} = bodo.hiframes.table.alloc_list_like(typ_list_{paos__omxa}, {len(new_table_typ.block_to_arr_ind[paos__omxa])}, False)
"""
        if fnl__nio in tohzc__psa:
            pbyn__dqgzw = table.type_to_blk[fnl__nio]
            if rlpk__errtc is None or pbyn__dqgzw in hbz__ytml:
                pzf__kuml = table.block_to_arr_ind[pbyn__dqgzw]
                ksrw__vsrux = [new_table_typ.block_offsets[mqjxw__yod] for
                    mqjxw__yod in pzf__kuml]
                bqxbc__loptt[f'new_idx_{pbyn__dqgzw}'] = np.array(ksrw__vsrux,
                    np.int64)
                bqxbc__loptt[f'orig_arr_inds_{pbyn__dqgzw}'] = np.array(
                    pzf__kuml, np.int64)
                dmkmw__fmys += f"""  arr_list_{pbyn__dqgzw} = bodo.hiframes.table.get_table_block(table, {pbyn__dqgzw})
"""
                dmkmw__fmys += (
                    f'  for i in range(len(arr_list_{pbyn__dqgzw})):\n')
                dmkmw__fmys += (
                    f'    arr_ind_{pbyn__dqgzw} = orig_arr_inds_{pbyn__dqgzw}[i]\n'
                    )
                dmkmw__fmys += (
                    f'    if arr_ind_{pbyn__dqgzw} not in copied_cols_set:\n')
                dmkmw__fmys += f'      continue\n'
                dmkmw__fmys += f"""    bodo.hiframes.table.ensure_column_unboxed(table, arr_list_{pbyn__dqgzw}, i, arr_ind_{pbyn__dqgzw})
"""
                dmkmw__fmys += f"""    out_idx_{paos__omxa}_{pbyn__dqgzw} = new_idx_{pbyn__dqgzw}[i]
"""
                dmkmw__fmys += (
                    f'    arr_val_{pbyn__dqgzw} = arr_list_{pbyn__dqgzw}[i]\n')
                if vyhed__dzh:
                    dmkmw__fmys += (
                        f'    arr_val_{pbyn__dqgzw} = arr_val_{pbyn__dqgzw}.copy()\n'
                        )
                elif ccxp__iilh:
                    dmkmw__fmys += f"""    arr_val_{pbyn__dqgzw} = arr_val_{pbyn__dqgzw}.copy() if copy else arr_val_{paos__omxa}
"""
                dmkmw__fmys += f"""    out_arr_list_{paos__omxa}[out_idx_{paos__omxa}_{pbyn__dqgzw}] = arr_val_{pbyn__dqgzw}
"""
    eid__ess = set()
    for fnl__nio, paos__omxa in new_table_typ.type_to_blk.items():
        if fnl__nio in qhzg__bamik:
            bqxbc__loptt[f'typ_{paos__omxa}'] = get_castable_arr_dtype(fnl__nio
                )
            qenor__gsw = qhzg__bamik[fnl__nio]
            for cfn__fdq in qenor__gsw:
                pbyn__dqgzw = table.type_to_blk[cfn__fdq]
                if rlpk__errtc is None or pbyn__dqgzw in hbz__ytml:
                    if cfn__fdq not in tohzc__psa and cfn__fdq not in eid__ess:
                        pzf__kuml = table.block_to_arr_ind[pbyn__dqgzw]
                        ksrw__vsrux = [new_table_typ.block_offsets[
                            mqjxw__yod] for mqjxw__yod in pzf__kuml]
                        bqxbc__loptt[f'new_idx_{pbyn__dqgzw}'] = np.array(
                            ksrw__vsrux, np.int64)
                        bqxbc__loptt[f'orig_arr_inds_{pbyn__dqgzw}'
                            ] = np.array(pzf__kuml, np.int64)
                        dmkmw__fmys += f"""  arr_list_{pbyn__dqgzw} = bodo.hiframes.table.get_table_block(table, {pbyn__dqgzw})
"""
                    eid__ess.add(cfn__fdq)
                    dmkmw__fmys += (
                        f'  for i in range(len(arr_list_{pbyn__dqgzw})):\n')
                    dmkmw__fmys += (
                        f'    arr_ind_{pbyn__dqgzw} = orig_arr_inds_{pbyn__dqgzw}[i]\n'
                        )
                    dmkmw__fmys += f"""    if arr_ind_{pbyn__dqgzw} not in cast_cols_{pbyn__dqgzw}_{paos__omxa}_set:
"""
                    dmkmw__fmys += f'      continue\n'
                    dmkmw__fmys += f"""    bodo.hiframes.table.ensure_column_unboxed(table, arr_list_{pbyn__dqgzw}, i, arr_ind_{pbyn__dqgzw})
"""
                    dmkmw__fmys += f"""    out_idx_{paos__omxa}_{pbyn__dqgzw} = new_idx_{pbyn__dqgzw}[i]
"""
                    dmkmw__fmys += f"""    arr_val_{paos__omxa} =  bodo.utils.conversion.fix_arr_dtype(arr_list_{pbyn__dqgzw}[i], typ_{paos__omxa}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)
"""
                    dmkmw__fmys += f"""    out_arr_list_{paos__omxa}[out_idx_{paos__omxa}_{pbyn__dqgzw}] = arr_val_{paos__omxa}
"""
        dmkmw__fmys += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, out_arr_list_{paos__omxa}, {paos__omxa})
"""
    dmkmw__fmys += '  return out_table\n'
    vmbf__feqzu = {}
    exec(dmkmw__fmys, bqxbc__loptt, vmbf__feqzu)
    return vmbf__feqzu['impl']


def table_astype_equiv(self, scope, equiv_set, loc, args, kws):
    ahmd__flm = args[0]
    if equiv_set.has_shape(ahmd__flm):
        return ArrayAnalysis.AnalyzeResult(shape=ahmd__flm, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_utils_table_utils_table_astype = (
    table_astype_equiv)
