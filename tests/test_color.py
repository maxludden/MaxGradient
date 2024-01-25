import unittest

from maxgradient.color import Color


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

    def test_color_creation_with_color_object(self):
        original_color = Color("#ff0000")
        color = Color(original_color)
        self.assertEqual(color._original, "#ff0000")
        self.assertEqual(color._rgba.red, 1.0)
        self.assertEqual(color._rgba.green, 0.0)
        self.assertEqual(color._rgba.blue, 0.0)
        self.assertEqual(color._rgba, original_color._rgba)

    def test_color_creation_with_rich_color_object(self):
        original_color = Color("#ff0000").as_rich()
        color = Color(original_color)
        self.assertEqual(color._original, "#ff0000")
        self.assertEqual(color._rgba.red, 1.0)
        self.assertEqual(color._rgba.green, 0.0)
        self.assertEqual(color._rgba.blue, 0.0)
        self.assertEqual(color._rgba, original_color.triplet)

    def test_color_creation_with_invalid_value(self):
        with self.assertRaises(ValueError):
            Color(123)

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
        self.assertEqual(rich_representation, expected_representation)

    def test_as_rich(self):
        color = Color("#ff0000")
        rich_color = color.as_rich()
        self.assertEqual(rich_color.triplet, color._rgba)

    def test_as_style(self):
        color = Color("#ff0000")
        style = color.as_style()
        self.assertEqual(style.color.triplet, color._rgba)

    def test_as_bg_style(self):
        color = Color("#ff0000")
        bg_style = color.as_bg_style()
        self.assertEqual(bg_style.bgcolor.triplet, color._rgba)

    def test_get_contrast(self):
        color = Color("#ff0000")
        contrast_color = color.get_contrast()
        self.assertEqual(contrast_color.triplet, (0, 0, 0))

    def test_get_alpha_style(self):
        color = Color("#ff0000")
        alpha_style = color.get_alpha_style()
        self.assertEqual(alpha_style, color._rgba.as_triplet())

    def test_get_alpha_style_with_bg_color(self):
        color = Color("#ff0000")
        bg_color = Color("#0000ff")
        alpha_style = color.get_alpha_style(bg_color)
        expected_alpha_style = color._rgba.blend(bg_color._rgba)
        self.assertEqual(alpha_style, expected_alpha_style)


if __name__ == "__main__":
    unittest.main()
