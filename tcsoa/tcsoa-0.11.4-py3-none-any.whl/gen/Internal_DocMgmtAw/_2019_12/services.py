from __future__ import annotations

from tcsoa.gen.BusinessObjects import Dataset
from tcsoa.gen.Internal.DocMgmtAw._2019_12.DocMgmt import ProcessTextDatasetResponse
from tcsoa.base import TcService


class DocMgmtService(TcService):

    @classmethod
    def processTextDataset(cls, baseObject: Dataset, content: str, action: str) -> ProcessTextDatasetResponse:
        """
        This operation extracts the contents of the text dataset to a string and returns it or saves the input string
        to the contents of a text dataset.
        
        Use cases:
        - Load the text from the dataset and return it in a string.
        - Save the input text string to the dataset.
        
        """
        return cls.execute_soa_method(
            method_name='processTextDataset',
            library='Internal-DocMgmtAw',
            service_date='2019_12',
            service_name='DocMgmt',
            params={'baseObject': baseObject, 'content': content, 'action': action},
            response_cls=ProcessTextDatasetResponse,
        )
