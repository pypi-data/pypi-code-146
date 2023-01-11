import unittest
import torch
from irisml.tasks.make_image_text_contrastive_model import Task


class TestMakeImageTextContrastiveModel(unittest.TestCase):
    def test_simple(self):
        image_model = torch.nn.Linear(3, 3)
        text_model = torch.nn.Linear(3, 3)

        inputs = Task.Inputs(image_model, text_model)
        outputs = Task(Task.Config(loss='clip')).execute(inputs)
        loss = outputs.model.training_step((torch.rand(2, 3), torch.rand(2, 3)), torch.tensor([0, 1]))
        self.assertEqual(len(loss['loss'].shape), 0)

        outputs = Task(Task.Config(loss='unicl')).execute(inputs)
        loss = outputs.model.training_step((torch.rand(2, 3), torch.rand(2, 3)), torch.tensor([0, 1]))
        self.assertEqual(len(loss['loss'].shape), 0)
