from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

if TYPE_CHECKING:
    from ..models.converter import Converter
    from ..models.formatter import Formatter
    from ..models.with_annotator import WithAnnotator
    from ..models.with_processor import WithProcessor
    from ..models.with_sentencizer import WithSentencizer


T = TypeVar("T", bound="ConvertFormatAnnotationPlan")


@attr.s(auto_attribs=True)
class ConvertFormatAnnotationPlan:
    """
    Attributes:
        converter (Converter):
        formatter (Formatter):
        pipeline (List[Union['WithAnnotator', 'WithProcessor', 'WithSentencizer']]):
    """

    converter: "Converter"
    formatter: "Formatter"
    pipeline: List[Union["WithAnnotator", "WithProcessor", "WithSentencizer"]]

    def to_dict(self) -> Dict[str, Any]:
        from ..models.with_annotator import WithAnnotator
        from ..models.with_processor import WithProcessor

        converter = self.converter.to_dict()

        formatter = self.formatter.to_dict()

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
                "converter": converter,
                "formatter": formatter,
                "pipeline": pipeline,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.converter import Converter
        from ..models.formatter import Formatter
        from ..models.with_annotator import WithAnnotator
        from ..models.with_processor import WithProcessor
        from ..models.with_sentencizer import WithSentencizer

        d = src_dict.copy()
        converter = Converter.from_dict(d.pop("converter"))

        formatter = Formatter.from_dict(d.pop("formatter"))

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

        convert_format_annotation_plan = cls(
            converter=converter,
            formatter=formatter,
            pipeline=pipeline,
        )

        return convert_format_annotation_plan
