from enum import Enum
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown):
    lines = markdown.split("\n")
    if markdown.startswith("# ") or markdown.startswith("## ") or markdown.startswith("### ") or markdown.startswith("#### ") or markdown.startswith("##### ") or markdown.startswith("###### "):  
        return BlockType.HEADING
    elif markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE
    for line in lines:
        if not line.startswith(">"):
            break
    else:
        return BlockType.QUOTE
    for line in lines:
        if not line.startswith("- "):
            break
    else:
        return BlockType.UNORDERED_LIST 
    for i, line in enumerate(lines, 1):
        prefix = f'{i}. '
        if not line.startswith(prefix):
            break
    else:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = []
    parts = markdown.split("\n\n")
    for part in parts:
        block = part.strip()
        if block != "":
            blocks.append(block)
    return blocks

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def markdown_to_html_node(markdown):
    html_children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type_of_block = block_to_block_type(block)
        if type_of_block == BlockType.PARAGRAPH:
            content = " ".join(block.splitlines())
            children = text_to_children(content)
            html_children.append(ParentNode("p", children))

        elif type_of_block == BlockType.HEADING:
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break

            content = block[level + 1:] 
            children = text_to_children(content)
            heading_node = ParentNode(f"h{level}", children)
            html_children.append(heading_node)


        elif type_of_block == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            list_items = []
            for line in lines:
                text = line[2:]
                children = text_to_children(text)
                list_items.append(ParentNode("li", children))
            ul_node = ParentNode("ul", list_items)
            html_children.append(ul_node)

        elif type_of_block == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            list_items = []
            for line in lines:
                text = line[3:]
                children = text_to_children(text)
                list_items.append(ParentNode("li", children))
            ol_node = ParentNode("ol", list_items)
            html_children.append(ol_node)

        elif type_of_block == BlockType.CODE:
            content = block[3:-3].lstrip("\n")
            child = text_node_to_html_node(TextNode(content, TextType.TEXT))
            html_children.append(ParentNode("pre", [ParentNode("code", [child])]))

        elif type_of_block == BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                new_lines.append(line.lstrip(">").strip())
            content = " ".join(new_lines)
            children = text_to_children(content)
            quote_node = ParentNode("blockquote", children)
            html_children.append(quote_node)
        
    return ParentNode("div", html_children)











