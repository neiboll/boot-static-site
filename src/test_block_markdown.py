import unittest
from block_markdown import BlockType, block_to_block_type, markdown_to_blocks, markdown_to_html_node, text_to_children  
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

class TestBlockToBlockType(unittest.TestCase):
    
    # Heading tests
    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
    
    def test_heading_h2(self):
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
    
    def test_heading_h3(self):
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
    
    def test_heading_h4(self):
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
    
    def test_heading_h5(self):
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
    
    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
    
    def test_not_heading_no_space(self):
        # This will currently return HEADING but might be a bug
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
    
    def test_not_heading_mid_line(self):
        self.assertEqual(block_to_block_type("Not a # heading"), BlockType.PARAGRAPH)
    
    # Code block tests
    def test_code_block_simple(self):
        code = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)
    
    def test_code_block_multiline(self):
        code = "```\ndef foo():\n    return 42\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)
    
    def test_code_block_empty(self):
        code = "```\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)
    
    def test_not_code_missing_closing(self):
        code = "```\nprint('hello')"
        self.assertEqual(block_to_block_type(code), BlockType.PARAGRAPH)
    
    def test_not_code_missing_opening(self):
        code = "print('hello')\n```"
        self.assertEqual(block_to_block_type(code), BlockType.PARAGRAPH)
    
    # Quote tests
    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type(">Quote"), BlockType.QUOTE)
    
    def test_quote_multiple_lines(self):
        quote = ">Line 1\n>Line 2\n>Line 3"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)
    
    def test_not_quote_missing_marker(self):
        quote = ">Line 1\nLine 2\n>Line 3"
        self.assertEqual(block_to_block_type(quote), BlockType.PARAGRAPH)
    
    def test_quote_with_spaces(self):
        quote = "> Quote with space\n> Another line"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)
    
    # Unordered list tests
    def test_unordered_list_single_item(self):
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)
    
    def test_unordered_list_multiple_items(self):
        list_text = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(list_text), BlockType.UNORDERED_LIST)
    
    def test_not_unordered_list_missing_marker(self):
        list_text = "- Item 1\nItem 2\n- Item 3"
        self.assertEqual(block_to_block_type(list_text), BlockType.PARAGRAPH)
    
    def test_not_unordered_list_wrong_marker(self):
        list_text = "* Item 1\n* Item 2"
        self.assertEqual(block_to_block_type(list_text), BlockType.PARAGRAPH)
    
    # Ordered list tests
    def test_ordered_list_single_item(self):
        self.assertEqual(block_to_block_type("1. Item 1"), BlockType.ORDERED_LIST)
    
    def test_ordered_list_multiple_items(self):
        list_text = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(list_text), BlockType.ORDERED_LIST)
    
    def test_not_ordered_list_wrong_numbers(self):
        list_text = "1. First\n3. Third\n2. Second"
        self.assertEqual(block_to_block_type(list_text), BlockType.PARAGRAPH)
    
    def test_not_ordered_list_missing_number(self):
        list_text = "1. First\nSecond\n3. Third"
        self.assertEqual(block_to_block_type(list_text), BlockType.PARAGRAPH)
    
    def test_ordered_list_ten_items(self):
        list_text = "\n".join([f"{i}. Item {i}" for i in range(1, 11)])
        self.assertEqual(block_to_block_type(list_text), BlockType.ORDERED_LIST)
    
    # Paragraph tests
    def test_paragraph_plain_text(self):
        self.assertEqual(block_to_block_type("Just plain text"), BlockType.PARAGRAPH)
    
    def test_paragraph_multiline(self):
        text = "Line 1\nLine 2\nLine 3"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    
    def test_paragraph_empty_string(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
    
    # Edge cases
    def test_newline_only(self):
        self.assertEqual(block_to_block_type("\n"), BlockType.PARAGRAPH)
    
    def test_multiple_newlines(self):
        self.assertEqual(block_to_block_type("\n\n\n"), BlockType.PARAGRAPH)
    
    def test_whitespace_only(self):
        self.assertEqual(block_to_block_type("   "), BlockType.PARAGRAPH)

class TestBlockToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
                html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()


