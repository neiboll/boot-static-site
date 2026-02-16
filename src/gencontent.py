import os
from pathlib import Path
from htmlnode import HTMLNode
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("# "):  
            return stripped_line[2:].strip()
    raise Exception("No header in MD.")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    with open(from_path, 'r') as f:
        markdown = f.read()
    with open(template_path, 'r') as f:
        template = f.read()

    title = extract_title(markdown)
    html_content = markdown_to_html_node(markdown).to_html()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)

    page_html = template.replace('href="/', f'href="{basepath}')
    page_html = page_html.replace('src="/', f'src="{basepath}')
        
    dest_dir = os.path.dirname(dest_path)

    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        src = os.path.join(dir_path_content, entry)
        dst = os.path.join(dest_dir_path, entry)

        if os.path.isfile(src) and entry.endswith(".md"):
            dest_path = os.path.splitext(dst)[0] + ".html"
            generate_page(src, template_path, dest_path, basepath)
        elif os.path.isdir(src):
            os.makedirs(dst, exist_ok=True)
            generate_pages_recursive(src, template_path, dst, basepath)
