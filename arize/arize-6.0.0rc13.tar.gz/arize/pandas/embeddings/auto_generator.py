import pandas as pd

from .base_generators import BaseEmbeddingGenerator
from .cv_generators import EmbeddingGeneratorForCVImageClassification
from .models import CV_PRETRAINED_MODELS, NLP_PRETRAINED_MODELS
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

    @classmethod
    def list_pretrained_models(cls) -> pd.DataFrame:
        data = {
            "Task": ["NLP" for _ in NLP_PRETRAINED_MODELS]
            + ["CV" for _ in CV_PRETRAINED_MODELS],
            "Architecture": [
                cls.__parse_model_arch(model)
                for model in NLP_PRETRAINED_MODELS + CV_PRETRAINED_MODELS
            ],
            "Model Name": NLP_PRETRAINED_MODELS + CV_PRETRAINED_MODELS,
        }
        df = pd.DataFrame(data)
        df.sort_values(by=[col for col in df.columns], ascending=True, inplace=True)
        return df.reset_index(drop=True)

    @staticmethod
    def __parse_model_arch(model_name: str) -> str:
        if "gpt" in model_name.lower():
            return "GPT"
        elif "bert" in model_name.lower():
            return "BERT"
        elif "vit" in model_name.lower():
            return "ViT"
        else:
            raise ValueError("Invalid model_name, unknown architecture.")
