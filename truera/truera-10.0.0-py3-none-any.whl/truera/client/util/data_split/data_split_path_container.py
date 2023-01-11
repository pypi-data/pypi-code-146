import os
from typing import Optional

from truera.client.client_utils import infer_format
from truera.client.client_utils import TextExtractorParams
from truera.client.util.data_split.base_data_split_path_container import \
    BaseDataSplitPathContainer


class DataSplitPathContainer(BaseDataSplitPathContainer):

    def _get_file_for_upload(self, data: str) -> Optional[str]:
        if data is None:
            return data
        elif not isinstance(data, str):
            raise ValueError(
                f"Provided data was not of a valid type: {type(data)}, "
                "only str is allowed."
            )
        elif not os.path.isfile(data):
            raise ValueError(f"Provided path does not point to a file: {data}")
        return data

    def _get_text_extractor_params_for_data(
        self, data: str
    ) -> TextExtractorParams:
        inferred_formats = set(
            [
                infer_format("infer", uri)
                for uri in self.data_sources.values()
                if uri is not None
            ]
        )
        if len(inferred_formats) > 1:
            raise ValueError(
                f"Provided data was not all of the same format. Provided formats: [{inferred_formats}]."
            )

        inferred_format = inferred_formats.pop()
        return TextExtractorParams(
            inferred_format, True, ",", "\"", "", "",
            TextExtractorParams.DEFAULT_DATE_FORMAT,
            TextExtractorParams.DEFAULT_COLUMNS
        )
