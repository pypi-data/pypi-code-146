from __future__ import annotations

from io import IOBase
from typing import Optional

from semantha_sdk.api import SemanthaAPIEndpoint
from semantha_sdk.model.Cluster import DocumentCluster, DocumentClusters
from semantha_sdk.model.Document import Document
from semantha_sdk.model.NamedEntities import NamedEntities
from semantha_sdk.model.Paragraphs import Paragraph
from semantha_sdk.model.ReferenceDocuments import ReferenceDocuments as _ReferenceDocumentsDTO, \
    ReferenceDocumentCollection, Statistic, DocumentInformation
from semantha_sdk.model.Sentences import Sentence


class ReferenceDocuments(SemanthaAPIEndpoint):
    @property
    def _endpoint(self):
        return self._parent_endpoint + "/referencedocuments"

    def get_all(self,
                offset: int = None,
                limit: int = None,
                filter_tags: str = None,
                filter_document_class_ids: str = None,
                filter_name: str = None,
                filter_created_before: int = None,
                filter_created_after: int = None,
                filter_metadata: str = None,
                filter_comment: str = None,
                sort_by: str = None,
                return_fields: str = None) -> _ReferenceDocumentsDTO:
        """ Get reference documents (library documents)

        If no parameters are set all reference documents are returned.
        However, the result set can be filtered (filter_*), sorted (sort_by), sliced (offset AND limit) and the returned
        attributes/fields can be manipulated (return_fields) to reduce the size of the response.
        Note that some filters and sorting can only be used iff slicing is used (offset and limit).

        Args:
            offset (int): the start index (inclusive) of the returned slice of reference documents
            limit (int): the end index (exclusive) of the returned slice of reference documents
            filter_tags (str): the tags to filter by: comma separated lists are interpreted as OR and + is interpreted
                               as AND. E.g. 'a+b,c+d' means a AND b OR c AND d. The tag filter can be used without
                               slicing.
            filter_document_class_ids (str): the class ids to filter by. Filtering by class ids can be done without
                                             slicing.
            filter_name (str): filter by (document) name. Can only be used with slicing (offset and limit).
            filter_created_before (int): filter by creation date before. Can only be used with slicing (offset and
                                         limit).
            filter_created_after (int): filter by creation date after. Can only be used with slicing (offset and
                                        limit).
            filter_metadata (str): filter by metadata. Can only be used with slicing (offset and limit).
            filter_comment (str): filter by comment. Can only be used with slicing (offset and limit).
            sort_by (str): (lexically) sort the result by one or more criteria: "name", "filename", "metadata",
                           "created", "updated", "color", "comment", "derivedcolor", "derivedcomment", "documentclass".
                           If a value is prefixed by a '-', the sorting is inverted. Can only be used with slicing
                           (offset and limit). Note that sorting is performed before slicing.
            return_fields (str): limit the returned fields to the defined (instead of a full response): "id", "name",
                                 "tags", "derivedtags", "metadata", "filename", "created", "processed", "lang",
                                 "updated", "color", "derivedcolor", "comment", "derivedcomment", "documentclass"
        """
        if (offset is None and limit is not None) or (limit is None and offset is not None):
            raise ValueError("'limit' and 'offset' must be set together.")
        if offset is None and limit is None:
            if filter_name is not None:
                raise ValueError("filter by name can only be used if 'limit' and 'offset' are set")
            if filter_created_before is not None:
                raise ValueError("filter by 'created before' can only be used if 'limit' and 'offset' are set")
            if filter_created_after is not None:
                raise ValueError("filter by 'created after' can only be used if 'limit' and 'offset' are set")
            if filter_metadata is not None:
                raise ValueError("filter by metadata can only be used if 'limit' and 'offset' are set")
            if filter_comment is not None:
                raise ValueError("filter by comment can only be used if 'limit' and 'offset' are set")
            if sort_by is not None:
                raise ValueError("sorting can only activated if 'limit' and 'offset' are set")

        q_params = {}
        if filter_tags is not None:
            q_params["tags"] = filter_tags
        if filter_document_class_ids is not None:
            q_params["document_class_ids"] = filter_document_class_ids
        if return_fields is not None:
            q_params["fields"] = return_fields
        if offset is not None and limit is not None:
            q_params["offset"] = offset
            q_params["limit"] = limit
            if filter_name is not None:
                q_params["name"] = filter_name
            if filter_created_before is not None:
                q_params["createdbefore"] = filter_created_before
            if filter_created_after is not None:
                q_params["createdafter"] = filter_created_after
            if filter_metadata is not None:
                q_params["metadata"] = filter_metadata
            if filter_comment is not None:
                q_params["comment"] = filter_comment
            if sort_by is not None:
                q_params["sort"] = sort_by

        return self._session.get(self._endpoint, q_params=q_params).execute().to(_ReferenceDocumentsDTO)

    def delete_all(self):
        """ Delete all reference documents """
        self._session.delete(self._endpoint).execute()

    def post(
            self,
            name: str = None,
            tags: str = None,
            metadata: str = None,
            file: IOBase = None,
            text: str = None,
            document_type: str = None,
            color: str = None,
            comment: str = None,
            detect_language: bool = False
    ) -> ReferenceDocumentCollection:
        """ Upload a reference document

        Args:
            name (str): The document name in your library (in contrast to the file name being used during upload).
            tags (str): List of tags to filter the reference library.
                You can combine the tags using a comma (OR) and using a plus sign (AND).
            metadata (str): Filter by metadata
            file (str): Input document (left document).
            text (str): Plain text input (left document). If set, the parameter file will be ignored.
            document_type (str): Specifies the document type that is to be used when reading the uploaded PDF document. 
            color (str): Use this parameter to specify the color for your reference document.
                Possible values are RED, MAGENTA, AQUA, ORANGE, GREY, or LAVENDER.
            comment (str): Use this parameter to add a comment to your reference document.
            detect_language (bool): Auto-detect the language of the document (only available if configured for the domain).
        """
        return self._session.post(
            self._endpoint,
            body={
                "name": name,
                "tags": tags,
                "metadata": metadata,
                "file": file,
                "text": text,
                "documenttype": document_type,
                "color": color,
                "comment": comment
            },
            q_params={
                "detectlanguage": str(detect_language)
            }
        ).execute().to(ReferenceDocumentCollection)

    def get_one(self, document_id: str) -> Document:
        """ Get a reference document by id """
        return self._session.get(f"{self._endpoint}/{document_id}").execute().to(Document)

    def delete_one(self, document_id: str):
        """ Delete a reference document by id """
        self._session.delete(f"{self._endpoint}/{document_id}").execute()

    def patch_document_information(
            self,
            document_id: str,
            update: Document,
            query_by_name: bool = False
    ) -> DocumentInformation:
        """ Update reference document by id

        Args:
            document_id (str): the id of the document to update
            update (DocumentInformation): (partial) document information that should be updated. Please provide an
                                          instance of DocumentInformation (semantha_sdk.model.ReferenceDocuments.
                                          DocumentInformation). E.g. to alter (only) the name of the document you can
                                          use something like Document({"name": "new name"}).
            query_by_name (bool): whether to query by name or not
        """
        return self._session.patch(
            url=f"{self._endpoint}/{document_id}",
            json=update.data,
            q_params={
                "querybyname": str(query_by_name)
            }
        ).execute().to(DocumentInformation)

    def get_paragraph(self, document_id: str, paragraph_id: str) -> Paragraph:
        """ Get a paragraph of a reference document by document id and paragraph id"""
        return self._session.get(f"{self._endpoint}/{document_id}/paragraphs/{paragraph_id}").execute().to(Paragraph)

    def delete_paragraph(self, document_id: str, paragraph_id: str):
        """ Delete a paragraph of a reference document by document id and paragraph id"""
        self._session.delete(f"{self._endpoint}/{document_id}/paragraphs/{paragraph_id}").execute()

    def patch_paragraph(self, document_id: str, paragraph_id: str, update: Paragraph) -> Paragraph:
        """Update a Paragraph by document id and paragraph id
        Args:
            document_id (str): the id of the document to update
            paragraph_id (str):the id of the paragraph to update
            update (Paragraph): (partial) paragraph information that should be updated. Please provide an instance of
                                Paragraph (semantha_sdk.model.Paragraphs.Paragraph). E.g. to alter (only) the text of
                                the paragraph you can use something like Paragraph({"text": "updated text"}).
        """
        return self._session.patch(
            url=f"{self._endpoint}/{document_id}/paragraphs/{paragraph_id}",
            json=update.data
        ).execute().to(Paragraph)

    def get_sentence(self, document_id: str, sentence_id: str) -> Sentence:
        """ Get a sentence of a reference document by document id and sentence id"""
        return self._session.get(f"{self._endpoint}/{document_id}/sentences/{sentence_id}").execute().to(Sentence)

    def get_clusters_of_documents(self) -> list[DocumentCluster]:
        """ Get document clusters, i.e. a semantic clustering of the documents in the library. Clusters are named and
        have an integer ID. Note that a special cluster with ID '-1' is reserved for outliers, i.e. documents that could
        not have been assigned to a cluster.

        Compatibility note: In future releases parameters will be added to alter the clustering.
        """
        return self._session.get(f"{self._endpoint}/clusters").execute().to(DocumentClusters).clusters

    # TODO implement 'get_clusters_of_paragraphs'

    def get_named_entities(self) -> Optional[NamedEntities]:
        """ Get all named entities (aka custom entities) that were extracted from the reference documents.
        Note: Might be None iff no named entities have been extracted.
        """
        return self._session.get(f"{self._endpoint}/namedentities").execute().to(NamedEntities)

    def get_statistic(self) -> Statistic:
        """ Get statistics for reference documents"""
        return self._session.get(f"{self._endpoint}/statistic").execute().to(Statistic)
