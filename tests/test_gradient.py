import unittest
from typing import List

from maxgradient.color import Color
from maxgradient.gradient import Gradient
from rich.style import Style


class TestGradient(unittest.TestCase):
    def test_text_property(self):
        # Test that the text property returns the correct value
        g = Gradient(text="Hello")
        self.assertEqual(g._text, ["Hello"])

    def test_hues_property(self):
        # Test that the hues property returns the correct value
        g = Gradient(hues=5)
        self.assertEqual(g.hues, 5)

    def test_style_property(self):
        # Test that the style property returns the correct value
        g = Gradient(style="bold")
        self.assertEqual(g.style, Style(bold=True))

    def test_rainbow_property(self):
        # Test that the rainbow property returns the correct value
        g = Gradient(rainbow=True)
        self.assertTrue(g.rainbow)

    def test_colors_property(self):
        # Test that the colors property returns the correct value
        colors = ["red", "green", "blue"]
        repr_colors: List[Color] = [Color(color) for color in colors]
        g = Gradient(colors=colors)  # type: ignore
        self.assertEqual(g.colors, repr_colors)

    def test_text_setter(self):
        # Test that the text setter sets the correct value
        g = Gradient()
        g.text = "Hello"
        self.assertEqual(g.text, "Hello")

    def test_hues_setter(self):
        # Test that the hues setter sets the correct value
        g = Gradient()
        g.hues = 5
        self.assertEqual(g.hues, 5)

    def test_style_setter(self):
        # Test that the style setter sets the correct value
        g = Gradient()
        g.style = Style(bold=True)
        self.assertEqual(str(g.style), "bold")

    def test_rainbow_setter(self):
        # Test that the rainbow setter sets the correct value
        g = Gradient()
        g.rainbow = True
        self.assertTrue(g.rainbow)

    def test_colors_setter(self):
        # Test that the colors setter sets the correct value
        colors = ["red", "green", "blue"]
        g = Gradient()
        g.colors = colors  # type: ignore
        self.assertEqual(g.colors, [Color(color) for color in colors])


if __name__ == "__main__":
    unittest.main()
