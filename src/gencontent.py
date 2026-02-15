import os
from htmlnode import HTMLNode
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("# "):  
            return stripped_line[2:].strip()
    raise Exception("No header in MD.")

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    with open(from_path, 'r') as f:
        markdown = f.read()
    with open(template_path, 'r') as f:
        template = f.read()

    title = extract_title(markdown)
    html_content = markdown_to_html_node(markdown).to_html()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)
        
    dest_dir = os.path.dirname(dest_path)

    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template)
