from abc import ABC
from abc import abstractmethod
from typing import List, Optional, Tuple

from truera.client.client_utils import TextExtractorParams


class BaseDataSplitPathContainer(ABC):

    def __init__(
        self,
        pre_data: Optional[any] = None,
        post_data: Optional[any] = None,
        extra_data: Optional[any] = None,
        label_data: Optional[any] = None,
        prediction_data: Optional[any] = None,
        feature_influence_data: Optional[any] = None
    ):
        self.data_sources = {
            "pre": pre_data,
            "post": post_data,
            "extra": extra_data,
            "label": label_data,
            "prediction": prediction_data,
            "feature_influence": feature_influence_data,
        }

    def get_valid_data_sources(
        self
    ) -> List[Tuple[Optional[str], str, TextExtractorParams]]:
        return [
            (
                self._get_file_for_upload(source), name,
                self._get_text_extractor_params_for_data(source)
            )
            for name, source in self.data_sources.items()
            if source is not None
        ]

    @abstractmethod
    def _get_file_for_upload(self, data: any) -> Optional[str]:
        pass

    @abstractmethod
    def _get_text_extractor_params_for_data(
        self, data: any
    ) -> TextExtractorParams:
        pass
