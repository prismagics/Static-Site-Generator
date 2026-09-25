import re
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    result = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            result.append(old_node)
            continue

        if old_node.text.count(delimiter) % 2 != 0:
            raise Exception("delimiter must be in the text")

        new_text = old_node.text.split(delimiter)

        for i in range(0, len(new_text)):
            if i % 2 == 0:
                result.append(TextNode(new_text[i], TextType.TEXT))

            else:
                result.append(TextNode(new_text[i], text_type))

    return result


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)

        if images == []:
            if old_node.text != "":
                result.append(old_node)
            continue

        remaining = old_node.text

        for desc, img in images:
            sections = remaining.split(f"![{desc}]({img})", 1)
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.TEXT))

            result.append(TextNode(desc, TextType.IMAGE, img))

            remaining = sections[1]

        if remaining != "":
            result.append(TextNode(remaining, TextType.TEXT))

    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)

        if links == []:
            if old_node.text != "":
                result.append(old_node)
            continue

        remaining = old_node.text

        for desc, link in links:
            sections = remaining.split(f"[{desc}]({link})", 1)
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.TEXT))

            result.append(TextNode(desc, TextType.LINK, link))

            remaining = sections[1]

        if remaining != "":
            result.append(TextNode(remaining, TextType.TEXT))

    return result


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
