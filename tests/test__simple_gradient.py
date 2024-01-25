import unittest

from maxgradient._simple_gradient import SimpleGradient
from rich import console
from rich.style import Style
from maxgradient.color import Color
from rich.text import Span
from rich.color import ColorType, ColorTriplet


class TestSimpleGradient(unittest.TestCase):
    def setUp(self):
        self.console = console.Console()

    def test_text_property(self):
        gradient = SimpleGradient("Hello World", color1="red", color2="blue")
        self.assertEqual(gradient.text, "Hello World")

    def test_text_property_with_text_object(self):
        text = "Hello World"
        gradient = SimpleGradient(text, color1="red", color2="blue")
        self.assertEqual(gradient.plain, "Hello World")

    def test_text_property_with_empty_string(self):
        with self.assertRaises(ValueError):
            SimpleGradient("", color1="red", color2="blue")

    def test_text_property_with_none(self):
        with self.assertRaises(ValueError):
            SimpleGradient(None, color1="red", color2="blue")

    def test_style_property(self):
        gradient = SimpleGradient(
            "Hello World", color1="red", color2="blue", style="bold"
        )
        self.assertEqual(gradient.style, Style(bold=True))

    def test_style_property_with_none(self):
        gradient = SimpleGradient(
            "Hello World", color1="red", color2="blue", style=None
        )
        self.assertEqual(gradient.style, Style())


if __name__ == "__main__":
    unittest.main()
