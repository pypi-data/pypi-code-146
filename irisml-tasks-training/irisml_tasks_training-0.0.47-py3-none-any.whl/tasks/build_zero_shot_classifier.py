import dataclasses
import logging
import typing
import torch
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Create a zero-shot classification layer."""
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        text_features: typing.List[torch.Tensor]
        text_classes: typing.Union[typing.List[int], torch.Tensor]

    @dataclasses.dataclass
    class Config:
        num_classes: int

    @dataclasses.dataclass
    class Outputs:
        classifier: torch.nn.Module = None

    def execute(self, inputs):
        num_examples = len(inputs.text_features)
        if len(inputs.text_classes) != num_examples:
            raise RuntimeError(f"The number of examples doesn't match. features={num_examples}, classes={len(inputs.text_classes)}")

        feature_shape = inputs.text_features[0].shape
        logger.debug(f"Feature shape is {feature_shape}. Got {num_examples} samples.")

        features_per_class = [[] for _ in range(self.config.num_classes)]
        for c, f in zip(inputs.text_classes, inputs.text_features):
            index = int(c)
            if not 0 <= index < self.config.num_classes:
                raise RuntimeError(f"Unexpected class index: {index}")
            features_per_class[index].append(f)

        embeddings_per_class = []
        for c in range(self.config.num_classes):
            if features_per_class[c]:
                class_embeddings = torch.stack(features_per_class[c])
                class_embeddings /= class_embeddings.norm(dim=-1, keepdim=True)
                class_embedding = class_embeddings.mean(dim=0)
                class_embedding /= class_embedding.norm()
            else:
                logger.warning(f"No features are provided for class {c}. Initializing with zeros.")
                class_embedding = torch.zeros(*feature_shape)

            embeddings_per_class.append(class_embedding)

        weights = torch.stack(embeddings_per_class, dim=1).transpose(0, 1)  # TODO: Multiply with logit_scale?
        with torch.no_grad():
            classifier = torch.nn.Linear(weights.shape[1], weights.shape[0], bias=False)
            classifier.weight.copy_(weights)
        return self.Outputs(classifier)
