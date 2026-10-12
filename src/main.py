from copystatic import delete_dest, copystatic
from gencontent import generate_page, generate_pages_recursive
from textnode import TextNode, TextType


def main():
    delete_dest("public")
    copystatic("static", "public")
    generate_pages_recursive("content", "template.html", "public")


main()
