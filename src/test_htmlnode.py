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

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click here", {"href": "https://www.example.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.example.com">Click here</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    def test_leaf_to_html_no_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "No value")

    def test_leaf_to_html_bold(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_leaf_to_html_italic(self):
        node = LeafNode("i", "Italic text")
        self.assertEqual(node.to_html(), "<i>Italic text</i>")

    def test_leaf_to_html_code(self):
        node = LeafNode("code", "print('hello')")
        self.assertEqual(node.to_html(), "<code>print('hello')</code>")

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "", {"src": "image.jpg", "alt": "A picture"})
        self.assertEqual(node.to_html(), '<img src="image.jpg" alt="A picture"></img>')

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode("a", "Link", {"href": "https://example.com", "target": "_blank", "class": "external"})
        html = node.to_html()
        self.assertIn('href="https://example.com"', html)
        self.assertIn('target="_blank"', html)
        self.assertIn('class="external"', html)
        self.assertTrue(html.startswith('<a '))
        self.assertTrue(html.endswith('>Link</a>'))

    def test_leaf_to_html_empty_string_value(self):
        node = LeafNode("span", "")
        self.assertEqual(node.to_html(), "<span></span>")

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello")
        self.assertEqual(repr(node), "LeafNode(p, Hello, None)")

    def test_leaf_repr_with_props(self):
        node = LeafNode("a", "Click", {"href": "url.com"})
        self.assertEqual(repr(node), "LeafNode(a, Click, {'href': 'url.com'})")

    def test_leaf_no_children(self):
        node = LeafNode("p", "Text")
        self.assertIsNone(node.children)

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Main Title")
        self.assertEqual(node.to_html(), "<h1>Main Title</h1>")

    def test_leaf_to_html_span_with_class(self):
        node = LeafNode("span", "Highlighted", {"class": "highlight"})
        self.assertEqual(node.to_html(), '<span class="highlight">Highlighted</span>')

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
