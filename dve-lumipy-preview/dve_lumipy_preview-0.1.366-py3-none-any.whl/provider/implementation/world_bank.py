import datetime as dt
from typing import Union, Dict, Optional, Iterable

import wbgapi as wb
from pandas import DataFrame, merge, concat

from lumipy.typing.sql_value_type import SqlValType
from ..base_provider import BaseProvider
from ..translation import apply_filter
from ..metadata import ColumnMeta, ParamMeta


class WorldBankDataSources(BaseProvider):

    def __init__(self):

        columns = [
            ColumnMeta('SourceName', SqlValType.Text),
            ColumnMeta('SourceCode', SqlValType.Text),
            ColumnMeta('SeriesName', SqlValType.Text),
            ColumnMeta('SeriesCode', SqlValType.Text),
        ]

        super().__init__(
            'WorldBank.MetaData.Source',
            columns=columns
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        src_df = DataFrame(
            wb.source.info().table()[:-1],
            columns=['ID', 'SourceName', 'SourceCode', 'Concepts', 'LastUpdated']
        )
        src_df = apply_filter(src_df, data_filter)

        for _, row in src_df.iterrows():

            # Looks like a DB sometimes drops but still shows up in the sources list
            try:
                ser = wb.series.info(db=row.ID)
                df = DataFrame(
                    ser.table()[:-1],
                    columns=['SeriesCode', 'SeriesName']
                )
                df['SourceName'] = row.SourceName
                df['SourceCode'] = row.SourceCode

            except Exception as e:
                print(e)
                print(row)
                continue

            yield apply_filter(df, data_filter)


class WorldBankEconomies(BaseProvider):

    def __init__(self):

        columns = [
            ColumnMeta('Code', SqlValType.Text),
            ColumnMeta('Name', SqlValType.Text),
            ColumnMeta('RegionCode', SqlValType.Text),
            ColumnMeta('IncomeLevel', SqlValType.Text),
            ColumnMeta('Type', SqlValType.Text),
            ColumnMeta('RegionName', SqlValType.Text),
        ]

        super().__init__(
            'WorldBank.Metadata.Economy',
            columns=columns
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:
        econ = wb.economy.info()
        region = wb.region.info()

        edf = DataFrame(econ.table(), columns=['Code', 'Name', 'RegionCode', 'IncomeLevel'])
        edf['Type'] = edf.RegionCode.apply(lambda x: 'Region' if x == '' else 'Country')
        edf = edf.iloc[:-1]

        rdf = DataFrame(region.table(), columns=region.columns)

        mdf = merge(edf, rdf, left_on='RegionCode', right_on='code', how='left')
        mdf['RegionName'] = mdf.apply(lambda x: x['name'] if x.Type == 'Country' else x['Name'], axis=1)
        return mdf.drop(labels=['code', 'name'], axis=1)


class WorldBankSeriesMetadata(BaseProvider):

    def __init__(self):

        columns = [
            ColumnMeta('MetadataLabel', SqlValType.Text),
            ColumnMeta('MetadataValue', SqlValType.Text),
        ]
        params = [
            ParamMeta('SeriesCode', SqlValType.Text, is_required=True)
        ]

        super().__init__(
            'WorldBank.Metadata.Series',
            columns=columns,
            parameters=params,
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        series_code = params['SeriesCode']
        sm = wb.series.metadata.get(series_code)
        df = DataFrame([sm.metadata]).T.reset_index()
        df.columns = ['MetadataLabel', 'MetadataValue']
        return df


class WorldBankSeriesData(BaseProvider):

    def __init__(self):

        columns = [
            ColumnMeta('Year', SqlValType.Int),
            ColumnMeta('Value', SqlValType.Double),
            ColumnMeta('EconCode', SqlValType.Text),
            ColumnMeta('Series', SqlValType.Text),
            ColumnMeta('SeriesName', SqlValType.Text),
        ]

        params = [
            ParamMeta('SeriesCode', SqlValType.Text, is_required=True),
            ParamMeta('EconomicRegion', SqlValType.Text),
            ParamMeta('StartYear', SqlValType.Int, default_value=1950),
            ParamMeta('EndYear', SqlValType.Int, default_value=dt.date.today().year + 1),
            ParamMeta('ExpandRegion', SqlValType.Boolean, default_value=True),
        ]

        super().__init__(
            'WorldBank.Data.Series',
            columns=columns,
            parameters=params,
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> Union[DataFrame, Iterable[DataFrame]]:

        # Handle series code and add human-readable info
        series_code = params['SeriesCode']
        series_name = wb.series.info(series_code).table()[0][1]

        # Handle economic region code
        econ_region = params.get('EconomicRegion')

        is_a_country = wb.economy.info(econ_region).table()[0][2] != '' if econ_region is not None else None

        if econ_region is not None and is_a_country:
            # This is a country such as the USA. Can't be split into constituents.
            economic_regions = [econ_region]
        elif econ_region is not None and not is_a_country:
            # This is a region such as south-east asia (SAS). Can be split into constituents.
            economic_regions = [econ_region]
            if params.get('ExpandRegion'):
                economic_regions = sorted(list(wb.region.members(econ_region)))
        else:
            # Otherwise default to global
            economic_regions = 'all'

        vdf = wb.data.DataFrame(
            series_code,
            economy=economic_regions,
            time=range(params['StartYear'], params['EndYear'])
        ).T

        def make_stack(e):

            _df = DataFrame(vdf[e])
            _df['Series'] = series_code
            _df['SeriesName'] = series_name
            _df['EconCode'] = e
            _df['Year'] = [int(v[2:]) for v in _df.index]

            _df.columns = ['Value', 'Series', 'SeriesName', 'EconCode', 'Year']
            return _df.reset_index(drop=True)

        return concat(map(make_stack, vdf.columns.tolist()))
