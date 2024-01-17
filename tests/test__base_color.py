import unittest

from abc_color._base_color import BaseColor, ColorTriplet, Mode, OutputFormat


class TestBaseColor(unittest.TestCase):
    def setUp(self):
        self.color = BaseColor()

    def test_names(self):
        self.assertIsInstance(self.color.NAMES, tuple)
        self.assertGreater(len(self.color.NAMES), 0)

    def test_hex(self):
        self.assertIsInstance(self.color.HEX, str)

    def test_rgb(self):
        self.assertIsInstance(self.color.RGB, tuple)
        self.assertGreater(len(self.color.RGB), 0)

    def test_triplets(self):
        self.assertIsInstance(self.color.TRIPLETS, tuple)
        self.assertGreater(len(self.color.TRIPLETS), 0)

    def test_find_index(self):
        with self.assertRaises(ValueError):
            self.color.find_index("nonexistent color")

    def test_name(self):
        self.color.name = "red"
        self.assertEqual(self.color.name, "red")

    def test_red(self):
        with self.assertRaises(AssertionError):
            self.color.red = 300
        self.color.red = 200
        self.assertEqual(self.color.red, 200)

    def test_green(self):
        with self.assertRaises(AssertionError):
            self.color.green = 300
        self.color.green = 200
        self.assertEqual(self.color.green, 200)

    def test_blue(self):
        with self.assertRaises(AssertionError):
            self.color.blue = 300
        self.color.blue = 200
        self.assertEqual(self.color.blue, 200)

    def test_mode(self):
        self.color.mode = Mode.RGB
        self.assertEqual(self.color.mode, Mode.RGB)

    def test_hex_property(self):
        self.color.red = 255
        self.color.green = 255
        self.color.blue = 255
        self.assertEqual(self.color.hex, "#FFFFFF")

    def test_rgb_property(self):
        self.color.red = 255
        self.color.green = 255
        self.color.blue = 255
        self.assertEqual(self.color.rgb, "rgb(255,255,255)")

    def test_triplet_property(self):
        self.color.triplet = ColorTriplet(255, 255, 255)
        self.assertEqual(self.color.triplet, ColorTriplet(255, 255, 255))

    def test_darken(self):
        self.color.triplet = ColorTriplet(255, 255, 255)
        self.assertIsInstance(
            self.color.darken(0.5, OutputFormat.COLOR_TRIPLET), ColorTriplet
        )

    def test_lighten(self):
        self.color.triplet = ColorTriplet(0, 0, 0)
        self.assertIsInstance(
            self.color.lighten(0.5, OutputFormat.COLOR_TRIPLET), ColorTriplet
        )


if __name__ == "__main__":
    unittest.main()
