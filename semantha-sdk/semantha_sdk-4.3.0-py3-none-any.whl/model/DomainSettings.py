from dataclasses import dataclass

from semantha_sdk.model import SemanthaModelEntity


@dataclass(frozen=True)
class DomainSettings(SemanthaModelEntity):

    def __post_init__(self):
        assert type(self.data) is dict

    @property
    def similarity_model_id(self) -> str:
        return str(self.data["similarityModelId"])

    @property
    def keep_numbers(self) -> bool:
        return bool(self.data["keepNumbers"])

    @property
    def min_tokens(self) -> int:
        return int(self.data["minTokens"])

    @property
    def similarity_measure(self) -> str:
        return str(self.data["similarityMeasure"])

    @property
    def context_weight(self) -> float:
        return float(self.data["contextWeight"])

    @property
    def enable_string_comparison(self) -> bool:
        return bool(self.data["enableStringComparison"])

    @property
    def default_document_type(self) -> str:
        return str(self.data["defaultDocumentType"])

    @property
    def enable_paragraph_sorting(self) -> bool:
        return bool(self.data["enableParagraphSorting"])

    @property
    def enable_paragraph_end_detection(self) -> bool:
        return bool(self.data["enableParagraphEndDetection"])

    @property
    def enable_paragraph_merging_based_on_formatting(self) -> bool:
        return bool(self.data["enableParagraphMergingBasedOnFormatting"])

    @property
    def enable_boost_word_filtering_for_input_documents(self) -> bool:
        return bool(self.data["enableBoostWordFilteringForInputDocuments"])

    @property
    def tagging_similarity_mode(self) -> str:
        return str(self.data["taggingSimilarityMode"])

    @property
    def enable_updating_fingerprints_on_tag_updates(self) -> bool:
        return bool(self.data["enableUpdatingFingerprintsOnTagUpdates"])

    @property
    def similarity_matcher(self) -> str:
        return str(self.data["similarityMatcher"])

    @property
    def similarity_max_deviation(self) -> int:
        return int(self.data["similarityMaxDeviation"])

    @property
    def similarity_threshold(self) -> float:
        return float(self.data["similarityThreshold"])

    @property
    def enable_tagging(self) -> bool:
        return bool(self.data["enableTagging"])

    @property
    def tagging_threshold(self) -> float:
        return float(self.data["taggingThreshold"])

    @property
    def tagging_strategy(self) -> str:
        return str(self.data["taggingStrategy"])

    @property
    def extraction_threshold(self) -> float:
        return float(self.data["extractionThreshold"])

    @property
    def extraction_strategy(self) -> str:
        return str(self.data["extractionStrategy"])

    @property
    def resize_paragraphs_on_extraction(self) -> bool:
        return bool(self.data["resizeParagraphsOnExtraction"])
