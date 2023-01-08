from inspect import stack
from logging import Logger, getLogger
from pathlib import Path

from pandas import ExcelWriter, DataFrame, read_excel

from com.enovation.helper.pandas_dataframe_typer import PandasDataframeTyper
from com.enovation.toolbox.predictability.bean import PredictabilityBean
from com.enovation.toolbox.predictability.dp_date_predictability.dp_computer import DatePredictabilityComputer


class DatePredictabilityPersister:
    _logger: Logger = getLogger(__name__)

    # sheets' names in the excel spreadsheet
    str_sheet_name__by_measure: str = "by_measure"
    str_sheet_name__by_key: str = "by_key"
    str_sheet_name__historical: str = "historical"

    def persist(
            self,
            obj_bean_to_persist: PredictabilityBean,
            p_file_path: Path,
            str_sheet_name__by_measure: str = str_sheet_name__by_measure,
            str_sheet_name__by_key: str = str_sheet_name__by_key,
            str_sheet_name__historical: str = str_sheet_name__historical,
    ):
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        # We check there is no existing file at the provided path
        # Note: if simlink, exists returns whether or not the simlink points to an existing file or directory
        if p_file_path.exists() | p_file_path.is_symlink():
            raise Exception(
                f"Cannot persist instance of PredictabilityBean, as provided path '{str(p_file_path)}' seems to exist:"
                f"\n\t- is_file: {p_file_path.is_file()}"
                f"\n\t- is_dir: {p_file_path.is_dir()}"
                f"\n\t- is_symlink: {p_file_path.is_symlink()}"
            )

        # Creating Excel Writer Object from Pandas
        with ExcelWriter(str(p_file_path)) as obj_the_writer:

            obj_bean_to_persist.df_by_measure.to_excel(
                obj_the_writer,
                sheet_name=str_sheet_name__by_measure,
                index=False
            )

            obj_bean_to_persist.df_by_key.to_excel(
                obj_the_writer,
                sheet_name=str_sheet_name__by_key,
                index=False
            )

            obj_bean_to_persist.df_historical.to_excel(
                obj_the_writer,
                sheet_name=str_sheet_name__historical,
                index=False
            )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

    def load(
            self,
            p_file_path: Path,
            str_sheet_name__by_measure: str = str_sheet_name__by_measure,
            str_sheet_name__by_key: str = str_sheet_name__by_key,
            str_sheet_name__historical: str = str_sheet_name__historical,
    ) -> PredictabilityBean:
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        # We check there is an existing file at the provided path
        if not p_file_path.is_file():
            raise Exception(
                f"Cannot load an instance of PredictabilityBean, as provided path '{str(p_file_path)}' does not seem "
                f"to exist or to be a file:"
                f"\n\t- is_file: {p_file_path.is_file()}"
                f"\n\t- is_dir: {p_file_path.is_dir()}"
                f"\n\t- is_symlink: {p_file_path.is_symlink()}"
            )

        # We load the 3 sheets

        # #################################################
        # 1.1. We load the measures
        try:
            df_the_by_measure: DataFrame = read_excel(
                io=p_file_path,
                sheet_name=str_sheet_name__by_measure
            )
            self._logger.info(f"Sheet {str_sheet_name__by_measure} read, shape '{df_the_by_measure.shape}'.")
        except Exception as obj_the_exception:
            raise Exception(
                f"Could not load sheet '{str_sheet_name__by_measure}' from file '{str(p_file_path)}'. Make sure the "
                f"file is effectively an excel spreadsheet that can be opened."
            ) from obj_the_exception
        # 1.2. We properly type the dataframe
        try:
            df_the_by_measure = PandasDataframeTyper.type(
                df_to_type=df_the_by_measure,
                dict_columns_to_type={
                    DatePredictabilityComputer.str__input__column_label__date: PandasDataframeTyper.str__type__date,
                    DatePredictabilityComputer.str__input__column_label__measure: PandasDataframeTyper.str__type__date,
                },
                b_strict=False
            )
        except Exception as an_exception:
            raise Exception(
                f"Could not type sheet '{str_sheet_name__by_measure}' from file '{str(p_file_path)}'. Make sure the "
                f"data is correctly formatted in the file.") from an_exception

        # #################################################
        # 2.1. We load the statistics by key
        try:
            df_the_by_key: DataFrame = read_excel(
                io=p_file_path,
                sheet_name=str_sheet_name__by_key
            )
            self._logger.info(f"Sheet {str_sheet_name__by_key} read, shape '{df_the_by_key.shape}'.")
        except Exception as obj_the_exception:
            raise Exception(
                f"Could not load sheet '{str_sheet_name__by_key}' from file '{str(p_file_path)}'. Make sure the "
                f"file is effectively an excel spreadsheet that can be opened."
            ) from obj_the_exception
        # 2.2. We properly type the dataframe
        try:
            df_the_by_key = PandasDataframeTyper.type(
                df_to_type=df_the_by_key,
                dict_columns_to_type={
                    DatePredictabilityComputer.str__statistics__column_label__measure_count:
                        PandasDataframeTyper.str__type__int,
                    DatePredictabilityComputer.str__statistics__column_label__date_first:
                        PandasDataframeTyper.str__type__date,
                    DatePredictabilityComputer.str__statistics__column_label__date_last:
                        PandasDataframeTyper.str__type__date,
                    DatePredictabilityComputer.str__statistics__column_label__measure_min:
                        PandasDataframeTyper.str__type__date,
                    DatePredictabilityComputer.str__statistics__column_label__measure_max:
                        PandasDataframeTyper.str__type__date,
                    DatePredictabilityComputer.str__statistics__column_label__measure_first:
                        PandasDataframeTyper.str__type__date,
                    DatePredictabilityComputer.str__statistics__column_label__measure_last:
                        PandasDataframeTyper.str__type__date,
                    DatePredictabilityComputer.str__statistics__column_label__predictability_last:
                        PandasDataframeTyper.str__type__float,
                },
                b_strict=False
            )
        except Exception as an_exception:
            raise Exception(
                f"Could not type sheet '{str_sheet_name__by_key}' from file '{str(p_file_path)}'. Make sure the "
                f"data is correctly formatted in the file.") from an_exception

        # #################################################
        # 3.1. We load the historical
        try:
            df_the_historical: DataFrame = read_excel(
                io=p_file_path,
                sheet_name=str_sheet_name__historical
            )
            self._logger.info(f"Sheet {str_sheet_name__historical} read, shape '{df_the_historical.shape}'.")
        except Exception as obj_the_exception:
            raise Exception(
                f"Could not load sheet '{str_sheet_name__historical}' from file '{str(p_file_path)}'. Make sure the "
                f"file is effectively an excel spreadsheet that can be opened."
            ) from obj_the_exception
        # 3.2. We properly type the dataframe
        try:
            df_the_historical = PandasDataframeTyper.type(
                df_to_type=df_the_historical,
                dict_columns_to_type={
                    DatePredictabilityComputer.str__input__column_label__date: PandasDataframeTyper.str__type__date,
                    DatePredictabilityComputer.str__input__column_label__measure: PandasDataframeTyper.str__type__date,
                    DatePredictabilityComputer.str__output__column_label__predictability:
                        PandasDataframeTyper.str__type__float,
                },
                b_strict=False
            )
        except Exception as an_exception:
            raise Exception(
                f"Could not type sheet '{str_sheet_name__historical}' from file '{str(p_file_path)}'. Make sure the "
                f"data is correctly formatted in the file.") from an_exception

        # We instantiate the bean to return
        obj_the_return: PredictabilityBean = PredictabilityBean(
            df_by_measure=df_the_by_measure,
            df_by_key=df_the_by_key,
            df_historical=df_the_historical
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")
        return obj_the_return
