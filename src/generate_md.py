#!/usr/bin/env python3
"""Render the Markdown CV template with values from the YAML data file."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml


PLACEHOLDER = re.compile(r"\{([^{}]+)\}")


def load_yaml(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    return yaml.safe_load(content) or {}


def lookup(name: str, context: list[Any], data: dict[str, Any]) -> Any:
    if not name:
        return ""

    for scope in context:
        if isinstance(scope, dict) and name in scope:
            return scope[name]

    person = data.get("person", {})
    if isinstance(person, dict):
        if name in person:
            return person[name]
        urls = person.get("urls", {})
        if isinstance(urls, dict) and name in urls:
            return urls[name]

    return data.get(name, "")


def render_template(template: str, context: list[Any], data: dict[str, Any]) -> str:
    result: list[str] = []
    index = 0
    while index < len(template):
        open_index = template.find("{", index)
        if open_index == -1:
            result.append(template[index:])
            break

        result.append(template[index:open_index])
        close_index = template.find("}", open_index + 1)
        if close_index == -1:
            result.append(template[open_index:])
            break

        token = template[open_index + 1:close_index].strip()
        if token == ";":
            result.append("")
            index = close_index + 1
            continue

        if token.endswith(":"):
            collection_name = token[:-1].strip()
            collection = lookup(collection_name, context, data)
            if not isinstance(collection, list):
                index = close_index + 1
                continue

            depth = 0
            cursor = close_index + 1
            block_end = None
            while cursor < len(template):
                next_open = template.find("{", cursor)
                if next_open == -1:
                    break
                next_close = template.find("}", next_open + 1)
                if next_close == -1:
                    break
                next_token = template[next_open + 1:next_close].strip()
                if next_token == ";":
                    if depth == 0:
                        block_end = next_open
                        break
                    depth -= 1
                elif next_token.endswith(":"):
                    depth += 1
                cursor = next_close + 1

            if block_end is None:
                result.append(template[open_index:close_index + 1])
                index = close_index + 1
                continue

            body = template[close_index + 1:block_end]
            rendered_items: list[str] = []
            for item in collection:
                item_context = [item, *context] if isinstance(item, dict) else [{collection_name[:-1] if collection_name.endswith("s") else collection_name: item}, *context]
                rendered_items.append(render_template(body, item_context, data))
            result.append("".join(rendered_items))
            index = block_end + 3
            continue

        if token == "*":
            current = context[0] if context else ""
            if isinstance(current, dict):
                for value in current.values():
                    if not isinstance(value, (dict, list)):
                        result.append(str(value))
                        break
                else:
                    result.append("")
            else:
                result.append(str(current))
        else:
            value = lookup(token, context, data)
            if value is None or isinstance(value, (dict, list)):
                result.append("")
            else:
                result.append(str(value))

        index = close_index + 1

    return "".join(result)


def render_collections(template: str, context: list[Any], data: dict[str, Any]) -> str:
    return render_template(template, context, data)


def generate(template_path: Path, data_path: Path, output_path: Path) -> None:
    data = load_yaml(data_path)
    template = template_path.read_text(encoding="utf-8")
    rendered = render_collections(template, [data], data)
    output_path.write_text(rendered, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", type=Path, default=Path(__file__).with_name("template.md"))
    parser.add_argument("--data", type=Path, default=Path(__file__).with_name("data.yaml"))
    parser.add_argument("--output", type=Path, default=Path(__file__).parent.parent / "output.md")
    args = parser.parse_args()
    generate(args.template, args.data, args.output)


if __name__ == "__main__":
    main()
