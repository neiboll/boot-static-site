import unittest

from textnode import TextNode, TextType


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
        
    
if __name__ == "__main__":
    unittest.main()
