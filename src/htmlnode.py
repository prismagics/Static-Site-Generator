class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list | None = None,
        props: dict | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None or self.props == {}:
            return ""

        ans = ""

        for k in self.props:
            ans += f' {k}="{self.props[k]}"'

        return ans

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str | None, props: dict | None = None):
        super(LeafNode, self).__init__(tag, value, None, props)  # pyright: ignore

    def to_html(self):
        if self.value is None:
            raise ValueError("You must input a value")

        if self.tag is None:
            return self.value

        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"

        html_props = self.props_to_html()

        return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str | None, children: list | None, props: dict | None = None
    ) -> None:
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError("You must provide a tag")

        if self.children is None:
            raise ValueError("You must provide children")

        result = f"<{self.tag}"

        if self.props is None:
            result = f"<{self.tag}>"

        else:
            for k in self.props:
                result += f' {k}="{self.props[k]}"'
            result += ">"

        for child in self.children:
            result += child.to_html()

        result += f"</{self.tag}>"

        return result
