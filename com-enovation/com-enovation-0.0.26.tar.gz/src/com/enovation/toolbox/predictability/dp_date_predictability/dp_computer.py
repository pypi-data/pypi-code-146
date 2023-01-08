from datetime import datetime, timedelta
from inspect import stack
from logging import Logger, getLogger

from enlighten import Manager, Counter
from numpy import where, ndarray, NaN
from pandas import DataFrame, MultiIndex, NaT, Series
from scipy.special import psi

from com.enovation.helper.pandas_dataframe_typer import PandasDataframeTyper
import enlighten

from com.enovation.toolbox.predictability.bean import PredictabilityBean


class DatePredictabilityComputer:
    _logger: Logger = getLogger(__name__)

    # Columns labels for the input file that is expected from the client
    str__input__column_label__key: str = "key"
    str__input__column_label__date: str = "date"
    str__input__column_label__measure: str = "measure"
    lst__input__column_labels: list = [
        str__input__column_label__key,
        str__input__column_label__date,
        str__input__column_label__measure,
    ]

    # Columns labels for the statistics
    str__statistics__column_label__measure_count: str = "measure_count"
    str__statistics__column_label__date_first: str = "date_first"
    str__statistics__column_label__date_last: str = "date_last"
    str__statistics__column_label__measure_first: str = "measure_first"
    str__statistics__column_label__measure_last: str = "measure_last"
    str__statistics__column_label__measure_min: str = "measure_min"
    str__statistics__column_label__measure_max: str = "measure_max"
    str__statistics__column_label__predictability_last: str = "predictability_last"

    lst__output__statistics_by_key__column_labels: list = [
        str__input__column_label__key,
        str__statistics__column_label__measure_count,
        str__statistics__column_label__date_first,
        str__statistics__column_label__date_last,
        str__statistics__column_label__measure_first,
        str__statistics__column_label__measure_last,
        str__statistics__column_label__measure_min,
        str__statistics__column_label__measure_max,
        str__statistics__column_label__predictability_last
    ]

    # Columns labels for working columns
    str__output__column_label__predictability: str = "predictability"
    str__output__column_label__duration: str = "duration"

    # Default resampling frequency: 1D
    _str__default_resampling_rule: str = "1D"

    def compute_historical_date_predictability(
            self,
            df_measures: DataFrame,
            b_resample: bool = True,
            int_sliding_window: int = None
    ) -> PredictabilityBean:
        """
        Function to compute date predictability for a set of measures provided as parameter.

        The parameter df_measures should comply to the below:
        - Instance of pandas.DataFrame
        - BR_Structure_001: the measures do not have multiindex index
        - BR_Structure_002: the measures do not have multiindex columns
        - BR_Structure_003: the measures contains exactly 3 columns:
            - str__input__column_label__key: str = "key"
            - str__input__column_label__date: str = "date"
            - str__input__column_label__measure: str = "measure"
        - BR_Data_001: at least 1 record is required in order to compute a predictability
        - BR_Data_002: there should not be any null value in the dataframe
        - BR_Data_003: both columns "date" and "measure" should be dates, or objects that can be typed to dates
        - BR_Data_004: there should not be any line with duplicated "date"

        Depending on the parameter b_resample, the logic differs:
        - If b_resample == True (default):
            - The logic takes more time, but enable to graph precisely the historical trend of the date_predictability
            - The measures are resampled daily. Illustration:
                - For an input dataframe that contains 2 rows, measure 'x' for date '1-Jan' and measure 'y' for date
                  '3-Jan'
                - We resample daily, leading to dataframe that contains 3 rows, measure 'x' for dates '1-Jan' and
                  '2-Jan' and measure 'y' for date '3-Jan'
            - The date predictability is then computed as
                - SUM for_each_measure(spot_predictability)
                - With spot_predictability =
                    - 0 if measure beyond the convergence_cone
                    - otherwise (measure - last_measure)/convergence_cone
                - With convergence_cone defined by:
                    - Upper limit: date + abs(date - last_measure)
                    - Lower limit: date - abs(date - last_measure)
        - If b_resample == False:
            - The logic is more optimal than when sampling, but graphing the historical trend of the
              date_predictability is far less meaningful, and even misleading
            - The date predictability is computed as:
                - For each measure that spans from its date until the next one, we compute date_predictability as
                    - SUM for_each_day (spot_predictabilty) with spot_predictability as defined above

        Regarding parameter int_sliding_window:
        - It can only be provided when b_resample is equal to True, or an exception is thrown
        - It set the length in days of the sliding window that filters historical measures: only measures within
          this sliding window are considered, the older ones are ignored
        - By default, all historical measures are considered, even the oldest ones

        :param df_measures: a dataframe that contains the measures
        :param b_resample: whether or not we want to resample daily the measures, for later graphing
        :return: the date predictability for the measures provided as a parameter
        """
        self._logger.debug(
            f"Function '{stack()[0].filename} - {stack()[0].function}' is called with parameters:"
            f"\n\t- df_measures: '{df_measures.shape}'"
        )

        # 1. We check structure
        self._check_structure(
            df_measures=df_measures,
            lst_column_labels=self.lst__input__column_labels,
        )
        self._logger.info(f"Function '{stack()[0].filename} - {stack()[0].function}': structure checked.")

        # 2. We check and type the data
        the_df_typed = self._check_and_cleanse_data(
            df_measures=df_measures.copy(),
            str_column_label_key=self.str__input__column_label__key,
            str_column_label_date=self.str__input__column_label__date,
            str_column_label_measure=self.str__input__column_label__measure,
        )

        # 2b. We check if a sliding window is set, that b_sample is true
        if (
            (int_sliding_window is not None)
            & (b_resample is False)
        ):
            raise Exception(f"Function '{stack()[0].filename} - {stack()[0].function}' is not properly called: "
                            f"parameter int_sliding_window is not null, equalt to '{int_sliding_window}', while"
                            f"parameter b_sample is '{b_resample}'.")

        # 3. Depending on whether or not we need to resample, we call the function to compute historical predictability
        if b_resample:
            df_the_historical_predictability: DataFrame = self._resample_and_compute_historical_date_predictability(
                df_measures=the_df_typed.copy(),
                str_column_label_key=self.str__input__column_label__key,
                str_column_label_date=self.str__input__column_label__date,
                str_column_label__measure=self.str__input__column_label__measure,
                str_column_label__predictability=self.str__output__column_label__predictability,
                str_resample_rule=self._str__default_resampling_rule,
                int_sliding_window=int_sliding_window
            )
        else:
            df_the_historical_predictability: DataFrame = \
                self._compute_historical_date_predictability_without_resampling(
                    df_measures=the_df_typed.copy(),
                    str_column_label__key=self.str__input__column_label__key,
                    str_column_label__date=self.str__input__column_label__date,
                    str_column_label__measure=self.str__input__column_label__measure,
                    str_column_label__duration=self.str__output__column_label__duration,
                    str_column_label__predictability=self.str__output__column_label__predictability,
                )

        # 4. We compute the statistics
        df_the_statistics_by_key: DataFrame = self.compute_statistics_by_key(
            df_measures=the_df_typed.copy(),
            df_historical_predictability=df_the_historical_predictability,
            str_column_label__key=self.str__input__column_label__key,
            str_column_label__date=self.str__input__column_label__date,
            str_column_label__measure=self.str__input__column_label__measure,
            str_column_label__predictability=self.str__output__column_label__predictability,
            str_column_label__measure_count=self.str__statistics__column_label__measure_count,
            str_column_label__date_first=self.str__statistics__column_label__date_first,
            str_column_label__date_last=self.str__statistics__column_label__date_last,
            str_column_label__measure_first=self.str__statistics__column_label__measure_first,
            str_column_label__measure_last=self.str__statistics__column_label__measure_last,
            str_column_label__measure_min=self.str__statistics__column_label__measure_min,
            str_column_label__measure_max=self.str__statistics__column_label__measure_max,
            str_column_label__predictability_last=self.str__statistics__column_label__predictability_last
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

        return PredictabilityBean(
            df_historical=df_the_historical_predictability,
            df_by_measure=df_measures,
            df_by_key=df_the_statistics_by_key,
        )

    def _check_structure(
            self,
            df_measures: DataFrame,
            lst_column_labels: list = None,
    ):
        """
        The measures provided by the client should comply to the following business rules:
            - BR_Structure_001: the measures do not have multiindex index
            - BR_Structure_002: the measures do not have multiindex columns
            - BR_Structure_003: the measures contains exactly 3 columns:
                - str__input__column_label__key: str = "key"
                - str__input__column_label__date: str = "date"
                - str__input__column_label__measure: str = "measure"

        The function:
            - Returns quietly in case the measures comply to these business rules
            - Or raises an alert in case the client's measures do not comply to any of these business rules.

        :param df_measures: the client's measures
        :param lst_column_labels: the expected columns labels
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        if lst_column_labels is None:
            lst_column_labels = self.lst__input__column_labels

        # BR_Structure_001: the measures do not have multiindex index
        if isinstance(df_measures.index, MultiIndex):
            raise Exception(f"BR_Structure_001 - Provided measures have a multiindex index, which is not expected. "
                            f"Flatten the index, and retry. Multiindex names: "
                            f"'{', '.join(df_measures.index.names)}'.")

        # BR_Structure_002: the measures do not have multiindex columns
        if isinstance(df_measures.columns, MultiIndex):
            raise Exception(f"BR_Structure_002 - Provided measures have multiindexed columns, which is not expected. "
                            f"Flatten the columns, and retry. Multiindex names: "
                            f"'{', '.join(df_measures.columns.names)}'.")

        # BR_Structure_003: the measures contains exactly 3 columns, aka "key", "date" and "measure"
        lst_the_missing_columns_in_df: list = list(
            set(lst_column_labels)
            - set(df_measures.columns)
        )
        if len(lst_the_missing_columns_in_df) > 0:
            raise Exception(f"BR_Structure_003 - Provided measures are missing the following mandatory columns: "
                            f"'{', '.join(lst_the_missing_columns_in_df)}'. Review your data, and retry.")
        lst_the_extra_columns_in_df: list = list(
            set(df_measures.columns)
            - set(lst_column_labels)
        )
        if len(lst_the_extra_columns_in_df) > 0:
            raise Exception(f"BR_Structure_003 - Provided measures contains extra unexpected columns: "
                            f"'{', '.join(lst_the_missing_columns_in_df)}'. Review your data, and retry.")

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

    def _check_and_cleanse_data(
            self,
            df_measures: DataFrame,
            str_column_label_key: str = str__input__column_label__key,
            str_column_label_date: str = str__input__column_label__date,
            str_column_label_measure: str = str__input__column_label__measure,
    ) -> DataFrame:
        """
        The measures provided by the client should comply to the following business rules:
            - BR_Data_001: at least 1 record is required in order to compute a predictability
            - BR_Data_002: there should not be any null value in the dataframe
            - BR_Data_003: both columns "date" and "measure" should be dates, or objects that can be typed to dates
            - BR_Data_004: there should not be any line with duplicated "date"

        Cleansing logic:
            - LOG_Data_001: Columns "date" and "measure" are typed into dates
            - LOG_Data_002: Remove useless measures, aka same measure duplicated across dates

        The function:
            - Returns quietly in case the client's measures comply to these business rules
            - Or raises an alert in case the client's measures do not comply to any of these business rules.

        :param df_measures: the client's measures
        :param str_column_label_date: the label of the column that bears the dates for the measures
        :param str_column_label_measure: the label of the column that bears the measures
        :return: the typed client's measures
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        # BR_Data_001. At least one record
        if len(df_measures.index) == 0:
            raise Exception(f"BR_Data_001 - The parameter df_measures contains '0' records, while it should contain at "
                            f"least '1'.")

        # BR_Data_002. No null value
        if df_measures.isnull().values.any():
            raise Exception(f"BR_Data_002 - The parameter df_measures contains '"
                            f"{df_measures.isnull().values.sum()}' null values, which is not expected. Make "
                            f"sure you call the function with a dataframe df_measures which does not contain any null "
                            f"value.")

        # BR_Data_003. We retype both columns "date" and "measure" into datetime:
        # LOG_Data_001: Columns "date" and "measure" are typed into dates
        try:
            df_the_return: DataFrame = PandasDataframeTyper.type(
                df_to_type=df_measures,
                dict_columns_to_type={
                    str_column_label_date: "date",
                    str_column_label_measure: "date"
                },
                b_strict=False
            )
        except Exception as an_exception:
            raise Exception(
                f"BR_Data_003 - An exception occurred while typing columns '{str_column_label_date}' and "
                f"'{str_column_label_measure}' to dates. Check the data, and retry.") from an_exception

        # BR_Data_004. duplicated records for a given "date" (excluding the "measure" column)
        df_the_working_df: DataFrame = df_measures.drop(columns=[str_column_label_measure])
        df_the_working_df = df_the_working_df[df_the_working_df.duplicated()]
        if len(df_the_working_df.index) > 0:
            the_unique_duplicated_records: DataFrame = df_the_working_df.drop_duplicates()
            the_msg: str = f"BR_Data_004 - The parameter df_measures contains '{len(df_the_working_df.index)}' " \
                           f"records duplicated, which is not expected. Make sure your remove all duplicates for " \
                           f"values:\n\n{the_unique_duplicated_records.to_string()}\n\n"
            raise Exception(the_msg)

        # LOG_Data_002: Remove useless measures, aka same measure duplicated across dates
        df_the_return = df_the_return.sort_values(
            by=[
                str_column_label_key,
                str_column_label_date
            ]
        ).reset_index(drop=True)
        df_the_return["tmp_" + str_column_label_key] = df_the_return[str_column_label_key].shift(1)
        df_the_return["tmp_" + str_column_label_measure] = df_the_return[str_column_label_measure].shift(1)

        # We override the very last measure for each key, not to drop it in case it is similar to previous one
        # df_the_return = df_the_return.loc[-1, "tmp_"+str_column_label_key] = NaN
        # df_the_return.loc[-1, "tmp_"+str_column_label_measure] = NaT
        df_the_return.loc[
            df_the_return.groupby(str_column_label_key).tail(1).index,
            ["tmp_" + str_column_label_key, "tmp_" + str_column_label_measure]
        ] = [NaN, NaT]

        df_the_return = df_the_return[
            (df_the_return[str_column_label_key] != df_the_return["tmp_" + str_column_label_key])
            | (df_the_return[str_column_label_measure] != df_the_return["tmp_" + str_column_label_measure])
            ]
        df_the_return = df_the_return.drop(columns=[
            "tmp_" + str_column_label_key,
            "tmp_" + str_column_label_measure
        ])

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        return df_the_return

    def _resample_and_compute_historical_date_predictability(
            self,
            df_measures: DataFrame,
            str_column_label_key: str = str__input__column_label__key,
            str_column_label_date: str = str__input__column_label__date,
            str_column_label__measure: str = str__input__column_label__measure,
            str_column_label__predictability: str = str__output__column_label__predictability,
            str_resample_rule: str = _str__default_resampling_rule,
            int_sliding_window: int = None
    ) -> DataFrame:

        # 1. We resample
        the_df_resampled: DataFrame = self._resample_measures(
            df_measures=df_measures,
            str_column_label_key=str_column_label_key,
            str_column_label_date=str_column_label_date,
            str_resample_rule=str_resample_rule,
        )
        self._logger.info(f"Function '{stack()[0].filename} - {stack()[0].function}': measures resampled.")

        # 2. We compute historical predictability
        the_df_historical_predictability: DataFrame = \
            self._compute_historical_date_predictability_for_resampled_measures(
                df_measures=the_df_resampled,
                str_column_label__key=str_column_label_key,
                str_column_label__date=str_column_label_date,
                str_column_label__measure=str_column_label__measure,
                str_column_label__predictability=str_column_label__predictability,
                int_sliding_window=int_sliding_window
            )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

        return the_df_historical_predictability

    def _resample_measures(
            self,
            df_measures: DataFrame,
            str_column_label_key: str = str__input__column_label__key,
            str_column_label_date: str = str__input__column_label__date,
            str_resample_rule: str = _str__default_resampling_rule,
    ) -> DataFrame:

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        df_measures = df_measures \
            .set_index(str_column_label_date) \
            .groupby(str_column_label_key) \
            .resample(str_resample_rule) \
            .ffill() \
            .reset_index(level=str_column_label_date) \
            .reset_index(drop=True)

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

        return df_measures

    def _compute_historical_date_predictability_for_resampled_measures(
            self,
            df_measures: DataFrame,
            str_column_label__key: str = str__input__column_label__key,
            str_column_label__date: str = str__input__column_label__date,
            str_column_label__measure: str = str__input__column_label__measure,
            str_column_label__predictability: str = str__output__column_label__predictability,
            int_sliding_window: int = None
    ) -> DataFrame:
        """
        A function to compute a date predictability across history.

        :param df_measures: measures for a given key
        :param int_sliding_window: the length in days of the sliding window to compute predictability. Old measures
          that falls outside this sliding window are ignored. By default, this filter is ignored, and all
          historical data, ever the oldest ones, are considered.
        :return: the historical predictability that would have been computed as of the last date.
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        df_measures[str_column_label__predictability] = -1

        # Setup progress bar
        obj_the_mgr: Manager = enlighten.get_manager()
        obj_the_counter: Counter = obj_the_mgr.counter(
            total=len(df_measures.index),
            desc='Progress:',
            unit='measures'
        )

        # For each line in the dataframe
        for t_i_row in df_measures.itertuples():
            # We compute the predictability:
            # - For the given key
            # - For all the previous records at the date

            # We filter the past measures for a given key
            df_the_filtered_measures: DataFrame = df_measures[
                (df_measures[str_column_label__key] == getattr(t_i_row, str_column_label__key))
                & (df_measures[str_column_label__date] <= getattr(t_i_row, str_column_label__date))
            ]

            # If the sliding window is defined
            if int_sliding_window is not None:
                df_the_filtered_measures = df_the_filtered_measures[
                    df_measures[str_column_label__date] >= (
                        getattr(t_i_row, str_column_label__date) -
                        timedelta(days=int_sliding_window)
                    )
                ]

            # Eventually, we call the function to compute the data predictability for the key and date
            f_i_predictability = self._compute_date_predictability_for_a_given_key_and_resampled_measures(
                df_measures=df_the_filtered_measures,
                str_column_label__date=str_column_label__date,
                str_column_label__measure=str_column_label__measure,
            )

            # We update the measures with these historical predictabilities
            df_measures.loc[getattr(t_i_row, 'Index'), str_column_label__predictability] = f_i_predictability

            # We update the progress bar
            obj_the_counter.update()

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

        return df_measures

    def _compute_date_predictability_for_a_given_key_and_resampled_measures(
            self,
            df_measures: DataFrame,
            str_column_label__date: str = str__input__column_label__date,
            str_column_label__measure: str = str__input__column_label__measure
    ) -> float:
        # Too many logs:
        # self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        dt_the_last_date: datetime = df_measures[self.str__input__column_label__date].max()

        dt_the_last_measure: datetime = \
            df_measures[
                df_measures[self.str__input__column_label__date] == dt_the_last_date
                ][
                self.str__input__column_label__measure
            ].iloc[0]

        a_measures_predictabilities: ndarray = where(

            # If date is at last measure
            df_measures[str_column_label__date] == dt_the_last_measure,

            where(

                # If measure is spot on
                df_measures[str_column_label__measure] == dt_the_last_measure,
                1,
                0
            ),

            where(

                # If outside the cone
                abs((df_measures[str_column_label__measure] - dt_the_last_measure).dt.days)
                >= abs((df_measures[str_column_label__date] - dt_the_last_measure).dt.days),
                0,
                1
                - abs((df_measures[str_column_label__measure] - dt_the_last_measure).dt.days)
                / abs((df_measures[str_column_label__date] - dt_the_last_measure).dt.days)
            )
        )

        # The last measure should not contribute to the aggregated predictability
        # Therefore, we remove the last record from the ndarray (only if more than 1 records)
        if len(a_measures_predictabilities) > 1:
            a_measures_predictabilities = a_measures_predictabilities[:-1]

        # Eventually, we compute the aggregated predictability
        f_the_return: float = \
            a_measures_predictabilities.sum() \
            / len(a_measures_predictabilities)

        # Too many logs:
        # self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

        return f_the_return

    def _compute_historical_date_predictability_without_resampling(
            self,
            df_measures: DataFrame,
            str_column_label__key: str = str__input__column_label__key,
            str_column_label__date: str = str__input__column_label__date,
            str_column_label__measure: str = str__input__column_label__measure,
            str_column_label__predictability: str = str__output__column_label__predictability,
            str_column_label__duration: str = str__output__column_label__duration,
    ) -> DataFrame:
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        the_df_enriched_measures: DataFrame = df_measures

        # Setup progress bar
        obj_the_mgr: Manager = enlighten.get_manager()
        obj_the_counter: Counter = obj_the_mgr.counter(
            total=len(df_measures.index),
            desc='Progress:',
            unit='measures'
        )

        # We instantiate the column to bear the predictability
        the_df_enriched_measures[str_column_label__predictability] = -1

        # For each line in the dataframe
        for t_i_row in df_measures.itertuples():
            # We compute the predictability:
            # - For the given key
            # - For all the previous records at the date
            f_i_predictability = self._compute_date_predictability_for_a_given_key_not_resampled(
                df_measures=the_df_enriched_measures[
                    (the_df_enriched_measures[str_column_label__key] == getattr(t_i_row, str_column_label__key))
                    & (the_df_enriched_measures[str_column_label__date] <= getattr(t_i_row, str_column_label__date))
                    ],
                str_column_label__date=str_column_label__date,
                str_column_label__measure=str_column_label__measure,
                str_column_label__duration=str_column_label__duration,
            )

            # We update the measures with these historical predictabilities
            df_measures.loc[getattr(t_i_row, 'Index'), str_column_label__predictability] = f_i_predictability

            # We update the progress bar
            obj_the_counter.update()

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

        return df_measures

    def _compute_date_predictability_for_a_given_key_not_resampled(
            self,
            df_measures: DataFrame,
            str_column_label__date: str = str__input__column_label__date,
            str_column_label__measure: str = str__input__column_label__measure,
            str_column_label__duration: str = str__output__column_label__duration,
    ) -> float:
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        the_df_enriched_measures: DataFrame = df_measures.copy()

        # We duplicate column "date", that we shift by one
        # Assumption: values already sorted in function _check_and_cleanse_data
        the_df_enriched_measures["date_end"] = the_df_enriched_measures[str_column_label__date].shift(-1)
        the_df_enriched_measures.loc[the_df_enriched_measures.index[-1], "date_end"] = \
            the_df_enriched_measures.loc[the_df_enriched_measures.index[-1],
                                         DatePredictabilityComputer.str__input__column_label__date]

        # We compute the duration for each measure
        the_df_enriched_measures[str_column_label__duration] = (
                the_df_enriched_measures["date_end"] - the_df_enriched_measures[str_column_label__date]).dt.days

        dt_the_last_date: datetime = df_measures[self.str__input__column_label__date].max()
        dt_the_last_measure: datetime = df_measures[
            df_measures[self.str__input__column_label__date] == dt_the_last_date
            ][
            self.str__input__column_label__measure
        ].iloc[0]

        def compute_magic_number(s_row: Series) -> float:
            dt_the_date_start: datetime = s_row[str_column_label__date]
            dt_the_date_end: datetime = s_row["date_end"]
            dt_the_measure: datetime = s_row[str_column_label__measure]
            int_the_duration: int = s_row[str_column_label__duration]

            # For the very last measure, the closing one,
            if int_the_duration == 0:
                return 0.0

            # If we are spot on
            if dt_the_measure == dt_the_last_measure:
                return int_the_duration

            # If date_start is before last measure, and within convergence cone
            if (dt_the_date_start < dt_the_last_measure) & (
                    abs((dt_the_measure - dt_the_last_measure).days)
                    < abs((dt_the_last_measure - dt_the_date_start).days)
            ):
                dt_the_effective_date_end: datetime = min(
                    dt_the_date_end,
                    dt_the_last_measure-timedelta(days=abs((dt_the_measure - dt_the_last_measure).days))
                )
                # int_the_cone_start: int = abs((dt_the_last_measure-dt_the_date_start).days)
                int_the_cone_effective_end: int = abs((dt_the_last_measure-dt_the_effective_date_end).days)+1

                # We prepare the operands
                int_b: int = int_the_cone_effective_end
                int_a: int = int_the_cone_effective_end - abs((dt_the_last_measure-dt_the_measure).days)
                int_m: int = (dt_the_effective_date_end-dt_the_date_start).days

                f_the_predictability: float = ((int_b-int_a)*(psi(int_b)-psi(int_b+int_m))+int_m)
            else:
                f_the_predictability: float = 0

            # If date_end is after last measure, and within convergence cone
            if (dt_the_date_end > dt_the_last_measure) & (
                    abs((dt_the_measure - dt_the_last_measure).days)
                    < abs((dt_the_last_measure - dt_the_date_end).days)
            ):
                dt_the_effective_date_start: datetime = max(
                    dt_the_date_start,
                    dt_the_last_measure+timedelta(days=abs((dt_the_measure - dt_the_last_measure).days))
                )
                # int_the_cone_end: int = abs((dt_the_last_measure-dt_the_date_end).days)-1
                int_the_cone_effective_start: int = abs((dt_the_last_measure-dt_the_effective_date_start).days)

                # We prepare the operands
                int_b: int = int_the_cone_effective_start
                int_a: int = int_the_cone_effective_start - abs((dt_the_last_measure-dt_the_measure).days)
                int_m: int = (dt_the_date_end-dt_the_effective_date_start).days

                f_the_predictability += ((int_b-int_a)*(psi(int_b)-psi(int_b+int_m))+int_m)
            else:
                pass

            return f_the_predictability

        if len(df_measures.index) == 1:
            f_the_return: float = 1.0

        else:
            the_s_historical_predictability: Series = the_df_enriched_measures.apply(compute_magic_number, axis=1)

            # Eventually, we compute the aggregated predictability
            f_the_return: float = \
                the_s_historical_predictability.sum() / \
                the_df_enriched_measures[str_column_label__duration].sum()

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

        return f_the_return

    def compute_statistics_by_key(
            self,
            df_measures: DataFrame,
            df_historical_predictability: DataFrame,

            str_column_label__key: str = str__input__column_label__key,
            str_column_label__date: str = str__input__column_label__date,
            str_column_label__measure: str = str__input__column_label__measure,

            str_column_label__predictability: str = str__output__column_label__predictability,

            str_column_label__measure_count: str = str__statistics__column_label__measure_count,
            str_column_label__date_first: str = str__statistics__column_label__date_first,
            str_column_label__date_last: str = str__statistics__column_label__date_last,
            str_column_label__measure_first: str = str__statistics__column_label__measure_first,
            str_column_label__measure_last: str = str__statistics__column_label__measure_last,
            str_column_label__measure_min: str = str__statistics__column_label__measure_min,
            str_column_label__measure_max: str = str__statistics__column_label__measure_max,
            str_column_label__predictability_last: str = str__statistics__column_label__predictability_last
    ) -> DataFrame:
        """
        todo.

        :param str_column_label__predictability_last:
        :param str_column_label__measure_max:
        :param str_column_label__measure_min:
        :param str_column_label__measure_last:
        :param str_column_label__measure_first:
        :param str_column_label__date_last:
        :param str_column_label__date_first:
        :param str_column_label__measure_count:
        :param str_column_label__predictability:
        :param str_column_label__measure:
        :param str_column_label__date:
        :param str_column_label__key:
        :param df_measures:
        :param df_historical_predictability: measures for a given key
        :return: the historical predictability that would have been computed as of the last date.
        """

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        # 1. We compute global statistics for each predictability.V2.V2 key:
        #       - date_first
        #       - date_last
        #       - measure_min
        #       - measure_max
        df_the_stats_by_key: DataFrame = df_measures.groupby(str_column_label__key).agg({
            str_column_label__key: "count",
            str_column_label__date: ["min", "max"],
            str_column_label__measure: ["min", "max"],
        }).reset_index()
        df_the_stats_by_key.columns = [
            str_column_label__key,
            str_column_label__measure_count,
            str_column_label__date_first,
            str_column_label__date_last,
            # str_column_label__measure_first,
            # str_column_label__measure_last,
            str_column_label__measure_min,
            str_column_label__measure_max,
            # str__output__column_label__predictability
        ]

        # 2. We compute the 2 residual statistics from the measures depending on date first and last:
        #    - measure_first
        #    - measure_last
        df_the_stats_by_key = df_the_stats_by_key.merge(
            right=df_measures.rename(columns={
                str_column_label__date: str_column_label__date_first,
                str_column_label__measure: str_column_label__measure_first
            }),
            on=[str_column_label__key, str_column_label__date_first],
            how="left"
        )
        df_the_stats_by_key = df_the_stats_by_key.merge(
            right=df_measures.rename(columns={
                str_column_label__date: str_column_label__date_last,
                str_column_label__measure: str_column_label__measure_last
            }),
            on=[str_column_label__key, str_column_label__date_last],
            how="left"
        )

        # 3. We compute the statistic based on the historical predictabilities
        #    - predictability_last
        df_the_stats_by_key = df_the_stats_by_key.merge(
            right=df_historical_predictability[[
                str_column_label__key,
                str_column_label__date,
                str_column_label__predictability,
            ]].rename(columns={
                str_column_label__date: str_column_label__date_last,
                str_column_label__predictability: str_column_label__predictability_last
            }),
            on=[str_column_label__key, str_column_label__date_last],
            how="left"
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

        return df_the_stats_by_key
