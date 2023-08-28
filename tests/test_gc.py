"""Gradient Color Tests `maxgradient/tests/test_gc.py`"""
# pylint: disable=W0105

import unittest
from maxgradient._gc import GradientColor


class TestGetNames(unittest.TestCase):
    """Code Analysis

    Objective:
    The 'get_names' method is a class method of the 'GradientColor' class that aims to retrieve the gradient colors.

    Inputs:
    - 'cls': the class itself.

    Flow:
    1. The method retrieves the gradient colors from the 'NAMES' attribute of the class.
    2. The method returns the gradient colors as a tuple of strings.

    Outputs:
    - A tuple of strings representing the gradient colors.

    Additional aspects:
    - The method uses the 'lru_cache' decorator to cache the results of the method calls, improving performance by avoiding unnecessary computations.
    - The method is a class method, meaning it can be called on the class itself, rather than an instance of the class.
    """

    def test_happy_path_returns_tuple_of_strings(self):
        """Tests that the method returns a tuple of strings."""
        result = GradientColor.get_names()
        self.assertIsInstance(result, tuple)
        for color in result:
            self.assertIsInstance(color, str)

    def test_happy_path_returns_same_result_multiple_times(self):
        """Tests that the method returns the same result when called \
            multiple times."""
        result1 = GradientColor.get_names()
        result2 = GradientColor.get_names()
        self.assertEqual(result1, result2)

    def test_edge_case_non_string_color_raises_type_error(self):
        """Tests that the method raises a TypeError when called with a color that is not a string"""
        with self.assertRaises(TypeError):
            GradientColor.get_names(123) # pylint: disable=E1121

    def test_general_behavior_returns_correct_number_of_colors(self):
        """Tests that the method returns the correct number of colors."""
        result = GradientColor.get_names()
        self.assertEqual(len(result), len(GradientColor.NAMES))
