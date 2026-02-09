import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_not_eq_diferent_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_diferent_url(self):
        node_url = TextNode("some text", TextType.TEXT, "https://www.boot.dev/")
        node_url2 = TextNode("some text", TextType.TEXT, "https://exercism.org/")
        self.assertNotEqual(node_url, node_url2)

    def test_not_eq_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_with_url_none(self):
        node = TextNode("some text", TextType.TEXT, None)
        node2 = TextNode("some text", TextType.TEXT, None)
        self.assertEqual(node, node2)

    def test_not_eq_one_url_none(self):
        node = TextNode("some text", TextType.TEXT, "https://www.boot.dev/")
        node2 = TextNode("some text", TextType.TEXT, None)
        self.assertNotEqual(node, node2)

    def test_eq_with_same_url(self):
        node = TextNode("some text", TextType.TEXT, "https://www.boot.dev/")
        node2 = TextNode("some text", TextType.TEXT, "https://www.boot.dev/")
        self.assertEqual(node, node2)
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_code(self):
        node = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello')")
        self.assertEqual(html_node.to_html(), "<code>print('Hello')</code>")

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})
        self.assertEqual(html_node.to_html(), '<a href="https://www.example.com">Click here</a>')

    def test_image(self):
        node = TextNode("A beautiful sunset", TextType.IMAGE, "https://example.com/sunset.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/sunset.jpg", "alt": "A beautiful sunset"})
        self.assertEqual(html_node.to_html(), '<img src="https://example.com/sunset.jpg" alt="A beautiful sunset"></img>')

    def test_text_to_html_output(self):
        node = TextNode("Plain text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "Plain text")

    def test_invalid_text_type(self):
        # Create a TextNode with an invalid/unknown text_type
        node = TextNode("Some text", "INVALID_TYPE")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "TextNode is getting wrong values") 


if __name__ == "__main__":
    unittest.main()
