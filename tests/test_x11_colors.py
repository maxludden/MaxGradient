"""Test X11 colors."""
# pylint: disable=E0401
import unittest
from maxgradient._x11 import X11


class X11ColorTestCase(unittest.TestCase):
    """Test X11 colors."""

    def test_names(self):
        """Test X11 names."""
        self.assertIsInstance(X11.NAMES, tuple)
        self.assertGreater(len(X11.NAMES), 0)

    def test_hex(self):
        """Test X11 hex."""
        self.assertIsInstance(X11.HEX, tuple)
        self.assertGreater(len(X11.HEX), 0)

    def test_rgb(self):
        """Test X11 rgb."""
        self.assertIsInstance(X11.RGB, tuple)
        self.assertGreater(len(X11.RGB), 0)


if __name__ == '__main__':
    unittest.main()
