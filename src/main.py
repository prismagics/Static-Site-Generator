import sys

from copystatic import delete_dest, copystatic
from gencontent import generate_page, generate_pages_recursive
from textnode import TextNode, TextType


def main():
    if len(sys.argv) == 1:
        base_path = "/"
    else:
        base_path = sys.argv[1]

    delete_dest("docs")
    copystatic("static", "docs")
    generate_pages_recursive(base_path, "content", "template.html", "docs")


main()
