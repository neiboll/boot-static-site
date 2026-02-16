import sys
import os
import shutil
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from copystatic import copy_files_recursive
from gencontent import extract_title, generate_page, generate_pages_recursive

def main():

    dir_path_static = "./static"
    dir_path_docs = "./docs"
    
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    os.mkdir(dir_path_docs)

    copy_files_recursive(dir_path_static, dir_path_docs)
 
    print("Generating page...")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()
