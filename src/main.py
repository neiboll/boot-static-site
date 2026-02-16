from textnode import TextNode, TextType
from htmlnode import HTMLNode
import os
import shutil
from copystatic import copy_files_recursive
from gencontent import extract_title, generate_page, generate_pages_recursive

def main():

    dir_path_static = "./static"
    dir_path_public = "./public"

    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    os.mkdir(dir_path_public)

    copy_files_recursive(dir_path_static, dir_path_public)
 
    print("Generating page...")
    generate_pages_recursive("content", "template.html", "public")

main()
