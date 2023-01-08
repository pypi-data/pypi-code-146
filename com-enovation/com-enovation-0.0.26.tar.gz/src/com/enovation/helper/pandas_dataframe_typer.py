import logging
import inspect

from numpy import nan
from pandas import DataFrame, to_datetime, isnull


class PandasDataframeTyper:

    _logger: logging.Logger = logging.getLogger(__name__)

    str__type__date = 'date'
    str__type__float = 'float'
    str__type__int = 'int'
    str__type__str = 'str'

    lst__types: list[str] = [
        str__type__date,
        str__type__float,
        str__type__int,
        str__type__str
    ]

    @staticmethod
    def type(
            df_to_type: DataFrame,
            dict_columns_to_type: dict,
            b_strict: bool = False,
    ) -> DataFrame:
        """
        dict_columns_to_type = {
            "a column name": "a format"
        }
        With "a format" among:
        - "date"
        - "float"
        - "int"
        - "str"

        :param b_strict: if True, we raise an exception in case we do not have a match between the columns in the
            dataframe and the dictionary
        :param df_to_type:
        :param dict_columns_to_type:
        :return:
        """

        PandasDataframeTyper._logger.debug(
            f"Function '{inspect.stack()[0].filename} - {inspect.stack()[0].function}' is called.")

        the_df_return: DataFrame = df_to_type

        # We check the dataframe columns versus the ones in the dictionary
        the_extra_columns_in_df: list = list(
            set(df_to_type.columns)
            - set([i_column_name for i_column_name in dict_columns_to_type.keys()])
        )

        the_extra_columns_in_dict: list = list(
            set([i_column_name for i_column_name in dict_columns_to_type.keys()])
            - set(df_to_type.columns)
        )

        if (len(the_extra_columns_in_df) + len(the_extra_columns_in_dict)) > 0:
            the_msg: str = f"When requesting to type a dataframe, we discovered the following discrepancies:\n\t" \
                           f"- Columns in dataframe, but missing in  dictionary: '" \
                           f"{', '.join(the_extra_columns_in_df)}'\n\t" \
                           f"- Columns in dictionary, but missing in dataframe: '" \
                           f"{', '.join(the_extra_columns_in_dict)}'."

            if b_strict:
                raise Exception(the_msg)

            else:
                PandasDataframeTyper._logger.info(the_msg)

        # We go through each columns to be retyped
        for k_field, v_df_type in dict_columns_to_type.items():

            # The field to retype might not exist (if b_strict is false)
            if k_field in df_to_type.columns:

                # Depending on the target type
                if v_df_type == PandasDataframeTyper.str__type__date:
                    try:
                        the_df_return.loc[:, k_field] = to_datetime(
                            the_df_return.loc[:, k_field], infer_datetime_format=True).dt.normalize()
                    except Exception as an_exception:
                        raise Exception(an_exception, f"Exception raised when typing column "
                                                      f"'{k_field}' into '{v_df_type}'.")

                elif v_df_type == PandasDataframeTyper.str__type__float:
                    try:
                        the_df_return.loc[:, k_field] = the_df_return[k_field].astype('Float64')
                        # Change as of 28-FEB-22, after upgrading packages:
                        # - Replaced below pandas.NaT by numpy.nan
                        # - In order to avoid an unexpected exception while typing to Float64 the column
                        the_df_return.loc[:, k_field] = \
                            the_df_return[k_field].apply(lambda x: nan if isnull(x) else round(x, 2))
                        the_df_return.loc[:, k_field] = the_df_return[k_field].astype('Float64')
                    except Exception as an_exception:
                        raise Exception(an_exception, f"Exception raised when typing column "
                                                      f"'{k_field}' into '{v_df_type}'.")

                elif v_df_type == PandasDataframeTyper.str__type__int:
                    try:
                        the_df_return.loc[:, k_field] = \
                            the_df_return[k_field].astype('Int64')
                    except Exception as an_exception:
                        raise Exception(an_exception, f"Exception raised when typing column "
                                                      f"'{k_field}' into '{v_df_type}'.")

                elif v_df_type == PandasDataframeTyper.str__type__str:
                    try:
                        the_df_return.loc[:, k_field] = \
                            the_df_return[k_field].astype('string')
                    except Exception as an_exception:
                        raise Exception(an_exception, f"Exception raised when typing column "
                                                      f"'{k_field}' into '{v_df_type}'.")

                else:
                    raise Exception(f"We don't know how to handle transco into '{v_df_type}'.")

        PandasDataframeTyper._logger.debug(
            f"Function '{inspect.stack()[0].filename} - {inspect.stack()[0].function}' is returning.")

        return the_df_return
