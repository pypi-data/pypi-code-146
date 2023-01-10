from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

if TYPE_CHECKING:
    from ..models.input_document import InputDocument
    from ..models.with_annotator import WithAnnotator
    from ..models.with_processor import WithProcessor
    from ..models.with_sentencizer import WithSentencizer


T = TypeVar("T", bound="AnnotateDocumentsWithMany")


@attr.s(auto_attribs=True)
class AnnotateDocumentsWithMany:
    """
    Attributes:
        documents (List['InputDocument']):
        pipeline (List[Union['WithAnnotator', 'WithProcessor', 'WithSentencizer']]):
    """

    documents: List["InputDocument"]
    pipeline: List[Union["WithAnnotator", "WithProcessor", "WithSentencizer"]]

    def to_dict(self) -> Dict[str, Any]:
        from ..models.with_annotator import WithAnnotator
        from ..models.with_processor import WithProcessor

        documents = []
        for documents_item_data in self.documents:
            documents_item = documents_item_data.to_dict()

            documents.append(documents_item)

        pipeline = []
        for pipeline_item_data in self.pipeline:
            pipeline_item: Dict[str, Any]

            if isinstance(pipeline_item_data, WithAnnotator):
                pipeline_item = pipeline_item_data.to_dict()

            elif isinstance(pipeline_item_data, WithProcessor):
                pipeline_item = pipeline_item_data.to_dict()

            else:
                pipeline_item = pipeline_item_data.to_dict()

            pipeline.append(pipeline_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "documents": documents,
                "pipeline": pipeline,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.input_document import InputDocument
        from ..models.with_annotator import WithAnnotator
        from ..models.with_processor import WithProcessor
        from ..models.with_sentencizer import WithSentencizer

        d = src_dict.copy()
        documents = []
        _documents = d.pop("documents")
        for documents_item_data in _documents:
            documents_item = InputDocument.from_dict(documents_item_data)

            documents.append(documents_item)

        pipeline = []
        _pipeline = d.pop("pipeline")
        for pipeline_item_data in _pipeline:

            def _parse_pipeline_item(data: object) -> Union["WithAnnotator", "WithProcessor", "WithSentencizer"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    pipeline_item_type_0 = WithAnnotator.from_dict(data)

                    return pipeline_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    pipeline_item_type_1 = WithProcessor.from_dict(data)

                    return pipeline_item_type_1
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                pipeline_item_type_2 = WithSentencizer.from_dict(data)

                return pipeline_item_type_2

            pipeline_item = _parse_pipeline_item(pipeline_item_data)

            pipeline.append(pipeline_item)

        annotate_documents_with_many = cls(
            documents=documents,
            pipeline=pipeline,
        )

        return annotate_documents_with_many
