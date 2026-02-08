from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)

    node = HTMLNode("a", "Boot.dev", None, {"href": "https://boot.dev", "target": "_blank"})
    print(node)
    print(node.props_to_html())

main()
