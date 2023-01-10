import os
from abc import ABC, abstractmethod
from enum import Enum

from .utils import logger

try:
    import torch
    from transformers import AutoTokenizer, AutoModel, AutoFeatureExtractor  # type: ignore
    from transformers.utils import logging as transformer_logging
    from PIL import Image
except ImportError:
    raise ImportError(
        "To enable embedding generation, "
        "the arize module must be installed with the EmbeddingGeneration option: "
        "pip install 'arize[EmbeddingGeneration]'."
    )

transformer_logging.set_verbosity(50)
transformer_logging.enable_progress_bar()
transformer_logging.disable_default_handler()


class BaseEmbeddingGenerator(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        pass

    def __init__(self, model_name: str, batch_size: int = 100):
        self.__model_name = model_name
        self.__device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.__batch_size = batch_size
        logger.info(f"Downloading pre-trained model {self.model_name}")
        self.__model = AutoModel.from_pretrained(self.model_name).to(self.device)

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
        uc_area = use_case.__class__.__name__.strip("UseCases")
        uc_task = use_case.name
        return f"{uc_area}.{uc_task}"

    @property
    @abstractmethod
    def use_case(self) -> str:
        pass


class NLPEmbeddingGenerator(BaseEmbeddingGenerator, ABC):
    def __init__(self, model_name, tokenizer_max_length=512, **kwargs):
        super(NLPEmbeddingGenerator, self).__init__(model_name, **kwargs)
        self.__tokenizer_max_length = tokenizer_max_length
        logger.info("Downloading tokenizer")
        self.__tokenizer = AutoTokenizer.from_pretrained(self.model_name,
                                                         model_max_length=self.tokenizer_max_length)

    @property
    def tokenizer(self):
        return self.__tokenizer

    @property
    def tokenizer_max_length(self):
        return self.__tokenizer_max_length

    @abstractmethod
    def tokenize(self, batch, text_col):
        pass

    @abstractmethod
    def generate_embeddings(self, df, text_col):
        pass


class CVEmbeddingGenerator(BaseEmbeddingGenerator, ABC):
    def __init__(self, model_name, **kwargs):
        super(CVEmbeddingGenerator, self).__init__(model_name, **kwargs)
        logger.info("Downloading feature extractor")
        self.__feature_extractor = AutoFeatureExtractor.from_pretrained(self.model_name)

    @property
    def feature_extractor(self):
        return self.__feature_extractor

    @staticmethod
    def open_image(image_path):
        if not os.path.exists(image_path):
            raise ValueError(f"Cannot find image {image_path}")
        return Image.open(image_path).convert("RGB")

    @abstractmethod
    def extract_image_features(self, batch, image_path_col):
        pass


class TabularEmbeddingGenerator(BaseEmbeddingGenerator, ABC):
    def __init__(self, model_name, max_length=512, **kwargs):
        super(TabularEmbeddingGenerator, self).__init__(model_name, **kwargs)
        self.__max_length = max_length
        logger.info("Downloading tokenizer")
        self.__tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    @property
    def tokenizer(self):
        return self.__tokenizer

    @property
    def max_length(self):
        return self.__max_length

    @staticmethod
    def default_prompt_fn(row, columns):
        msg = ""
        for col in columns:
            repl_text = col.replace("_", " ")
            msg += f"The {repl_text} is {row[col]}. "
        return msg.strip(" ")

    @abstractmethod
    def tokenize(self, batch, text_col):
        pass
