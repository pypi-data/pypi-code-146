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
    orq__bgoy = not is_overload_none(func_name)
    if orq__bgoy:
        func_name = get_overload_const_str(func_name)
        brw__aogz = get_overload_const_bool(is_method)
    yyxha__sjfs = out_arr_typ.instance_type if isinstance(out_arr_typ,
        types.TypeRef) else out_arr_typ
    cmjr__grfbu = yyxha__sjfs == types.none
    ynuid__kjxa = len(table.arr_types)
    if cmjr__grfbu:
        tucnl__mfyji = table
    else:
        wvq__knig = tuple([yyxha__sjfs] * ynuid__kjxa)
        tucnl__mfyji = TableType(wvq__knig)
    rgkwr__fnmx = {'bodo': bodo, 'lst_dtype': yyxha__sjfs, 'table_typ':
        tucnl__mfyji}
    gojm__epq = (
        'def impl(table, func_name, out_arr_typ, is_method, used_cols=None):\n'
        )
    if cmjr__grfbu:
        gojm__epq += (
            f'  out_table = bodo.hiframes.table.init_table(table, False)\n')
        gojm__epq += f'  l = len(table)\n'
    else:
        gojm__epq += f"""  out_list = bodo.hiframes.table.alloc_empty_list_type({ynuid__kjxa}, lst_dtype)
"""
    if not is_overload_none(used_cols):
        nwfd__zibud = used_cols.instance_type
        xbkp__emcju = np.array(nwfd__zibud.meta, dtype=np.int64)
        rgkwr__fnmx['used_cols_glbl'] = xbkp__emcju
        vha__zuw = set([table.block_nums[uhvaz__fdvj] for uhvaz__fdvj in
            xbkp__emcju])
        gojm__epq += f'  used_cols_set = set(used_cols_glbl)\n'
    else:
        gojm__epq += f'  used_cols_set = None\n'
        xbkp__emcju = None
    gojm__epq += (
        f'  bodo.hiframes.table.ensure_table_unboxed(table, used_cols_set)\n')
    for ulard__dbv in table.type_to_blk.values():
        gojm__epq += f"""  blk_{ulard__dbv} = bodo.hiframes.table.get_table_block(table, {ulard__dbv})
"""
        if cmjr__grfbu:
            gojm__epq += f"""  out_list_{ulard__dbv} = bodo.hiframes.table.alloc_list_like(blk_{ulard__dbv}, len(blk_{ulard__dbv}), False)
"""
            rxa__cgdds = f'out_list_{ulard__dbv}'
        else:
            rxa__cgdds = 'out_list'
        if xbkp__emcju is None or ulard__dbv in vha__zuw:
            gojm__epq += f'  for i in range(len(blk_{ulard__dbv})):\n'
            rgkwr__fnmx[f'col_indices_{ulard__dbv}'] = np.array(table.
                block_to_arr_ind[ulard__dbv], dtype=np.int64)
            gojm__epq += f'    col_loc = col_indices_{ulard__dbv}[i]\n'
            if xbkp__emcju is not None:
                gojm__epq += f'    if col_loc not in used_cols_set:\n'
                gojm__epq += f'        continue\n'
            if cmjr__grfbu:
                ytrdc__pypa = 'i'
            else:
                ytrdc__pypa = 'col_loc'
            if not orq__bgoy:
                gojm__epq += (
                    f'    {rxa__cgdds}[{ytrdc__pypa}] = blk_{ulard__dbv}[i]\n')
            elif brw__aogz:
                gojm__epq += f"""    {rxa__cgdds}[{ytrdc__pypa}] = blk_{ulard__dbv}[i].{func_name}()
"""
            else:
                gojm__epq += (
                    f'    {rxa__cgdds}[{ytrdc__pypa}] = {func_name}(blk_{ulard__dbv}[i])\n'
                    )
        if cmjr__grfbu:
            gojm__epq += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, {rxa__cgdds}, {ulard__dbv})
"""
    if cmjr__grfbu:
        gojm__epq += (
            f'  out_table = bodo.hiframes.table.set_table_len(out_table, l)\n')
        gojm__epq += '  return out_table\n'
    else:
        gojm__epq += (
            '  return bodo.hiframes.table.init_table_from_lists((out_list,), table_typ)\n'
            )
    edhh__xqu = {}
    exec(gojm__epq, rgkwr__fnmx, edhh__xqu)
    return edhh__xqu['impl']


def generate_mappable_table_func_equiv(self, scope, equiv_set, loc, args, kws):
    ablgn__qlib = args[0]
    if equiv_set.has_shape(ablgn__qlib):
        return ArrayAnalysis.AnalyzeResult(shape=ablgn__qlib, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_utils_table_utils_generate_mappable_table_func
    ) = generate_mappable_table_func_equiv


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_table_nbytes(table, out_arr, start_offset, parallel=False):
    rgkwr__fnmx = {'bodo': bodo, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value)}
    gojm__epq = 'def impl(table, out_arr, start_offset, parallel=False):\n'
    gojm__epq += '  bodo.hiframes.table.ensure_table_unboxed(table, None)\n'
    for ulard__dbv in table.type_to_blk.values():
        gojm__epq += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {ulard__dbv})\n'
            )
        rgkwr__fnmx[f'col_indices_{ulard__dbv}'] = np.array(table.
            block_to_arr_ind[ulard__dbv], dtype=np.int64)
        gojm__epq += '  for i in range(len(blk)):\n'
        gojm__epq += f'    col_loc = col_indices_{ulard__dbv}[i]\n'
        gojm__epq += '    out_arr[col_loc + start_offset] = blk[i].nbytes\n'
    gojm__epq += '  if parallel:\n'
    gojm__epq += '    for i in range(start_offset, len(out_arr)):\n'
    gojm__epq += (
        '      out_arr[i] = bodo.libs.distributed_api.dist_reduce(out_arr[i], sum_op)\n'
        )
    edhh__xqu = {}
    exec(gojm__epq, rgkwr__fnmx, edhh__xqu)
    return edhh__xqu['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_concat(table, col_nums_meta, arr_type):
    arr_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type
    gqq__uchrp = table.type_to_blk[arr_type]
    rgkwr__fnmx: Dict[str, Any] = {'bodo': bodo}
    rgkwr__fnmx['col_indices'] = np.array(table.block_to_arr_ind[gqq__uchrp
        ], dtype=np.int64)
    msspk__hpn = col_nums_meta.instance_type
    rgkwr__fnmx['col_nums'] = np.array(msspk__hpn.meta, np.int64)
    gojm__epq = 'def impl(table, col_nums_meta, arr_type):\n'
    gojm__epq += (
        f'  blk = bodo.hiframes.table.get_table_block(table, {gqq__uchrp})\n')
    gojm__epq += (
        '  col_num_to_ind_in_blk = {c : i for i, c in enumerate(col_indices)}\n'
        )
    gojm__epq += '  n = len(table)\n'
    dxk__wnjom = arr_type == bodo.string_array_type
    if dxk__wnjom:
        gojm__epq += '  total_chars = 0\n'
        gojm__epq += '  for c in col_nums:\n'
        gojm__epq += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
        gojm__epq += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
        gojm__epq += (
            '    total_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n')
        gojm__epq += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n * len(col_nums), total_chars)
"""
    else:
        gojm__epq += """  out_arr = bodo.utils.utils.alloc_type(n * len(col_nums), arr_type, (-1,))
"""
    gojm__epq += '  for i in range(len(col_nums)):\n'
    gojm__epq += '    c = col_nums[i]\n'
    if not dxk__wnjom:
        gojm__epq += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
    gojm__epq += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
    gojm__epq += '    off = i * n\n'
    gojm__epq += '    for j in range(len(arr)):\n'
    gojm__epq += '      if bodo.libs.array_kernels.isna(arr, j):\n'
    gojm__epq += '        bodo.libs.array_kernels.setna(out_arr, off+j)\n'
    gojm__epq += '      else:\n'
    gojm__epq += '        out_arr[off+j] = arr[j]\n'
    gojm__epq += '  return out_arr\n'
    dkq__olqn = {}
    exec(gojm__epq, rgkwr__fnmx, dkq__olqn)
    hpm__nyjtd = dkq__olqn['impl']
    return hpm__nyjtd


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_astype(table, new_table_typ, copy, _bodo_nan_to_str, used_cols=None):
    new_table_typ = new_table_typ.instance_type
    pyi__qhon = not is_overload_false(copy)
    ewtis__lxdi = is_overload_true(copy)
    rgkwr__fnmx: Dict[str, Any] = {'bodo': bodo}
    vov__jnvtr = table.arr_types
    opf__lccpf = new_table_typ.arr_types
    abh__ujmh: Set[int] = set()
    jij__tjg: Dict[types.Type, Set[types.Type]] = defaultdict(set)
    xwfv__xqx: Set[types.Type] = set()
    for uhvaz__fdvj, xvayt__hjjg in enumerate(vov__jnvtr):
        rgcn__vpr = opf__lccpf[uhvaz__fdvj]
        if xvayt__hjjg == rgcn__vpr:
            xwfv__xqx.add(xvayt__hjjg)
        else:
            abh__ujmh.add(uhvaz__fdvj)
            jij__tjg[rgcn__vpr].add(xvayt__hjjg)
    gojm__epq = (
        'def impl(table, new_table_typ, copy, _bodo_nan_to_str, used_cols=None):\n'
        )
    gojm__epq += (
        f'  out_table = bodo.hiframes.table.init_table(new_table_typ, False)\n'
        )
    gojm__epq += (
        f'  out_table = bodo.hiframes.table.set_table_len(out_table, len(table))\n'
        )
    vqgzz__wht = set(range(len(vov__jnvtr)))
    jbvlg__hjfh = vqgzz__wht - abh__ujmh
    if not is_overload_none(used_cols):
        nwfd__zibud = used_cols.instance_type
        opz__ply = set(nwfd__zibud.meta)
        abh__ujmh = abh__ujmh & opz__ply
        jbvlg__hjfh = jbvlg__hjfh & opz__ply
        vha__zuw = set([table.block_nums[uhvaz__fdvj] for uhvaz__fdvj in
            opz__ply])
    else:
        opz__ply = None
    fwchr__srknf = dict()
    for ofkta__qvye in abh__ujmh:
        rxrue__jkc = table.block_nums[ofkta__qvye]
        kjyt__sguxn = new_table_typ.block_nums[ofkta__qvye]
        if f'cast_cols_{rxrue__jkc}_{kjyt__sguxn}' in fwchr__srknf:
            fwchr__srknf[f'cast_cols_{rxrue__jkc}_{kjyt__sguxn}'].append(
                ofkta__qvye)
        else:
            fwchr__srknf[f'cast_cols_{rxrue__jkc}_{kjyt__sguxn}'] = [
                ofkta__qvye]
    for nfpo__tvh in table.blk_to_type:
        for kjyt__sguxn in new_table_typ.blk_to_type:
            khvv__dtw = fwchr__srknf.get(f'cast_cols_{nfpo__tvh}_{kjyt__sguxn}'
                , [])
            rgkwr__fnmx[f'cast_cols_{nfpo__tvh}_{kjyt__sguxn}'] = np.array(list
                (khvv__dtw), dtype=np.int64)
            gojm__epq += f"""  cast_cols_{nfpo__tvh}_{kjyt__sguxn}_set = set(cast_cols_{nfpo__tvh}_{kjyt__sguxn})
"""
    rgkwr__fnmx['copied_cols'] = np.array(list(jbvlg__hjfh), dtype=np.int64)
    gojm__epq += f'  copied_cols_set = set(copied_cols)\n'
    for zne__ezoyj, oayqo__spbd in new_table_typ.type_to_blk.items():
        rgkwr__fnmx[f'typ_list_{oayqo__spbd}'] = types.List(zne__ezoyj)
        gojm__epq += f"""  out_arr_list_{oayqo__spbd} = bodo.hiframes.table.alloc_list_like(typ_list_{oayqo__spbd}, {len(new_table_typ.block_to_arr_ind[oayqo__spbd])}, False)
"""
        if zne__ezoyj in xwfv__xqx:
            obgjq__jgpj = table.type_to_blk[zne__ezoyj]
            if opz__ply is None or obgjq__jgpj in vha__zuw:
                eatg__uru = table.block_to_arr_ind[obgjq__jgpj]
                wki__hbby = [new_table_typ.block_offsets[hxwf__ldxct] for
                    hxwf__ldxct in eatg__uru]
                rgkwr__fnmx[f'new_idx_{obgjq__jgpj}'] = np.array(wki__hbby,
                    np.int64)
                rgkwr__fnmx[f'orig_arr_inds_{obgjq__jgpj}'] = np.array(
                    eatg__uru, np.int64)
                gojm__epq += f"""  arr_list_{obgjq__jgpj} = bodo.hiframes.table.get_table_block(table, {obgjq__jgpj})
"""
                gojm__epq += (
                    f'  for i in range(len(arr_list_{obgjq__jgpj})):\n')
                gojm__epq += (
                    f'    arr_ind_{obgjq__jgpj} = orig_arr_inds_{obgjq__jgpj}[i]\n'
                    )
                gojm__epq += (
                    f'    if arr_ind_{obgjq__jgpj} not in copied_cols_set:\n')
                gojm__epq += f'      continue\n'
                gojm__epq += f"""    bodo.hiframes.table.ensure_column_unboxed(table, arr_list_{obgjq__jgpj}, i, arr_ind_{obgjq__jgpj})
"""
                gojm__epq += (
                    f'    out_idx_{oayqo__spbd}_{obgjq__jgpj} = new_idx_{obgjq__jgpj}[i]\n'
                    )
                gojm__epq += (
                    f'    arr_val_{obgjq__jgpj} = arr_list_{obgjq__jgpj}[i]\n')
                if ewtis__lxdi:
                    gojm__epq += (
                        f'    arr_val_{obgjq__jgpj} = arr_val_{obgjq__jgpj}.copy()\n'
                        )
                elif pyi__qhon:
                    gojm__epq += f"""    arr_val_{obgjq__jgpj} = arr_val_{obgjq__jgpj}.copy() if copy else arr_val_{oayqo__spbd}
"""
                gojm__epq += f"""    out_arr_list_{oayqo__spbd}[out_idx_{oayqo__spbd}_{obgjq__jgpj}] = arr_val_{obgjq__jgpj}
"""
    zimz__wfjc = set()
    for zne__ezoyj, oayqo__spbd in new_table_typ.type_to_blk.items():
        if zne__ezoyj in jij__tjg:
            rgkwr__fnmx[f'typ_{oayqo__spbd}'] = get_castable_arr_dtype(
                zne__ezoyj)
            pbjeu__lewm = jij__tjg[zne__ezoyj]
            for jua__uwm in pbjeu__lewm:
                obgjq__jgpj = table.type_to_blk[jua__uwm]
                if opz__ply is None or obgjq__jgpj in vha__zuw:
                    if (jua__uwm not in xwfv__xqx and jua__uwm not in
                        zimz__wfjc):
                        eatg__uru = table.block_to_arr_ind[obgjq__jgpj]
                        wki__hbby = [new_table_typ.block_offsets[
                            hxwf__ldxct] for hxwf__ldxct in eatg__uru]
                        rgkwr__fnmx[f'new_idx_{obgjq__jgpj}'] = np.array(
                            wki__hbby, np.int64)
                        rgkwr__fnmx[f'orig_arr_inds_{obgjq__jgpj}'] = np.array(
                            eatg__uru, np.int64)
                        gojm__epq += f"""  arr_list_{obgjq__jgpj} = bodo.hiframes.table.get_table_block(table, {obgjq__jgpj})
"""
                    zimz__wfjc.add(jua__uwm)
                    gojm__epq += (
                        f'  for i in range(len(arr_list_{obgjq__jgpj})):\n')
                    gojm__epq += (
                        f'    arr_ind_{obgjq__jgpj} = orig_arr_inds_{obgjq__jgpj}[i]\n'
                        )
                    gojm__epq += f"""    if arr_ind_{obgjq__jgpj} not in cast_cols_{obgjq__jgpj}_{oayqo__spbd}_set:
"""
                    gojm__epq += f'      continue\n'
                    gojm__epq += f"""    bodo.hiframes.table.ensure_column_unboxed(table, arr_list_{obgjq__jgpj}, i, arr_ind_{obgjq__jgpj})
"""
                    gojm__epq += f"""    out_idx_{oayqo__spbd}_{obgjq__jgpj} = new_idx_{obgjq__jgpj}[i]
"""
                    gojm__epq += f"""    arr_val_{oayqo__spbd} =  bodo.utils.conversion.fix_arr_dtype(arr_list_{obgjq__jgpj}[i], typ_{oayqo__spbd}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)
"""
                    gojm__epq += f"""    out_arr_list_{oayqo__spbd}[out_idx_{oayqo__spbd}_{obgjq__jgpj}] = arr_val_{oayqo__spbd}
"""
        gojm__epq += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, out_arr_list_{oayqo__spbd}, {oayqo__spbd})
"""
    gojm__epq += '  return out_table\n'
    edhh__xqu = {}
    exec(gojm__epq, rgkwr__fnmx, edhh__xqu)
    return edhh__xqu['impl']


def table_astype_equiv(self, scope, equiv_set, loc, args, kws):
    ablgn__qlib = args[0]
    if equiv_set.has_shape(ablgn__qlib):
        return ArrayAnalysis.AnalyzeResult(shape=ablgn__qlib, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_utils_table_utils_table_astype = (
    table_astype_equiv)
