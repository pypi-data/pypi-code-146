"""
Indexing support for pd.DataFrame type.
"""
import operator
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported
from bodo.utils.transform import gen_const_tup
from bodo.utils.typing import BodoError, get_overload_const_int, get_overload_const_list, get_overload_const_str, is_immutable_array, is_list_like_index_type, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, raise_bodo_error


@infer_global(operator.getitem)
class DataFrameGetItemTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        check_runtime_cols_unsupported(args[0], 'DataFrame getitem (df[])')
        if isinstance(args[0], DataFrameType):
            return self.typecheck_df_getitem(args)
        elif isinstance(args[0], DataFrameLocType):
            return self.typecheck_loc_getitem(args)
        else:
            return

    def typecheck_loc_getitem(self, args):
        I = args[0]
        idx = args[1]
        df = I.df_type
        if isinstance(df.columns[0], tuple):
            raise_bodo_error(
                'DataFrame.loc[] getitem (location-based indexing) with multi-indexed columns not supported yet'
                )
        if is_list_like_index_type(idx) and idx.dtype == types.bool_:
            hyj__wkd = idx
            sfvl__wrjg = df.data
            owto__vjnsb = df.columns
            sck__dfs = self.replace_range_with_numeric_idx_if_needed(df,
                hyj__wkd)
            tywa__swvl = DataFrameType(sfvl__wrjg, sck__dfs, owto__vjnsb,
                is_table_format=df.is_table_format)
            return tywa__swvl(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            smebf__mmr = idx.types[0]
            zaqrx__cwct = idx.types[1]
            if isinstance(smebf__mmr, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(zaqrx__cwct):
                    gex__jdoib = get_overload_const_str(zaqrx__cwct)
                    if gex__jdoib not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, gex__jdoib))
                    cgmv__bqkl = df.columns.index(gex__jdoib)
                    return df.data[cgmv__bqkl].dtype(*args)
                if isinstance(zaqrx__cwct, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(smebf__mmr
                ) and smebf__mmr.dtype == types.bool_ or isinstance(smebf__mmr,
                types.SliceType):
                sck__dfs = self.replace_range_with_numeric_idx_if_needed(df,
                    smebf__mmr)
                if is_overload_constant_str(zaqrx__cwct):
                    zlnq__bvd = get_overload_const_str(zaqrx__cwct)
                    if zlnq__bvd not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {zlnq__bvd}'
                            )
                    cgmv__bqkl = df.columns.index(zlnq__bvd)
                    bsv__gpt = df.data[cgmv__bqkl]
                    nxg__mdvd = bsv__gpt.dtype
                    jfcw__gxc = types.literal(df.columns[cgmv__bqkl])
                    tywa__swvl = bodo.SeriesType(nxg__mdvd, bsv__gpt,
                        sck__dfs, jfcw__gxc)
                    return tywa__swvl(*args)
                if isinstance(zaqrx__cwct, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                elif is_overload_constant_list(zaqrx__cwct):
                    kihj__rnom = get_overload_const_list(zaqrx__cwct)
                    grqm__aff = types.unliteral(zaqrx__cwct)
                    if grqm__aff.dtype == types.bool_:
                        if len(df.columns) != len(kihj__rnom):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {kihj__rnom} has {len(kihj__rnom)} values'
                                )
                        acw__kbtq = []
                        eenky__tup = []
                        for mgsrk__xmu in range(len(kihj__rnom)):
                            if kihj__rnom[mgsrk__xmu]:
                                acw__kbtq.append(df.columns[mgsrk__xmu])
                                eenky__tup.append(df.data[mgsrk__xmu])
                        wvx__gglr = tuple()
                        krb__dhqk = df.is_table_format and len(acw__kbtq
                            ) > 0 and len(acw__kbtq
                            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
                        tywa__swvl = DataFrameType(tuple(eenky__tup),
                            sck__dfs, tuple(acw__kbtq), is_table_format=
                            krb__dhqk)
                        return tywa__swvl(*args)
                    elif grqm__aff.dtype == bodo.string_type:
                        wvx__gglr, eenky__tup = (
                            get_df_getitem_kept_cols_and_data(df, kihj__rnom))
                        krb__dhqk = df.is_table_format and len(kihj__rnom
                            ) > 0 and len(kihj__rnom
                            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
                        tywa__swvl = DataFrameType(eenky__tup, sck__dfs,
                            wvx__gglr, is_table_format=krb__dhqk)
                        return tywa__swvl(*args)
        raise_bodo_error(
            f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet. If you are trying to select a subset of the columns by passing a list of column names, that list must be a compile time constant. See https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )

    def typecheck_df_getitem(self, args):
        df = args[0]
        ind = args[1]
        if is_overload_constant_str(ind) or is_overload_constant_int(ind):
            ind_val = get_overload_const_str(ind) if is_overload_constant_str(
                ind) else get_overload_const_int(ind)
            if isinstance(df.columns[0], tuple):
                acw__kbtq = []
                eenky__tup = []
                for mgsrk__xmu, nwfi__tzl in enumerate(df.columns):
                    if nwfi__tzl[0] != ind_val:
                        continue
                    acw__kbtq.append(nwfi__tzl[1] if len(nwfi__tzl) == 2 else
                        nwfi__tzl[1:])
                    eenky__tup.append(df.data[mgsrk__xmu])
                bsv__gpt = tuple(eenky__tup)
                zfs__evyfx = df.index
                mzenc__ymt = tuple(acw__kbtq)
                tywa__swvl = DataFrameType(bsv__gpt, zfs__evyfx, mzenc__ymt)
                return tywa__swvl(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                cgmv__bqkl = df.columns.index(ind_val)
                bsv__gpt = df.data[cgmv__bqkl]
                nxg__mdvd = bsv__gpt.dtype
                zfs__evyfx = df.index
                jfcw__gxc = types.literal(df.columns[cgmv__bqkl])
                tywa__swvl = bodo.SeriesType(nxg__mdvd, bsv__gpt,
                    zfs__evyfx, jfcw__gxc)
                return tywa__swvl(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            bsv__gpt = df.data
            zfs__evyfx = self.replace_range_with_numeric_idx_if_needed(df, ind)
            mzenc__ymt = df.columns
            tywa__swvl = DataFrameType(bsv__gpt, zfs__evyfx, mzenc__ymt,
                is_table_format=df.is_table_format)
            return tywa__swvl(*args)
        elif is_overload_constant_list(ind):
            gksvi__bkqit = get_overload_const_list(ind)
            mzenc__ymt, bsv__gpt = get_df_getitem_kept_cols_and_data(df,
                gksvi__bkqit)
            zfs__evyfx = df.index
            krb__dhqk = df.is_table_format and len(gksvi__bkqit) > 0 and len(
                gksvi__bkqit) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
            tywa__swvl = DataFrameType(bsv__gpt, zfs__evyfx, mzenc__ymt,
                is_table_format=krb__dhqk)
            return tywa__swvl(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        sck__dfs = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64,
            df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return sck__dfs


DataFrameGetItemTemplate._no_unliteral = True


def get_df_getitem_kept_cols_and_data(df, cols_to_keep_list):
    for mzhr__lyzjt in cols_to_keep_list:
        if mzhr__lyzjt not in df.column_index:
            raise_bodo_error('Column {} not found in dataframe columns {}'.
                format(mzhr__lyzjt, df.columns))
    mzenc__ymt = tuple(cols_to_keep_list)
    bsv__gpt = tuple(df.data[df.column_index[fntce__hlnfz]] for
        fntce__hlnfz in mzenc__ymt)
    return mzenc__ymt, bsv__gpt


@lower_builtin(operator.getitem, DataFrameType, types.Any)
def getitem_df_lower(context, builder, sig, args):
    impl = df_getitem_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def df_getitem_overload(df, ind):
    if not isinstance(df, DataFrameType):
        return
    if is_overload_constant_str(ind) or is_overload_constant_int(ind):
        ind_val = get_overload_const_str(ind) if is_overload_constant_str(ind
            ) else get_overload_const_int(ind)
        if isinstance(df.columns[0], tuple):
            acw__kbtq = []
            eenky__tup = []
            for mgsrk__xmu, nwfi__tzl in enumerate(df.columns):
                if nwfi__tzl[0] != ind_val:
                    continue
                acw__kbtq.append(nwfi__tzl[1] if len(nwfi__tzl) == 2 else
                    nwfi__tzl[1:])
                eenky__tup.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(mgsrk__xmu))
            hhf__vmx = 'def impl(df, ind):\n'
            bxi__vlfa = (
                'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
            return bodo.hiframes.dataframe_impl._gen_init_df(hhf__vmx,
                acw__kbtq, ', '.join(eenky__tup), bxi__vlfa)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        gksvi__bkqit = get_overload_const_list(ind)
        for mzhr__lyzjt in gksvi__bkqit:
            if mzhr__lyzjt not in df.column_index:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(mzhr__lyzjt, df.columns))
        pgrnh__dqgdu = None
        if df.is_table_format and len(gksvi__bkqit) > 0 and len(gksvi__bkqit
            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD:
            nnzqp__ufv = [df.column_index[mzhr__lyzjt] for mzhr__lyzjt in
                gksvi__bkqit]
            pgrnh__dqgdu = {'col_nums_meta': bodo.utils.typing.MetaType(
                tuple(nnzqp__ufv))}
            eenky__tup = (
                f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, True)'
                )
        else:
            eenky__tup = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[mzhr__lyzjt]}).copy()'
                 for mzhr__lyzjt in gksvi__bkqit)
        hhf__vmx = 'def impl(df, ind):\n'
        bxi__vlfa = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(hhf__vmx,
            gksvi__bkqit, eenky__tup, bxi__vlfa, extra_globals=pgrnh__dqgdu)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        hhf__vmx = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            hhf__vmx += '  ind = bodo.utils.conversion.coerce_to_array(ind)\n'
        bxi__vlfa = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        if df.is_table_format:
            eenky__tup = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[ind]')
        else:
            eenky__tup = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[mzhr__lyzjt]})[ind]'
                 for mzhr__lyzjt in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(hhf__vmx, df.
            columns, eenky__tup, bxi__vlfa)
    raise_bodo_error('df[] getitem using {} not supported'.format(ind))


@overload(operator.setitem, no_unliteral=True)
def df_setitem_overload(df, idx, val):
    check_runtime_cols_unsupported(df, 'DataFrame setitem (df[])')
    if not isinstance(df, DataFrameType):
        return
    raise_bodo_error('DataFrame setitem: transform necessary')


class DataFrameILocType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        fntce__hlnfz = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(fntce__hlnfz)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vux__chflw = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, vux__chflw)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        nfdk__bvm, = args
        lbpgf__hvha = signature.return_type
        xbqi__ljmvc = cgutils.create_struct_proxy(lbpgf__hvha)(context, builder
            )
        xbqi__ljmvc.obj = nfdk__bvm
        context.nrt.incref(builder, signature.args[0], nfdk__bvm)
        return xbqi__ljmvc._getvalue()
    return DataFrameILocType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'iloc')
def overload_dataframe_iloc(df):
    check_runtime_cols_unsupported(df, 'DataFrame.iloc')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_iloc(df)


@overload(operator.getitem, no_unliteral=True)
def overload_iloc_getitem(I, idx):
    if not isinstance(I, DataFrameILocType):
        return
    df = I.df_type
    if isinstance(idx, types.Integer):
        return _gen_iloc_getitem_row_impl(df, df.columns, 'idx')
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and not isinstance(
        idx[1], types.SliceType):
        if not (is_overload_constant_list(idx.types[1]) or
            is_overload_constant_int(idx.types[1])):
            raise_bodo_error(
                'idx2 in df.iloc[idx1, idx2] should be a constant integer or constant list of integers. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        tqcys__kldl = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            azw__jmgjw = get_overload_const_int(idx.types[1])
            if azw__jmgjw < 0 or azw__jmgjw >= tqcys__kldl:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            jrn__mqr = [azw__jmgjw]
        else:
            is_out_series = False
            jrn__mqr = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >=
                tqcys__kldl for ind in jrn__mqr):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[jrn__mqr])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                azw__jmgjw = jrn__mqr[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df, azw__jmgjw)
                        [idx[0]])
                return impl
            return _gen_iloc_getitem_row_impl(df, col_names, 'idx[0]')
        if is_list_like_index_type(idx.types[0]) and isinstance(idx.types[0
            ].dtype, (types.Integer, types.Boolean)) or isinstance(idx.
            types[0], types.SliceType):
            return _gen_iloc_getitem_bool_slice_impl(df, col_names, idx.
                types[0], 'idx[0]', is_out_series)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, (types.
        Integer, types.Boolean)) or isinstance(idx, types.SliceType):
        return _gen_iloc_getitem_bool_slice_impl(df, df.columns, idx, 'idx',
            False)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):
        raise_bodo_error(
            'slice2 in df.iloc[slice1,slice2] should be constant. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )
    raise_bodo_error(f'df.iloc[] getitem using {idx} not supported')


def _gen_iloc_getitem_bool_slice_impl(df, col_names, idx_typ, idx,
    is_out_series):
    hhf__vmx = 'def impl(I, idx):\n'
    hhf__vmx += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        hhf__vmx += f'  idx_t = {idx}\n'
    else:
        hhf__vmx += f'  idx_t = bodo.utils.conversion.coerce_to_array({idx})\n'
    bxi__vlfa = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]'
    pgrnh__dqgdu = None
    if df.is_table_format and not is_out_series:
        nnzqp__ufv = [df.column_index[mzhr__lyzjt] for mzhr__lyzjt in col_names
            ]
        pgrnh__dqgdu = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
            nnzqp__ufv))}
        eenky__tup = (
            f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, False)[idx_t]'
            )
    else:
        eenky__tup = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[mzhr__lyzjt]})[idx_t]'
             for mzhr__lyzjt in col_names)
    if is_out_series:
        jttdk__ubtjo = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        hhf__vmx += f"""  return bodo.hiframes.pd_series_ext.init_series({eenky__tup}, {bxi__vlfa}, {jttdk__ubtjo})
"""
        kltxx__ytqa = {}
        exec(hhf__vmx, {'bodo': bodo}, kltxx__ytqa)
        return kltxx__ytqa['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(hhf__vmx, col_names,
        eenky__tup, bxi__vlfa, extra_globals=pgrnh__dqgdu)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    hhf__vmx = 'def impl(I, idx):\n'
    hhf__vmx += '  df = I._obj\n'
    lxq__nnsel = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[mzhr__lyzjt]})[{idx}]'
         for mzhr__lyzjt in col_names)
    hhf__vmx += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    hhf__vmx += f"""  return bodo.hiframes.pd_series_ext.init_series(({lxq__nnsel},), row_idx, None)
"""
    kltxx__ytqa = {}
    exec(hhf__vmx, {'bodo': bodo}, kltxx__ytqa)
    impl = kltxx__ytqa['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def df_iloc_setitem_overload(df, idx, val):
    if not isinstance(df, DataFrameILocType):
        return
    raise_bodo_error(
        f'DataFrame.iloc setitem unsupported for dataframe {df.df_type}, index {idx}, value {val}'
        )


class DataFrameLocType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        fntce__hlnfz = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(fntce__hlnfz)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vux__chflw = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, vux__chflw)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        nfdk__bvm, = args
        xmmw__zwh = signature.return_type
        bvt__jhxap = cgutils.create_struct_proxy(xmmw__zwh)(context, builder)
        bvt__jhxap.obj = nfdk__bvm
        context.nrt.incref(builder, signature.args[0], nfdk__bvm)
        return bvt__jhxap._getvalue()
    return DataFrameLocType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'loc')
def overload_dataframe_loc(df):
    check_runtime_cols_unsupported(df, 'DataFrame.loc')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_loc(df)


@lower_builtin(operator.getitem, DataFrameLocType, types.Any)
def loc_getitem_lower(context, builder, sig, args):
    impl = overload_loc_getitem(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def overload_loc_getitem(I, idx):
    if not isinstance(I, DataFrameLocType):
        return
    df = I.df_type
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        hhf__vmx = 'def impl(I, idx):\n'
        hhf__vmx += '  df = I._obj\n'
        hhf__vmx += '  idx_t = bodo.utils.conversion.coerce_to_array(idx)\n'
        bxi__vlfa = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        if df.is_table_format:
            eenky__tup = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[idx_t]'
                )
        else:
            eenky__tup = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[mzhr__lyzjt]})[idx_t]'
                 for mzhr__lyzjt in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(hhf__vmx, df.
            columns, eenky__tup, bxi__vlfa)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        ofqwy__qwxsv = idx.types[1]
        if is_overload_constant_str(ofqwy__qwxsv):
            wfvag__iipr = get_overload_const_str(ofqwy__qwxsv)
            azw__jmgjw = df.columns.index(wfvag__iipr)

            def impl_col_name(I, idx):
                df = I._obj
                bxi__vlfa = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
                    df)
                jtov__foe = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
                    df, azw__jmgjw)
                return bodo.hiframes.pd_series_ext.init_series(jtov__foe,
                    bxi__vlfa, wfvag__iipr).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(ofqwy__qwxsv):
            col_idx_list = get_overload_const_list(ofqwy__qwxsv)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(mzhr__lyzjt in df.column_index for
                mzhr__lyzjt in col_idx_list):
                raise_bodo_error(
                    f'DataFrame.loc[]: invalid column list {col_idx_list}; not all in dataframe columns {df.columns}'
                    )
            return gen_df_loc_col_select_impl(df, col_idx_list)
    raise_bodo_error(
        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
        )


def gen_df_loc_col_select_impl(df, col_idx_list):
    col_names = []
    jrn__mqr = []
    if len(col_idx_list) > 0 and isinstance(col_idx_list[0], (bool, np.bool_)):
        for mgsrk__xmu, mjo__dlzd in enumerate(col_idx_list):
            if mjo__dlzd:
                jrn__mqr.append(mgsrk__xmu)
                col_names.append(df.columns[mgsrk__xmu])
    else:
        col_names = col_idx_list
        jrn__mqr = [df.column_index[mzhr__lyzjt] for mzhr__lyzjt in
            col_idx_list]
    pgrnh__dqgdu = None
    if df.is_table_format and len(col_idx_list) > 0 and len(col_idx_list
        ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD:
        pgrnh__dqgdu = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
            jrn__mqr))}
        eenky__tup = (
            f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, False)[idx[0]]'
            )
    else:
        eenky__tup = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {ind})[idx[0]]'
             for ind in jrn__mqr)
    bxi__vlfa = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]')
    hhf__vmx = 'def impl(I, idx):\n'
    hhf__vmx += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(hhf__vmx, col_names,
        eenky__tup, bxi__vlfa, extra_globals=pgrnh__dqgdu)


@overload(operator.setitem, no_unliteral=True)
def df_loc_setitem_overload(df, idx, val):
    if not isinstance(df, DataFrameLocType):
        return
    raise_bodo_error(
        f'DataFrame.loc setitem unsupported for dataframe {df.df_type}, index {idx}, value {val}'
        )


class DataFrameIatType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        fntce__hlnfz = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(fntce__hlnfz)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vux__chflw = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, vux__chflw)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        nfdk__bvm, = args
        dcrpv__hhdr = signature.return_type
        nfe__ogzff = cgutils.create_struct_proxy(dcrpv__hhdr)(context, builder)
        nfe__ogzff.obj = nfdk__bvm
        context.nrt.incref(builder, signature.args[0], nfdk__bvm)
        return nfe__ogzff._getvalue()
    return DataFrameIatType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'iat')
def overload_dataframe_iat(df):
    check_runtime_cols_unsupported(df, 'DataFrame.iat')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_iat(df)


@overload(operator.getitem, no_unliteral=True)
def overload_iat_getitem(I, idx):
    if not isinstance(I, DataFrameIatType):
        return
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        if not isinstance(idx.types[0], types.Integer):
            raise BodoError(
                'DataFrame.iat: iAt based indexing can only have integer indexers'
                )
        if not is_overload_constant_int(idx.types[1]):
            raise_bodo_error(
                'DataFrame.iat getitem: column index must be a constant integer. For more informaton, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        azw__jmgjw = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            jtov__foe = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                azw__jmgjw)
            return bodo.utils.conversion.box_if_dt64(jtov__foe[idx[0]])
        return impl_col_ind
    raise BodoError('df.iat[] getitem using {} not supported'.format(idx))


@overload(operator.setitem, no_unliteral=True)
def overload_iat_setitem(I, idx, val):
    if not isinstance(I, DataFrameIatType):
        return
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        if not isinstance(idx.types[0], types.Integer):
            raise BodoError(
                'DataFrame.iat: iAt based indexing can only have integer indexers'
                )
        if not is_overload_constant_int(idx.types[1]):
            raise_bodo_error(
                'DataFrame.iat setitem: column index must be a constant integer. For more informaton, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        azw__jmgjw = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[azw__jmgjw]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            jtov__foe = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                azw__jmgjw)
            jtov__foe[idx[0]
                ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(val)
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    nfe__ogzff = cgutils.create_struct_proxy(fromty)(context, builder, val)
    xxde__uokpd = context.cast(builder, nfe__ogzff.obj, fromty.df_type,
        toty.df_type)
    fma__dwsz = cgutils.create_struct_proxy(toty)(context, builder)
    fma__dwsz.obj = xxde__uokpd
    return fma__dwsz._getvalue()
