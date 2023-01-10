from typing import Optional, Dict, Union

from pandas import DataFrame
from sklearn.decomposition import PCA

from lumipy.provider.base_provider import BaseProvider
from lumipy.provider.metadata import TableParam, ColumnMeta
from lumipy.typing.sql_value_type import SqlValType


class PcaProjectionProvider(BaseProvider):
    """Provider that computes a Principal Component Analysis (PCA) given some data and then projects them onto
    the first n-many principal components.

    This provider uses the sklearn implementation of a PCA.

    """

    def __init__(self, n_components: int):
        """Constructor of the PCA projection provider.

        Args:
            n_components (int): number of components in the principal component analysis.
        """

        self.n_components = n_components

        cols = [
            ColumnMeta(f'PC{i}', SqlValType.Double, f"Projection onto principal component {i}")
            for i in range(n_components)
        ]

        table_params = [TableParam("InputData", description="Input data to the PCA transformer.")]

        super().__init__(
            f"Sklearn.Pca.Projector{n_components}D",
            columns=cols,
            table_parameters=table_params,
            description=self.__doc__
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        pca = PCA(n_components=self.n_components)
        out_array = pca.fit_transform(params['InputData'])
        return DataFrame(out_array, columns=[c.name for c in self.columns])
