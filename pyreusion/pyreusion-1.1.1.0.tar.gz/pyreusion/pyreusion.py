#%%
# Pyreusion
from datetime import datetime
import logging
import numpy as np
from pandas import DataFrame, isna
from pandas.core.series import Series
from pymysql.converters import escape_string
from decimal import Decimal
import re
from typing import Optional, Union
import emoji
import zipfile
import os
from chardet import detect


#%%
class Operations:
    """"""

    @classmethod
    def unzip_file(cls, fp: str, dest_fp: str):
        flag = False
        if zipfile.is_zipfile(fp):
            with zipfile.ZipFile(fp, 'r') as zipf:
                zipf.extractall(dest_fp)
                flag = True
        return {'fp': fp, 'flag': flag}

    @classmethod
    def chk_file(cls, path: str) -> bool:
        """Checks whether the file in the folder
        """
        try:
            os.stat(path)
            return True
        except FileNotFoundError:
            return False

    @classmethod
    def ls(cls,
           dir: str,
           by: str = 'name',
           reverse: bool = False,
           pattern: str = '.*',
           drop_folder: bool = False,
           flags: re.RegexFlag = 0):
        """Get the sorted filename from dir & selected by regex

        Args:
            dir: folder path.
            by: sorted type.
                support: 'name'|'ctime'|'mtime'
            reverse: reverse order.
            pattern: regular expression.
            drop_folder: drop the name which is folder
            flags: regex matching strategy.
        """
        if by == 'name':
            lsdir = sorted(os.listdir(dir), reverse=reverse)
        elif by == 'ctime':
            lsdir = sorted(os.listdir(dir), key=lambda x: os.stat(os.path.join(dir, x)).st_ctime, reverse=reverse)
        elif by == 'mtime':
            lsdir = sorted(os.listdir(dir), key=lambda x: os.stat(os.path.join(dir, x)).st_mtime, reverse=reverse)
        else:
            raise ValueError
        listdir = [name for name in lsdir if re.search(pattern=pattern, string=name, flags=flags)]
        if drop_folder:
            listdir = [name for name in listdir if not os.path.isdir(os.path.join(dir, name))]
        return listdir

    @classmethod
    def get_encoding(cls, fp: str):
        """Get file encoding.
        Help to use the correct encoding for pandas reading.
        """
        encoding_dict = {
            'Windows-1254': 'ISO8859-9',
            'ascii': 'ansi',
            'cp936': 'cp936',
            'utf-8': 'utf8',
        }

        with open(fp, 'rb') as f:
            encoding = detect(f.read())['encoding']
        try:
            suggestion = encoding_dict[encoding]
        except KeyError:
            suggestion = None

        return (encoding, suggestion)


#%%
class Converters:
    """Common data converters"""

    @classmethod
    def utc_to_datetime(cls, t: str, format: str = '%Y-%m-%dT%H:%M:%S%z', str_format: Optional[str] = None):
        src_datetime = datetime.strptime(t, format)
        utcoffset = src_datetime.utcoffset()
        if utcoffset is not None:
            dst_datetime = src_datetime - utcoffset
        else:
            dst_datetime = src_datetime
        if str_format is not None:
            if str_format == 'default':
                str_format = '%Y-%m-%d %H:%M:%S'
            dst_datetime = dst_datetime.strftime(str_format)
        return dst_datetime

    @classmethod
    def turn_docstr_dict(cls, refer: Union[str, list, dict], value=None) -> dict:
        """Turn docstr to dict
        Make the docstring-dict like {a.b.c: 1}
            to normal dict like {a: {b: {c: 1}}}
        """
        if type(refer) is dict:
            key_list = list(refer.keys())[0].split('.')
            value = list(refer.values())[0]
        elif type(refer) is list:
            key_list = refer
            value = value
        elif type(refer) is str:
            key_list = refer.split('.')
            value = value
        else:
            key_list = []
        flag = True
        while flag:
            try:
                value = {key_list.pop(): value}
            except IndexError:
                flag = False
        return value  # type: ignore


#%%
class Filters:

    @classmethod
    def rep_emoji(cls, text: str, rep_value: str = ''):
        return re.sub(':\S+?:', rep_value, emoji.demojize(text))


#%%
class DFTools:
    """Pandas DataFrame common tools
    """

    @classmethod
    def cols_lower(cls, df: DataFrame, inplace: bool = False) -> DataFrame:
        """Make DataFrame columns name lower & replace special characters
        """
        new_cols = {col: (re.sub('[^\w]', '_', col.strip()).lower()) for col in df.columns}
        # delete extra underline
        for col in new_cols:
            while new_cols[col][0] == '_':
                new_cols[col] = new_cols[col][1:]
            while new_cols[col][-1] == '_':
                new_cols[col] = new_cols[col][:-1]
        return df.rename(columns=new_cols, inplace=inplace)

    @classmethod
    def drop_unnamed_cols(cls, df: DataFrame, inplace: bool = False) -> DataFrame:
        """Drop Unnamed__XX cols for DF read from read_excel().
        """
        drop_cols = [col for col in df.columns.tolist() if 'unnamed__' in col.lower()]
        logging.debug(f'{drop_cols}')
        return df.drop(columns=drop_cols, inplace=inplace)

    @classmethod
    def get_duplicate_update_sql(cls, df: DataFrame, schema: str, table: str, update_cols: Optional[list] = None):
        """Help to get the 'INSERT ON DUPLICATE KEY UPDATE' sql string.
        """
        # get import cols
        db_import_cols = ', '.join([f'`{col}`' for col in df.columns.tolist()])
        db_import_cols = f'({db_import_cols})'
        # get import datas
        db_import_values = []
        for i in df.index:
            temp_values = ', '.join([f'"{escape_string(str(value))}"' for value in df.loc[i].tolist()])
            temp_values = f'({temp_values})'
            db_import_values.append(temp_values)
        db_import_values = ', '.join(db_import_values)
        # set update cols
        aliased = 'temp'
        if update_cols is None:
            update_cols = df.columns
        db_update_cols = ",".join([f'`{col}` = {aliased}.`{col}`' for col in update_cols])
        # concat SQL
        sql = f"""
        INSERT INTO `{schema}`.`{table}`
        {db_import_cols} VALUES {db_import_values} AS {aliased}
        ON DUPLICATE KEY UPDATE {db_update_cols};
        """
        return sql

    @classmethod
    def to_bool(cls, series: Series, na_value: Union[str, int, bool] = False, to_num: bool = False):
        """Help to turn into [bool] value type.
        """
        series = series.astype('str')
        if na_value in ['0', 0, False]:
            series.fillna('false', inplace=True)
        else:
            series.fillna('true', inplace=True)
        series = series.apply(lambda x: x.lower() if x is not np.nan else x)
        false_value = ['false', 'no', '0']
        series = series.apply(lambda x: False if x in false_value else True)
        if to_num:
            series = series.apply(lambda x: 0 if x is False else 1)
        return series

    @classmethod
    def to_string(cls, series: Series, emoji_value: Optional[str] = None):
        """Help to turn into [string] value type.
        """
        series = series.copy()
        series.fillna('', inplace=True)
        series = series.astype('str')
        series = series.apply(lambda x: x.replace('\n', ' '))
        series = series.apply(lambda x: x[0:-2] if x[-2:] == '.0' else x)
        if emoji_value is not None:
            series = series.apply(lambda x: Filters.rep_emoji(x, emoji_value))
        return series

    @classmethod
    def to_decimal(cls, series: Series, to_str: bool = False):
        """"""
        series = series.copy()
        series.fillna('0.0000', inplace=True)
        series = series.astype('str')
        series = series.apply(lambda x: Decimal(x))
        if to_str:
            series = series.apply(lambda x: str(x))
        return series

    @classmethod
    def to_int(cls, series: Series, na_value: int = 0, to_str: bool = False):
        series = series.copy()
        series.fillna(na_value, inplace=True)
        series = series.astype('str')
        series = series.astype('float64')
        series = series.astype('int64')
        if to_str:
            series = series.apply(lambda x: str(x))
        return series

    @classmethod
    def to_datetime(cls,
                    series: Series,
                    format: str = '%Y-%m-%d %H:%M:%S',
                    to_str: bool = False,
                    auto_fillna: bool = False):
        """Makes the series value into [string like datetime] as arg format
        """
        s = series.copy()
        fillna_dict = {
            '%Y': '1677',
            '%y': '1677',
            '%m': '09',
            '%d': '22',
            '%H': '00',
            '%M': '00',
            '%S': '00',
            '%z': '+00:00'
        }  # The minimum Timestamp support value
        fillna = format
        for old in fillna_dict:
            fillna = fillna.replace(old, fillna_dict[old])
        if auto_fillna:
            s.fillna(fillna, inplace=True)
        if '%z' in format:
            if to_str:
                s = s.apply(lambda x: Converters.utc_to_datetime(x, format, '%Y-%m-%d %H:%M:%S')
                            if not isna(x) else np.nan)
            else:
                s = s.apply(lambda x: Converters.utc_to_datetime(x, format) if not isna(x) else np.nan)
        else:
            if to_str:
                s = s.apply(lambda x: datetime.strptime(x, format).strftime('%Y-%m-%d %H:%M:%S')
                            if not isna(x) else np.nan)
            else:
                s = s.apply(lambda x: datetime.strptime(x, format) if not isna(x) else np.nan)
        return s

    @classmethod
    def enhance_replace(cls, series: Series, dict: dict, regex: bool = False):
        series = series.astype('str')
        for new_value in dict:
            if regex:
                pattern = '|'.join([old_value.lower() for old_value in dict[new_value]])
                series = series.apply(lambda x: new_value if re.search(pattern, x.lower()) is not None else x)
            else:
                series = series.apply(lambda x: new_value if x in dict[new_value] else x)
        return series

    @classmethod
    def str_datetime_cols(cls, df: DataFrame, cols: Union[list, dict]):
        """"""
        df = df.copy()
        for col in cols:
            if type(cols) is dict:
                format = cols[col]
            elif type(cols) is list:
                format = '%Y-%m-%d %H:%M:%S'
            else:
                raise ValueError
            df[col] = cls.to_datetime(series=df[col], format=format, to_str=True, auto_fillna=True)
        return df

    @classmethod
    def str_string_cols(cls, df: DataFrame, cols: list):
        """"""
        df = df.copy()
        for col in cols:
            df[col] = cls.to_string(series=df[col], emoji_value='')  # drop_emoji
        return df

    @classmethod
    def str_bool_cols(cls, df: DataFrame, cols: list):
        """"""
        df = df.copy()
        for col in cols:
            df[col] = cls.to_bool(series=df[col], to_num=True)
        return df

    @classmethod
    def str_decimal_cols(cls, df: DataFrame, cols: list):
        """"""
        df = df.copy()
        for col in cols:
            df[col] = cls.to_decimal(series=df[col], to_str=True)
        return df

    @classmethod
    def str_int_cols(cls, df: DataFrame, cols: list):
        """"""
        df = df.copy()
        for col in cols:
            df[col] = cls.to_int(series=df[col], to_str=True)
        return df

    @classmethod
    def sql_df(
        cls,
        df: DataFrame,
        datetime_cols: Optional[Union[list, dict]] = None,
        bool_cols: Optional[list] = None,
        int_cols: Optional[list] = None,
        decimal_cols: Optional[list] = None,
    ):
        """Help to organise the DF values into suitable SQL import format.
            e.g. datetime-string: 'YYYY-MM-DD HH:MM:SS'
                 decimal-string: '1234.6789'
                 bool-int: 0 | 1
        """
        df = df.copy()
        drop_cols = []
        # datetime
        if datetime_cols is not None:
            df = cls.str_datetime_cols(df, datetime_cols)
            if type(datetime_cols) is list:
                drop_cols = [*drop_cols, *datetime_cols]
            elif type(datetime_cols) is dict:
                drop_cols = [*drop_cols, *datetime_cols.keys()]
        # bool
        if bool_cols is not None:
            df = cls.str_bool_cols(df, bool_cols)
            drop_cols = [*drop_cols, *bool_cols]
        # int
        if int_cols is not None:
            df = cls.str_int_cols(df, int_cols)
            drop_cols = [*drop_cols, *int_cols]
        # decimal
        if decimal_cols is not None:
            df = cls.str_decimal_cols(df, decimal_cols)
            drop_cols = [*drop_cols, *decimal_cols]
        # string
        str_cols = df.columns.tolist()
        if drop_cols is not None:
            for col in drop_cols:
                str_cols.remove(col)
        df = cls.str_string_cols(df, str_cols)
        return df
