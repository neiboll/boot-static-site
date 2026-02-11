import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_single(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_bold_single(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_italic_single(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " text")

    def test_split_multiple_delimiters(self):
        node = TextNode("Code `block1` and `block2` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "Code ")
        self.assertEqual(new_nodes[1].text, "block1")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[3].text, "block2")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[4].text, " here")

    def test_split_no_delimiter(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is plain text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_split_delimiter_at_start(self):
        node = TextNode("**bold** at start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " at start")

    def test_split_delimiter_at_end(self):
        node = TextNode("at end **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "at end ")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, "")

    def test_split_non_text_node_unchanged(self):
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Already bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

    def test_split_multiple_nodes(self):
        node1 = TextNode("First `code` node", TextType.TEXT)
        node2 = TextNode("Already bold", TextType.BOLD)
        node3 = TextNode("Second `code` node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[0].text, "First ")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[4].text, "Second ")

    def test_missing_closing_delimiter(self):
        node = TextNode("This has `unclosed code", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(context.exception), "Invalid markdown: missing closing delimiter")

    def test_empty_delimiter_content(self):
        node = TextNode("Empty `` delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Empty ")
        self.assertEqual(new_nodes[1].text, "")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " delimiters")


class TestExtractMarkdown(unittest.TestCase):
    # Tests for extract_markdown_images
    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![first](https://example.com/1.png) and ![second](https://example.com/2.png)"
        )
        self.assertListEqual(
            [("first", "https://example.com/1.png"), ("second", "https://example.com/2.png")],
            matches
        )

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This is text with no images")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty_alt(self):
        matches = extract_markdown_images("![](https://example.com/image.png)")
        self.assertListEqual([("", "https://example.com/image.png")], matches)

    def test_extract_markdown_images_with_links(self):
        # Should only extract images, not links
        matches = extract_markdown_images(
            "![image](https://example.com/img.png) and [link](https://example.com)"
        )
        self.assertListEqual([("image", "https://example.com/img.png")], matches)

    def test_extract_markdown_images_alt_with_spaces(self):
        matches = extract_markdown_images(
            "![alt text with spaces](https://example.com/image.png)"
        )
        self.assertListEqual([("alt text with spaces", "https://example.com/image.png")], matches)

    # Tests for extract_markdown_links
    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com)"
        )
        self.assertListEqual([("link", "https://www.example.com")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "[first](https://example.com/1) and [second](https://example.com/2)"
        )
        self.assertListEqual(
            [("first", "https://example.com/1"), ("second", "https://example.com/2")],
            matches
        )

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("This is text with no links")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_empty_text(self):
        matches = extract_markdown_links("[](https://example.com)")
        self.assertListEqual([("", "https://example.com")], matches)

    def test_extract_markdown_links_with_images(self):
        # Should only extract links, not images
        matches = extract_markdown_links(
            "[link](https://example.com) and ![image](https://example.com/img.png)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_links_text_with_spaces(self):
        matches = extract_markdown_links(
            "[link text with spaces](https://example.com)"
        )
        self.assertListEqual([("link text with spaces", "https://example.com")], matches)

    def test_extract_markdown_links_and_images_mixed(self):
        text = "![image](https://img.com/pic.png) text [link](https://example.com) more ![another](https://img.com/2.png)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertListEqual(
            [("image", "https://img.com/pic.png"), ("another", "https://img.com/2.png")],
            images
        )
        self.assertListEqual([("link", "https://example.com")], links)

    def test_extract_markdown_images_consecutive(self):
        matches = extract_markdown_images(
            "![first](url1.png)![second](url2.png)"
        )
        self.assertListEqual([("first", "url1.png"), ("second", "url2.png")], matches)

    def test_extract_markdown_links_consecutive(self):
        matches = extract_markdown_links(
            "[first](url1.com)[second](url2.com)"
        )
        self.assertListEqual([("first", "url1.com"), ("second", "url2.com")], matches)


if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    unittest.main()
