import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


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
        self.assertEqual(len(new_nodes), 2)  # Changed from 3
        self.assertEqual(new_nodes[0].text, "bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, " at start")

    def test_split_delimiter_at_end(self):
        node = TextNode("at end **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)  # Changed from 3
        self.assertEqual(new_nodes[0].text, "at end ")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

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
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Empty ")
        self.assertEqual(new_nodes[1].text, " delimiters")


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

class TestSplitImageLinks(unittest.TestCase):
    def test_split_links_single(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and another [second link](https://www.example2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.example2.com"),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("This is plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is plain text with no links", TextType.TEXT)], new_nodes)

    def test_split_links_at_start(self):
        node = TextNode("[link](https://example.com) at the start", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" at the start", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_at_end(self):
        node = TextNode("Text ending with [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text ending with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_links_only_link(self):
        node = TextNode("[link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "https://example.com")],
            new_nodes,
        )

    def test_split_links_consecutive(self):
        node = TextNode("[first](https://example.com)[second](https://example2.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "https://example.com"),
                TextNode("second", TextType.LINK, "https://example2.com"),
            ],
            new_nodes,
        )

    def test_split_links_non_text_node_unchanged(self):
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("Already bold", TextType.BOLD)], new_nodes)

    def test_split_links_multiple_nodes(self):
        node1 = TextNode("First [link](https://example.com) node", TextType.TEXT)
        node2 = TextNode("Already bold", TextType.BOLD)
        node3 = TextNode("Second [link](https://example2.com) node", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" node", TextType.TEXT),
                TextNode("Already bold", TextType.BOLD),
                TextNode("Second ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example2.com"),
                TextNode(" node", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_empty_link_text(self):
        node = TextNode("Text with [](https://example.com) empty link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://example.com"),
                TextNode(" empty link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_three_links(self):
        node = TextNode(
            "[first](url1) middle [second](url2) more [third](url3)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "url1"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("second", TextType.LINK, "url2"),
                TextNode(" more ", TextType.TEXT),
                TextNode("third", TextType.LINK, "url3"),
            ],
            new_nodes,
        )
class Test_text_to_textnodes(unittest.TestCase):
    def test_text_to_textnodes_plain_text(self):
        text = "This is just plain text"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("This is just plain text", TextType.TEXT)],
            nodes,
        )

    def test_text_to_textnodes_bold(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_italic(self):
        text = "This is _italic_ text"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_code(self):
        text = "This is `code` text"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_image(self):
        text = "This is text with an ![image](https://example.com/image.png)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            ],
            nodes,
        )

    def test_text_to_textnodes_link(self):
        text = "This is text with a [link](https://example.com)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            nodes,
        )

    def test_text_to_textnodes_all_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_multiple_bold(self):
        text = "**bold1** and **bold2**"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("bold1", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold2", TextType.BOLD),
            ],
            nodes,
        )

    def test_text_to_textnodes_multiple_images(self):
        text = "![first](url1.png) and ![second](url2.png)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "url1.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "url2.png"),
            ],
            nodes,
        )

    def test_text_to_textnodes_bold_and_italic(self):
        text = "**bold** and _italic_"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            nodes,
        )

    def test_text_to_textnodes_link_and_image(self):
        text = "[link](https://example.com) and ![image](https://example.com/pic.png)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/pic.png"),
            ],
            nodes,
        )    

    def test_text_to_textnodes_only_formatting(self):
        text = "**bold**"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("bold", TextType.BOLD)],
            nodes,
        )

    def test_text_to_textnodes_consecutive_formatting(self):
        text = "**bold**_italic_`code`"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
            ],
            nodes,
        )

    def test_text_to_textnodes_empty_string(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [],  
            nodes,
        )

if __name__ == "__main__":
    unittest.main()
