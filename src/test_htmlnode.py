import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple(self):
        node = HTMLNode(
            "a",
            "Boot.dev",
            None,
            {"href": "https://boot.dev", "target": "_blank"},
        )
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://boot.dev" target="_blank"')

    def test_props_to_html_none(self):
        node = HTMLNode("p", "Hello", None, None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_props_to_html_single(self):
        node = HTMLNode("img", None, None, {"alt": "bear"})
        result = node.props_to_html()
        self.assertEqual(result, ' alt="bear"')
    
    def test_repr_all_fields(self):
        node = HTMLNode("p", "Hello world", None, {"class": "greeting"})
        expected = "HTMLNode: p, Hello world, None, {'class': 'greeting'}"
        self.assertEqual(repr(node), expected)

    def test_repr_only_tag(self):
        node = HTMLNode("div")
        expected = "HTMLNode: div, None, None, None"
        self.assertEqual(repr(node), expected)

    def test_repr_with_children(self):
        child = HTMLNode("span", "child text")
        node = HTMLNode("div", None, [child], None)
        expected = f"HTMLNode: div, None, [{repr(child)}], None"
        self.assertEqual(repr(node), expected)

    def test_repr_tag_and_value(self):
        node = HTMLNode("h1", "Title")
        expected = "HTMLNode: h1, Title, None, None"
        self.assertEqual(repr(node), expected)

    def test_repr_with_props(self):
        node = HTMLNode("a", "Click here", None, {"href": "https://example.com", "target": "_blank"})
        expected = "HTMLNode: a, Click here, None, {'href': 'https://example.com', 'target': '_blank'}"
        self.assertEqual(repr(node), expected)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
