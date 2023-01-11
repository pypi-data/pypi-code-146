import numpy as np
from datasets import load_metric
from transformers import TrainingArguments
from transformers import ViTForImageClassification
from transformers import Trainer
from txp.ml.common.tasks.policy import Policy
from txp.common.ml.tasks import ClassificationLabelDefinition, AssetTask
from txp.ml.common.tasks.task import Task
from txp.ml.common.tasks.hf_image_classification.encoder import (
    HFImageClassificationEncoder,
)
import datasets
import logging
import torch

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class HFImageClassificationPolicy(Policy):
    def __init__(
        self,
        model_checkpoint_str,
        classification_label_def: ClassificationLabelDefinition,
        policy_file: str = None,
    ):
        super().__init__(policy_file)
        self._model_checkpoint = model_checkpoint_str
        self._classification_label_def: ClassificationLabelDefinition = (
            classification_label_def
        )
        self._classifier: ViTForImageClassification = (
            ViTForImageClassification.from_pretrained(
                model_checkpoint_str,
                num_labels=len(self._classification_label_def.int_to_label),
            )
        )

    def name(self):
        return self.__class__.name()

    def _collator(self, batch):
        return {
            "pixel_values": torch.stack([x["pixel_values"] for x in batch]),
            "labels": torch.tensor([x["label"] for x in batch]),
        }

    def _compute_metrics(self, p):
        metric = load_metric("accuracy")
        return metric.compute(
            predictions=np.argmax(p.predictions, axis=1), references=p.label_ids
        )

    def train(self, dataset: datasets.Dataset, target, test_size=0.3):
        training_args = TrainingArguments(
            output_dir="./vit-base-beans-demo-v5",
            per_device_train_batch_size=16,
            evaluation_strategy="steps",
            num_train_epochs=4,
            fp16=False,
            save_steps=100,
            eval_steps=100,
            logging_steps=10,
            learning_rate=2e-4,
            save_total_limit=2,
            remove_unused_columns=False,
            push_to_hub=False,
            load_best_model_at_end=True,
        )

        trainer = Trainer(
            model=self._classifier,
            args=training_args,
            data_collator=self._collator,
            compute_metrics=self._compute_metrics,
            train_dataset=dataset,
        )

        train_results = trainer.train()
        trainer.log_metrics("train", train_results.metrics)
        trainer.save_metrics("train", train_results.metrics)

    def predict(self, tensor):
        """Tensor is inputs IDs"""
        output = self._classifier.forward(tensor["pixel_values"])
        return output.logits.argmax(-1).item()


class HFImageClassificationTask(Task):
    """A HuggingFace Image classification Task wrapper."""

    def __init__(self, task_definition=None, credentials_str=None):
        super(HFImageClassificationTask, self).__init__(
            self._build_encoder(task_definition),
            self._build_policy(task_definition),
            task_definition,
            credentials_str,
        )

        if self.task_definition.task_data and credentials_str is not None:
            self.load_from_bucket(self.task_definition.task_data)

            if task_definition.schema_:
                self.encoder.set_schema(task_definition.schema_)

        self.ready = True

        log.info(
            f"{self.__class__.__name__} instance is ready with file: {self.task_definition.task_data}"
        )

    def _build_encoder(
        self, task_definition: AssetTask
    ) -> HFImageClassificationEncoder:
        return HFImageClassificationEncoder(
            task_definition.parameters["model_name_or_path"],
            classification_label=task_definition.label_def,
            schema=task_definition.schema_,
        )

    def _build_policy(self, task_definition: AssetTask) -> Policy:
        return HFImageClassificationPolicy(
            task_definition.parameters["model_name_or_path"],
            task_definition.label_def,
            None,
        )

    def predict(self, sampling_window_rows) -> tuple:
        """Returns the prediction results for the given sampling windows
        generated input vectors.

        Args:
            sampling_window_rows: filled Firestore dictionary, this dict
                contains all the rows present in bigquery tables.

        Returns:
            Appropriate enumerated label.
        """
        prediction_dataset = self.encoder.transform_input_signals(sampling_window_rows)
        if not prediction_dataset.size:
            return None

        return self.task_definition.label_def.int_to_label[
            self.policy.predict(prediction_dataset)[0]
        ]

    def train(self, dataset) -> None:
        self.policy.train(dataset, self.encoder.target)
