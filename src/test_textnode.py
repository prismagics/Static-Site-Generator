import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node_1 = TextNode("This is a text node", TextType.BOLD, "http://boot.dev")
        node_2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node_1, node_2)
        node_3 = TextNode("1", TextType.BOLD)
        node_4 = TextNode("2", TextType.BOLD)
        self.assertNotEqual(node_3, node_4)
        node_5 = TextNode("1", TextType.ITALIC)
        node_6 = TextNode("1", TextType.TEXT)
        self.assertNotEqual(node_5, node_6)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        node = TextNode("bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold")
        node = TextNode("italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic")


if __name__ == "__main__":
    unittest.main()
