from __future__ import annotations

from io import IOBase

from semantha_sdk.api import SemanthaAPIEndpoint
from semantha_sdk.model.Document import Document
from semantha_sdk.model.DocumentMetadata import DocumentMetadata


class References(SemanthaAPIEndpoint):

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/references"

    def post(
            self,
            file: IOBase = None,
            reference_document: IOBase = None,
            reference_document_ids: list[str] = None,
            tags: str = "",
            document_class_ids: list[str] = None,
            similarity_threshold: float = 0.85,
            synonymous_threshold: float = 0.98,
            mark_no_match: bool = False,
            with_reference_text: bool = False,
            language: str = None,
            mode: str = "fingerprint",
            document_type: str = None,
            meta_data: list[DocumentMetadata] = None,
            with_context: bool = True,
            consider_text_type: bool = False,
            resize_paragraphs: bool = False,
            text: str = None,
            with_areas: bool = False,
            detect_language: bool = False,
            max_references: int = 50
    ) -> Document:
        """ Matches one input document to a set of reference documents.

            If you match against internal library the 'tags' parameter can be used to filter the library.

            Args:
                file (str): Input document (left document).
                reference_document (str): Reference document(s) to be used instead of the documents in the domain's library.
                reference_document_ids (list[str]): To filter for document IDs. The limit here is 1000 IDs.
                    The IDs are passed as a JSON array.
                tags (str): List of tags to filter the reference library.
                    You can combine the tags using a comma (OR) and using a plus sign (AND).
                document_class_ids (list[str]): List of documentclass IDs for the target.
                    The limit here is 1000 IDs. The IDs are passed as a JSON array.
                    This does not apply on the GET referencedocuments call. Here the ids are separated with a comma.
                similarity_threshold (float): Threshold for the similarity score.
                    semantha will not deliver results with a sentence score lower than the threshold.
                    In general, the higher the threshold, the more precise the results.
                synonymous_threshold (float): Threshold for good matches.
                mark_no_match (bool): Marks the matches that have not matched.
                with_reference_text (bool): Provide the reference text in the result JSON.
                    If set to false, you have to query the library to resolve the references yourself.
                language (str): The language of the input document (only available if configured for the domain).
                mode (str):
                    Determine references:
                        Mode to enable if a semantic search ("fingerprint") or keyword search ("keyword") should be considered.
                    Creating document model:
                        It also defines what structure should be considered for what operator (similarity or extraction).
                    One of "fingerprint", "keyword", "document" or "auto".
                document_type (str):
                    Specifies the document type that is to be used by semantha when reading the uploaded PDF document.
                meta_data (list[DocumentMetadataDTO]): Filter documents by metadata.
                with_context (bool): Creates and saves the context.
                consider_text_type (bool):
                    Use this parameter to ensure that only paragraphs of the same type are compared with each other.
                    The parameter is of type boolean and is set to false by default.
                resize_paragraphs (bool): Automatically resizes paragraphs based on their semantic meaning.
                text (str): Plain text input (left document). If set, the parameter file will be ignored.
                with_areas (bool): Gives back the coordinates of referenced area.
                detect_language (bool):
                    Auto-detect the language of the document (only available if configured for the domain).
                max_references (int): Maximum number of returned results.
        """
        response = self._session.post(
            self._endpoint,
            body={
                "file": file,
                "referencedocument": reference_document,
                "referencedocumentids": reference_document_ids,
                "tags": tags,
                "documentclassids": document_class_ids,
                "similaritythreshold": str(similarity_threshold),
                "synonymousthreshold": str(synonymous_threshold),
                "marknomatch": str(mark_no_match),
                "withreferencetext": str(with_reference_text),
                "language": language,
                "mode": mode,
                "documenttype": document_type,
                "metadata": meta_data,
                "withcontext": str(with_context),
                "considertexttype": str(consider_text_type),
                "resizeparagraphs": str(resize_paragraphs),
                "text": text,
                "withareas": str(with_areas)
            },
            q_params={
                "detectlanguage": str(detect_language),
                "maxreferences": str(max_references)
            }
        ).execute()
        return response.to(Document)
