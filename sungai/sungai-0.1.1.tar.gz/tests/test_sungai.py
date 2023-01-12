"""
Sungai.

- Project URL: https://github.com/hugocartwright/sungai
"""
import unittest

from sungai.sungai import DirectoryRater, depth_set, get_r2_ln, nested_sum


class TestUtils(unittest.TestCase):
    """Test sungai utils."""

    def test_get_r2_ln(self):
        """Test linear regression."""
        assert round(get_r2_ln([17, 7, 4, 3])[2], 5) == 0.94668
        assert get_r2_ln([1, 0])[2] == 1.0
        assert get_r2_ln([0, 0])[2] == 0.0
        assert get_r2_ln([2, 2, 2, 2, 2])[2] == 0.0

    def test_nested_sum(self):
        """Test sum of nested list."""
        assert nested_sum([3, [4, 4, 2, 0], 0, 2, [3, [4, 2]]]) == 24
        assert nested_sum([3, 4, 5]) == 12

    def depth_set(self):
        """Test depth_set."""
        assert depth_set(
            [],
            0,
            1,
        ) == [1]

        assert depth_set(
            [[], 0, 3],
            1,
            2,
        ) == [[2], 0, 3]

        assert depth_set(
            [[2], 3, 0],
            1,
            0,
        ) == [[0, 2], 3, 0]

        assert depth_set(
            [[[], 2, 0], 3, 0],
            2,
            2,
        ) == [[[[2], 2, 0], 3, 0], 3, 0]


class TestDirectoryRater(unittest.TestCase):
    """Test DirectoryRater."""

    def test_get_structure(self):
        """Test get_structure method."""
        directory_rater = DirectoryRater(
            "tests/directory_tree",
        )
        directory_rater.run(False, 1.0, quiet=True)

        correct_structure = [32, 8, 6, 2, 0]
        assert directory_rater.structure == correct_structure

    def test_score_nodes(self):
        """Test score_nodes method."""

    def test_run(self):
        """Test sungai output."""
        directory_rater = DirectoryRater(
            "tests/directory_tree",
        )
        assert directory_rater.run(False, 0.8786859111811026, quiet=True) == 0

        directory_rater = DirectoryRater(
            "tests/directory_tree",
        )
        assert directory_rater.run(False, 1.0, quiet=True) == 1

        nodes = [
            [2, 0],
            [2, 2, 0],
            [5, 0],
            [1, 0],
            [5, 1, 1, 0],
            [7, 0, 0],
            [1, 0],
            [17, 1, 0],
            [18, 7, 4, 3, 0],
            [1, 0],
            [1, 0],
            [1, 1, 0, 0],
            [2, 2, 0],
            [2, 0],
            [1, 0],
            [4, 2, 1, 1, 0],
            [2, 0],
            [32, 8, 6, 2, 0],
        ]

        for i, node in enumerate(directory_rater.get_nodes()):
            assert node[1] == sum(nodes[i])
