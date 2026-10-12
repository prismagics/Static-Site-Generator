import unittest

from gencontent import extract_title


class testGenContent(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(
            extract_title(
                """
# My Website

This is some text.

## About Me
Some more text.
            """
            ),
            "My Website",
        )
