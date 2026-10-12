from enum import Enum
from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(text: str) -> list[str]:
    split_text = text.split("\n\n")
    new_text = []
    for text_block in split_text:
        if text_block.strip() == "":
            continue

        new_text.append(text_block.strip())

    return new_text


def block_to_block_type(block: str):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(line.startswith(f"{index}. ") for index, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        html_nodes.append(block_to_html_node(block))
    return ParentNode("div", html_nodes)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def heading_to_html_node(block):
    heading_number = len(block.split(" ")[0])
    return ParentNode(
        f"h{heading_number}", text_to_children(block[heading_number + 1 :])
    )


def code_to_html_node(block):
    text = block[4:-3]
    html_node = text_node_to_html_node(TextNode(text, TextType.TEXT))
    return ParentNode("pre", [ParentNode("code", [html_node])])


def quote_to_html_node(block):
    lines = block.split("\n")
    for i in range(len(lines)):
        lines[i] = lines[i][2:]
    text = " ".join(lines)
    return ParentNode("blockquote", text_to_children(text))


def unordered_list_to_html_node(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        li_node = ParentNode("li", children)
        html_items.append(li_node)
    return ParentNode("ul", html_items)


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    html_items = []
    for index, line in enumerate(lines, start=1):
        text = line.removeprefix(f"{index}. ")
        children = text_to_children(text)
        li_node = ParentNode("li", children)
        html_items.append(li_node)
    return ParentNode("ol", html_items)
