"""Test Rich colors."""
# pylint: disable=E0401
import unittest

from maxgradient.color import Color


class ColorTests(unittest.TestCase):
    """Test Color class"""

    def test_color_creation_named(self):
        """Test Color creation with named color"""
        color = Color("red")
        self.assertEqual(color.name, "red")

    def test_color_creation_hex(self):
        """Test Color creation with hex color"""
        color = Color("#ff00ff")
        self.assertEqual(color.hex, "#ff00ff")

    def test_color_creation_rgb(self):
        """Test Color creation with rgb color"""
        color = Color("rgb(255, 0, 255)")
        self.assertEqual(color.rgb_tuple, (255, 0, 255))

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
            color = Color("invalid_color") # pylint: disable=W0612

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


if __name__ == "__main__":
    unittest.main()
if __name__ == "__main__":
    unittest.main()
