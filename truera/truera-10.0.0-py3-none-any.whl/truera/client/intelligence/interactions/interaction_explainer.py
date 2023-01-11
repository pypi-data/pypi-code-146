from typing import Optional, Tuple

from truera.client.intelligence.interactions.interaction_plots import \
    InteractionPlots
from truera.rnn.general.aiq import AIQ
from truera.rnn.general.container.artifacts import ArtifactsContainer


class InteractionExplainer():
    """
    An Explainer class to help feature interaction workflows.
    """

    def __init__(self, aiq: AIQ, artifacts_container: ArtifactsContainer):
        self._aiq = aiq
        self._artifacts_container = artifacts_container

    def gradient_paths(
        self,
        record_idx: int,
        qoi_class: int = 0,
        figsize: Optional[Tuple[int, int]] = (800, 400)
    ) -> None:
        """
        Visualize the gradient paths by feature.

        Args:
            record_idx (int): The record to show gradient paths for.
            qoi_class (int): The class in which influences are calculated for. 
            figsize: Size for plot in pixels. Defaults to (800, 400).
        """
        record_info = self._aiq.gradient_landscape_info(
            self._artifacts_container,
            num_records=1,
            offset=record_idx,
            qoi_class=qoi_class
        )
        fig = InteractionPlots.gradient_landscape_graph(
            record_info=record_info, record_idx=record_idx, figsize=figsize
        )
        fig.show()

    def interaction_dendrogram(
        self,
        record_idx: int,
        qoi_class: int = 0,
        path_max_filter: float = 0.30,
        filter_top_n: int = 50,
        figsize: Optional[Tuple[int, int]] = (800, 800)
    ) -> None:
        """
        Visualize the most interacting features based on gradient path similarity.

        Args:
            record_idx (int): The record to show the interaction dendrogram.
            qoi_class (int): The class in which influences are calculated for. 
            path_max_filter (float, optional): Filters out any paths with max gradient level in the bottom of the specified percentage. 
                Must be between 0 and 1. This happens before the filter_top_n. Defaults to 0.30.
            filter_top_n (int, optional): Keep only the top n most interacting features. This happens after the path_max_filter.
                Interaction strength is determined by pearson correlation of path. Defaults to 50.
            figsize: Size for plot in pixels. Defaults to (800, 800).
        """
        record_info = self._aiq.feature_interaction_dendrogram_info(
            self._artifacts_container,
            num_records=1,
            offset=record_idx,
            qoi_class=qoi_class,
            path_max_filter=path_max_filter,
            filter_top_n=filter_top_n
        )[0]

        fig = InteractionPlots.feature_interaction_dendrogram(
            record_info, record_idx, figsize=figsize
        )
        fig.show()
