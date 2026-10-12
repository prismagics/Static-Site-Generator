import os
from pathlib import Path

from block_markdown import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise ValueError("no header found")


def generate_page(base_path, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown_contents = f.read()

    with open(template_path, "r") as f:
        template_contents = f.read()

    node = markdown_to_html_node(markdown_contents)
    html_str = node.to_html()
    title = extract_title(markdown_contents)
    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html_str)
    template_contents = template_contents.replace('href="/', f'href="{base_path}')
    template_contents = template_contents.replace('src"/', f'src="{base_path}')
    os.makedirs(os.path.dirname(dest_path) or ".", exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template_contents)


def generate_pages_recursive(base_path, dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        if os.path.isfile(os.path.join(dir_path_content, item)):
            dest_path = Path(dest_dir_path) / item
            dest_path = dest_path.with_suffix(".html")
            generate_page(
                base_path,
                os.path.join(dir_path_content, item),
                template_path,
                dest_path,
            )

        else:
            generate_pages_recursive(
                base_path,
                os.path.join(dir_path_content, item),
                template_path,
                os.path.join(dest_dir_path, item),
            )
