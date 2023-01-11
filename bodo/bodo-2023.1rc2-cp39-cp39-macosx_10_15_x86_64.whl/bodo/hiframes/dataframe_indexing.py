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
            nsv__zvpk = idx
            mkuw__fbhu = df.data
            igv__wgibu = df.columns
            zqvw__ldfvy = self.replace_range_with_numeric_idx_if_needed(df,
                nsv__zvpk)
            cyg__cpli = DataFrameType(mkuw__fbhu, zqvw__ldfvy, igv__wgibu,
                is_table_format=df.is_table_format)
            return cyg__cpli(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            nrx__vffo = idx.types[0]
            uvdzw__fryp = idx.types[1]
            if isinstance(nrx__vffo, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(uvdzw__fryp):
                    alzo__effqd = get_overload_const_str(uvdzw__fryp)
                    if alzo__effqd not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, alzo__effqd))
                    vbk__sqbr = df.columns.index(alzo__effqd)
                    return df.data[vbk__sqbr].dtype(*args)
                if isinstance(uvdzw__fryp, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(nrx__vffo
                ) and nrx__vffo.dtype == types.bool_ or isinstance(nrx__vffo,
                types.SliceType):
                zqvw__ldfvy = self.replace_range_with_numeric_idx_if_needed(df,
                    nrx__vffo)
                if is_overload_constant_str(uvdzw__fryp):
                    wsj__nipu = get_overload_const_str(uvdzw__fryp)
                    if wsj__nipu not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {wsj__nipu}'
                            )
                    vbk__sqbr = df.columns.index(wsj__nipu)
                    xknlw__dam = df.data[vbk__sqbr]
                    yrrx__ywyab = xknlw__dam.dtype
                    xcu__vgws = types.literal(df.columns[vbk__sqbr])
                    cyg__cpli = bodo.SeriesType(yrrx__ywyab, xknlw__dam,
                        zqvw__ldfvy, xcu__vgws)
                    return cyg__cpli(*args)
                if isinstance(uvdzw__fryp, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                elif is_overload_constant_list(uvdzw__fryp):
                    vvlt__frr = get_overload_const_list(uvdzw__fryp)
                    gqgz__ecbmr = types.unliteral(uvdzw__fryp)
                    if gqgz__ecbmr.dtype == types.bool_:
                        if len(df.columns) != len(vvlt__frr):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {vvlt__frr} has {len(vvlt__frr)} values'
                                )
                        ijvzu__xengp = []
                        aeg__lrj = []
                        for wnpwt__cll in range(len(vvlt__frr)):
                            if vvlt__frr[wnpwt__cll]:
                                ijvzu__xengp.append(df.columns[wnpwt__cll])
                                aeg__lrj.append(df.data[wnpwt__cll])
                        kmjqz__xsd = tuple()
                        otvq__ypi = df.is_table_format and len(ijvzu__xengp
                            ) > 0 and len(ijvzu__xengp
                            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
                        cyg__cpli = DataFrameType(tuple(aeg__lrj),
                            zqvw__ldfvy, tuple(ijvzu__xengp),
                            is_table_format=otvq__ypi)
                        return cyg__cpli(*args)
                    elif gqgz__ecbmr.dtype == bodo.string_type:
                        kmjqz__xsd, aeg__lrj = (
                            get_df_getitem_kept_cols_and_data(df, vvlt__frr))
                        otvq__ypi = df.is_table_format and len(vvlt__frr
                            ) > 0 and len(vvlt__frr
                            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
                        cyg__cpli = DataFrameType(aeg__lrj, zqvw__ldfvy,
                            kmjqz__xsd, is_table_format=otvq__ypi)
                        return cyg__cpli(*args)
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
                ijvzu__xengp = []
                aeg__lrj = []
                for wnpwt__cll, pzp__ygg in enumerate(df.columns):
                    if pzp__ygg[0] != ind_val:
                        continue
                    ijvzu__xengp.append(pzp__ygg[1] if len(pzp__ygg) == 2 else
                        pzp__ygg[1:])
                    aeg__lrj.append(df.data[wnpwt__cll])
                xknlw__dam = tuple(aeg__lrj)
                ksph__hgnyt = df.index
                tgexg__cwc = tuple(ijvzu__xengp)
                cyg__cpli = DataFrameType(xknlw__dam, ksph__hgnyt, tgexg__cwc)
                return cyg__cpli(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                vbk__sqbr = df.columns.index(ind_val)
                xknlw__dam = df.data[vbk__sqbr]
                yrrx__ywyab = xknlw__dam.dtype
                ksph__hgnyt = df.index
                xcu__vgws = types.literal(df.columns[vbk__sqbr])
                cyg__cpli = bodo.SeriesType(yrrx__ywyab, xknlw__dam,
                    ksph__hgnyt, xcu__vgws)
                return cyg__cpli(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            xknlw__dam = df.data
            ksph__hgnyt = self.replace_range_with_numeric_idx_if_needed(df, ind
                )
            tgexg__cwc = df.columns
            cyg__cpli = DataFrameType(xknlw__dam, ksph__hgnyt, tgexg__cwc,
                is_table_format=df.is_table_format)
            return cyg__cpli(*args)
        elif is_overload_constant_list(ind):
            rgbh__luc = get_overload_const_list(ind)
            tgexg__cwc, xknlw__dam = get_df_getitem_kept_cols_and_data(df,
                rgbh__luc)
            ksph__hgnyt = df.index
            otvq__ypi = df.is_table_format and len(rgbh__luc) > 0 and len(
                rgbh__luc) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
            cyg__cpli = DataFrameType(xknlw__dam, ksph__hgnyt, tgexg__cwc,
                is_table_format=otvq__ypi)
            return cyg__cpli(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        zqvw__ldfvy = bodo.hiframes.pd_index_ext.NumericIndexType(types.
            int64, df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return zqvw__ldfvy


DataFrameGetItemTemplate._no_unliteral = True


def get_df_getitem_kept_cols_and_data(df, cols_to_keep_list):
    for tcy__gxyqz in cols_to_keep_list:
        if tcy__gxyqz not in df.column_index:
            raise_bodo_error('Column {} not found in dataframe columns {}'.
                format(tcy__gxyqz, df.columns))
    tgexg__cwc = tuple(cols_to_keep_list)
    xknlw__dam = tuple(df.data[df.column_index[aezf__uot]] for aezf__uot in
        tgexg__cwc)
    return tgexg__cwc, xknlw__dam


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
            ijvzu__xengp = []
            aeg__lrj = []
            for wnpwt__cll, pzp__ygg in enumerate(df.columns):
                if pzp__ygg[0] != ind_val:
                    continue
                ijvzu__xengp.append(pzp__ygg[1] if len(pzp__ygg) == 2 else
                    pzp__ygg[1:])
                aeg__lrj.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(wnpwt__cll))
            iclh__vsj = 'def impl(df, ind):\n'
            fwxu__wwy = (
                'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
            return bodo.hiframes.dataframe_impl._gen_init_df(iclh__vsj,
                ijvzu__xengp, ', '.join(aeg__lrj), fwxu__wwy)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        rgbh__luc = get_overload_const_list(ind)
        for tcy__gxyqz in rgbh__luc:
            if tcy__gxyqz not in df.column_index:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(tcy__gxyqz, df.columns))
        jygt__avss = None
        if df.is_table_format and len(rgbh__luc) > 0 and len(rgbh__luc
            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD:
            wygx__khf = [df.column_index[tcy__gxyqz] for tcy__gxyqz in
                rgbh__luc]
            jygt__avss = {'col_nums_meta': bodo.utils.typing.MetaType(tuple
                (wygx__khf))}
            aeg__lrj = (
                f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, True)'
                )
        else:
            aeg__lrj = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[tcy__gxyqz]}).copy()'
                 for tcy__gxyqz in rgbh__luc)
        iclh__vsj = 'def impl(df, ind):\n'
        fwxu__wwy = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(iclh__vsj,
            rgbh__luc, aeg__lrj, fwxu__wwy, extra_globals=jygt__avss)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        iclh__vsj = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            iclh__vsj += '  ind = bodo.utils.conversion.coerce_to_array(ind)\n'
        fwxu__wwy = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        if df.is_table_format:
            aeg__lrj = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[ind]')
        else:
            aeg__lrj = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[tcy__gxyqz]})[ind]'
                 for tcy__gxyqz in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(iclh__vsj, df.
            columns, aeg__lrj, fwxu__wwy)
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
        aezf__uot = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(aezf__uot)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        qfog__qtob = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, qfog__qtob)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        zrzhn__wxv, = args
        ylx__gbud = signature.return_type
        zmaa__pcm = cgutils.create_struct_proxy(ylx__gbud)(context, builder)
        zmaa__pcm.obj = zrzhn__wxv
        context.nrt.incref(builder, signature.args[0], zrzhn__wxv)
        return zmaa__pcm._getvalue()
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
        xrs__knmrn = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            fyfd__qba = get_overload_const_int(idx.types[1])
            if fyfd__qba < 0 or fyfd__qba >= xrs__knmrn:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            xeyt__etizd = [fyfd__qba]
        else:
            is_out_series = False
            xeyt__etizd = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >= xrs__knmrn for
                ind in xeyt__etizd):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[xeyt__etizd])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                fyfd__qba = xeyt__etizd[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df, fyfd__qba)[
                        idx[0]])
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
    iclh__vsj = 'def impl(I, idx):\n'
    iclh__vsj += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        iclh__vsj += f'  idx_t = {idx}\n'
    else:
        iclh__vsj += (
            f'  idx_t = bodo.utils.conversion.coerce_to_array({idx})\n')
    fwxu__wwy = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]'
    jygt__avss = None
    if df.is_table_format and not is_out_series:
        wygx__khf = [df.column_index[tcy__gxyqz] for tcy__gxyqz in col_names]
        jygt__avss = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
            wygx__khf))}
        aeg__lrj = (
            f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, False)[idx_t]'
            )
    else:
        aeg__lrj = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[tcy__gxyqz]})[idx_t]'
             for tcy__gxyqz in col_names)
    if is_out_series:
        puf__hpi = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        iclh__vsj += f"""  return bodo.hiframes.pd_series_ext.init_series({aeg__lrj}, {fwxu__wwy}, {puf__hpi})
"""
        xesy__wsgcz = {}
        exec(iclh__vsj, {'bodo': bodo}, xesy__wsgcz)
        return xesy__wsgcz['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(iclh__vsj, col_names,
        aeg__lrj, fwxu__wwy, extra_globals=jygt__avss)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    iclh__vsj = 'def impl(I, idx):\n'
    iclh__vsj += '  df = I._obj\n'
    zgt__wwuw = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[tcy__gxyqz]})[{idx}]'
         for tcy__gxyqz in col_names)
    iclh__vsj += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    iclh__vsj += f"""  return bodo.hiframes.pd_series_ext.init_series(({zgt__wwuw},), row_idx, None)
"""
    xesy__wsgcz = {}
    exec(iclh__vsj, {'bodo': bodo}, xesy__wsgcz)
    impl = xesy__wsgcz['impl']
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
        aezf__uot = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(aezf__uot)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        qfog__qtob = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, qfog__qtob)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        zrzhn__wxv, = args
        sfrwp__onku = signature.return_type
        przo__jnjwe = cgutils.create_struct_proxy(sfrwp__onku)(context, builder
            )
        przo__jnjwe.obj = zrzhn__wxv
        context.nrt.incref(builder, signature.args[0], zrzhn__wxv)
        return przo__jnjwe._getvalue()
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
        iclh__vsj = 'def impl(I, idx):\n'
        iclh__vsj += '  df = I._obj\n'
        iclh__vsj += '  idx_t = bodo.utils.conversion.coerce_to_array(idx)\n'
        fwxu__wwy = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        if df.is_table_format:
            aeg__lrj = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[idx_t]'
                )
        else:
            aeg__lrj = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[tcy__gxyqz]})[idx_t]'
                 for tcy__gxyqz in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(iclh__vsj, df.
            columns, aeg__lrj, fwxu__wwy)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        tedd__qqckl = idx.types[1]
        if is_overload_constant_str(tedd__qqckl):
            yoeqi__fpol = get_overload_const_str(tedd__qqckl)
            fyfd__qba = df.columns.index(yoeqi__fpol)

            def impl_col_name(I, idx):
                df = I._obj
                fwxu__wwy = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
                    df)
                ste__ioo = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df
                    , fyfd__qba)
                return bodo.hiframes.pd_series_ext.init_series(ste__ioo,
                    fwxu__wwy, yoeqi__fpol).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(tedd__qqckl):
            col_idx_list = get_overload_const_list(tedd__qqckl)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(tcy__gxyqz in df.column_index for
                tcy__gxyqz in col_idx_list):
                raise_bodo_error(
                    f'DataFrame.loc[]: invalid column list {col_idx_list}; not all in dataframe columns {df.columns}'
                    )
            return gen_df_loc_col_select_impl(df, col_idx_list)
    raise_bodo_error(
        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
        )


def gen_df_loc_col_select_impl(df, col_idx_list):
    col_names = []
    xeyt__etizd = []
    if len(col_idx_list) > 0 and isinstance(col_idx_list[0], (bool, np.bool_)):
        for wnpwt__cll, csre__eozf in enumerate(col_idx_list):
            if csre__eozf:
                xeyt__etizd.append(wnpwt__cll)
                col_names.append(df.columns[wnpwt__cll])
    else:
        col_names = col_idx_list
        xeyt__etizd = [df.column_index[tcy__gxyqz] for tcy__gxyqz in
            col_idx_list]
    jygt__avss = None
    if df.is_table_format and len(col_idx_list) > 0 and len(col_idx_list
        ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD:
        jygt__avss = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
            xeyt__etizd))}
        aeg__lrj = (
            f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, False)[idx[0]]'
            )
    else:
        aeg__lrj = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {ind})[idx[0]]'
             for ind in xeyt__etizd)
    fwxu__wwy = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]')
    iclh__vsj = 'def impl(I, idx):\n'
    iclh__vsj += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(iclh__vsj, col_names,
        aeg__lrj, fwxu__wwy, extra_globals=jygt__avss)


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
        aezf__uot = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(aezf__uot)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        qfog__qtob = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, qfog__qtob)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        zrzhn__wxv, = args
        osb__adkz = signature.return_type
        yyd__kuox = cgutils.create_struct_proxy(osb__adkz)(context, builder)
        yyd__kuox.obj = zrzhn__wxv
        context.nrt.incref(builder, signature.args[0], zrzhn__wxv)
        return yyd__kuox._getvalue()
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
        fyfd__qba = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            ste__ioo = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                fyfd__qba)
            return bodo.utils.conversion.box_if_dt64(ste__ioo[idx[0]])
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
        fyfd__qba = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[fyfd__qba]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            ste__ioo = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                fyfd__qba)
            ste__ioo[idx[0]
                ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(val)
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    yyd__kuox = cgutils.create_struct_proxy(fromty)(context, builder, val)
    oalj__fjibl = context.cast(builder, yyd__kuox.obj, fromty.df_type, toty
        .df_type)
    bfy__bpcw = cgutils.create_struct_proxy(toty)(context, builder)
    bfy__bpcw.obj = oalj__fjibl
    return bfy__bpcw._getvalue()
