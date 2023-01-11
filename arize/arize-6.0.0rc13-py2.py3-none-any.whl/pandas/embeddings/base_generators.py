import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List

from .models import CV_PRETRAINED_MODELS, NLP_PRETRAINED_MODELS
from .utils import logger

try:
    import torch
    from transformers import AutoTokenizer, AutoModel, AutoFeatureExtractor  # type: ignore
    from transformers.utils import logging as transformer_logging  # type: ignore
    from PIL import Image
except ImportError:
    raise ImportError(
        "To enable embedding generation, "
        "the arize module must be installed with the EmbeddingGeneration option: "
        "pip install 'arize[EmbeddingGeneration]'."
    )

transformer_logging.set_verbosity(50)
transformer_logging.enable_progress_bar()


class BaseEmbeddingGenerator(ABC):
    def __init__(self, use_case: Enum, model_name: str, batch_size: int = 100):
        self.__use_case = self._parse_use_case(use_case=use_case)
        self.__model_name = model_name
        self.__device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.__batch_size = batch_size
        logger.info(f"Downloading pre-trained model '{self.model_name}'")
        self.__model = AutoModel.from_pretrained(self.model_name).to(self.device)

    @property
    def use_case(self) -> str:
        return self.__use_case

    @property
    def model_name(self) -> str:
        return self.__model_name

    @property
    def model(self):
        return self.__model

    @property
    def device(self) -> torch.device:
        return self.__device

    @property
    def batch_size(self) -> int:
        return self.__batch_size

    @batch_size.setter
    def batch_size(self, new_batch_size: int) -> None:
        err_message = "New batch size should be an integer greater than 0."
        if not isinstance(new_batch_size, int):
            raise TypeError(err_message)
        elif new_batch_size <= 0:
            raise ValueError(err_message)
        else:
            self.__batch_size = new_batch_size
            logger.info(f"Batch size has been set to {new_batch_size}.")

    @staticmethod
    def _parse_use_case(use_case: Enum) -> str:
        uc_area = use_case.__class__.__name__.split("UseCases")[0]
        uc_task = use_case.name
        return f"{uc_area}.{uc_task}"

    @abstractmethod
    def __repr__(self) -> str:
        pass


class NLPEmbeddingGenerator(BaseEmbeddingGenerator):
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"  use_case={self.use_case},\n"
            f"  model_name='{self.model_name}',\n"
            f"  tokenizer_max_length={self.tokenizer_max_length},\n"
            f"  tokenizer={self.tokenizer.__class__},\n"
            f"  model={self.model.__class__},\n"
            f"  batch_size={self.batch_size},\n"
            f")"
        )

    def __init__(
        self, use_case: Enum, model_name: str, tokenizer_max_length: int = 512, **kwargs
    ):
        if model_name not in NLP_PRETRAINED_MODELS:
            raise ValueError(f"model_name not supported. Check supported models with "
                             f"`AutoEmbeddingGenerator.list_pretrained_models()`")
        super(NLPEmbeddingGenerator, self).__init__(
            use_case=use_case, model_name=model_name, **kwargs
        )
        self.__tokenizer_max_length = tokenizer_max_length
        logger.info(f"Downloading tokenizer for '{self.model_name}'")
        self.__tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, model_max_length=self.tokenizer_max_length
        )

    @property
    def tokenizer(self):
        return self.__tokenizer

    @property
    def tokenizer_max_length(self) -> int:
        return self.__tokenizer_max_length

    def tokenize(
        self, batch: Dict[str, List[str]], text_col: str
    ) -> Dict[str, torch.Tensor]:
        return self.tokenizer(
            batch[text_col],
            padding=True,
            truncation=True,
            max_length=self.tokenizer_max_length,
            return_tensors="pt",
        ).to(self.device)


class CVEmbeddingGenerator(BaseEmbeddingGenerator):
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"  use_case={self.use_case},\n"
            f"  model_name='{self.model_name}',\n"
            f"  feature_extractor={self.feature_extractor.__class__},\n"
            f"  model={self.model.__class__},\n"
            f"  batch_size={self.batch_size},\n"
            f")"
        )

    def __init__(self, use_case: Enum, model_name: str, **kwargs):
        if model_name not in CV_PRETRAINED_MODELS:
            raise ValueError(f"model_name not supported. Check supported models with "
                             f"`AutoEmbeddingGenerator.list_pretrained_models()`")
        super(CVEmbeddingGenerator, self).__init__(
            use_case=use_case, model_name=model_name, **kwargs
        )
        logger.info("Downloading feature extractor")
        self.__feature_extractor = AutoFeatureExtractor.from_pretrained(self.model_name)

    @property
    def feature_extractor(self):
        return self.__feature_extractor

    @staticmethod
    def open_image(image_path: str) -> Image.Image:
        if not os.path.exists(image_path):
            raise ValueError(f"Cannot find image {image_path}")
        return Image.open(image_path).convert("RGB")

    def extract_image_features(
        self, batch: Dict[str, torch.Tensor], image_path_col: str
    ):
        # TODO: Check type of batch
        return self.feature_extractor(
            [self.open_image(image_path) for image_path in batch[image_path_col]],
            return_tensors="pt",
        ).to(self.device)
