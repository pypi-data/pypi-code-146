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
    rupgd__nrlf = not is_overload_none(func_name)
    if rupgd__nrlf:
        func_name = get_overload_const_str(func_name)
        cvsl__ozhi = get_overload_const_bool(is_method)
    qsd__fcpel = out_arr_typ.instance_type if isinstance(out_arr_typ, types
        .TypeRef) else out_arr_typ
    yczy__fljmo = qsd__fcpel == types.none
    sgij__sppo = len(table.arr_types)
    if yczy__fljmo:
        lhf__livw = table
    else:
        cuyvy__wpb = tuple([qsd__fcpel] * sgij__sppo)
        lhf__livw = TableType(cuyvy__wpb)
    sfay__eddit = {'bodo': bodo, 'lst_dtype': qsd__fcpel, 'table_typ':
        lhf__livw}
    umsck__zlg = (
        'def impl(table, func_name, out_arr_typ, is_method, used_cols=None):\n'
        )
    if yczy__fljmo:
        umsck__zlg += (
            f'  out_table = bodo.hiframes.table.init_table(table, False)\n')
        umsck__zlg += f'  l = len(table)\n'
    else:
        umsck__zlg += f"""  out_list = bodo.hiframes.table.alloc_empty_list_type({sgij__sppo}, lst_dtype)
"""
    if not is_overload_none(used_cols):
        bkuw__huzye = used_cols.instance_type
        plyx__lwnup = np.array(bkuw__huzye.meta, dtype=np.int64)
        sfay__eddit['used_cols_glbl'] = plyx__lwnup
        ujl__zbj = set([table.block_nums[vph__ljbs] for vph__ljbs in
            plyx__lwnup])
        umsck__zlg += f'  used_cols_set = set(used_cols_glbl)\n'
    else:
        umsck__zlg += f'  used_cols_set = None\n'
        plyx__lwnup = None
    umsck__zlg += (
        f'  bodo.hiframes.table.ensure_table_unboxed(table, used_cols_set)\n')
    for gck__rmib in table.type_to_blk.values():
        umsck__zlg += f"""  blk_{gck__rmib} = bodo.hiframes.table.get_table_block(table, {gck__rmib})
"""
        if yczy__fljmo:
            umsck__zlg += f"""  out_list_{gck__rmib} = bodo.hiframes.table.alloc_list_like(blk_{gck__rmib}, len(blk_{gck__rmib}), False)
"""
            oaus__uhfv = f'out_list_{gck__rmib}'
        else:
            oaus__uhfv = 'out_list'
        if plyx__lwnup is None or gck__rmib in ujl__zbj:
            umsck__zlg += f'  for i in range(len(blk_{gck__rmib})):\n'
            sfay__eddit[f'col_indices_{gck__rmib}'] = np.array(table.
                block_to_arr_ind[gck__rmib], dtype=np.int64)
            umsck__zlg += f'    col_loc = col_indices_{gck__rmib}[i]\n'
            if plyx__lwnup is not None:
                umsck__zlg += f'    if col_loc not in used_cols_set:\n'
                umsck__zlg += f'        continue\n'
            if yczy__fljmo:
                eukpa__yruor = 'i'
            else:
                eukpa__yruor = 'col_loc'
            if not rupgd__nrlf:
                umsck__zlg += (
                    f'    {oaus__uhfv}[{eukpa__yruor}] = blk_{gck__rmib}[i]\n')
            elif cvsl__ozhi:
                umsck__zlg += f"""    {oaus__uhfv}[{eukpa__yruor}] = blk_{gck__rmib}[i].{func_name}()
"""
            else:
                umsck__zlg += f"""    {oaus__uhfv}[{eukpa__yruor}] = {func_name}(blk_{gck__rmib}[i])
"""
        if yczy__fljmo:
            umsck__zlg += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, {oaus__uhfv}, {gck__rmib})
"""
    if yczy__fljmo:
        umsck__zlg += (
            f'  out_table = bodo.hiframes.table.set_table_len(out_table, l)\n')
        umsck__zlg += '  return out_table\n'
    else:
        umsck__zlg += """  return bodo.hiframes.table.init_table_from_lists((out_list,), table_typ)
"""
    wri__skqii = {}
    exec(umsck__zlg, sfay__eddit, wri__skqii)
    return wri__skqii['impl']


def generate_mappable_table_func_equiv(self, scope, equiv_set, loc, args, kws):
    jlki__kbal = args[0]
    if equiv_set.has_shape(jlki__kbal):
        return ArrayAnalysis.AnalyzeResult(shape=jlki__kbal, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_utils_table_utils_generate_mappable_table_func
    ) = generate_mappable_table_func_equiv


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_table_nbytes(table, out_arr, start_offset, parallel=False):
    sfay__eddit = {'bodo': bodo, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value)}
    umsck__zlg = 'def impl(table, out_arr, start_offset, parallel=False):\n'
    umsck__zlg += '  bodo.hiframes.table.ensure_table_unboxed(table, None)\n'
    for gck__rmib in table.type_to_blk.values():
        umsck__zlg += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {gck__rmib})\n'
            )
        sfay__eddit[f'col_indices_{gck__rmib}'] = np.array(table.
            block_to_arr_ind[gck__rmib], dtype=np.int64)
        umsck__zlg += '  for i in range(len(blk)):\n'
        umsck__zlg += f'    col_loc = col_indices_{gck__rmib}[i]\n'
        umsck__zlg += '    out_arr[col_loc + start_offset] = blk[i].nbytes\n'
    umsck__zlg += '  if parallel:\n'
    umsck__zlg += '    for i in range(start_offset, len(out_arr)):\n'
    umsck__zlg += (
        '      out_arr[i] = bodo.libs.distributed_api.dist_reduce(out_arr[i], sum_op)\n'
        )
    wri__skqii = {}
    exec(umsck__zlg, sfay__eddit, wri__skqii)
    return wri__skqii['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_concat(table, col_nums_meta, arr_type):
    arr_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type
    gryod__uyqfb = table.type_to_blk[arr_type]
    sfay__eddit: Dict[str, Any] = {'bodo': bodo}
    sfay__eddit['col_indices'] = np.array(table.block_to_arr_ind[
        gryod__uyqfb], dtype=np.int64)
    klz__rcy = col_nums_meta.instance_type
    sfay__eddit['col_nums'] = np.array(klz__rcy.meta, np.int64)
    umsck__zlg = 'def impl(table, col_nums_meta, arr_type):\n'
    umsck__zlg += (
        f'  blk = bodo.hiframes.table.get_table_block(table, {gryod__uyqfb})\n'
        )
    umsck__zlg += (
        '  col_num_to_ind_in_blk = {c : i for i, c in enumerate(col_indices)}\n'
        )
    umsck__zlg += '  n = len(table)\n'
    huj__pfgi = arr_type == bodo.string_array_type
    if huj__pfgi:
        umsck__zlg += '  total_chars = 0\n'
        umsck__zlg += '  for c in col_nums:\n'
        umsck__zlg += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
        umsck__zlg += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
        umsck__zlg += (
            '    total_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n')
        umsck__zlg += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n * len(col_nums), total_chars)
"""
    else:
        umsck__zlg += """  out_arr = bodo.utils.utils.alloc_type(n * len(col_nums), arr_type, (-1,))
"""
    umsck__zlg += '  for i in range(len(col_nums)):\n'
    umsck__zlg += '    c = col_nums[i]\n'
    if not huj__pfgi:
        umsck__zlg += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
    umsck__zlg += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
    umsck__zlg += '    off = i * n\n'
    umsck__zlg += '    for j in range(len(arr)):\n'
    umsck__zlg += '      if bodo.libs.array_kernels.isna(arr, j):\n'
    umsck__zlg += '        bodo.libs.array_kernels.setna(out_arr, off+j)\n'
    umsck__zlg += '      else:\n'
    umsck__zlg += '        out_arr[off+j] = arr[j]\n'
    umsck__zlg += '  return out_arr\n'
    dtxey__qtteu = {}
    exec(umsck__zlg, sfay__eddit, dtxey__qtteu)
    wqom__vzb = dtxey__qtteu['impl']
    return wqom__vzb


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_astype(table, new_table_typ, copy, _bodo_nan_to_str, used_cols=None):
    new_table_typ = new_table_typ.instance_type
    xvlnl__mqw = not is_overload_false(copy)
    ktp__owq = is_overload_true(copy)
    sfay__eddit: Dict[str, Any] = {'bodo': bodo}
    oxl__rcl = table.arr_types
    ebiit__dqi = new_table_typ.arr_types
    xji__dyvp: Set[int] = set()
    ixhow__nnfl: Dict[types.Type, Set[types.Type]] = defaultdict(set)
    akul__qmtb: Set[types.Type] = set()
    for vph__ljbs, drjpa__vnu in enumerate(oxl__rcl):
        xrx__dkau = ebiit__dqi[vph__ljbs]
        if drjpa__vnu == xrx__dkau:
            akul__qmtb.add(drjpa__vnu)
        else:
            xji__dyvp.add(vph__ljbs)
            ixhow__nnfl[xrx__dkau].add(drjpa__vnu)
    umsck__zlg = (
        'def impl(table, new_table_typ, copy, _bodo_nan_to_str, used_cols=None):\n'
        )
    umsck__zlg += (
        f'  out_table = bodo.hiframes.table.init_table(new_table_typ, False)\n'
        )
    umsck__zlg += (
        f'  out_table = bodo.hiframes.table.set_table_len(out_table, len(table))\n'
        )
    skr__ffg = set(range(len(oxl__rcl)))
    lun__tmaa = skr__ffg - xji__dyvp
    if not is_overload_none(used_cols):
        bkuw__huzye = used_cols.instance_type
        flv__wbbq = set(bkuw__huzye.meta)
        xji__dyvp = xji__dyvp & flv__wbbq
        lun__tmaa = lun__tmaa & flv__wbbq
        ujl__zbj = set([table.block_nums[vph__ljbs] for vph__ljbs in flv__wbbq]
            )
    else:
        flv__wbbq = None
    ckr__kur = dict()
    for ele__clt in xji__dyvp:
        pcujv__hgoiw = table.block_nums[ele__clt]
        fikil__ejbn = new_table_typ.block_nums[ele__clt]
        if f'cast_cols_{pcujv__hgoiw}_{fikil__ejbn}' in ckr__kur:
            ckr__kur[f'cast_cols_{pcujv__hgoiw}_{fikil__ejbn}'].append(ele__clt
                )
        else:
            ckr__kur[f'cast_cols_{pcujv__hgoiw}_{fikil__ejbn}'] = [ele__clt]
    for bkl__mpfoy in table.blk_to_type:
        for fikil__ejbn in new_table_typ.blk_to_type:
            qlhd__nrs = ckr__kur.get(f'cast_cols_{bkl__mpfoy}_{fikil__ejbn}',
                [])
            sfay__eddit[f'cast_cols_{bkl__mpfoy}_{fikil__ejbn}'] = np.array(
                list(qlhd__nrs), dtype=np.int64)
            umsck__zlg += f"""  cast_cols_{bkl__mpfoy}_{fikil__ejbn}_set = set(cast_cols_{bkl__mpfoy}_{fikil__ejbn})
"""
    sfay__eddit['copied_cols'] = np.array(list(lun__tmaa), dtype=np.int64)
    umsck__zlg += f'  copied_cols_set = set(copied_cols)\n'
    for vwp__smb, cdinf__cid in new_table_typ.type_to_blk.items():
        sfay__eddit[f'typ_list_{cdinf__cid}'] = types.List(vwp__smb)
        umsck__zlg += f"""  out_arr_list_{cdinf__cid} = bodo.hiframes.table.alloc_list_like(typ_list_{cdinf__cid}, {len(new_table_typ.block_to_arr_ind[cdinf__cid])}, False)
"""
        if vwp__smb in akul__qmtb:
            pdb__asxf = table.type_to_blk[vwp__smb]
            if flv__wbbq is None or pdb__asxf in ujl__zbj:
                yfck__ejm = table.block_to_arr_ind[pdb__asxf]
                zfn__qpuvh = [new_table_typ.block_offsets[nos__yfho] for
                    nos__yfho in yfck__ejm]
                sfay__eddit[f'new_idx_{pdb__asxf}'] = np.array(zfn__qpuvh,
                    np.int64)
                sfay__eddit[f'orig_arr_inds_{pdb__asxf}'] = np.array(yfck__ejm,
                    np.int64)
                umsck__zlg += f"""  arr_list_{pdb__asxf} = bodo.hiframes.table.get_table_block(table, {pdb__asxf})
"""
                umsck__zlg += f'  for i in range(len(arr_list_{pdb__asxf})):\n'
                umsck__zlg += (
                    f'    arr_ind_{pdb__asxf} = orig_arr_inds_{pdb__asxf}[i]\n'
                    )
                umsck__zlg += (
                    f'    if arr_ind_{pdb__asxf} not in copied_cols_set:\n')
                umsck__zlg += f'      continue\n'
                umsck__zlg += f"""    bodo.hiframes.table.ensure_column_unboxed(table, arr_list_{pdb__asxf}, i, arr_ind_{pdb__asxf})
"""
                umsck__zlg += (
                    f'    out_idx_{cdinf__cid}_{pdb__asxf} = new_idx_{pdb__asxf}[i]\n'
                    )
                umsck__zlg += (
                    f'    arr_val_{pdb__asxf} = arr_list_{pdb__asxf}[i]\n')
                if ktp__owq:
                    umsck__zlg += (
                        f'    arr_val_{pdb__asxf} = arr_val_{pdb__asxf}.copy()\n'
                        )
                elif xvlnl__mqw:
                    umsck__zlg += f"""    arr_val_{pdb__asxf} = arr_val_{pdb__asxf}.copy() if copy else arr_val_{cdinf__cid}
"""
                umsck__zlg += f"""    out_arr_list_{cdinf__cid}[out_idx_{cdinf__cid}_{pdb__asxf}] = arr_val_{pdb__asxf}
"""
    ttbns__neuee = set()
    for vwp__smb, cdinf__cid in new_table_typ.type_to_blk.items():
        if vwp__smb in ixhow__nnfl:
            sfay__eddit[f'typ_{cdinf__cid}'] = get_castable_arr_dtype(vwp__smb)
            fvam__awm = ixhow__nnfl[vwp__smb]
            for duj__dft in fvam__awm:
                pdb__asxf = table.type_to_blk[duj__dft]
                if flv__wbbq is None or pdb__asxf in ujl__zbj:
                    if (duj__dft not in akul__qmtb and duj__dft not in
                        ttbns__neuee):
                        yfck__ejm = table.block_to_arr_ind[pdb__asxf]
                        zfn__qpuvh = [new_table_typ.block_offsets[nos__yfho
                            ] for nos__yfho in yfck__ejm]
                        sfay__eddit[f'new_idx_{pdb__asxf}'] = np.array(
                            zfn__qpuvh, np.int64)
                        sfay__eddit[f'orig_arr_inds_{pdb__asxf}'] = np.array(
                            yfck__ejm, np.int64)
                        umsck__zlg += f"""  arr_list_{pdb__asxf} = bodo.hiframes.table.get_table_block(table, {pdb__asxf})
"""
                    ttbns__neuee.add(duj__dft)
                    umsck__zlg += (
                        f'  for i in range(len(arr_list_{pdb__asxf})):\n')
                    umsck__zlg += (
                        f'    arr_ind_{pdb__asxf} = orig_arr_inds_{pdb__asxf}[i]\n'
                        )
                    umsck__zlg += f"""    if arr_ind_{pdb__asxf} not in cast_cols_{pdb__asxf}_{cdinf__cid}_set:
"""
                    umsck__zlg += f'      continue\n'
                    umsck__zlg += f"""    bodo.hiframes.table.ensure_column_unboxed(table, arr_list_{pdb__asxf}, i, arr_ind_{pdb__asxf})
"""
                    umsck__zlg += (
                        f'    out_idx_{cdinf__cid}_{pdb__asxf} = new_idx_{pdb__asxf}[i]\n'
                        )
                    umsck__zlg += f"""    arr_val_{cdinf__cid} =  bodo.utils.conversion.fix_arr_dtype(arr_list_{pdb__asxf}[i], typ_{cdinf__cid}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)
"""
                    umsck__zlg += f"""    out_arr_list_{cdinf__cid}[out_idx_{cdinf__cid}_{pdb__asxf}] = arr_val_{cdinf__cid}
"""
        umsck__zlg += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, out_arr_list_{cdinf__cid}, {cdinf__cid})
"""
    umsck__zlg += '  return out_table\n'
    wri__skqii = {}
    exec(umsck__zlg, sfay__eddit, wri__skqii)
    return wri__skqii['impl']


def table_astype_equiv(self, scope, equiv_set, loc, args, kws):
    jlki__kbal = args[0]
    if equiv_set.has_shape(jlki__kbal):
        return ArrayAnalysis.AnalyzeResult(shape=jlki__kbal, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_utils_table_utils_table_astype = (
    table_astype_equiv)
