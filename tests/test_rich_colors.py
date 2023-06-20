"""Test Rich colors."""
# pylint: disable=E0401
import unittest
from maxgradient._rich import Rich


class RichTests(unittest.TestCase):
    """Test Rich colors."""
    def test_names(self):
        """Test Rich names."""
        self.assertIsInstance(Rich.NAMES, tuple)
        self.assertGreater(len(Rich.NAMES), 0)

    def test_hex(self):
        """Test Rich hex."""
        self.assertIsInstance(Rich.HEX, tuple)
        self.assertGreater(len(Rich.HEX), 0)

    def test_rgb(self):
        """Test Rich rgb."""
        self.assertIsInstance(Rich.RGB, tuple)
        self.assertGreater(len(Rich.RGB), 0)

if __name__ == "__main__":
    unittest.main()
