import unittest
from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        md = "# Hello World"
        title = extract_title(md)
        self.assertEqual(title, "Hello World")

    def test_extract_title_with_content(self):
        md = """# My Title

    This is some content below the title.

    More content here."""
        title = extract_title(md)
        self.assertEqual(title, "My Title")

    def test_extract_title_multiple_headings(self):
        md = """# Main Title

    ## Subtitle

    ### Another heading"""
        title = extract_title(md)
        self.assertEqual(title, "Main Title")

    def test_extract_title_with_extra_spaces(self):
        md = "#    Title with spaces   "
        title = extract_title(md)
        self.assertEqual(title, "Title with spaces")

    def test_extract_title_not_first_line(self):
        md = """Some introductory text

    # The Real Title

    More content"""
        title = extract_title(md)
        self.assertEqual(title, "The Real Title")

    def test_extract_title_no_h1_raises_exception(self):
        md = """## This is h2

    ### This is h3

    Regular paragraph"""
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No header in MD.")

    def test_extract_title_empty_markdown_raises_exception(self):
        md = ""
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No header in MD.")

    def test_extract_title_no_space_after_hash(self):
        md = "#NoSpace"
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No header in MD.")

    def test_extract_title_with_formatting(self):
        md = "# Title with **bold** and *italic*"
        title = extract_title(md)
        self.assertEqual(title, "Title with **bold** and *italic*")

    def test_extract_title_only_h1(self):
        md = "# Just a title"
        title = extract_title(md)
        self.assertEqual(title, "Just a title")

    def test_extract_title_h1_after_blank_lines(self):
        md = """

    # Title After Blank Lines"""
        title = extract_title(md)
        self.assertEqual(title, "Title After Blank Lines")

    def test_extract_title_only_whitespace_before_h1(self):
        md = """   

    # Title"""
        title = extract_title(md)
        self.assertEqual(title, "Title")

    def test_extract_title_with_special_characters(self):
        md = "# Title with $pecial Ch@racters & Symbols!"
        title = extract_title(md)
        self.assertEqual(title, "Title with $pecial Ch@racters & Symbols!")

    def test_extract_title_multiple_hashes_not_h1(self):
        md = """#### Four hashes

    ### Three hashes

    ## Two hashes"""
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No header in MD.")

    def test_extract_title_hash_in_middle_of_line(self):
        md = """Regular text # with hash

    # Real Title"""
        title = extract_title(md)
        self.assertEqual(title, "Real Title")
