#!/usr/bin/env python3
"""Render the CV HTML template with values from the YAML data file."""

from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import yaml


PLACEHOLDER = re.compile(r"\{([^{}]+)\}")


@dataclass
class Node:
    tag: str | None = None
    start_tag: str = ""
    end_tag: str = ""
    children: list["Node"] = field(default_factory=list)
    text: str = ""


class TemplateParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.root = Node()
        self.stack = [self.root]

    def handle_decl(self, decl: str) -> None:
        self.stack[-1].children.append(Node(text=f"<!{decl}>"))

    def handle_comment(self, data: str) -> None:
        self.stack[-1].children.append(Node(text=f"<!--{data}-->"))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = Node(tag=tag, start_tag=self.get_starttag_text() or f"<{tag}>")
        self.stack[-1].children.append(node)
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.stack[-1].children.append(Node(tag=tag, start_tag=self.get_starttag_text() or f"<{tag} />"))

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                self.stack[index].end_tag = f"</{tag}>"
                del self.stack[index:]
                return

    def handle_data(self, data: str) -> None:
        self.stack[-1].children.append(Node(text=data))

    def handle_entityref(self, name: str) -> None:
        self.handle_data(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.handle_data(f"&#{name};")


def attributes(node: Node) -> dict[str, str]:
    match = re.match(r"<[^\s>]+(?P<attrs>.*?)\s*/?>$", node.start_tag, re.DOTALL)
    if not match:
        return {}
    return dict(re.findall(r"([\w:-]+)\s*=\s*['\"]([^'\"]*)['\"]", match.group("attrs")))


def lookup(name: str, context: list[Any], fallback: dict[str, Any]) -> Any:
    for value in context:
        if isinstance(value, dict) and name in value:
            return value[name]
    person = fallback.get("person", {})
    if isinstance(person, dict) and name in person:
        return person[name]
    urls = person.get("urls", {}) if isinstance(person, dict) else {}
    if isinstance(urls, dict) and name in urls:
        return urls[name]
    return fallback.get(name, "")


def replace_fields(value: str, context: list[Any], fallback: dict[str, Any]) -> str:
    def replacement(match: re.Match[str]) -> str:
        field_name = match.group(1).strip()
        value = lookup(field_name, context, fallback)
        if value == "" or value is None:
            return ""
        return html.escape(str(value), quote=True)

    return PLACEHOLDER.sub(replacement, value)


def render_about(node: Node, data: dict[str, Any]) -> str:
    about = str(data.get("about", ""))
    paragraphs = "".join(f"<p>{html.escape(line.strip())}</p>" for line in about.splitlines() if line.strip())
    return node.start_tag + paragraphs + node.end_tag


def list_name(node: Node) -> str | None:
    class_name = attributes(node).get("class", "")
    return class_name.split()[0] if class_name else None


def render_raw(node: Node) -> str:
    if node.tag is None:
        return node.text
    return node.start_tag + "".join(render_raw(child) for child in node.children) + node.end_tag


def render(node: Node, context: list[Any], data: dict[str, Any]) -> str:
    if node.tag is None:
        return replace_fields(node.text, context, data)

    if node.tag == "style":
        return render_raw(node)

    if node.tag == "div" and attributes(node).get("class") == "about":
        return render_about(node, data)

    if node.tag == "ul":
        name = list_name(node)
        values = lookup(name or "", context, data)
        if isinstance(values, list):
            if name == "experience":
                values = values[: int(data["n"])]
            rendered = []
            for item in values:
                item_name = name[:-1] if name.endswith("s") else name
                item_context = [{item_name: item}, item, *context] if not isinstance(item, dict) else [item, *context]
                rendered.append("".join(render(child, item_context, data) for child in node.children))
            return node.start_tag + "".join(rendered) + node.end_tag

    rendered_children = "".join(render(child, context, data) for child in node.children)
    return replace_fields(node.start_tag, context, data) + rendered_children + node.end_tag


def generate(template_path: Path, data_path: Path, output_path: Path) -> None:
    data = yaml.safe_load(data_path.read_text(encoding="utf-8")) or {}
    data["n"] = data.get("n", 5)
    template = template_path.read_text(encoding="utf-8")
    parser = TemplateParser()
    parser.feed(template)
    output_path.write_text("".join(render(node, [data], data) for node in parser.root.children), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", type=Path, default=Path(__file__).with_name("template.html"))
    parser.add_argument("--data", type=Path, default=Path(__file__).with_name("data.yaml"))
    parser.add_argument("--output", type=Path, default=Path(__file__).parent.parent / "index.html")
    args = parser.parse_args()
    generate(args.template, args.data, args.output)


if __name__ == "__main__":
    main()