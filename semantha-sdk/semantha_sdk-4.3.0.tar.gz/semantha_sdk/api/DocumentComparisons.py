from __future__ import annotations

from io import IOBase

from semantha_sdk.api import SemanthaAPIEndpoint
from semantha_sdk.model import Metadata


class DocumentComparisons(SemanthaAPIEndpoint):

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/documentcomparisons"

    def post(
            self,
            file: IOBase,
            reference_document: IOBase,
            similarity_threshold: float = 0.85,
            synonymous_threshold: float = 0.98,
            mark_no_match: bool = True,
            with_reference_text: bool = True,
            document_type: str = None,
            metadata: list[Metadata] = None,
            with_context: bool = True,
            consider_text_type: bool = False,
            resize_paragraphs: bool = False

    ):
        """ Determine references (for temporary data)

        Args:
            file (IOBase): Input document (left document).
            reference_document (Document): Reference document(s) to be used instead of the documents in the domain's library.
            similarity_threshold (float): Threshold for the similarity score.
                semantha will not deliver results with a sentence score lower than the threshold.
                In general, the higher the threshold, the more precise the results.
            synonymous_threshold (float): Threshold for good matches.
            mark_no_match (bool): Marks paragraphs that have not matched.
            with_reference_text (bool): Provide the reference text in the result JSON.
                If set to false, you have to query the library to resolve the references yourself.
            document_type (str): Specifies the document type that is to be used by semantha when reading the uploaded PDF document.
            metadata (list[Metadata]): Filter by metadata
            with_context (bool): Creates and saves the context.
            consider_text_type (bool): Use this parameter to ensure that only paragraphs of the same type are compared with each other.
                The parameter is of type boolean and is set to false by default.
            resize_paragraphs (bool): Automatically resizes paragraphs based on their semantic meaning
        """

        return self._session.post(
            self._endpoint,
            body={
                "file": file,
                "referencedocument": reference_document.data,
                "similaritythreshold": str(similarity_threshold),
                "synonymousthreshold": str(synonymous_threshold),
                "marknomatch": str(mark_no_match),
                "withreferencetext": str(with_reference_text),
                "documenttype": document_type,
                "metadata": metadata,
                "withcontext": str(with_context),
                "considertexttype": str(consider_text_type),
                "resizeparagraphs": str(resize_paragraphs)
            }
        ).execute()

