"""Tests that the ColorReprHighlighter applies style to color names and hex codes"""
import unittest

from colorama import Style
from rich.segment import Segment
from rich.style import Style

from maxgradient.color import Color
from maxgradient.console import Console
from maxgradient.highlighter import ColorReprHighlighter


class TestColorHighlighter(unittest.TestCase):
    """Tests that the ColorReprHighlighter applies style to color names and hex codes"""

    def test_apply_style_to_color_names_and_hex_codes(self):
        """Tests that the ColorReprHighlighter applies style to color names and hex codes"""
        from rich.segment import Segment

        from maxgradient.console import Console

        console = Console(highlighter=ColorReprHighlighter())
        result = console.render_lines("magenta\n#f0f\nrgb(255, 0, 255)")
        expected = [
            Segment("magenta", Style(color=Color("#f0f"))),
            Segment("#f0f", Style(color=Color("#f0f"))),
            Segment("rgb(255, 0, 255)", Style(color=Color("#f0f"))),
        ]
        self.assertEqual(result, expected)

    # Tests that the ColorReprHighlighter applies style to RGB values
    def test_apply_style_to_RGB_values(self):
        """Tests that the ColorReprHighlighter applies style to RGB values"""
        console = Console(highlighter=ColorReprHighlighter())
        result = console.render_lines(
            ["rgb(0, 0, 255)", "rgb(0, 136, 255)", "rgb(0, 255, 0)"]
        )
        expected = "\x1b[1mrgb(0, 0, 255)\x1b[0m\n\x1b[1mrgb(0, 136, 255)\x1b[0m\n\x1b[1mrgb(0, 255, 0)\x1b[0m\n"
        self.assertEqual(result, expected)

    # Tests that the ColorReprHighlighter applies style to HTML tags
    def test_apply_style_to_HTML_tags(self):
        """Tests that the ColorReprHighlighter applies style to HTML tags"""
        console = Console(highlighter=ColorReprHighlighterhter())
        result = console.render_lines(["<div>", "<span>", "<p>"])
        expected = "\x1b[1m<div>\x1b[0m\n\x1b[1m<span>\x1b[0m\n\x1b[1m<p>\x1b[0m\n"
        self.assertEqual(result, expected)

    # Tests that the ColorReprHighlighter applies style to attribute names and values
    def test_apply_style_to_attribute_names_and_values(self):
        """Tests that the ColorReprHighlighter applies style to attribute names and values"""
        console = Console(highlighter=ColorReprHighlighter())
        result = console.render_lines(
            ['class="my-class"', 'id="my-id"', 'data-value="123"']
        )
        expected = '\x1b[1mclass\x1b[0m=\x1b[1m"my-class"\x1b[0m\n\x1b[1mid\x1b[0m=\x1b[1m"my-id"\x1b[0m\n\x1b[1mdata-value\x1b[0m=\x1b[1m"123"\x1b[0m\n'
        self.assertEqual(result, expected)

    # Tests that the ColorReprHighlighter applies style to braces and ellipsis
    def test_apply_style_to_braces_and_ellipsis(self):
        """Tests that the ColorReprHighlighter applies style to braces and ellipsis"""
        console = Console(highlighter=ColorReprHighlighter())
        result = console.render_lines(["{", "}", "..."])
        expected = "\x1b[1m{\x1b[0m\n\x1b[1m}\x1b[0m\n\x1b[1m...\x1b[0m\n"
        self.assertEqual(result, expected)

    # Tests that the ColorReprHighlighter applies style to IPv4, IPv6, EUI-48, EUI-64, and UUID
    def test_apply_style_to_IPv4_IPv6_EUI48_EUI64_and_UUID(self):
        """Tests that the ColorReprHighlighter applies style to IPv4, IPv6, EUI-48, EUI-64, and UUID"""
        console = Console(highlighter=ColorReprHighlighter())
        result = console.render_lines(
            [
                "192.168.0.1",
                "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
                "00-14-22-01-23-45",
                "00:14:22:01:23:45",
                "123e4567-e89b-12d3-a456-426655440000",
            ]
        )
        expected = "\x1b[1m192.168.0.1\x1b[0m\n\x1b[1m2001:0db8:85a3:0000:0000:8a2e:0370:7334\x1b[0m\n\x1b[1m00-14-22-01-23-45\x1b[0m\n\x1b[1m00:14:22:01:23:45\x1b[0m\n\x1b[1m123e4567-e89b-12d3-a456-426655440000\x1b[0m\n"
        self.assertEqual(result, expected)
