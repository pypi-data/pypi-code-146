from inspect import stack
from logging import Logger, getLogger
from datetime import timedelta, datetime

from pandas import Series, DataFrame

from com.enovation.toolbox.predictability.bean import PredictabilityBean
from com.enovation.toolbox.predictability.dp_date_predictability.dp_computer import DatePredictabilityComputer


class DataToGraph:
    _str_figure_title: str
    _str_abscissa_label: str

    _str_predictabilities_ordinate_label: str  # the label for the ordinate axis
    _s_predictabilities_values: Series  # the ordinate predictability values to print in the graph
    _s_predictabilities_dates: Series  # the abscissa dates to print in the graph
    _str_predictabilities_name: str  # the trace name, displayed in the legend

    _str_measures_ordinate_label: str  # the label for the ordinate axis
    _s_measures_values: Series  # the ordinate measure values to print in the graph
    _s_measures_dates: Series  # the abscissa dates to print in the graph
    _str_measures_name: str  # the trace name, displayed in the legend

    # the cone in the measure widget
    _lst_increasing_cone_values: list[datetime]
    _lst_increasing_cone_dates: list[datetime]
    _str_increasing_cone_name: str
    _lst_decreasing_cone_values: list[datetime]
    _lst_decreasing_cone_dates: list[datetime]
    _str_decreasing_cone_name: str
    _lst_last_measure_values: list[datetime]
    _lst_last_measure_dates: list[datetime]
    _str_last_measure_name: str

    @property
    def str_figure_title(self) -> str:
        return self._str_figure_title

    @property
    def str_abscissa_label(self) -> str:
        return self._str_abscissa_label

    @property
    def str_predictabilities_ordinate_label(self) -> str:
        return self._str_predictabilities_ordinate_label

    @property
    def s_predictabilities_values(self) -> Series:
        return self._s_predictabilities_values

    @property
    def s_predictabilities_dates(self) -> Series:
        return self._s_predictabilities_dates

    @property
    def str_predictabilities_name(self) -> str:
        return self._str_predictabilities_name

    @property
    def str_measures_ordinate_label(self) -> str:
        return self._str_measures_ordinate_label

    @property
    def s_measures_values(self) -> Series:
        return self._s_measures_values

    @property
    def s_measures_dates(self) -> Series:
        return self._s_measures_dates

    @property
    def str_measures_name(self) -> str:
        return self._str_measures_name

    @property
    def lst_increasing_cone_values(self) -> list[datetime]:
        return self._lst_increasing_cone_values

    @property
    def lst_increasing_cone_dates(self) -> list[datetime]:
        return self._lst_increasing_cone_dates

    @property
    def str_increasing_cone_name(self) -> str:
        return self._str_increasing_cone_name

    @property
    def lst_decreasing_cone_values(self) -> list[datetime]:
        return self._lst_decreasing_cone_values

    @property
    def lst_decreasing_cone_dates(self) -> list[datetime]:
        return self._lst_decreasing_cone_dates

    @property
    def str_decreasing_cone_name(self) -> str:
        return self._str_decreasing_cone_name

    @property
    def lst_last_measure_values(self) -> list[datetime]:
        return self._lst_last_measure_values

    @property
    def lst_last_measure_dates(self) -> list[datetime]:
        return self._lst_last_measure_dates

    @property
    def str_last_measure_name(self) -> str:
        return self._str_last_measure_name

    _logger: Logger = getLogger(__name__)

    def _compute_cones_coordinates(
            self,
            df_the_historical_data: DataFrame
    ) -> tuple[
        list[datetime],  # _lst_increasing_cone_values
        list[datetime],  # _lst_increasing_cone_dates
        list[datetime],  # _lst_decreasing_cone_values
        list[datetime],  # _lst_decreasing_cone_dates
        list[datetime],  # _lst_last_measure_values
        list[datetime]   # _lst_last_measure_dates
    ]:
        """
        From a given historical dataframe, the function returns the following variables:
        - _lst_increasing_cone_values
        - _lst_increasing_cone_dates
        - _lst_decreasing_cone_values
        - _lst_decreasing_cone_dates
        - _lst_last_measure_values
        - _lst_last_measure_dates
        """

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        df_the_stats: DataFrame = DatePredictabilityComputer().compute_statistics_by_key(
            df_measures=df_the_historical_data,
            df_historical_predictability=df_the_historical_data,
        )

        if len(df_the_stats.index) != 1:
            raise Exception(f"The function DatePredictabilityComputer.compute_statistics_by_key returned "
                            f"'{len(df_the_stats.index)}' rows, while '1' one expected.")

        # We retrieve the stats as a directory
        d_the_stats: dict = df_the_stats.iloc[0, :].to_dict()

        dt_the_bottom_left_corner: datetime = min(
            d_the_stats[DatePredictabilityComputer.str__statistics__column_label__measure_last],
            d_the_stats[DatePredictabilityComputer.str__statistics__column_label__date_first]
        )
        dt_the_top_right_corner: datetime = max(
            d_the_stats[DatePredictabilityComputer.str__statistics__column_label__measure_last],
            d_the_stats[DatePredictabilityComputer.str__statistics__column_label__date_last]
        )
        dt_the_top_left_corner: datetime = max(
            d_the_stats[DatePredictabilityComputer.str__statistics__column_label__measure_last],
            d_the_stats[DatePredictabilityComputer.str__statistics__column_label__measure_last]
            + timedelta(
                days=(
                        d_the_stats[
                            DatePredictabilityComputer.str__statistics__column_label__measure_last]
                        - d_the_stats[
                            DatePredictabilityComputer.str__statistics__column_label__date_first]
                ).days
            )
        )
        dt_the_bottom_right_corner: datetime = min(
            d_the_stats[DatePredictabilityComputer.str__statistics__column_label__measure_last],
            d_the_stats[DatePredictabilityComputer.str__statistics__column_label__measure_last]
            - timedelta(
                days=(
                        d_the_stats[
                            DatePredictabilityComputer.str__statistics__column_label__date_last]
                        - d_the_stats[
                            DatePredictabilityComputer.str__statistics__column_label__measure_last]
                ).days
            )
        )

        lst_the_increasing_cone_values: list[datetime] = [dt_the_bottom_left_corner, dt_the_top_right_corner]
        lst_the_increasing_cone_dates: list[datetime] = [dt_the_bottom_left_corner, dt_the_top_right_corner]

        lst_the_decreasing_cone_values: list[datetime] = [dt_the_top_left_corner, dt_the_bottom_right_corner]
        lst_the_decreasing_cone_dates: list[datetime] = [dt_the_bottom_left_corner, dt_the_top_right_corner]

        lst_the_last_measure_values: list[datetime] = \
            [d_the_stats[DatePredictabilityComputer.str__statistics__column_label__measure_last]]*2
        lst_the_last_measure_dates: list[datetime] = [dt_the_bottom_left_corner, dt_the_top_right_corner]

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

        return \
            lst_the_increasing_cone_values, lst_the_increasing_cone_dates, \
            lst_the_decreasing_cone_values, lst_the_decreasing_cone_dates, \
            lst_the_last_measure_values, lst_the_last_measure_dates

    def __init__(
            self,
            obj_predictability: PredictabilityBean,
            str_filter_on_key: str,
            dt_as_of_date: datetime = None
    ):
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        # We set the figures titles and labels
        self._str_figure_title = f"Date Predictability for <b>{str_filter_on_key}</b>"
        self._str_abscissa_label = DatePredictabilityComputer.str__input__column_label__date
        self._str_predictabilities_ordinate_label = DatePredictabilityComputer.str__output__column_label__predictability
        self._str_measures_ordinate_label = DatePredictabilityComputer.str__input__column_label__measure

        # We select the data for that selected key
        df_the_historical_data: DataFrame = obj_predictability.df_historical[
            obj_predictability.df_historical[
                DatePredictabilityComputer.str__input__column_label__key
            ] == str_filter_on_key
        ]

        # If we do not zoom on a given date, we set it to the maximum (as later filter will always consider this date)
        if dt_as_of_date is None:
            dt_as_of_date = df_the_historical_data[DatePredictabilityComputer.str__input__column_label__date].max()

        # We prepare the data for the historical evolution of the predictability
        self._s_predictabilities_values = \
            df_the_historical_data[DatePredictabilityComputer.str__output__column_label__predictability]
        self._s_predictabilities_dates = \
            df_the_historical_data[DatePredictabilityComputer.str__input__column_label__date]
        self._str_predictabilities_name = DatePredictabilityComputer.str__output__column_label__predictability

        # We prepare the data for the historical evolution of the measures
        self._s_measures_values = \
            df_the_historical_data[
                df_the_historical_data[DatePredictabilityComputer.str__input__column_label__date] <= dt_as_of_date
            ][DatePredictabilityComputer.str__input__column_label__measure]
        self._s_measures_dates = \
            df_the_historical_data[
                df_the_historical_data[DatePredictabilityComputer.str__input__column_label__date] <= dt_as_of_date
            ][DatePredictabilityComputer.str__input__column_label__date]
        self._str_measures_name = DatePredictabilityComputer.str__input__column_label__measure

        # We prepare the data for displaying the convergence cone alongside the measures
        self._lst_increasing_cone_values, \
            self._lst_increasing_cone_dates, \
            self._lst_decreasing_cone_values, \
            self._lst_decreasing_cone_dates, \
            self._lst_last_measure_values, \
            self._lst_last_measure_dates = self._compute_cones_coordinates(
                df_the_historical_data=df_the_historical_data[
                    df_the_historical_data[DatePredictabilityComputer.str__input__column_label__date] <= dt_as_of_date
                ]
            )
        self._str_increasing_cone_name = "Increasing convergence cone"
        self._str_decreasing_cone_name = "Decreasing convergence cone"
        self._str_last_measure_name = "Final measure"

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")


class DataToTable:
    _dict_values: dict[str, ]

    @property
    def dict_values(self) -> dict[str, ]:
        return self._dict_values

    _logger: Logger = getLogger(__name__)

    def __init__(
            self,
            obj_predictability: PredictabilityBean,
            str_filter_on_key: str,
            dt_as_of_date: datetime = None
    ):
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        # If we do not zoom on a given date, we just get the statistics already available
        if dt_as_of_date is None:
            # We select the data for that selected key
            df_the_statistics_data: DataFrame = obj_predictability.df_by_key[
                obj_predictability.df_by_key[
                    DatePredictabilityComputer.str__input__column_label__key
                ] == str_filter_on_key
            ][DatePredictabilityComputer.lst__output__statistics_by_key__column_labels]  # Required to order columns

        # Otherwise, we need to compute the statistics
        else:

            # We select the data for that selected key, and date
            df_by_measure_data: DataFrame = obj_predictability.df_historical[
                (
                    obj_predictability.df_historical[
                        DatePredictabilityComputer.str__input__column_label__key
                    ] == str_filter_on_key
                )
                & (
                    obj_predictability.df_historical[
                        DatePredictabilityComputer.str__input__column_label__date
                    ] <= dt_as_of_date
                )
            ]
            df_historical_data: DataFrame = obj_predictability.df_historical[
                (
                    obj_predictability.df_historical[
                        DatePredictabilityComputer.str__input__column_label__key
                    ] == str_filter_on_key
                )
                & (
                    obj_predictability.df_historical[
                        DatePredictabilityComputer.str__input__column_label__date
                    ] <= dt_as_of_date
                )
            ]

            df_the_statistics_data: DataFrame = DatePredictabilityComputer().compute_statistics_by_key(
                    df_measures=df_by_measure_data,
                    df_historical_predictability=df_historical_data
            )

        # We expect only one record
        if len(df_the_statistics_data.index) != 1:
            raise Exception(f"When filtering statistics on key '{str_filter_on_key}', we got "
                            f"'{len(df_the_statistics_data.index)}' line while one and only one was expected.")

        # self._lst_values = df_the_statistics_data.iloc[0, :].tolist()
        self._dict_values = df_the_statistics_data.to_dict("records")[0]

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning "
                           f"'{self._dict_values}'.")
