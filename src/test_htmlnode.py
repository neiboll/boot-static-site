import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("p", "First paragraph")
        child2 = LeafNode("p", "Second paragraph")
        child3 = LeafNode("p", "Third paragraph")
        parent_node = ParentNode("div", [child1, child2, child3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>First paragraph</p><p>Second paragraph</p><p>Third paragraph</p></div>"
        )

    def test_to_html_with_props(self):
        child = LeafNode("span", "text")
        parent_node = ParentNode("div", [child], {"class": "container", "id": "main"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main"><span>text</span></div>'
        )

    def test_to_html_no_tag_raises_error(self):
        child = LeafNode("span", "text")
        parent_node = ParentNode(None, [child])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "No tag found")

    def test_to_html_no_children_raises_error(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "Children is missing a value")

    def test_to_html_empty_children_list(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_nested_parents(self):
        leaf1 = LeafNode("b", "bold text")
        leaf2 = LeafNode("i", "italic text")
        child_parent = ParentNode("p", [leaf1, leaf2])
        grandchild_parent = ParentNode("div", [child_parent])
        parent_node = ParentNode("section", [grandchild_parent])
        self.assertEqual(
            parent_node.to_html(),
            "<section><div><p><b>bold text</b><i>italic text</i></p></div></section>"
        )

    def test_to_html_mixed_leaf_and_parent_children(self):
        leaf1 = LeafNode("span", "Hello")
        inner_parent = ParentNode("b", [LeafNode(None, "world")])
        leaf2 = LeafNode("span", "!")
        parent_node = ParentNode("p", [leaf1, inner_parent, leaf2])
        self.assertEqual(
            parent_node.to_html(),
            "<p><span>Hello</span><b>world</b><span>!</span></p>"
        )

    def test_to_html_leaf_with_props_inside_parent(self):
        child = LeafNode("a", "Click here", {"href": "https://example.com"})
        parent_node = ParentNode("div", [child])
        self.assertEqual(
            parent_node.to_html(),
            '<div><a href="https://example.com">Click here</a></div>'
        )
