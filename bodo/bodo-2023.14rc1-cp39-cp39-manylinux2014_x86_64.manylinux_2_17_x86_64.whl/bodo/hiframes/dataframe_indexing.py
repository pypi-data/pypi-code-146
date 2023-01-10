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
            hno__mkkf = idx
            leegi__knuw = df.data
            nlg__ydndw = df.columns
            kgdg__dnvo = self.replace_range_with_numeric_idx_if_needed(df,
                hno__mkkf)
            jrex__gtay = DataFrameType(leegi__knuw, kgdg__dnvo, nlg__ydndw,
                is_table_format=df.is_table_format)
            return jrex__gtay(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            rtd__ohww = idx.types[0]
            frru__nteup = idx.types[1]
            if isinstance(rtd__ohww, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(frru__nteup):
                    fugs__ntt = get_overload_const_str(frru__nteup)
                    if fugs__ntt not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, fugs__ntt))
                    vnv__naci = df.columns.index(fugs__ntt)
                    return df.data[vnv__naci].dtype(*args)
                if isinstance(frru__nteup, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(rtd__ohww
                ) and rtd__ohww.dtype == types.bool_ or isinstance(rtd__ohww,
                types.SliceType):
                kgdg__dnvo = self.replace_range_with_numeric_idx_if_needed(df,
                    rtd__ohww)
                if is_overload_constant_str(frru__nteup):
                    ppub__xrhmi = get_overload_const_str(frru__nteup)
                    if ppub__xrhmi not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {ppub__xrhmi}'
                            )
                    vnv__naci = df.columns.index(ppub__xrhmi)
                    tfhjv__umww = df.data[vnv__naci]
                    oweb__ucv = tfhjv__umww.dtype
                    ria__jscy = types.literal(df.columns[vnv__naci])
                    jrex__gtay = bodo.SeriesType(oweb__ucv, tfhjv__umww,
                        kgdg__dnvo, ria__jscy)
                    return jrex__gtay(*args)
                if isinstance(frru__nteup, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                elif is_overload_constant_list(frru__nteup):
                    bup__dmbi = get_overload_const_list(frru__nteup)
                    zhbm__rzg = types.unliteral(frru__nteup)
                    if zhbm__rzg.dtype == types.bool_:
                        if len(df.columns) != len(bup__dmbi):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {bup__dmbi} has {len(bup__dmbi)} values'
                                )
                        kxup__yxey = []
                        ujw__xvat = []
                        for iaibm__pfiat in range(len(bup__dmbi)):
                            if bup__dmbi[iaibm__pfiat]:
                                kxup__yxey.append(df.columns[iaibm__pfiat])
                                ujw__xvat.append(df.data[iaibm__pfiat])
                        gquxz__uwao = tuple()
                        niu__fobm = df.is_table_format and len(kxup__yxey
                            ) > 0 and len(kxup__yxey
                            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
                        jrex__gtay = DataFrameType(tuple(ujw__xvat),
                            kgdg__dnvo, tuple(kxup__yxey), is_table_format=
                            niu__fobm)
                        return jrex__gtay(*args)
                    elif zhbm__rzg.dtype == bodo.string_type:
                        gquxz__uwao, ujw__xvat = (
                            get_df_getitem_kept_cols_and_data(df, bup__dmbi))
                        niu__fobm = df.is_table_format and len(bup__dmbi
                            ) > 0 and len(bup__dmbi
                            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
                        jrex__gtay = DataFrameType(ujw__xvat, kgdg__dnvo,
                            gquxz__uwao, is_table_format=niu__fobm)
                        return jrex__gtay(*args)
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
                kxup__yxey = []
                ujw__xvat = []
                for iaibm__pfiat, dzfxg__dqrn in enumerate(df.columns):
                    if dzfxg__dqrn[0] != ind_val:
                        continue
                    kxup__yxey.append(dzfxg__dqrn[1] if len(dzfxg__dqrn) ==
                        2 else dzfxg__dqrn[1:])
                    ujw__xvat.append(df.data[iaibm__pfiat])
                tfhjv__umww = tuple(ujw__xvat)
                tcs__nvcto = df.index
                lpyph__oxa = tuple(kxup__yxey)
                jrex__gtay = DataFrameType(tfhjv__umww, tcs__nvcto, lpyph__oxa)
                return jrex__gtay(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                vnv__naci = df.columns.index(ind_val)
                tfhjv__umww = df.data[vnv__naci]
                oweb__ucv = tfhjv__umww.dtype
                tcs__nvcto = df.index
                ria__jscy = types.literal(df.columns[vnv__naci])
                jrex__gtay = bodo.SeriesType(oweb__ucv, tfhjv__umww,
                    tcs__nvcto, ria__jscy)
                return jrex__gtay(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            tfhjv__umww = df.data
            tcs__nvcto = self.replace_range_with_numeric_idx_if_needed(df, ind)
            lpyph__oxa = df.columns
            jrex__gtay = DataFrameType(tfhjv__umww, tcs__nvcto, lpyph__oxa,
                is_table_format=df.is_table_format)
            return jrex__gtay(*args)
        elif is_overload_constant_list(ind):
            jye__bznug = get_overload_const_list(ind)
            lpyph__oxa, tfhjv__umww = get_df_getitem_kept_cols_and_data(df,
                jye__bznug)
            tcs__nvcto = df.index
            niu__fobm = df.is_table_format and len(jye__bznug) > 0 and len(
                jye__bznug) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
            jrex__gtay = DataFrameType(tfhjv__umww, tcs__nvcto, lpyph__oxa,
                is_table_format=niu__fobm)
            return jrex__gtay(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        kgdg__dnvo = bodo.hiframes.pd_index_ext.NumericIndexType(types.
            int64, df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return kgdg__dnvo


DataFrameGetItemTemplate._no_unliteral = True


def get_df_getitem_kept_cols_and_data(df, cols_to_keep_list):
    for ssga__ojuz in cols_to_keep_list:
        if ssga__ojuz not in df.column_index:
            raise_bodo_error('Column {} not found in dataframe columns {}'.
                format(ssga__ojuz, df.columns))
    lpyph__oxa = tuple(cols_to_keep_list)
    tfhjv__umww = tuple(df.data[df.column_index[jbsr__stsib]] for
        jbsr__stsib in lpyph__oxa)
    return lpyph__oxa, tfhjv__umww


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
            kxup__yxey = []
            ujw__xvat = []
            for iaibm__pfiat, dzfxg__dqrn in enumerate(df.columns):
                if dzfxg__dqrn[0] != ind_val:
                    continue
                kxup__yxey.append(dzfxg__dqrn[1] if len(dzfxg__dqrn) == 2 else
                    dzfxg__dqrn[1:])
                ujw__xvat.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(iaibm__pfiat))
            rufe__ebs = 'def impl(df, ind):\n'
            abq__oek = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
            return bodo.hiframes.dataframe_impl._gen_init_df(rufe__ebs,
                kxup__yxey, ', '.join(ujw__xvat), abq__oek)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        jye__bznug = get_overload_const_list(ind)
        for ssga__ojuz in jye__bznug:
            if ssga__ojuz not in df.column_index:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(ssga__ojuz, df.columns))
        kcwlz__jha = None
        if df.is_table_format and len(jye__bznug) > 0 and len(jye__bznug
            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD:
            gqmob__mjbux = [df.column_index[ssga__ojuz] for ssga__ojuz in
                jye__bznug]
            kcwlz__jha = {'col_nums_meta': bodo.utils.typing.MetaType(tuple
                (gqmob__mjbux))}
            ujw__xvat = (
                f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, True)'
                )
        else:
            ujw__xvat = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[ssga__ojuz]}).copy()'
                 for ssga__ojuz in jye__bznug)
        rufe__ebs = 'def impl(df, ind):\n'
        abq__oek = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(rufe__ebs,
            jye__bznug, ujw__xvat, abq__oek, extra_globals=kcwlz__jha)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        rufe__ebs = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            rufe__ebs += '  ind = bodo.utils.conversion.coerce_to_array(ind)\n'
        abq__oek = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        if df.is_table_format:
            ujw__xvat = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[ind]')
        else:
            ujw__xvat = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[ssga__ojuz]})[ind]'
                 for ssga__ojuz in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(rufe__ebs, df.
            columns, ujw__xvat, abq__oek)
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
        jbsr__stsib = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(jbsr__stsib)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        hnzp__tcmtn = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, hnzp__tcmtn)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        gjxj__uer, = args
        wpej__fyfed = signature.return_type
        cfv__lts = cgutils.create_struct_proxy(wpej__fyfed)(context, builder)
        cfv__lts.obj = gjxj__uer
        context.nrt.incref(builder, signature.args[0], gjxj__uer)
        return cfv__lts._getvalue()
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
        afwld__sqrna = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            oxfgp__zgf = get_overload_const_int(idx.types[1])
            if oxfgp__zgf < 0 or oxfgp__zgf >= afwld__sqrna:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            fsu__ivfp = [oxfgp__zgf]
        else:
            is_out_series = False
            fsu__ivfp = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >=
                afwld__sqrna for ind in fsu__ivfp):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[fsu__ivfp])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                oxfgp__zgf = fsu__ivfp[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df, oxfgp__zgf)
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
    rufe__ebs = 'def impl(I, idx):\n'
    rufe__ebs += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        rufe__ebs += f'  idx_t = {idx}\n'
    else:
        rufe__ebs += (
            f'  idx_t = bodo.utils.conversion.coerce_to_array({idx})\n')
    abq__oek = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]'
    kcwlz__jha = None
    if df.is_table_format and not is_out_series:
        gqmob__mjbux = [df.column_index[ssga__ojuz] for ssga__ojuz in col_names
            ]
        kcwlz__jha = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
            gqmob__mjbux))}
        ujw__xvat = (
            f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, False)[idx_t]'
            )
    else:
        ujw__xvat = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[ssga__ojuz]})[idx_t]'
             for ssga__ojuz in col_names)
    if is_out_series:
        age__mfxo = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        rufe__ebs += f"""  return bodo.hiframes.pd_series_ext.init_series({ujw__xvat}, {abq__oek}, {age__mfxo})
"""
        cky__cemn = {}
        exec(rufe__ebs, {'bodo': bodo}, cky__cemn)
        return cky__cemn['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(rufe__ebs, col_names,
        ujw__xvat, abq__oek, extra_globals=kcwlz__jha)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    rufe__ebs = 'def impl(I, idx):\n'
    rufe__ebs += '  df = I._obj\n'
    lguo__ams = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[ssga__ojuz]})[{idx}]'
         for ssga__ojuz in col_names)
    rufe__ebs += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    rufe__ebs += f"""  return bodo.hiframes.pd_series_ext.init_series(({lguo__ams},), row_idx, None)
"""
    cky__cemn = {}
    exec(rufe__ebs, {'bodo': bodo}, cky__cemn)
    impl = cky__cemn['impl']
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
        jbsr__stsib = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(jbsr__stsib)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        hnzp__tcmtn = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, hnzp__tcmtn)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        gjxj__uer, = args
        cidpn__gnkbq = signature.return_type
        dkd__makld = cgutils.create_struct_proxy(cidpn__gnkbq)(context, builder
            )
        dkd__makld.obj = gjxj__uer
        context.nrt.incref(builder, signature.args[0], gjxj__uer)
        return dkd__makld._getvalue()
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
        rufe__ebs = 'def impl(I, idx):\n'
        rufe__ebs += '  df = I._obj\n'
        rufe__ebs += '  idx_t = bodo.utils.conversion.coerce_to_array(idx)\n'
        abq__oek = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        if df.is_table_format:
            ujw__xvat = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[idx_t]'
                )
        else:
            ujw__xvat = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[ssga__ojuz]})[idx_t]'
                 for ssga__ojuz in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(rufe__ebs, df.
            columns, ujw__xvat, abq__oek)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        jcwv__ptggi = idx.types[1]
        if is_overload_constant_str(jcwv__ptggi):
            tjrc__dlrq = get_overload_const_str(jcwv__ptggi)
            oxfgp__zgf = df.columns.index(tjrc__dlrq)

            def impl_col_name(I, idx):
                df = I._obj
                abq__oek = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
                    df)
                skcf__siaey = (bodo.hiframes.pd_dataframe_ext.
                    get_dataframe_data(df, oxfgp__zgf))
                return bodo.hiframes.pd_series_ext.init_series(skcf__siaey,
                    abq__oek, tjrc__dlrq).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(jcwv__ptggi):
            col_idx_list = get_overload_const_list(jcwv__ptggi)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(ssga__ojuz in df.column_index for
                ssga__ojuz in col_idx_list):
                raise_bodo_error(
                    f'DataFrame.loc[]: invalid column list {col_idx_list}; not all in dataframe columns {df.columns}'
                    )
            return gen_df_loc_col_select_impl(df, col_idx_list)
    raise_bodo_error(
        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
        )


def gen_df_loc_col_select_impl(df, col_idx_list):
    col_names = []
    fsu__ivfp = []
    if len(col_idx_list) > 0 and isinstance(col_idx_list[0], (bool, np.bool_)):
        for iaibm__pfiat, bhrea__lks in enumerate(col_idx_list):
            if bhrea__lks:
                fsu__ivfp.append(iaibm__pfiat)
                col_names.append(df.columns[iaibm__pfiat])
    else:
        col_names = col_idx_list
        fsu__ivfp = [df.column_index[ssga__ojuz] for ssga__ojuz in col_idx_list
            ]
    kcwlz__jha = None
    if df.is_table_format and len(col_idx_list) > 0 and len(col_idx_list
        ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD:
        kcwlz__jha = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
            fsu__ivfp))}
        ujw__xvat = (
            f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, False)[idx[0]]'
            )
    else:
        ujw__xvat = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {ind})[idx[0]]'
             for ind in fsu__ivfp)
    abq__oek = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]'
    rufe__ebs = 'def impl(I, idx):\n'
    rufe__ebs += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(rufe__ebs, col_names,
        ujw__xvat, abq__oek, extra_globals=kcwlz__jha)


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
        jbsr__stsib = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(jbsr__stsib)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        hnzp__tcmtn = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, hnzp__tcmtn)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        gjxj__uer, = args
        ppagp__kvaw = signature.return_type
        hvb__dquj = cgutils.create_struct_proxy(ppagp__kvaw)(context, builder)
        hvb__dquj.obj = gjxj__uer
        context.nrt.incref(builder, signature.args[0], gjxj__uer)
        return hvb__dquj._getvalue()
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
        oxfgp__zgf = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            skcf__siaey = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                oxfgp__zgf)
            return bodo.utils.conversion.box_if_dt64(skcf__siaey[idx[0]])
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
        oxfgp__zgf = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[oxfgp__zgf]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            skcf__siaey = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                oxfgp__zgf)
            skcf__siaey[idx[0]
                ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(val)
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    hvb__dquj = cgutils.create_struct_proxy(fromty)(context, builder, val)
    xznfs__veku = context.cast(builder, hvb__dquj.obj, fromty.df_type, toty
        .df_type)
    motb__ljx = cgutils.create_struct_proxy(toty)(context, builder)
    motb__ljx.obj = xznfs__veku
    return motb__ljx._getvalue()
