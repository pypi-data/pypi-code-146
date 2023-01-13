import pandas as pd


class TimeHandler:
    def __init__(self):
        pass

    def convert_utc_cet(self, datetime_obj):
        """_summary_
        Converts datetime-like Series from UTC to CET.

        Args:
            datetime_obj (pd Series object): datetime-like pd Series
        """
        datetime_utc = pd.to_datetime(datetime_obj, utc=True)
        datetime_cet = datetime_utc.tz_convert(tz="Europe/Berlin")
        return datetime_cet

    def apply_date_interval(self, df, interval_first_day=None, interval_next_day=None):
        """_summary_ Apply date interval

        Args:
            df (pd DataFrame):
                dataframe to apply filter to, with datetime-index
            INTERVAL_FIRST_DAY (datetime object with tzinfo):
                first day of interval
            INTERVAL_NEXT_DAY (datetime object with tzinfo):
                first day after interval

        Returns:
            pd DataFrame: data of last 6 months
        """
        after_interval_first_day = df.index.date >= interval_first_day
        before_last_month_last_day = df.index.date < interval_next_day
        between_dates = after_interval_first_day & before_last_month_last_day
        return df[between_dates]
