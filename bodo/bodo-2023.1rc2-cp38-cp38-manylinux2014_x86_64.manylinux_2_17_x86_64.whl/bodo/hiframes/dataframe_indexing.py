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
            iaqir__tcbn = idx
            mch__zlcr = df.data
            tbzzv__xeu = df.columns
            lvqov__htoz = self.replace_range_with_numeric_idx_if_needed(df,
                iaqir__tcbn)
            ebz__ngxk = DataFrameType(mch__zlcr, lvqov__htoz, tbzzv__xeu,
                is_table_format=df.is_table_format)
            return ebz__ngxk(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            ghdqy__qgv = idx.types[0]
            vzpl__wkkcs = idx.types[1]
            if isinstance(ghdqy__qgv, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(vzpl__wkkcs):
                    ivilk__mratr = get_overload_const_str(vzpl__wkkcs)
                    if ivilk__mratr not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, ivilk__mratr))
                    cvxi__uux = df.columns.index(ivilk__mratr)
                    return df.data[cvxi__uux].dtype(*args)
                if isinstance(vzpl__wkkcs, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(ghdqy__qgv
                ) and ghdqy__qgv.dtype == types.bool_ or isinstance(ghdqy__qgv,
                types.SliceType):
                lvqov__htoz = self.replace_range_with_numeric_idx_if_needed(df,
                    ghdqy__qgv)
                if is_overload_constant_str(vzpl__wkkcs):
                    jbqa__cbif = get_overload_const_str(vzpl__wkkcs)
                    if jbqa__cbif not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {jbqa__cbif}'
                            )
                    cvxi__uux = df.columns.index(jbqa__cbif)
                    nbzc__wvixt = df.data[cvxi__uux]
                    bml__wegi = nbzc__wvixt.dtype
                    xptz__aqjf = types.literal(df.columns[cvxi__uux])
                    ebz__ngxk = bodo.SeriesType(bml__wegi, nbzc__wvixt,
                        lvqov__htoz, xptz__aqjf)
                    return ebz__ngxk(*args)
                if isinstance(vzpl__wkkcs, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                elif is_overload_constant_list(vzpl__wkkcs):
                    eynxr__kyiw = get_overload_const_list(vzpl__wkkcs)
                    hylw__qzxih = types.unliteral(vzpl__wkkcs)
                    if hylw__qzxih.dtype == types.bool_:
                        if len(df.columns) != len(eynxr__kyiw):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {eynxr__kyiw} has {len(eynxr__kyiw)} values'
                                )
                        nhtez__pivu = []
                        liqxb__gpy = []
                        for zvtpr__lqztv in range(len(eynxr__kyiw)):
                            if eynxr__kyiw[zvtpr__lqztv]:
                                nhtez__pivu.append(df.columns[zvtpr__lqztv])
                                liqxb__gpy.append(df.data[zvtpr__lqztv])
                        urf__yaoin = tuple()
                        tvzc__osu = df.is_table_format and len(nhtez__pivu
                            ) > 0 and len(nhtez__pivu
                            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
                        ebz__ngxk = DataFrameType(tuple(liqxb__gpy),
                            lvqov__htoz, tuple(nhtez__pivu),
                            is_table_format=tvzc__osu)
                        return ebz__ngxk(*args)
                    elif hylw__qzxih.dtype == bodo.string_type:
                        urf__yaoin, liqxb__gpy = (
                            get_df_getitem_kept_cols_and_data(df, eynxr__kyiw))
                        tvzc__osu = df.is_table_format and len(eynxr__kyiw
                            ) > 0 and len(eynxr__kyiw
                            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
                        ebz__ngxk = DataFrameType(liqxb__gpy, lvqov__htoz,
                            urf__yaoin, is_table_format=tvzc__osu)
                        return ebz__ngxk(*args)
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
                nhtez__pivu = []
                liqxb__gpy = []
                for zvtpr__lqztv, pwrvc__acwct in enumerate(df.columns):
                    if pwrvc__acwct[0] != ind_val:
                        continue
                    nhtez__pivu.append(pwrvc__acwct[1] if len(pwrvc__acwct) ==
                        2 else pwrvc__acwct[1:])
                    liqxb__gpy.append(df.data[zvtpr__lqztv])
                nbzc__wvixt = tuple(liqxb__gpy)
                rrzb__mncu = df.index
                yppez__otwrf = tuple(nhtez__pivu)
                ebz__ngxk = DataFrameType(nbzc__wvixt, rrzb__mncu, yppez__otwrf
                    )
                return ebz__ngxk(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                cvxi__uux = df.columns.index(ind_val)
                nbzc__wvixt = df.data[cvxi__uux]
                bml__wegi = nbzc__wvixt.dtype
                rrzb__mncu = df.index
                xptz__aqjf = types.literal(df.columns[cvxi__uux])
                ebz__ngxk = bodo.SeriesType(bml__wegi, nbzc__wvixt,
                    rrzb__mncu, xptz__aqjf)
                return ebz__ngxk(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            nbzc__wvixt = df.data
            rrzb__mncu = self.replace_range_with_numeric_idx_if_needed(df, ind)
            yppez__otwrf = df.columns
            ebz__ngxk = DataFrameType(nbzc__wvixt, rrzb__mncu, yppez__otwrf,
                is_table_format=df.is_table_format)
            return ebz__ngxk(*args)
        elif is_overload_constant_list(ind):
            cnk__phms = get_overload_const_list(ind)
            yppez__otwrf, nbzc__wvixt = get_df_getitem_kept_cols_and_data(df,
                cnk__phms)
            rrzb__mncu = df.index
            tvzc__osu = df.is_table_format and len(cnk__phms) > 0 and len(
                cnk__phms) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
            ebz__ngxk = DataFrameType(nbzc__wvixt, rrzb__mncu, yppez__otwrf,
                is_table_format=tvzc__osu)
            return ebz__ngxk(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        lvqov__htoz = bodo.hiframes.pd_index_ext.NumericIndexType(types.
            int64, df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return lvqov__htoz


DataFrameGetItemTemplate._no_unliteral = True


def get_df_getitem_kept_cols_and_data(df, cols_to_keep_list):
    for eipg__ypavt in cols_to_keep_list:
        if eipg__ypavt not in df.column_index:
            raise_bodo_error('Column {} not found in dataframe columns {}'.
                format(eipg__ypavt, df.columns))
    yppez__otwrf = tuple(cols_to_keep_list)
    nbzc__wvixt = tuple(df.data[df.column_index[uasbe__nht]] for uasbe__nht in
        yppez__otwrf)
    return yppez__otwrf, nbzc__wvixt


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
            nhtez__pivu = []
            liqxb__gpy = []
            for zvtpr__lqztv, pwrvc__acwct in enumerate(df.columns):
                if pwrvc__acwct[0] != ind_val:
                    continue
                nhtez__pivu.append(pwrvc__acwct[1] if len(pwrvc__acwct) == 
                    2 else pwrvc__acwct[1:])
                liqxb__gpy.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(zvtpr__lqztv))
            rvzny__zjmg = 'def impl(df, ind):\n'
            gyu__hxy = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
            return bodo.hiframes.dataframe_impl._gen_init_df(rvzny__zjmg,
                nhtez__pivu, ', '.join(liqxb__gpy), gyu__hxy)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        cnk__phms = get_overload_const_list(ind)
        for eipg__ypavt in cnk__phms:
            if eipg__ypavt not in df.column_index:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(eipg__ypavt, df.columns))
        egrmn__viycb = None
        if df.is_table_format and len(cnk__phms) > 0 and len(cnk__phms
            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD:
            aaik__sxlh = [df.column_index[eipg__ypavt] for eipg__ypavt in
                cnk__phms]
            egrmn__viycb = {'col_nums_meta': bodo.utils.typing.MetaType(
                tuple(aaik__sxlh))}
            liqxb__gpy = (
                f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, True)'
                )
        else:
            liqxb__gpy = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[eipg__ypavt]}).copy()'
                 for eipg__ypavt in cnk__phms)
        rvzny__zjmg = 'def impl(df, ind):\n'
        gyu__hxy = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(rvzny__zjmg,
            cnk__phms, liqxb__gpy, gyu__hxy, extra_globals=egrmn__viycb)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        rvzny__zjmg = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            rvzny__zjmg += (
                '  ind = bodo.utils.conversion.coerce_to_array(ind)\n')
        gyu__hxy = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        if df.is_table_format:
            liqxb__gpy = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[ind]')
        else:
            liqxb__gpy = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[eipg__ypavt]})[ind]'
                 for eipg__ypavt in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(rvzny__zjmg, df.
            columns, liqxb__gpy, gyu__hxy)
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
        uasbe__nht = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(uasbe__nht)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        egiv__zmwyl = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, egiv__zmwyl)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        lrxfv__onqe, = args
        czn__arsxu = signature.return_type
        rrg__rnahg = cgutils.create_struct_proxy(czn__arsxu)(context, builder)
        rrg__rnahg.obj = lrxfv__onqe
        context.nrt.incref(builder, signature.args[0], lrxfv__onqe)
        return rrg__rnahg._getvalue()
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
        viz__kmojj = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            nmkhs__uiql = get_overload_const_int(idx.types[1])
            if nmkhs__uiql < 0 or nmkhs__uiql >= viz__kmojj:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            agojf__tasw = [nmkhs__uiql]
        else:
            is_out_series = False
            agojf__tasw = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >= viz__kmojj for
                ind in agojf__tasw):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[agojf__tasw])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                nmkhs__uiql = agojf__tasw[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df, nmkhs__uiql
                        )[idx[0]])
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
    rvzny__zjmg = 'def impl(I, idx):\n'
    rvzny__zjmg += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        rvzny__zjmg += f'  idx_t = {idx}\n'
    else:
        rvzny__zjmg += (
            f'  idx_t = bodo.utils.conversion.coerce_to_array({idx})\n')
    gyu__hxy = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]'
    egrmn__viycb = None
    if df.is_table_format and not is_out_series:
        aaik__sxlh = [df.column_index[eipg__ypavt] for eipg__ypavt in col_names
            ]
        egrmn__viycb = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
            aaik__sxlh))}
        liqxb__gpy = (
            f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, False)[idx_t]'
            )
    else:
        liqxb__gpy = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[eipg__ypavt]})[idx_t]'
             for eipg__ypavt in col_names)
    if is_out_series:
        wqasq__cyhtb = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        rvzny__zjmg += f"""  return bodo.hiframes.pd_series_ext.init_series({liqxb__gpy}, {gyu__hxy}, {wqasq__cyhtb})
"""
        rmbr__kosz = {}
        exec(rvzny__zjmg, {'bodo': bodo}, rmbr__kosz)
        return rmbr__kosz['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(rvzny__zjmg, col_names,
        liqxb__gpy, gyu__hxy, extra_globals=egrmn__viycb)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    rvzny__zjmg = 'def impl(I, idx):\n'
    rvzny__zjmg += '  df = I._obj\n'
    ewm__imtci = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[eipg__ypavt]})[{idx}]'
         for eipg__ypavt in col_names)
    rvzny__zjmg += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    rvzny__zjmg += f"""  return bodo.hiframes.pd_series_ext.init_series(({ewm__imtci},), row_idx, None)
"""
    rmbr__kosz = {}
    exec(rvzny__zjmg, {'bodo': bodo}, rmbr__kosz)
    impl = rmbr__kosz['impl']
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
        uasbe__nht = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(uasbe__nht)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        egiv__zmwyl = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, egiv__zmwyl)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        lrxfv__onqe, = args
        zxt__qnk = signature.return_type
        fjal__hgcj = cgutils.create_struct_proxy(zxt__qnk)(context, builder)
        fjal__hgcj.obj = lrxfv__onqe
        context.nrt.incref(builder, signature.args[0], lrxfv__onqe)
        return fjal__hgcj._getvalue()
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
        rvzny__zjmg = 'def impl(I, idx):\n'
        rvzny__zjmg += '  df = I._obj\n'
        rvzny__zjmg += '  idx_t = bodo.utils.conversion.coerce_to_array(idx)\n'
        gyu__hxy = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        if df.is_table_format:
            liqxb__gpy = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[idx_t]'
                )
        else:
            liqxb__gpy = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[eipg__ypavt]})[idx_t]'
                 for eipg__ypavt in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(rvzny__zjmg, df.
            columns, liqxb__gpy, gyu__hxy)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        zle__fur = idx.types[1]
        if is_overload_constant_str(zle__fur):
            liw__isyry = get_overload_const_str(zle__fur)
            nmkhs__uiql = df.columns.index(liw__isyry)

            def impl_col_name(I, idx):
                df = I._obj
                gyu__hxy = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
                    df)
                rdk__rpu = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df
                    , nmkhs__uiql)
                return bodo.hiframes.pd_series_ext.init_series(rdk__rpu,
                    gyu__hxy, liw__isyry).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(zle__fur):
            col_idx_list = get_overload_const_list(zle__fur)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(eipg__ypavt in df.column_index for
                eipg__ypavt in col_idx_list):
                raise_bodo_error(
                    f'DataFrame.loc[]: invalid column list {col_idx_list}; not all in dataframe columns {df.columns}'
                    )
            return gen_df_loc_col_select_impl(df, col_idx_list)
    raise_bodo_error(
        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
        )


def gen_df_loc_col_select_impl(df, col_idx_list):
    col_names = []
    agojf__tasw = []
    if len(col_idx_list) > 0 and isinstance(col_idx_list[0], (bool, np.bool_)):
        for zvtpr__lqztv, vnl__xuwh in enumerate(col_idx_list):
            if vnl__xuwh:
                agojf__tasw.append(zvtpr__lqztv)
                col_names.append(df.columns[zvtpr__lqztv])
    else:
        col_names = col_idx_list
        agojf__tasw = [df.column_index[eipg__ypavt] for eipg__ypavt in
            col_idx_list]
    egrmn__viycb = None
    if df.is_table_format and len(col_idx_list) > 0 and len(col_idx_list
        ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD:
        egrmn__viycb = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
            agojf__tasw))}
        liqxb__gpy = (
            f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, False)[idx[0]]'
            )
    else:
        liqxb__gpy = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {ind})[idx[0]]'
             for ind in agojf__tasw)
    gyu__hxy = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]'
    rvzny__zjmg = 'def impl(I, idx):\n'
    rvzny__zjmg += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(rvzny__zjmg, col_names,
        liqxb__gpy, gyu__hxy, extra_globals=egrmn__viycb)


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
        uasbe__nht = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(uasbe__nht)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        egiv__zmwyl = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, egiv__zmwyl)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        lrxfv__onqe, = args
        kszy__hzhr = signature.return_type
        qwevx__oltd = cgutils.create_struct_proxy(kszy__hzhr)(context, builder)
        qwevx__oltd.obj = lrxfv__onqe
        context.nrt.incref(builder, signature.args[0], lrxfv__onqe)
        return qwevx__oltd._getvalue()
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
        nmkhs__uiql = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            rdk__rpu = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                nmkhs__uiql)
            return bodo.utils.conversion.box_if_dt64(rdk__rpu[idx[0]])
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
        nmkhs__uiql = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[nmkhs__uiql]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            rdk__rpu = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                nmkhs__uiql)
            rdk__rpu[idx[0]
                ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(val)
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    qwevx__oltd = cgutils.create_struct_proxy(fromty)(context, builder, val)
    gqkr__yypk = context.cast(builder, qwevx__oltd.obj, fromty.df_type,
        toty.df_type)
    xdwr__veu = cgutils.create_struct_proxy(toty)(context, builder)
    xdwr__veu.obj = gqkr__yypk
    return xdwr__veu._getvalue()
