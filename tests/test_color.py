"""Test Rich colors."""
# pylint: disable=E0401
import unittest

from maxgradient._mode import Mode
from maxgradient.color import Color, ColorParseError
from maxgradient.gradient_color import GradientColor as GC


class ColorTests(unittest.TestCase):
    """Test Color class"""

    def test_color_creation_named(self):
        """Test Color creation with named color"""
        color = Color("red")
        self.assertEqual(color.name, "Red")

    def test_color_creation_hex(self):
        """Test Color creation with hex color"""
        color = Color("#ff00ff")
        self.assertEqual(color.hex, "#FF00FF")

    def test_color_creation_rgb(self):
        """Test Color creation with rgb color"""
        color = Color("rgb(255, 0, 255)")
        self.assertEqual(color.rgb_tuple, (255, 0, 255))

    # Tests that a Color object can be created with a valid RGB color
    def test_create_color_with_valid_rgb_color(self):
        color = Color("rgb(0, 0, 255)")
        self.assertEqual(color.name, "blue")
        self.assertEqual(color.mode, Mode.RGB)
        self.assertEqual(color.hex, "#0000FF")
        self.assertEqual(color.rgb, "rgb(0,0,255)")
        self.assertEqual(color.rgb_tuple, (0, 0, 255))

    def test_color_creation_x11(self):
        """Test Color creation with x11 color"""
        color = Color("deepskyblue")
        self.assertEqual(color.name, "deepskyblue")

    def test_color_creation_rich(self):
        """Test Color creation with rich color"""
        color = Color("magenta3")
        self.assertEqual(color.name, "magenta3")

    def test_color_creation_invalid(self):
        """Test Color creation with invalid color"""
        with self.assertRaises(Exception):
            color = Color("invalid_color")  # pylint: disable=W0612

    def test_color_equality(self):
        """Test Color equality"""
        color1 = Color("red")
        color2 = Color("red")
        self.assertEqual(color1, color2)

    def test_color_hash(self):
        """Test Color hash."""
        color = Color("red")
        hash_value = hash(color)
        self.assertIsInstance(hash_value, int)

    def test_color_repr(self):
        """Test Color representation."""
        color = Color("red")
        repr_str = repr(color)
        self.assertIsInstance(repr_str, str)

    def test_color_string_conversion(self):
        """Test Color string conversion."""
        color = Color("red")
        string = str(color)
        self.assertIsInstance(string, str)

    def test_color_rich_console_representation(self):
        """Test Color rich console representation."""
        color = Color("red")
        rich_table = color.__rich__()
        self.assertEqual(rich_table.caption, "\n\n")


    # Tests that a Color object can be created with a valid color string
    def test_create_color_valid_string(self):
        color = Color('#FF0000')
        self.assertEqual(color.original, '#FF0000')

    # Tests that the original color value can be accessed
    def test_access_original_color(self):
        color = Color('#FF0000')
        self.assertEqual(color.original, '#FF0000')

    # Tests that the red, green, and blue values can be accessed
    def test_access_rgb_values(self):
        color = Color('#FF0000')
        self.assertEqual(color.red, 255)
        self.assertEqual(color.green, 0)
        self.assertEqual(color.blue, 0)

    # Tests that a Color object cannot be created with an invalid color string
    def test_create_color_invalid_string(self):
        with self.assertRaises(ColorParseError):
            color = Color('invalid')

    # Tests that the red, green, or blue values cannot be set to values outside the valid range
    def test_set_rgb_values_outside_range(self):
        color = Color('#FF0000')
        with self.assertRaises(AssertionError):
            color.red = 300
        with self.assertRaises(AssertionError):
            color.green = -50
        with self.assertRaises(AssertionError):
            color.blue = 500

    # Tests that the contrast color for a color can be found
    def test_get_contrast_color(self):
        color = Color('#FF0000')
        contrast = color.get_contrast()
        self.assertEqual(contrast, '#000000')
if __name__ == "__main__":
    unittest.main()
if __name__ == "__main__":
    unittest.main()
