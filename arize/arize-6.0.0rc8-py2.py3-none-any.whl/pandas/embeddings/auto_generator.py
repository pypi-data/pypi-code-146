from .base_generators import BaseEmbeddingGenerator
from .cv_generators import EmbeddingGeneratorForCVImageClassification
from .nlp_generators import EmbeddingGeneratorForNLPSequenceClassification
from .tabular_generators import EmbeddingGeneratorForTabularFeatures
from .usecases import UseCases


class AutoEmbeddingGenerator:
    def __init__(self, **kwargs):
        raise EnvironmentError(
            f"{self.__class__.__name__} is designed to be instantiated using the "
            f"`{self.__class__.__name__}.from_use_case(use_case, **kwargs)` method."
        )

    @staticmethod
    def from_use_case(use_case: str, **kwargs) -> BaseEmbeddingGenerator:
        if use_case == UseCases.NLP.SEQUENCE_CLASSIFICATION:
            return EmbeddingGeneratorForNLPSequenceClassification(**kwargs)
        elif use_case == UseCases.CV.IMAGE_CLASSIFICATION:
            return EmbeddingGeneratorForCVImageClassification(**kwargs)
        elif use_case == UseCases.STRUCTURED.TABULAR_FEATURES:
            return EmbeddingGeneratorForTabularFeatures(**kwargs)
        else:
            raise ValueError(f"Invalid use case {use_case}")
