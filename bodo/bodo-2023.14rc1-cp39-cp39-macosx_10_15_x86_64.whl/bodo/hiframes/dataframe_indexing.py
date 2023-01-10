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
            vsfc__csk = idx
            dugl__oivc = df.data
            awayi__wkbi = df.columns
            hqdel__qpmmy = self.replace_range_with_numeric_idx_if_needed(df,
                vsfc__csk)
            ooif__fvnpm = DataFrameType(dugl__oivc, hqdel__qpmmy,
                awayi__wkbi, is_table_format=df.is_table_format)
            return ooif__fvnpm(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            powla__prknn = idx.types[0]
            eylaf__vnbrb = idx.types[1]
            if isinstance(powla__prknn, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(eylaf__vnbrb):
                    ugqen__ryjxl = get_overload_const_str(eylaf__vnbrb)
                    if ugqen__ryjxl not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, ugqen__ryjxl))
                    qakqg__gfz = df.columns.index(ugqen__ryjxl)
                    return df.data[qakqg__gfz].dtype(*args)
                if isinstance(eylaf__vnbrb, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(powla__prknn
                ) and powla__prknn.dtype == types.bool_ or isinstance(
                powla__prknn, types.SliceType):
                hqdel__qpmmy = self.replace_range_with_numeric_idx_if_needed(df
                    , powla__prknn)
                if is_overload_constant_str(eylaf__vnbrb):
                    dmkmc__oibw = get_overload_const_str(eylaf__vnbrb)
                    if dmkmc__oibw not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {dmkmc__oibw}'
                            )
                    qakqg__gfz = df.columns.index(dmkmc__oibw)
                    hmouo__nwvlg = df.data[qakqg__gfz]
                    cfw__jretu = hmouo__nwvlg.dtype
                    rfhy__gcgsr = types.literal(df.columns[qakqg__gfz])
                    ooif__fvnpm = bodo.SeriesType(cfw__jretu, hmouo__nwvlg,
                        hqdel__qpmmy, rfhy__gcgsr)
                    return ooif__fvnpm(*args)
                if isinstance(eylaf__vnbrb, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                elif is_overload_constant_list(eylaf__vnbrb):
                    uudsx__nrre = get_overload_const_list(eylaf__vnbrb)
                    vjbnt__xahj = types.unliteral(eylaf__vnbrb)
                    if vjbnt__xahj.dtype == types.bool_:
                        if len(df.columns) != len(uudsx__nrre):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {uudsx__nrre} has {len(uudsx__nrre)} values'
                                )
                        wbqo__nywz = []
                        smv__vlu = []
                        for vao__jqjn in range(len(uudsx__nrre)):
                            if uudsx__nrre[vao__jqjn]:
                                wbqo__nywz.append(df.columns[vao__jqjn])
                                smv__vlu.append(df.data[vao__jqjn])
                        jxu__cxt = tuple()
                        ichb__aticr = df.is_table_format and len(wbqo__nywz
                            ) > 0 and len(wbqo__nywz
                            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
                        ooif__fvnpm = DataFrameType(tuple(smv__vlu),
                            hqdel__qpmmy, tuple(wbqo__nywz),
                            is_table_format=ichb__aticr)
                        return ooif__fvnpm(*args)
                    elif vjbnt__xahj.dtype == bodo.string_type:
                        jxu__cxt, smv__vlu = get_df_getitem_kept_cols_and_data(
                            df, uudsx__nrre)
                        ichb__aticr = df.is_table_format and len(uudsx__nrre
                            ) > 0 and len(uudsx__nrre
                            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
                        ooif__fvnpm = DataFrameType(smv__vlu, hqdel__qpmmy,
                            jxu__cxt, is_table_format=ichb__aticr)
                        return ooif__fvnpm(*args)
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
                wbqo__nywz = []
                smv__vlu = []
                for vao__jqjn, gpsx__dets in enumerate(df.columns):
                    if gpsx__dets[0] != ind_val:
                        continue
                    wbqo__nywz.append(gpsx__dets[1] if len(gpsx__dets) == 2
                         else gpsx__dets[1:])
                    smv__vlu.append(df.data[vao__jqjn])
                hmouo__nwvlg = tuple(smv__vlu)
                gbos__jroj = df.index
                xmnk__dcmfs = tuple(wbqo__nywz)
                ooif__fvnpm = DataFrameType(hmouo__nwvlg, gbos__jroj,
                    xmnk__dcmfs)
                return ooif__fvnpm(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                qakqg__gfz = df.columns.index(ind_val)
                hmouo__nwvlg = df.data[qakqg__gfz]
                cfw__jretu = hmouo__nwvlg.dtype
                gbos__jroj = df.index
                rfhy__gcgsr = types.literal(df.columns[qakqg__gfz])
                ooif__fvnpm = bodo.SeriesType(cfw__jretu, hmouo__nwvlg,
                    gbos__jroj, rfhy__gcgsr)
                return ooif__fvnpm(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            hmouo__nwvlg = df.data
            gbos__jroj = self.replace_range_with_numeric_idx_if_needed(df, ind)
            xmnk__dcmfs = df.columns
            ooif__fvnpm = DataFrameType(hmouo__nwvlg, gbos__jroj,
                xmnk__dcmfs, is_table_format=df.is_table_format)
            return ooif__fvnpm(*args)
        elif is_overload_constant_list(ind):
            zorkj__pnxt = get_overload_const_list(ind)
            xmnk__dcmfs, hmouo__nwvlg = get_df_getitem_kept_cols_and_data(df,
                zorkj__pnxt)
            gbos__jroj = df.index
            ichb__aticr = df.is_table_format and len(zorkj__pnxt) > 0 and len(
                zorkj__pnxt) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
            ooif__fvnpm = DataFrameType(hmouo__nwvlg, gbos__jroj,
                xmnk__dcmfs, is_table_format=ichb__aticr)
            return ooif__fvnpm(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        hqdel__qpmmy = bodo.hiframes.pd_index_ext.NumericIndexType(types.
            int64, df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return hqdel__qpmmy


DataFrameGetItemTemplate._no_unliteral = True


def get_df_getitem_kept_cols_and_data(df, cols_to_keep_list):
    for tmmdb__tqlr in cols_to_keep_list:
        if tmmdb__tqlr not in df.column_index:
            raise_bodo_error('Column {} not found in dataframe columns {}'.
                format(tmmdb__tqlr, df.columns))
    xmnk__dcmfs = tuple(cols_to_keep_list)
    hmouo__nwvlg = tuple(df.data[df.column_index[mgmsq__flfkq]] for
        mgmsq__flfkq in xmnk__dcmfs)
    return xmnk__dcmfs, hmouo__nwvlg


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
            wbqo__nywz = []
            smv__vlu = []
            for vao__jqjn, gpsx__dets in enumerate(df.columns):
                if gpsx__dets[0] != ind_val:
                    continue
                wbqo__nywz.append(gpsx__dets[1] if len(gpsx__dets) == 2 else
                    gpsx__dets[1:])
                smv__vlu.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(vao__jqjn))
            rxug__mbwoh = 'def impl(df, ind):\n'
            kgo__eae = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
            return bodo.hiframes.dataframe_impl._gen_init_df(rxug__mbwoh,
                wbqo__nywz, ', '.join(smv__vlu), kgo__eae)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        zorkj__pnxt = get_overload_const_list(ind)
        for tmmdb__tqlr in zorkj__pnxt:
            if tmmdb__tqlr not in df.column_index:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(tmmdb__tqlr, df.columns))
        mjswv__cls = None
        if df.is_table_format and len(zorkj__pnxt) > 0 and len(zorkj__pnxt
            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD:
            vjije__cxjxu = [df.column_index[tmmdb__tqlr] for tmmdb__tqlr in
                zorkj__pnxt]
            mjswv__cls = {'col_nums_meta': bodo.utils.typing.MetaType(tuple
                (vjije__cxjxu))}
            smv__vlu = (
                f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, True)'
                )
        else:
            smv__vlu = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[tmmdb__tqlr]}).copy()'
                 for tmmdb__tqlr in zorkj__pnxt)
        rxug__mbwoh = 'def impl(df, ind):\n'
        kgo__eae = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(rxug__mbwoh,
            zorkj__pnxt, smv__vlu, kgo__eae, extra_globals=mjswv__cls)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        rxug__mbwoh = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            rxug__mbwoh += (
                '  ind = bodo.utils.conversion.coerce_to_array(ind)\n')
        kgo__eae = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        if df.is_table_format:
            smv__vlu = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[ind]')
        else:
            smv__vlu = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[tmmdb__tqlr]})[ind]'
                 for tmmdb__tqlr in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(rxug__mbwoh, df.
            columns, smv__vlu, kgo__eae)
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
        mgmsq__flfkq = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(mgmsq__flfkq)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        fwyx__giq = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, fwyx__giq)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        aai__kuuvz, = args
        kfqqr__gxda = signature.return_type
        pdr__zgz = cgutils.create_struct_proxy(kfqqr__gxda)(context, builder)
        pdr__zgz.obj = aai__kuuvz
        context.nrt.incref(builder, signature.args[0], aai__kuuvz)
        return pdr__zgz._getvalue()
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
        zdvpu__bbur = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            tss__ukjha = get_overload_const_int(idx.types[1])
            if tss__ukjha < 0 or tss__ukjha >= zdvpu__bbur:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            jhwg__uvkm = [tss__ukjha]
        else:
            is_out_series = False
            jhwg__uvkm = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >=
                zdvpu__bbur for ind in jhwg__uvkm):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[jhwg__uvkm])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                tss__ukjha = jhwg__uvkm[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df, tss__ukjha)
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
    rxug__mbwoh = 'def impl(I, idx):\n'
    rxug__mbwoh += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        rxug__mbwoh += f'  idx_t = {idx}\n'
    else:
        rxug__mbwoh += (
            f'  idx_t = bodo.utils.conversion.coerce_to_array({idx})\n')
    kgo__eae = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]'
    mjswv__cls = None
    if df.is_table_format and not is_out_series:
        vjije__cxjxu = [df.column_index[tmmdb__tqlr] for tmmdb__tqlr in
            col_names]
        mjswv__cls = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
            vjije__cxjxu))}
        smv__vlu = (
            f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, False)[idx_t]'
            )
    else:
        smv__vlu = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[tmmdb__tqlr]})[idx_t]'
             for tmmdb__tqlr in col_names)
    if is_out_series:
        kqa__xpqpt = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        rxug__mbwoh += f"""  return bodo.hiframes.pd_series_ext.init_series({smv__vlu}, {kgo__eae}, {kqa__xpqpt})
"""
        wglup__ydb = {}
        exec(rxug__mbwoh, {'bodo': bodo}, wglup__ydb)
        return wglup__ydb['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(rxug__mbwoh, col_names,
        smv__vlu, kgo__eae, extra_globals=mjswv__cls)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    rxug__mbwoh = 'def impl(I, idx):\n'
    rxug__mbwoh += '  df = I._obj\n'
    dnap__bmgc = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[tmmdb__tqlr]})[{idx}]'
         for tmmdb__tqlr in col_names)
    rxug__mbwoh += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    rxug__mbwoh += f"""  return bodo.hiframes.pd_series_ext.init_series(({dnap__bmgc},), row_idx, None)
"""
    wglup__ydb = {}
    exec(rxug__mbwoh, {'bodo': bodo}, wglup__ydb)
    impl = wglup__ydb['impl']
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
        mgmsq__flfkq = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(mgmsq__flfkq)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        fwyx__giq = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, fwyx__giq)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        aai__kuuvz, = args
        znmk__uxy = signature.return_type
        vmoil__rtwq = cgutils.create_struct_proxy(znmk__uxy)(context, builder)
        vmoil__rtwq.obj = aai__kuuvz
        context.nrt.incref(builder, signature.args[0], aai__kuuvz)
        return vmoil__rtwq._getvalue()
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
        rxug__mbwoh = 'def impl(I, idx):\n'
        rxug__mbwoh += '  df = I._obj\n'
        rxug__mbwoh += '  idx_t = bodo.utils.conversion.coerce_to_array(idx)\n'
        kgo__eae = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        if df.is_table_format:
            smv__vlu = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[idx_t]'
                )
        else:
            smv__vlu = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[tmmdb__tqlr]})[idx_t]'
                 for tmmdb__tqlr in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(rxug__mbwoh, df.
            columns, smv__vlu, kgo__eae)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        osqk__xmli = idx.types[1]
        if is_overload_constant_str(osqk__xmli):
            cpe__bmq = get_overload_const_str(osqk__xmli)
            tss__ukjha = df.columns.index(cpe__bmq)

            def impl_col_name(I, idx):
                df = I._obj
                kgo__eae = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
                    df)
                wed__pypyd = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
                    df, tss__ukjha)
                return bodo.hiframes.pd_series_ext.init_series(wed__pypyd,
                    kgo__eae, cpe__bmq).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(osqk__xmli):
            col_idx_list = get_overload_const_list(osqk__xmli)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(tmmdb__tqlr in df.column_index for
                tmmdb__tqlr in col_idx_list):
                raise_bodo_error(
                    f'DataFrame.loc[]: invalid column list {col_idx_list}; not all in dataframe columns {df.columns}'
                    )
            return gen_df_loc_col_select_impl(df, col_idx_list)
    raise_bodo_error(
        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
        )


def gen_df_loc_col_select_impl(df, col_idx_list):
    col_names = []
    jhwg__uvkm = []
    if len(col_idx_list) > 0 and isinstance(col_idx_list[0], (bool, np.bool_)):
        for vao__jqjn, ikmyz__nheur in enumerate(col_idx_list):
            if ikmyz__nheur:
                jhwg__uvkm.append(vao__jqjn)
                col_names.append(df.columns[vao__jqjn])
    else:
        col_names = col_idx_list
        jhwg__uvkm = [df.column_index[tmmdb__tqlr] for tmmdb__tqlr in
            col_idx_list]
    mjswv__cls = None
    if df.is_table_format and len(col_idx_list) > 0 and len(col_idx_list
        ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD:
        mjswv__cls = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
            jhwg__uvkm))}
        smv__vlu = (
            f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, False)[idx[0]]'
            )
    else:
        smv__vlu = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {ind})[idx[0]]'
             for ind in jhwg__uvkm)
    kgo__eae = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]'
    rxug__mbwoh = 'def impl(I, idx):\n'
    rxug__mbwoh += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(rxug__mbwoh, col_names,
        smv__vlu, kgo__eae, extra_globals=mjswv__cls)


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
        mgmsq__flfkq = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(mgmsq__flfkq)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        fwyx__giq = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, fwyx__giq)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        aai__kuuvz, = args
        auaao__rgn = signature.return_type
        dzub__fnk = cgutils.create_struct_proxy(auaao__rgn)(context, builder)
        dzub__fnk.obj = aai__kuuvz
        context.nrt.incref(builder, signature.args[0], aai__kuuvz)
        return dzub__fnk._getvalue()
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
        tss__ukjha = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            wed__pypyd = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                tss__ukjha)
            return bodo.utils.conversion.box_if_dt64(wed__pypyd[idx[0]])
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
        tss__ukjha = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[tss__ukjha]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            wed__pypyd = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                tss__ukjha)
            wed__pypyd[idx[0]
                ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(val)
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    dzub__fnk = cgutils.create_struct_proxy(fromty)(context, builder, val)
    shgor__beab = context.cast(builder, dzub__fnk.obj, fromty.df_type, toty
        .df_type)
    uhwq__prf = cgutils.create_struct_proxy(toty)(context, builder)
    uhwq__prf.obj = shgor__beab
    return uhwq__prf._getvalue()
