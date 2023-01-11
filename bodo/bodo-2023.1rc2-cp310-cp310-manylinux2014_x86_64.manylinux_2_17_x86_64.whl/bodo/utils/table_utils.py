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
    vsoiz__nqyu = not is_overload_none(func_name)
    if vsoiz__nqyu:
        func_name = get_overload_const_str(func_name)
        qdk__tkqh = get_overload_const_bool(is_method)
    wlk__pee = out_arr_typ.instance_type if isinstance(out_arr_typ, types.
        TypeRef) else out_arr_typ
    yrmm__kza = wlk__pee == types.none
    vxbop__har = len(table.arr_types)
    if yrmm__kza:
        zrifa__fop = table
    else:
        xyuoy__kgdg = tuple([wlk__pee] * vxbop__har)
        zrifa__fop = TableType(xyuoy__kgdg)
    obye__perdj = {'bodo': bodo, 'lst_dtype': wlk__pee, 'table_typ': zrifa__fop
        }
    yssg__cwxxv = (
        'def impl(table, func_name, out_arr_typ, is_method, used_cols=None):\n'
        )
    if yrmm__kza:
        yssg__cwxxv += (
            f'  out_table = bodo.hiframes.table.init_table(table, False)\n')
        yssg__cwxxv += f'  l = len(table)\n'
    else:
        yssg__cwxxv += f"""  out_list = bodo.hiframes.table.alloc_empty_list_type({vxbop__har}, lst_dtype)
"""
    if not is_overload_none(used_cols):
        gum__msrud = used_cols.instance_type
        lyvz__fuwef = np.array(gum__msrud.meta, dtype=np.int64)
        obye__perdj['used_cols_glbl'] = lyvz__fuwef
        hekwb__cru = set([table.block_nums[couh__pudm] for couh__pudm in
            lyvz__fuwef])
        yssg__cwxxv += f'  used_cols_set = set(used_cols_glbl)\n'
    else:
        yssg__cwxxv += f'  used_cols_set = None\n'
        lyvz__fuwef = None
    yssg__cwxxv += (
        f'  bodo.hiframes.table.ensure_table_unboxed(table, used_cols_set)\n')
    for zdws__jcvjf in table.type_to_blk.values():
        yssg__cwxxv += f"""  blk_{zdws__jcvjf} = bodo.hiframes.table.get_table_block(table, {zdws__jcvjf})
"""
        if yrmm__kza:
            yssg__cwxxv += f"""  out_list_{zdws__jcvjf} = bodo.hiframes.table.alloc_list_like(blk_{zdws__jcvjf}, len(blk_{zdws__jcvjf}), False)
"""
            yjdo__nzbw = f'out_list_{zdws__jcvjf}'
        else:
            yjdo__nzbw = 'out_list'
        if lyvz__fuwef is None or zdws__jcvjf in hekwb__cru:
            yssg__cwxxv += f'  for i in range(len(blk_{zdws__jcvjf})):\n'
            obye__perdj[f'col_indices_{zdws__jcvjf}'] = np.array(table.
                block_to_arr_ind[zdws__jcvjf], dtype=np.int64)
            yssg__cwxxv += f'    col_loc = col_indices_{zdws__jcvjf}[i]\n'
            if lyvz__fuwef is not None:
                yssg__cwxxv += f'    if col_loc not in used_cols_set:\n'
                yssg__cwxxv += f'        continue\n'
            if yrmm__kza:
                ctgml__afnyx = 'i'
            else:
                ctgml__afnyx = 'col_loc'
            if not vsoiz__nqyu:
                yssg__cwxxv += (
                    f'    {yjdo__nzbw}[{ctgml__afnyx}] = blk_{zdws__jcvjf}[i]\n'
                    )
            elif qdk__tkqh:
                yssg__cwxxv += f"""    {yjdo__nzbw}[{ctgml__afnyx}] = blk_{zdws__jcvjf}[i].{func_name}()
"""
            else:
                yssg__cwxxv += f"""    {yjdo__nzbw}[{ctgml__afnyx}] = {func_name}(blk_{zdws__jcvjf}[i])
"""
        if yrmm__kza:
            yssg__cwxxv += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, {yjdo__nzbw}, {zdws__jcvjf})
"""
    if yrmm__kza:
        yssg__cwxxv += (
            f'  out_table = bodo.hiframes.table.set_table_len(out_table, l)\n')
        yssg__cwxxv += '  return out_table\n'
    else:
        yssg__cwxxv += """  return bodo.hiframes.table.init_table_from_lists((out_list,), table_typ)
"""
    qeq__zwh = {}
    exec(yssg__cwxxv, obye__perdj, qeq__zwh)
    return qeq__zwh['impl']


def generate_mappable_table_func_equiv(self, scope, equiv_set, loc, args, kws):
    mrlp__zrc = args[0]
    if equiv_set.has_shape(mrlp__zrc):
        return ArrayAnalysis.AnalyzeResult(shape=mrlp__zrc, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_utils_table_utils_generate_mappable_table_func
    ) = generate_mappable_table_func_equiv


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_table_nbytes(table, out_arr, start_offset, parallel=False):
    obye__perdj = {'bodo': bodo, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value)}
    yssg__cwxxv = 'def impl(table, out_arr, start_offset, parallel=False):\n'
    yssg__cwxxv += '  bodo.hiframes.table.ensure_table_unboxed(table, None)\n'
    for zdws__jcvjf in table.type_to_blk.values():
        yssg__cwxxv += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {zdws__jcvjf})\n'
            )
        obye__perdj[f'col_indices_{zdws__jcvjf}'] = np.array(table.
            block_to_arr_ind[zdws__jcvjf], dtype=np.int64)
        yssg__cwxxv += '  for i in range(len(blk)):\n'
        yssg__cwxxv += f'    col_loc = col_indices_{zdws__jcvjf}[i]\n'
        yssg__cwxxv += '    out_arr[col_loc + start_offset] = blk[i].nbytes\n'
    yssg__cwxxv += '  if parallel:\n'
    yssg__cwxxv += '    for i in range(start_offset, len(out_arr)):\n'
    yssg__cwxxv += (
        '      out_arr[i] = bodo.libs.distributed_api.dist_reduce(out_arr[i], sum_op)\n'
        )
    qeq__zwh = {}
    exec(yssg__cwxxv, obye__perdj, qeq__zwh)
    return qeq__zwh['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_concat(table, col_nums_meta, arr_type):
    arr_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type
    psqc__etlav = table.type_to_blk[arr_type]
    obye__perdj: Dict[str, Any] = {'bodo': bodo}
    obye__perdj['col_indices'] = np.array(table.block_to_arr_ind[
        psqc__etlav], dtype=np.int64)
    jnc__myrdl = col_nums_meta.instance_type
    obye__perdj['col_nums'] = np.array(jnc__myrdl.meta, np.int64)
    yssg__cwxxv = 'def impl(table, col_nums_meta, arr_type):\n'
    yssg__cwxxv += (
        f'  blk = bodo.hiframes.table.get_table_block(table, {psqc__etlav})\n')
    yssg__cwxxv += (
        '  col_num_to_ind_in_blk = {c : i for i, c in enumerate(col_indices)}\n'
        )
    yssg__cwxxv += '  n = len(table)\n'
    otib__dli = arr_type == bodo.string_array_type
    if otib__dli:
        yssg__cwxxv += '  total_chars = 0\n'
        yssg__cwxxv += '  for c in col_nums:\n'
        yssg__cwxxv += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
        yssg__cwxxv += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
        yssg__cwxxv += (
            '    total_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n')
        yssg__cwxxv += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n * len(col_nums), total_chars)
"""
    else:
        yssg__cwxxv += """  out_arr = bodo.utils.utils.alloc_type(n * len(col_nums), arr_type, (-1,))
"""
    yssg__cwxxv += '  for i in range(len(col_nums)):\n'
    yssg__cwxxv += '    c = col_nums[i]\n'
    if not otib__dli:
        yssg__cwxxv += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
    yssg__cwxxv += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
    yssg__cwxxv += '    off = i * n\n'
    yssg__cwxxv += '    for j in range(len(arr)):\n'
    yssg__cwxxv += '      if bodo.libs.array_kernels.isna(arr, j):\n'
    yssg__cwxxv += '        bodo.libs.array_kernels.setna(out_arr, off+j)\n'
    yssg__cwxxv += '      else:\n'
    yssg__cwxxv += '        out_arr[off+j] = arr[j]\n'
    yssg__cwxxv += '  return out_arr\n'
    nxdl__pyjkj = {}
    exec(yssg__cwxxv, obye__perdj, nxdl__pyjkj)
    hhju__qql = nxdl__pyjkj['impl']
    return hhju__qql


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_astype(table, new_table_typ, copy, _bodo_nan_to_str, used_cols=None):
    new_table_typ = new_table_typ.instance_type
    oog__tno = not is_overload_false(copy)
    dgc__yhmuz = is_overload_true(copy)
    obye__perdj: Dict[str, Any] = {'bodo': bodo}
    jil__pyn = table.arr_types
    ttkop__ytn = new_table_typ.arr_types
    zlq__lhk: Set[int] = set()
    nshmf__kkcp: Dict[types.Type, Set[types.Type]] = defaultdict(set)
    uket__zzle: Set[types.Type] = set()
    for couh__pudm, rlt__qneo in enumerate(jil__pyn):
        xoy__ntjif = ttkop__ytn[couh__pudm]
        if rlt__qneo == xoy__ntjif:
            uket__zzle.add(rlt__qneo)
        else:
            zlq__lhk.add(couh__pudm)
            nshmf__kkcp[xoy__ntjif].add(rlt__qneo)
    yssg__cwxxv = (
        'def impl(table, new_table_typ, copy, _bodo_nan_to_str, used_cols=None):\n'
        )
    yssg__cwxxv += (
        f'  out_table = bodo.hiframes.table.init_table(new_table_typ, False)\n'
        )
    yssg__cwxxv += (
        f'  out_table = bodo.hiframes.table.set_table_len(out_table, len(table))\n'
        )
    zglk__yjxe = set(range(len(jil__pyn)))
    ftyf__vwx = zglk__yjxe - zlq__lhk
    if not is_overload_none(used_cols):
        gum__msrud = used_cols.instance_type
        glh__gfy = set(gum__msrud.meta)
        zlq__lhk = zlq__lhk & glh__gfy
        ftyf__vwx = ftyf__vwx & glh__gfy
        hekwb__cru = set([table.block_nums[couh__pudm] for couh__pudm in
            glh__gfy])
    else:
        glh__gfy = None
    jlpg__git = dict()
    for sjvsf__ubwo in zlq__lhk:
        dqyd__ojvgh = table.block_nums[sjvsf__ubwo]
        ipu__zncu = new_table_typ.block_nums[sjvsf__ubwo]
        if f'cast_cols_{dqyd__ojvgh}_{ipu__zncu}' in jlpg__git:
            jlpg__git[f'cast_cols_{dqyd__ojvgh}_{ipu__zncu}'].append(
                sjvsf__ubwo)
        else:
            jlpg__git[f'cast_cols_{dqyd__ojvgh}_{ipu__zncu}'] = [sjvsf__ubwo]
    for aydm__wnq in table.blk_to_type:
        for ipu__zncu in new_table_typ.blk_to_type:
            hyci__nrden = jlpg__git.get(f'cast_cols_{aydm__wnq}_{ipu__zncu}',
                [])
            obye__perdj[f'cast_cols_{aydm__wnq}_{ipu__zncu}'] = np.array(list
                (hyci__nrden), dtype=np.int64)
            yssg__cwxxv += f"""  cast_cols_{aydm__wnq}_{ipu__zncu}_set = set(cast_cols_{aydm__wnq}_{ipu__zncu})
"""
    obye__perdj['copied_cols'] = np.array(list(ftyf__vwx), dtype=np.int64)
    yssg__cwxxv += f'  copied_cols_set = set(copied_cols)\n'
    for hdwm__imo, funn__kjvm in new_table_typ.type_to_blk.items():
        obye__perdj[f'typ_list_{funn__kjvm}'] = types.List(hdwm__imo)
        yssg__cwxxv += f"""  out_arr_list_{funn__kjvm} = bodo.hiframes.table.alloc_list_like(typ_list_{funn__kjvm}, {len(new_table_typ.block_to_arr_ind[funn__kjvm])}, False)
"""
        if hdwm__imo in uket__zzle:
            otkmc__utwj = table.type_to_blk[hdwm__imo]
            if glh__gfy is None or otkmc__utwj in hekwb__cru:
                twueb__irmtz = table.block_to_arr_ind[otkmc__utwj]
                foo__ycf = [new_table_typ.block_offsets[uaee__vxwgq] for
                    uaee__vxwgq in twueb__irmtz]
                obye__perdj[f'new_idx_{otkmc__utwj}'] = np.array(foo__ycf,
                    np.int64)
                obye__perdj[f'orig_arr_inds_{otkmc__utwj}'] = np.array(
                    twueb__irmtz, np.int64)
                yssg__cwxxv += f"""  arr_list_{otkmc__utwj} = bodo.hiframes.table.get_table_block(table, {otkmc__utwj})
"""
                yssg__cwxxv += (
                    f'  for i in range(len(arr_list_{otkmc__utwj})):\n')
                yssg__cwxxv += (
                    f'    arr_ind_{otkmc__utwj} = orig_arr_inds_{otkmc__utwj}[i]\n'
                    )
                yssg__cwxxv += (
                    f'    if arr_ind_{otkmc__utwj} not in copied_cols_set:\n')
                yssg__cwxxv += f'      continue\n'
                yssg__cwxxv += f"""    bodo.hiframes.table.ensure_column_unboxed(table, arr_list_{otkmc__utwj}, i, arr_ind_{otkmc__utwj})
"""
                yssg__cwxxv += f"""    out_idx_{funn__kjvm}_{otkmc__utwj} = new_idx_{otkmc__utwj}[i]
"""
                yssg__cwxxv += (
                    f'    arr_val_{otkmc__utwj} = arr_list_{otkmc__utwj}[i]\n')
                if dgc__yhmuz:
                    yssg__cwxxv += (
                        f'    arr_val_{otkmc__utwj} = arr_val_{otkmc__utwj}.copy()\n'
                        )
                elif oog__tno:
                    yssg__cwxxv += f"""    arr_val_{otkmc__utwj} = arr_val_{otkmc__utwj}.copy() if copy else arr_val_{funn__kjvm}
"""
                yssg__cwxxv += f"""    out_arr_list_{funn__kjvm}[out_idx_{funn__kjvm}_{otkmc__utwj}] = arr_val_{otkmc__utwj}
"""
    bglwi__xfbwv = set()
    for hdwm__imo, funn__kjvm in new_table_typ.type_to_blk.items():
        if hdwm__imo in nshmf__kkcp:
            obye__perdj[f'typ_{funn__kjvm}'] = get_castable_arr_dtype(hdwm__imo
                )
            gdcc__vqld = nshmf__kkcp[hdwm__imo]
            for izll__nntgt in gdcc__vqld:
                otkmc__utwj = table.type_to_blk[izll__nntgt]
                if glh__gfy is None or otkmc__utwj in hekwb__cru:
                    if (izll__nntgt not in uket__zzle and izll__nntgt not in
                        bglwi__xfbwv):
                        twueb__irmtz = table.block_to_arr_ind[otkmc__utwj]
                        foo__ycf = [new_table_typ.block_offsets[uaee__vxwgq
                            ] for uaee__vxwgq in twueb__irmtz]
                        obye__perdj[f'new_idx_{otkmc__utwj}'] = np.array(
                            foo__ycf, np.int64)
                        obye__perdj[f'orig_arr_inds_{otkmc__utwj}'] = np.array(
                            twueb__irmtz, np.int64)
                        yssg__cwxxv += f"""  arr_list_{otkmc__utwj} = bodo.hiframes.table.get_table_block(table, {otkmc__utwj})
"""
                    bglwi__xfbwv.add(izll__nntgt)
                    yssg__cwxxv += (
                        f'  for i in range(len(arr_list_{otkmc__utwj})):\n')
                    yssg__cwxxv += (
                        f'    arr_ind_{otkmc__utwj} = orig_arr_inds_{otkmc__utwj}[i]\n'
                        )
                    yssg__cwxxv += f"""    if arr_ind_{otkmc__utwj} not in cast_cols_{otkmc__utwj}_{funn__kjvm}_set:
"""
                    yssg__cwxxv += f'      continue\n'
                    yssg__cwxxv += f"""    bodo.hiframes.table.ensure_column_unboxed(table, arr_list_{otkmc__utwj}, i, arr_ind_{otkmc__utwj})
"""
                    yssg__cwxxv += f"""    out_idx_{funn__kjvm}_{otkmc__utwj} = new_idx_{otkmc__utwj}[i]
"""
                    yssg__cwxxv += f"""    arr_val_{funn__kjvm} =  bodo.utils.conversion.fix_arr_dtype(arr_list_{otkmc__utwj}[i], typ_{funn__kjvm}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)
"""
                    yssg__cwxxv += f"""    out_arr_list_{funn__kjvm}[out_idx_{funn__kjvm}_{otkmc__utwj}] = arr_val_{funn__kjvm}
"""
        yssg__cwxxv += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, out_arr_list_{funn__kjvm}, {funn__kjvm})
"""
    yssg__cwxxv += '  return out_table\n'
    qeq__zwh = {}
    exec(yssg__cwxxv, obye__perdj, qeq__zwh)
    return qeq__zwh['impl']


def table_astype_equiv(self, scope, equiv_set, loc, args, kws):
    mrlp__zrc = args[0]
    if equiv_set.has_shape(mrlp__zrc):
        return ArrayAnalysis.AnalyzeResult(shape=mrlp__zrc, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_utils_table_utils_table_astype = (
    table_astype_equiv)
