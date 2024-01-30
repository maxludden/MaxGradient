import unittest
from rich.color import blend_rgb
from rich.color_triplet import ColorTriplet
from maxgradient.color import Color
from rich.console import Console
from rich.traceback import install as tr_install

console = Console()
tr_install(console=console)


class TestColor(unittest.TestCase):
    def test_color_creation_with_tuple(self):
        color = Color((255, 0, 0))
        self.assertEqual(color._original, (255, 0, 0))
        self.assertEqual(color._rgba.red, 1.0)
        self.assertEqual(color._rgba.green, 0.0)
        self.assertEqual(color._rgba.blue, 0.0)

    def test_color_creation_with_string(self):
        color = Color("#ff0000")
        self.assertEqual(color._original, "#ff0000")
        self.assertEqual(color._rgba.red, 1.0)
        self.assertEqual(color._rgba.green, 0.0)
        self.assertEqual(color._rgba.blue, 0.0)

    def test_color_creation_with_invalid_value(self):
        with self.assertRaises(ValueError):
            Color(123)

    def test_get_contrast(self):
        color = Color("#ff0000")
        contrast_color = color.get_contrast()
        self.assertEqual(contrast_color.triplet, (0, 0, 0))

    def test_get_alpha_style(self):
        color = Color("#ff0000")
        alpha_style = color.get_alpha_style()
        self.assertEqual(alpha_style, color._rgba.as_triplet())

    def test_get_alpha_style_with_bg_color(self):
        color = Color("rgb(255,0,0,0.5)")
        bg_color = Color("#000000")
        alpha_style = color.get_alpha_style(bg_color)
        expected_alpha_style = blend_rgb(
            ColorTriplet(255,0,0),
            ColorTriplet(0,0,0),
            0.5
        )
def test_rich_representation(self):
    color = Color("#ff0000")
    rich_representation = color.__rich__()
    expected_representation = (
        "Color("
        "[bold #ffffff]Color[bold #ffffff]"
        "("
        "[bold #ff0000]#ff0000[bold #ff0000]"
        ")[bold #ffffff]"
        ")"
    )
    print("rich_representation:", rich_representation)
    print("expected_representation:", expected_representation)
    self.assertEqual(rich_representation, expected_representation)
