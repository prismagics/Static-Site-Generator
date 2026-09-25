from textnode import TextNode, TextType


def main():
    obj = TextNode("hallo", TextType.LINK, "https://www.boot.dev")
    print(obj)


main()
