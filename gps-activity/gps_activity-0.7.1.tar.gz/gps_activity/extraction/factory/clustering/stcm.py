from typing import Dict, List, Union

from sklearn.pipeline import Pipeline


from ... import nodes as local_nodes
from .... import nodes as global_nodes
from ....abstract import AbstractPipelineFactory
from ....models import DataFramePivotFields


class STCMFactory(AbstractPipelineFactory):

    # flake8: noqa: CFQ002
    @staticmethod
    def factory_pipeline(
        source_vehicle_id_column: str,
        eps: float = 20,
        min_duration_sec: Union[int, float] = 60,
    ) -> Pipeline:
        """
        Function builds scikit-learn clustering pipeline
        with Spatio-temporal clustering model.

        Built-in constraints:
        - Only one vehicle per pipeline run

        Returns:
        sklear.pipeline.Pipeline: Scikit-learn clustering pipeline
        """
        pivot_fields = DataFramePivotFields(source_vehicle_id=source_vehicle_id_column)
        return Pipeline(
            [
                (
                    "unique_vehicle_constrain",
                    global_nodes.UniqueVehicleConstraint(pivot_fields=pivot_fields),
                ),
                (
                    "select_columns",
                    global_nodes.SelectColumns(
                        columns=[
                            pivot_fields.projected_lat,
                            pivot_fields.projected_lon,
                            pivot_fields.computed_unixtime,
                            pivot_fields.fragmentation_output,
                        ],
                    ),
                ),
                (
                    "clustering_stcm",
                    local_nodes.STCM(
                        eps=eps,
                        min_duration_sec=min_duration_sec,
                    ),
                ),
            ],
        )
