import inspect
import logging

from numpy import where
from pandas import DataFrame


class PandasDataframeSampler:
    _logger: logging.Logger = logging.getLogger(__name__)

    @staticmethod
    def compress(
            df_measures: DataFrame,
            lst_key_columns: list = None,
            lst_value_columns: list = None,
            lst_ordering_columns: list = None,
            b_keep_last: bool = False,
    ) -> DataFrame:
        """
        The function screens the rows within each universe one by one, and it drops the rows which are equal to the
        previous one.

        Three list of columns are provided:
        - lst_key_columns are used to define the universes. Each universe is processed independently from the others. In
          other words, calling the function universe by universe would return the same result.
        - lst_value_columns are reconciled, and if all values are equal, then 2 rows are deemed identical. In case at
          least one value is different, then rows are considered NOT identical.
        - lst_ordering_columns are used to sort the values in the dataframe before processing the lines one by one. If
          the parameter is null, the function assume the rows are already sorted.

        If argument b_keep_last is set to True, the very last record of each key is kept, even if it is a duplicate
        with a previous row.

        BR_001, dataframe expected not to contain several columns with the same label
        BR_002, all columns from lst_key_columns expected to be in the dataframe
        BR_003, all columns from lst_value_columns expected to be in the dataframe
        BR_004, all columns from lst_ordering_columns expected to be in the dataframe
        BR_005, all columns from dataframe should be listed into one of the list: key, value or ordering
        BR_006, dataframe expected not to contain any duplicate across the ordering columns (within the same universe)

        :param df_measures: the dataframe from which duplicates will be dropped
        :param lst_key_columns: lst_key_columns are used to define the universes. Each universe is processed
            independently from the others
        :param lst_value_columns: lst_value_columns are reconciled, and if all values are equal, then 2 rows are deemed
            identical. In case at least one value is different, then rows are considered NOT identical
        :param lst_ordering_columns: lst_ordering_columns are used to sort the values in the dataframe before
            processing the lines one by one. If the parameter is null, the function assume the rows are already sorted.
        :param b_keep_last: whether or not the last row of each keys is to be kept even if duplicate
        """

        PandasDataframeSampler._logger.debug(
            f"Function '{inspect.stack()[0].filename} - {inspect.stack()[0].function}' is called.")

        # We duplicate the data, not to alter the source...
        df_measures = df_measures.copy()

        # Not to have conflicts with working columns that will be added in the below logic...
        df_measures.columns = ["_" + i_col for i_col in df_measures.columns]

        # ############################################################################################################ #
        # ## First step: we prepare the various lists, as we authorize null values...
        # ## - If key columns are null, we consider an empty list
        # ## - If ordering columns are null, we consider an empty list
        # ##   - Otherwise, we ensure there is not duplicate with the key columns
        # ## - If value columns are null, we consider all the columns from the dataframe, minus the key and ordering
        # ##   columns
        # ##   - Otherwise, we ensure there is not duplicate with the key columns
        # ############################################################################################################ #

        # If no key columns are provided
        if lst_key_columns is None:
            lst_key_columns = []
        else:
            # Not to have conflicts with working columns that will be added in the below logic...
            lst_key_columns = ["_" + i_key for i_key in lst_key_columns]

        # If no ordering columns are provided
        if lst_ordering_columns is None:
            lst_ordering_columns = []
        # Particular case: to avoid duplicates, we make sure no columns are both in key and ordering columns
        else:
            # Not to have conflicts with working columns that will be added in the below logic...
            lst_ordering_columns = ["_" + i_key for i_key in lst_ordering_columns]

            # The following is buggy, as using set could impact the order in the list, thus impacting the ordering logic
            # lst_ordering_columns = list(set(lst_ordering_columns) - set(lst_key_columns))
            # Replaced by
            for i_col in lst_key_columns:
                try:
                    lst_ordering_columns.remove(i_col)
                except ValueError:
                    pass

        # If no value columns are provided, we consider all the columns from the dataframe, minus the keys and orderings
        if lst_value_columns is None:
            lst_value_columns = list(set(df_measures.columns)-set(lst_key_columns)-set(lst_ordering_columns))
            PandasDataframeSampler._logger.info(
                f"The list of value columns was None:"
                f"\n\t- We took all the columns: '{', '.join(df_measures.columns)}'"
                f"\n\t- We removed the keys: '{', '.join(lst_key_columns)}'"
                f"\n\t- We removed the ordering columns: '{', '.join(lst_ordering_columns)}'"
                f"\n\t--> We eventually returned: '{', '.join(lst_value_columns)}'.")
        # Particular case: to avoid duplicates, we make sure no columns are both in key, ordering and value columns
        else:
            # Not to have conflicts with working columns that will be added in the below logic...
            lst_value_columns = ["_" + i_key for i_key in lst_value_columns]

            lst_value_columns = list(set(lst_value_columns) - set(lst_ordering_columns) - set(lst_key_columns))

        # ############################################################################################################ #
        # ## Second step: we implement the business rules
        # ############################################################################################################ #

        # BR_001, dataframe expected not to contain several columns with the same label
        lst_all_columns: list = df_measures.columns
        lst_unique_columns: list = list(set(lst_all_columns))
        lst_duplicated_columns: list = list(set(lst_all_columns)-set(lst_unique_columns))
        if len(lst_duplicated_columns) > 0:
            raise Exception(f"BR_001, dataframe provided as a parameter does contain several columns labelled "
                            f"'{', '.join(lst_duplicated_columns)}' (discard the '_' ahead of the column labels).")

        # BR_002, all columns from lst_key_columns expected to be in the dataframe
        lst_missing_key_columns: list = list(set(lst_key_columns) - set(df_measures.columns))
        if len(lst_missing_key_columns) > 0:
            raise Exception(f"BR_002, dataframe provided as a parameter (discard the '_' ahead of the column labels)"
                            f"\n\t- does not contain key columns '{', '.join(lst_missing_key_columns)}'"
                            f"\n\t- but does only contain '{', '.join(df_measures.columns)}'")

        # BR_003, all columns from lst_value_columns expected to be in the dataframe
        lst_missing_value_columns: list = list(set(lst_value_columns) - set(df_measures.columns))
        if len(lst_missing_value_columns) > 0:
            raise Exception(f"BR_003, dataframe provided as a parameter"
                            f"\n\t- does not contain value columns '{', '.join(lst_missing_value_columns)}'"
                            f"\n\t- but does only contain '{', '.join(df_measures.columns)}' (discard the '_' ahead of "
                            f"the column labels)")

        # BR_004, all columns from lst_ordering_columns expected to be in the dataframe
        if len(lst_ordering_columns) > 0:
            lst_missing_ordering_columns: list = list(set(lst_ordering_columns) - set(df_measures.columns))
            if len(lst_missing_value_columns) > 0:
                raise Exception(f"BR_004, dataframe provided as a parameter"
                                f"\n\t- does not contain value columns '{', '.join(lst_missing_ordering_columns)}'"
                                f"\n\t- but does only contain '{', '.join(df_measures.columns)}' (discard the '_' "
                                f"ahead of the column labels)")

        # BR_005, all columns from dataframe should be listed into one of the list: key, value or ordering
        lst_all_columns: list = lst_key_columns + lst_value_columns
        if len(lst_ordering_columns) > 0:
            lst_all_columns = lst_all_columns + lst_ordering_columns
        lst_all_columns = list(dict.fromkeys(lst_all_columns))  # To remove any duplicates
        lst_missing_columns: list = list(set(df_measures.columns)-set(lst_all_columns))
        if len(lst_missing_columns) > 0:
            raise Exception(f"BR_005, dataframe has columns not typed among 'key', 'value', or 'ordering'. Ensure "
                            f"to effectively type these columns when calling the function: "
                            f"'{', '. join(lst_missing_columns)}' (discard the '_' ahead of the column labels).")

        # BR_006, dataframe expected not to contain any duplicate across the ordering columns (within the same universe)
        if len(lst_ordering_columns) > 0:
            df_keys_ordering_only: DataFrame = \
                df_measures[lst_key_columns+lst_ordering_columns] \
                .groupby(by=lst_key_columns+lst_ordering_columns) \
                .size().reset_index()
            df_keys_ordering_only.columns = lst_key_columns+lst_ordering_columns+["count"]
            if len(df_keys_ordering_only[df_keys_ordering_only["count"] > 1].index) > 0:
                raise Exception(f"BR_006, dataframe provided contains duplicates among key and ordering columns\n"
                                f"{df_keys_ordering_only[df_keys_ordering_only['count'] > 1].to_string()}")

        # ############################################################################################################ #
        # ## Third step: we sort values
        # ############################################################################################################ #

        # If not yet ordered, we sort values in the dataframe
        if len(lst_ordering_columns) > 0:
            df_measures = df_measures.sort_values(by=lst_ordering_columns)

        # ############################################################################################################ #
        # ## Fourth step: we process the dataframe
        # ############################################################################################################ #

        # We now split the dataframe by the keys into groups that are processed one by one
        if len(lst_key_columns) > 0:
            df_the_return: DataFrame = \
                df_measures.groupby(by=lst_key_columns).apply(
                    func=PandasDataframeSampler.little_magic,
                    lst_value_columns=lst_value_columns,
                    b_keep_last=b_keep_last
                )
        else:
            df_the_return: DataFrame = PandasDataframeSampler.little_magic(
                df_group=df_measures,
                lst_value_columns=lst_value_columns,
                b_keep_last=b_keep_last
            )

        # ############################################################################################################ #
        # ## Fifth step: eventually, we prepare the return value
        # ## - We remove all temporary and working columns that were added in the "little_magic"
        # ## - We remove the "_" we added at the very beginning
        # ## - We remove the multiindex
        # ############################################################################################################ #
        df_the_return = df_the_return[lst_all_columns]
        df_the_return.columns = [i_col[1:] for i_col in df_the_return.columns]
        df_the_return = df_the_return.reset_index(drop=True)

        PandasDataframeSampler._logger.debug(
            f"Function '{inspect.stack()[0].filename} - {inspect.stack()[0].function}' is returning.")

        return df_the_return

    @staticmethod
    def little_magic(
            df_group: DataFrame,
            lst_value_columns: list,
            b_keep_last: bool,
    ) -> DataFrame:

        df_group = df_group.copy()

        # We duplicate, and shift, the value columns that we want to compare across rows
        # And we compare values
        for i_col in lst_value_columns:

            df_group["tmp_" + i_col] = df_group[i_col].shift(1)
            df_group["equal_" + i_col] = where(
                (df_group["tmp_" + i_col].isnull() & df_group[i_col].isnull())
                | (
                        ~df_group["tmp_" + i_col].isnull() & ~df_group[i_col].isnull()
                        & (df_group["tmp_" + i_col] == df_group[i_col])
                ),
                True,
                False
            )

        # We compute for each line whether or not the row is similar to the previous one
        df_group["equal"] = df_group[["equal_" + i_col for i_col in lst_value_columns]].all(axis=1)

        # The first line should not be dropped
        df_group.loc[df_group.head(1).index, "equal"] = False

        # If b_keep_last, the last line should not be dropped neither
        if b_keep_last:
            df_group.loc[df_group.tail(1).index, "equal"] = False

        # Eventually, we drop duplicated rows
        df_group = df_group[~df_group["equal"]]

        return df_group
