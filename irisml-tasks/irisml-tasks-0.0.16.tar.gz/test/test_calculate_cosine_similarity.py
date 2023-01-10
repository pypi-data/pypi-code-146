import unittest
import torch
from irisml.tasks.calculate_cosine_similarity import Task


class TestCalculcateCosineSimilarity(unittest.TestCase):
    def test_identical_vectors(self):
        one_vector = torch.randn(1, 64)
        tensor0 = one_vector.expand(10, 64)
        tensor1 = one_vector.expand(8, 64)
        outputs = Task(Task.Config()).execute(Task.Inputs(tensor0, tensor1))
        self.assertEqual(outputs.cosine_similarity.shape, (10, 8))
        max_diff = torch.max(torch.abs(outputs.cosine_similarity - 1.0))
        self.assertAlmostEqual(float(max_diff), 0, places=6)  # Assert that cosine_similarity is 1 for all combinations.

    def test_zeros(self):
        tensor = torch.zeros((10, 64))
        outputs = Task(Task.Config()).execute(Task.Inputs(tensor, tensor))
        self.assertEqual(outputs.cosine_similarity.shape, (10, 10))
        self.assertAlmostEqual(float(torch.max(torch.abs(outputs.cosine_similarity))), 0)

    def test_random(self):
        tensor0 = torch.randn((3, 64))
        tensor1 = torch.randn((5, 64))
        outputs = Task(Task.Config()).execute(Task.Inputs(tensor0, tensor1))
        self.assertTrue(torch.all((-1 <= outputs.cosine_similarity) & (outputs.cosine_similarity <= 1)))
