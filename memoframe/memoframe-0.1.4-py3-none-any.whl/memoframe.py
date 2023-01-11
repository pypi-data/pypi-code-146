import pandas as pd
from pandas.errors import ParserError


class OptimizeDataset:
    """
    Contains various functions to perform memory usage optimization
    on integers, floats and objects column of Pandas Dataframes
    """

    def _optimize_integer_features(self, dataframe) -> pd.DataFrame:
        dataframe_int = dataframe.select_dtypes(include=["int"])
        converted_int = dataframe_int.apply(pd.to_numeric, downcast="unsigned")
        return converted_int

    def _optimize_float_features(self, dataframe) -> pd.DataFrame:
        dataframe_float = dataframe.select_dtypes(include=["float"])
        converted_float = dataframe_float.apply(pd.to_numeric, downcast="float")
        return converted_float

    def _optimize_object_features(self, dataframe) -> pd.DataFrame:
        dataframe_object = dataframe.select_dtypes(include=["object"])
        converted_object = dataframe_object.copy()
        len_dataframe = len(dataframe_object)
        for col in converted_object.columns:
            num_unique_values = len(converted_object[col].unique())
            if num_unique_values / len_dataframe < 0.5:
                converted_object[col] = converted_object[col].astype("category")
        return converted_object

    def get_opti_info(self, dataframe) -> str:
        """
        Print potential memory usage gains

        Args:
            dataframe (pd.DataFrame): Dataframe to audit

        Returns:
            Ratio of memory optimized with optimization function
        """

        original_mem_usage = dataframe.memory_usage(deep=True).sum()
        optimized_mem_usage = (
            self.downsize_memory(dataframe).memory_usage(deep=True).sum()
        )
        memory_ratio = round((1 - optimized_mem_usage / original_mem_usage) * 100)
        return f"Up to: {memory_ratio} % memory usage can be saved"

    def downsize_memory(self, dataframe, to_datetime=False) -> pd.DataFrame:
        """
        Pandas dataframe memory optimization

        Args:
            dataframe (pd.DataFrame): Dataframe to be optimized

        Returns:
            Optimized Dataframe df_optimized
        """

        # optimize int features
        converted_int = self._optimize_integer_features(dataframe)
        # optimize float features
        converted_float = self._optimize_float_features(dataframe)
        # optimize object features
        converted_obj = self._optimize_object_features(dataframe)

        # concatanate optimized features
        return pd.concat([converted_obj, converted_float, converted_int], axis=1)
