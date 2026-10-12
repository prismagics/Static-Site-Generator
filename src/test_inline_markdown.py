import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class Test_Inline_Markdown(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        lst = split_nodes_delimiter(
            [TextNode("1 *2* 3", TextType.TEXT)], "*", TextType.BOLD
        )
        self.assertEqual(
            [
                TextNode("1 ", TextType.TEXT),
                TextNode("2", TextType.BOLD),
                TextNode(" 3", TextType.TEXT),
            ],
            lst,
        )

        with self.assertRaises(Exception):  # pyright: ignore
            split_nodes_delimiter(
                [TextNode("1 *2 3", TextType.TEXT)], "*", TextType.BOLD
            )

    def test_extract_markdown_images(self):

        ans = extract_markdown_images("brrrrrrrrr ![image](https://www.example.com)")

        self.assertEqual([("image", "https://www.example.com")], ans)

        ans = extract_markdown_images("lol")

        self.assertEqual([], ans)

        ans = extract_markdown_images("brrrrrrrrr ![](https://www.example.com)")

        self.assertEqual([("", "https://www.example.com")], ans)

    def test_extract_markdown_links(self):

        ans = extract_markdown_links("brrrrrrrrr [link](https://www.example.com)")

        self.assertEqual([("link", "https://www.example.com")], ans)

        ans = extract_markdown_links("brrrrrrrrr ![image](https://www.example.com)")

        self.assertEqual([], ans)

        ans = extract_markdown_links("brrrrrrrrr [](https://www.example.com)")

        self.assertEqual([("", "https://www.example.com")], ans)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        node = TextNode("Nada", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        self.assertListEqual([TextNode("Nada", TextType.TEXT)], new_nodes)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        node = TextNode("Nada", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        self.assertListEqual([TextNode("Nada", TextType.TEXT)], new_nodes)

    def test_text_to_textnode(self):
        ans = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertListEqual(
            text_to_textnodes(
                "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
            ),
            ans,
        )
