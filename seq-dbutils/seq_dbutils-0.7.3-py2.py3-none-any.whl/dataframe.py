import logging
import sys
from datetime import datetime
from os.path import isfile

import pandas as pd

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class DataFrameUtils:

    @staticmethod
    def read_csv_with_header_mapping(csv_filepath, sep=',', col_name_mapping_dict=None):
        if isfile(csv_filepath):
            df = pd.read_csv(csv_filepath, sep=sep, header='infer', low_memory=False)
            logging.info(f'Read file {csv_filepath} with lines: %s', len(df))
            if col_name_mapping_dict:
                df.rename(columns=col_name_mapping_dict, inplace=True)
            return df
        else:
            logging.error(f'File {csv_filepath} does not exist. Exiting...')
            sys.exit(1)

    @staticmethod
    def apply_date_format(input_date, format_date):
        if input_date:
            if input_date == '-':
                input_date = None
            else:
                format_time = format_date + ' %H:%M:%S'
                try:
                    input_date = datetime.strptime(input_date, format_date).date()
                except ValueError as ex:
                    if 'unconverted data remains:' in ex.args[0]:
                        input_date = datetime.strptime(input_date, format_time).date()
                    else:
                        logging.error(str(ex))
                        sys.exit(1)
        else:
            input_date = None
        return input_date

    @staticmethod
    def format_date_cols(df, date_col_list):
        for date_col in date_col_list:
            if date_col in df.columns:
                df[date_col] = df[date_col].apply(
                    lambda x: DataFrameUtils.apply_date_format(str(x), '%Y-%m-%d') if x else None)
        return df

    @staticmethod
    def add_dob_month_col(df, dob_date_col='dob'):
        if 'dob_month' not in list(df):
            df['dob_month'] = df[dob_date_col].apply(lambda x: x.month)
        return df

    @staticmethod
    def add_dob_year_col(df, dob_date_col='dob'):
        if 'dob_year' not in list(df):
            df['dob_year'] = df[dob_date_col].apply(lambda x: x.year)
        return df

    @staticmethod
    def replace_nan_with_none(df):
        df = df.astype(object)
        df = df.where(pd.notnull(df), None)
        return df
