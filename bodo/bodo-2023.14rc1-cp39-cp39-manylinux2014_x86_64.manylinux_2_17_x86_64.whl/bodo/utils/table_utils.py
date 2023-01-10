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
    dttvo__knn = not is_overload_none(func_name)
    if dttvo__knn:
        func_name = get_overload_const_str(func_name)
        tja__agsg = get_overload_const_bool(is_method)
    orkjz__tcnbl = out_arr_typ.instance_type if isinstance(out_arr_typ,
        types.TypeRef) else out_arr_typ
    zlfbb__ocivv = orkjz__tcnbl == types.none
    tmz__fwra = len(table.arr_types)
    if zlfbb__ocivv:
        dkk__wkq = table
    else:
        ksoma__bmkyv = tuple([orkjz__tcnbl] * tmz__fwra)
        dkk__wkq = TableType(ksoma__bmkyv)
    kvyp__pcyk = {'bodo': bodo, 'lst_dtype': orkjz__tcnbl, 'table_typ':
        dkk__wkq}
    dha__kudj = (
        'def impl(table, func_name, out_arr_typ, is_method, used_cols=None):\n'
        )
    if zlfbb__ocivv:
        dha__kudj += (
            f'  out_table = bodo.hiframes.table.init_table(table, False)\n')
        dha__kudj += f'  l = len(table)\n'
    else:
        dha__kudj += f"""  out_list = bodo.hiframes.table.alloc_empty_list_type({tmz__fwra}, lst_dtype)
"""
    if not is_overload_none(used_cols):
        tuw__rhv = used_cols.instance_type
        dgodx__kjb = np.array(tuw__rhv.meta, dtype=np.int64)
        kvyp__pcyk['used_cols_glbl'] = dgodx__kjb
        ttxc__umlbx = set([table.block_nums[ehuwx__inci] for ehuwx__inci in
            dgodx__kjb])
        dha__kudj += f'  used_cols_set = set(used_cols_glbl)\n'
    else:
        dha__kudj += f'  used_cols_set = None\n'
        dgodx__kjb = None
    dha__kudj += (
        f'  bodo.hiframes.table.ensure_table_unboxed(table, used_cols_set)\n')
    for dwdk__sme in table.type_to_blk.values():
        dha__kudj += f"""  blk_{dwdk__sme} = bodo.hiframes.table.get_table_block(table, {dwdk__sme})
"""
        if zlfbb__ocivv:
            dha__kudj += f"""  out_list_{dwdk__sme} = bodo.hiframes.table.alloc_list_like(blk_{dwdk__sme}, len(blk_{dwdk__sme}), False)
"""
            bnwc__url = f'out_list_{dwdk__sme}'
        else:
            bnwc__url = 'out_list'
        if dgodx__kjb is None or dwdk__sme in ttxc__umlbx:
            dha__kudj += f'  for i in range(len(blk_{dwdk__sme})):\n'
            kvyp__pcyk[f'col_indices_{dwdk__sme}'] = np.array(table.
                block_to_arr_ind[dwdk__sme], dtype=np.int64)
            dha__kudj += f'    col_loc = col_indices_{dwdk__sme}[i]\n'
            if dgodx__kjb is not None:
                dha__kudj += f'    if col_loc not in used_cols_set:\n'
                dha__kudj += f'        continue\n'
            if zlfbb__ocivv:
                htp__cer = 'i'
            else:
                htp__cer = 'col_loc'
            if not dttvo__knn:
                dha__kudj += (
                    f'    {bnwc__url}[{htp__cer}] = blk_{dwdk__sme}[i]\n')
            elif tja__agsg:
                dha__kudj += (
                    f'    {bnwc__url}[{htp__cer}] = blk_{dwdk__sme}[i].{func_name}()\n'
                    )
            else:
                dha__kudj += (
                    f'    {bnwc__url}[{htp__cer}] = {func_name}(blk_{dwdk__sme}[i])\n'
                    )
        if zlfbb__ocivv:
            dha__kudj += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, {bnwc__url}, {dwdk__sme})
"""
    if zlfbb__ocivv:
        dha__kudj += (
            f'  out_table = bodo.hiframes.table.set_table_len(out_table, l)\n')
        dha__kudj += '  return out_table\n'
    else:
        dha__kudj += (
            '  return bodo.hiframes.table.init_table_from_lists((out_list,), table_typ)\n'
            )
    nusb__jghg = {}
    exec(dha__kudj, kvyp__pcyk, nusb__jghg)
    return nusb__jghg['impl']


def generate_mappable_table_func_equiv(self, scope, equiv_set, loc, args, kws):
    ocag__vqb = args[0]
    if equiv_set.has_shape(ocag__vqb):
        return ArrayAnalysis.AnalyzeResult(shape=ocag__vqb, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_utils_table_utils_generate_mappable_table_func
    ) = generate_mappable_table_func_equiv


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_table_nbytes(table, out_arr, start_offset, parallel=False):
    kvyp__pcyk = {'bodo': bodo, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value)}
    dha__kudj = 'def impl(table, out_arr, start_offset, parallel=False):\n'
    dha__kudj += '  bodo.hiframes.table.ensure_table_unboxed(table, None)\n'
    for dwdk__sme in table.type_to_blk.values():
        dha__kudj += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {dwdk__sme})\n'
            )
        kvyp__pcyk[f'col_indices_{dwdk__sme}'] = np.array(table.
            block_to_arr_ind[dwdk__sme], dtype=np.int64)
        dha__kudj += '  for i in range(len(blk)):\n'
        dha__kudj += f'    col_loc = col_indices_{dwdk__sme}[i]\n'
        dha__kudj += '    out_arr[col_loc + start_offset] = blk[i].nbytes\n'
    dha__kudj += '  if parallel:\n'
    dha__kudj += '    for i in range(start_offset, len(out_arr)):\n'
    dha__kudj += (
        '      out_arr[i] = bodo.libs.distributed_api.dist_reduce(out_arr[i], sum_op)\n'
        )
    nusb__jghg = {}
    exec(dha__kudj, kvyp__pcyk, nusb__jghg)
    return nusb__jghg['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_concat(table, col_nums_meta, arr_type):
    arr_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type
    ecxl__mhm = table.type_to_blk[arr_type]
    kvyp__pcyk: Dict[str, Any] = {'bodo': bodo}
    kvyp__pcyk['col_indices'] = np.array(table.block_to_arr_ind[ecxl__mhm],
        dtype=np.int64)
    pbey__iadqp = col_nums_meta.instance_type
    kvyp__pcyk['col_nums'] = np.array(pbey__iadqp.meta, np.int64)
    dha__kudj = 'def impl(table, col_nums_meta, arr_type):\n'
    dha__kudj += (
        f'  blk = bodo.hiframes.table.get_table_block(table, {ecxl__mhm})\n')
    dha__kudj += (
        '  col_num_to_ind_in_blk = {c : i for i, c in enumerate(col_indices)}\n'
        )
    dha__kudj += '  n = len(table)\n'
    kair__ejxty = arr_type == bodo.string_array_type
    if kair__ejxty:
        dha__kudj += '  total_chars = 0\n'
        dha__kudj += '  for c in col_nums:\n'
        dha__kudj += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
        dha__kudj += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
        dha__kudj += (
            '    total_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n')
        dha__kudj += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n * len(col_nums), total_chars)
"""
    else:
        dha__kudj += """  out_arr = bodo.utils.utils.alloc_type(n * len(col_nums), arr_type, (-1,))
"""
    dha__kudj += '  for i in range(len(col_nums)):\n'
    dha__kudj += '    c = col_nums[i]\n'
    if not kair__ejxty:
        dha__kudj += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
    dha__kudj += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
    dha__kudj += '    off = i * n\n'
    dha__kudj += '    for j in range(len(arr)):\n'
    dha__kudj += '      if bodo.libs.array_kernels.isna(arr, j):\n'
    dha__kudj += '        bodo.libs.array_kernels.setna(out_arr, off+j)\n'
    dha__kudj += '      else:\n'
    dha__kudj += '        out_arr[off+j] = arr[j]\n'
    dha__kudj += '  return out_arr\n'
    kmaxb__okdkd = {}
    exec(dha__kudj, kvyp__pcyk, kmaxb__okdkd)
    ymgvq__yguo = kmaxb__okdkd['impl']
    return ymgvq__yguo


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_astype(table, new_table_typ, copy, _bodo_nan_to_str, used_cols=None):
    new_table_typ = new_table_typ.instance_type
    iyfl__zkqfh = not is_overload_false(copy)
    iymkh__lxvl = is_overload_true(copy)
    kvyp__pcyk: Dict[str, Any] = {'bodo': bodo}
    mjpdc__bcw = table.arr_types
    hzwiz__hbj = new_table_typ.arr_types
    eackx__myq: Set[int] = set()
    rqyy__tyxid: Dict[types.Type, Set[types.Type]] = defaultdict(set)
    lsbax__dfi: Set[types.Type] = set()
    for ehuwx__inci, iik__snc in enumerate(mjpdc__bcw):
        dqgdb__uop = hzwiz__hbj[ehuwx__inci]
        if iik__snc == dqgdb__uop:
            lsbax__dfi.add(iik__snc)
        else:
            eackx__myq.add(ehuwx__inci)
            rqyy__tyxid[dqgdb__uop].add(iik__snc)
    dha__kudj = (
        'def impl(table, new_table_typ, copy, _bodo_nan_to_str, used_cols=None):\n'
        )
    dha__kudj += (
        f'  out_table = bodo.hiframes.table.init_table(new_table_typ, False)\n'
        )
    dha__kudj += (
        f'  out_table = bodo.hiframes.table.set_table_len(out_table, len(table))\n'
        )
    ljmle__xsbka = set(range(len(mjpdc__bcw)))
    lyw__ttc = ljmle__xsbka - eackx__myq
    if not is_overload_none(used_cols):
        tuw__rhv = used_cols.instance_type
        yfrwo__fut = set(tuw__rhv.meta)
        eackx__myq = eackx__myq & yfrwo__fut
        lyw__ttc = lyw__ttc & yfrwo__fut
        ttxc__umlbx = set([table.block_nums[ehuwx__inci] for ehuwx__inci in
            yfrwo__fut])
    else:
        yfrwo__fut = None
    oggqa__tdwfe = dict()
    for kocu__bvp in eackx__myq:
        enmr__ppvu = table.block_nums[kocu__bvp]
        ruh__bylnr = new_table_typ.block_nums[kocu__bvp]
        if f'cast_cols_{enmr__ppvu}_{ruh__bylnr}' in oggqa__tdwfe:
            oggqa__tdwfe[f'cast_cols_{enmr__ppvu}_{ruh__bylnr}'].append(
                kocu__bvp)
        else:
            oggqa__tdwfe[f'cast_cols_{enmr__ppvu}_{ruh__bylnr}'] = [kocu__bvp]
    for rfi__hwnx in table.blk_to_type:
        for ruh__bylnr in new_table_typ.blk_to_type:
            ssev__hixng = oggqa__tdwfe.get(
                f'cast_cols_{rfi__hwnx}_{ruh__bylnr}', [])
            kvyp__pcyk[f'cast_cols_{rfi__hwnx}_{ruh__bylnr}'] = np.array(list
                (ssev__hixng), dtype=np.int64)
            dha__kudj += f"""  cast_cols_{rfi__hwnx}_{ruh__bylnr}_set = set(cast_cols_{rfi__hwnx}_{ruh__bylnr})
"""
    kvyp__pcyk['copied_cols'] = np.array(list(lyw__ttc), dtype=np.int64)
    dha__kudj += f'  copied_cols_set = set(copied_cols)\n'
    for lzgm__oftx, akhi__nezxj in new_table_typ.type_to_blk.items():
        kvyp__pcyk[f'typ_list_{akhi__nezxj}'] = types.List(lzgm__oftx)
        dha__kudj += f"""  out_arr_list_{akhi__nezxj} = bodo.hiframes.table.alloc_list_like(typ_list_{akhi__nezxj}, {len(new_table_typ.block_to_arr_ind[akhi__nezxj])}, False)
"""
        if lzgm__oftx in lsbax__dfi:
            epq__srzfs = table.type_to_blk[lzgm__oftx]
            if yfrwo__fut is None or epq__srzfs in ttxc__umlbx:
                uibg__nvi = table.block_to_arr_ind[epq__srzfs]
                cpks__ffde = [new_table_typ.block_offsets[juctz__eocm] for
                    juctz__eocm in uibg__nvi]
                kvyp__pcyk[f'new_idx_{epq__srzfs}'] = np.array(cpks__ffde,
                    np.int64)
                kvyp__pcyk[f'orig_arr_inds_{epq__srzfs}'] = np.array(uibg__nvi,
                    np.int64)
                dha__kudj += f"""  arr_list_{epq__srzfs} = bodo.hiframes.table.get_table_block(table, {epq__srzfs})
"""
                dha__kudj += f'  for i in range(len(arr_list_{epq__srzfs})):\n'
                dha__kudj += (
                    f'    arr_ind_{epq__srzfs} = orig_arr_inds_{epq__srzfs}[i]\n'
                    )
                dha__kudj += (
                    f'    if arr_ind_{epq__srzfs} not in copied_cols_set:\n')
                dha__kudj += f'      continue\n'
                dha__kudj += f"""    bodo.hiframes.table.ensure_column_unboxed(table, arr_list_{epq__srzfs}, i, arr_ind_{epq__srzfs})
"""
                dha__kudj += (
                    f'    out_idx_{akhi__nezxj}_{epq__srzfs} = new_idx_{epq__srzfs}[i]\n'
                    )
                dha__kudj += (
                    f'    arr_val_{epq__srzfs} = arr_list_{epq__srzfs}[i]\n')
                if iymkh__lxvl:
                    dha__kudj += (
                        f'    arr_val_{epq__srzfs} = arr_val_{epq__srzfs}.copy()\n'
                        )
                elif iyfl__zkqfh:
                    dha__kudj += f"""    arr_val_{epq__srzfs} = arr_val_{epq__srzfs}.copy() if copy else arr_val_{akhi__nezxj}
"""
                dha__kudj += f"""    out_arr_list_{akhi__nezxj}[out_idx_{akhi__nezxj}_{epq__srzfs}] = arr_val_{epq__srzfs}
"""
    ttsfx__qfke = set()
    for lzgm__oftx, akhi__nezxj in new_table_typ.type_to_blk.items():
        if lzgm__oftx in rqyy__tyxid:
            kvyp__pcyk[f'typ_{akhi__nezxj}'] = get_castable_arr_dtype(
                lzgm__oftx)
            rgrv__csxkr = rqyy__tyxid[lzgm__oftx]
            for ixgqx__tfwo in rgrv__csxkr:
                epq__srzfs = table.type_to_blk[ixgqx__tfwo]
                if yfrwo__fut is None or epq__srzfs in ttxc__umlbx:
                    if (ixgqx__tfwo not in lsbax__dfi and ixgqx__tfwo not in
                        ttsfx__qfke):
                        uibg__nvi = table.block_to_arr_ind[epq__srzfs]
                        cpks__ffde = [new_table_typ.block_offsets[
                            juctz__eocm] for juctz__eocm in uibg__nvi]
                        kvyp__pcyk[f'new_idx_{epq__srzfs}'] = np.array(
                            cpks__ffde, np.int64)
                        kvyp__pcyk[f'orig_arr_inds_{epq__srzfs}'] = np.array(
                            uibg__nvi, np.int64)
                        dha__kudj += f"""  arr_list_{epq__srzfs} = bodo.hiframes.table.get_table_block(table, {epq__srzfs})
"""
                    ttsfx__qfke.add(ixgqx__tfwo)
                    dha__kudj += (
                        f'  for i in range(len(arr_list_{epq__srzfs})):\n')
                    dha__kudj += (
                        f'    arr_ind_{epq__srzfs} = orig_arr_inds_{epq__srzfs}[i]\n'
                        )
                    dha__kudj += f"""    if arr_ind_{epq__srzfs} not in cast_cols_{epq__srzfs}_{akhi__nezxj}_set:
"""
                    dha__kudj += f'      continue\n'
                    dha__kudj += f"""    bodo.hiframes.table.ensure_column_unboxed(table, arr_list_{epq__srzfs}, i, arr_ind_{epq__srzfs})
"""
                    dha__kudj += f"""    out_idx_{akhi__nezxj}_{epq__srzfs} = new_idx_{epq__srzfs}[i]
"""
                    dha__kudj += f"""    arr_val_{akhi__nezxj} =  bodo.utils.conversion.fix_arr_dtype(arr_list_{epq__srzfs}[i], typ_{akhi__nezxj}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)
"""
                    dha__kudj += f"""    out_arr_list_{akhi__nezxj}[out_idx_{akhi__nezxj}_{epq__srzfs}] = arr_val_{akhi__nezxj}
"""
        dha__kudj += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, out_arr_list_{akhi__nezxj}, {akhi__nezxj})
"""
    dha__kudj += '  return out_table\n'
    nusb__jghg = {}
    exec(dha__kudj, kvyp__pcyk, nusb__jghg)
    return nusb__jghg['impl']


def table_astype_equiv(self, scope, equiv_set, loc, args, kws):
    ocag__vqb = args[0]
    if equiv_set.has_shape(ocag__vqb):
        return ArrayAnalysis.AnalyzeResult(shape=ocag__vqb, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_utils_table_utils_table_astype = (
    table_astype_equiv)
