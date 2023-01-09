"""@Author: Rayane AMROUCHE

Column transformation methods for the Utils class for the DataManager.
"""

from typing import Any, List

import pandas as pd  # type: ignore

from dsmanager.datamanager.datastorage import DataStorage


class ColumnUtils:
    """ColumnUtils class brings utils tools for the data manager."""

    def __init__(self) -> None:
        self.categories = DataStorage()

    def create_category(
        self,
        name: str,
        categories: List[Any],
        ordered: bool = False,
    ) -> pd.CategoricalDtype:
        """Create a category type and save it in a DataStorage.

        Args:
            name (str): Name of the category type to create.
            categories (List[Any]): Unique list of values of the category.
            ordered (bool): True if this category is ordered.

        Returns:
            pd.CategoricalDtype: Category type created.
        """
        category = pd.CategoricalDtype(
            categories,
            ordered,
        )
        self.categories[name] = category
        return category

    def as_category(
        self, df_: pd.DataFrame, column: str, category_name: str = "", **kwargs: Any
    ) -> pd.DataFrame:
        """Transform a DataFrame column's type to a pd.Categorical.

        Args:
            df_ (pd.DataFrame): DataFrame with a column that needs to be transformed.
            column (str): Column which type is to be changed to a pd.Categorical.
            category_name (str, optional): Name of the category to create. Defaults to
                "".

        Returns:
            pd.DataFrame: Returns DataFrame to keep chaining.
        """
        if category_name == "":
            category_name = column
        if category_name in self.categories:
            category = self.categories[category_name]
        else:
            if "categories" not in kwargs:
                kwargs["categories"] = df_[column].dropna().unique()

            category = self.create_category(category_name, **kwargs)
        return df_.astype({column: category})

    def bin_column(self, df_: pd.DataFrame, column: str, k: int = 20) -> pd.DataFrame:
        """Apply k binning on a given column of a given dataframe.

        Args:
            df_ (pd.DataFrame): Dataframe from which a column will be transformed.
            column (str): Column on which apply binning.
            k (int, optional): Number of bins to create for the given column. Defaults
                to 20.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        if df_[column].nunique() < k:
            return df_.assign(**{f"{column}_bin": lambda df__: df__[column]})
        return df_.assign(
            **pd.cut(df_[column], bins=k)
            .astype(str)
            .str.strip("(]")
            .str.split(", ")
            .to_frame()
            .pipe(
                lambda df__: df__.assign(
                    **pd.DataFrame(
                        df__[column].to_list(),
                        columns=[f"{column}_lb", f"{column}_hb"],
                        index=df__.index,
                    )
                )
            )
            .assign(
                **{
                    f"{column}_bin": lambda df__: df__[[f"{column}_lb", f"{column}_hb"]]
                    .astype(float)
                    .mean(axis=1)
                }
            )
            .pipe(self.as_category, f"{column}_bin", ordered=True)
            .drop(columns=[column])
        )

    @staticmethod
    def onehot_encode(df_: pd.DataFrame, column: str, **kwargs: Any) -> pd.DataFrame:
        """Encode a column using the onehot method.

        Args:
            df_ (pd.DataFrame): DataFrame which column are to be onehot encoded.
            column (str): Column to onehot encode.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        return df_.assign(**pd.get_dummies(df_[column], prefix=column, **kwargs))

    @staticmethod
    def onehot_decode(df_: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Decode a list of columns using the onehot method.

        Args:
            df_ (pd.DataFrame): DataFrame which columns are the result of a onehot
                encoding.
            columns (str): Column to onehot decode.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        return df_.assign(**pd.from_dummies(df_[columns]))

    @staticmethod
    def column_spliter(
        df_: pd.DataFrame, column: str, columns: List[str] | None = None
    ) -> pd.DataFrame:
        """Split a column which contain a dict or a list.

        Args:
            df_ (pd.DataFrame): Dataframe from which a column will be splited.
            column (str): Column to split.
            columns (List[str]): Name of the columns after split.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        if columns is None:
            return df_.assign(**pd.DataFrame(df_[column].to_list()).add_prefix(column))
        return df_.assign(
            **pd.DataFrame(df_[column].to_list(), columns=columns).add_prefix(column)
        )
