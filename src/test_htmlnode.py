import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode(None, None, None, {"href": "https", "target": "_blank"})
        self.assertEqual(' href="https" target="_blank"', node1.props_to_html())
        node2 = HTMLNode(None, None, None, {})
        self.assertEqual("", node2.props_to_html())
        node3 = HTMLNode()
        self.assertEqual("", node3.props_to_html())
        node4 = LeafNode("a", None)
        with self.assertRaises(ValueError):
            node4.to_html()
        node5 = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
        self.assertEqual('<a href="https://www.google.com">Click me!</a>', node5)
        node6 = LeafNode("p", "This is a paragraph of text.").to_html()
        self.assertEqual("<p>This is a paragraph of text.</p>", node6)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        child_node = LeafNode("a", "yes")
        parent_node = ParentNode("div", [child_node])

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
