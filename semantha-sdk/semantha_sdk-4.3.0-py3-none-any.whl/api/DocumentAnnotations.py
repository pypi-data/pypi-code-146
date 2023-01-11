from io import IOBase

from semantha_sdk.api import SemanthaAPIEndpoint
from semantha_sdk.model import Document


class DocumentAnnotations(SemanthaAPIEndpoint):
    @property
    def _endpoint(self):
        return self._parent_endpoint + "/documentannotations"

    def post_document_annotations(
            self,
            file: IOBase,
            document: Document,
            similarity_threshold: float = 0.85,
            synonymous_threshold: float = 0.98,
            mark_no_match: bool = False,
            with_reference_text: bool = False
    ):
        """ Download the original input document with the referenced document/library matches as annotated comments.

        Args:
            file (IOBase): Input document (left document).
            document (Document): ...
            similarity_threshold (float): Threshold for the similarity score.
                semantha will not deliver results with a sentence score lower than the threshold.
                In general, the higher the threshold, the more precise the results.
            synonymous_threshold (float): Threshold for good matches.
            mark_no_match (bool): Marks paragraphs that have not matched.
            with_reference_text (bool): Provide the reference text in the result JSON.
                If set to false, you have to query the library to resolve the references yourself.
        """
        return self._session.post(
            self._endpoint,
            body={
                "file": file,
                "document": document.data,
                "similaritythreshold": str(similarity_threshold),
                "synonymousthreshold": str(synonymous_threshold),
                "marknomatch": str(mark_no_match),
                "withreferencetext": str(with_reference_text)
            }
        ).execute()
