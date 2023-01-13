import dataclasses
import logging
import torch
import PIL.Image
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Convert an object detection dataset into a classification dataset."""
    VERSION = '0.1.1'

    @dataclasses.dataclass
    class Inputs:
        dataset: torch.utils.data.Dataset

    @dataclasses.dataclass
    class Outputs:
        dataset: torch.utils.data.Dataset

    def execute(self, inputs):
        if (len(inputs.dataset) == 0 or inputs.dataset[0][1].dim() <= 1):
            # Return input dataset if it is already a multiclass or multilabel classification dataset.
            logger.debug("Dataset is already classification. Skip the task.")
            return self.Outputs(inputs.dataset)
        else:
            return self.Outputs(ClassificationFromDetectionDataset(inputs.dataset))

    def dry_run(self, inputs):
        return self.execute(inputs)


class ClassificationFromDetectionDataset(torch.utils.data.Dataset):
    def __init__(self, dataset):
        self._dataset = dataset
        num_boxes = [len(targets) for _, targets in dataset]
        self._index_mappings = []
        for i, n in enumerate(num_boxes):
            self._index_mappings.extend([(i, j) for j in range(n)])

        logger.info(f"Created a classificaiton dataset with {len(self._index_mappings)} samples. The source dataset has {len(self._dataset)} samples.")
        assert len(self._index_mappings) == sum(num_boxes)

    def __len__(self):
        return len(self._index_mappings)

    def __getitem__(self, index):
        image_index, box_index = self._index_mappings[index]
        image, targets = self._dataset[image_index]
        assert isinstance(image, PIL.Image.Image)
        w, h = image.size
        box = targets[box_index]
        cropped = image.crop((int(w * box[1]), int(h * box[2]), int(w * box[3]), int(h * box[4])))
        return cropped, box[0].int()
