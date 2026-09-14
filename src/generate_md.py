#!/usr/bin/env python3
"""Render the Markdown CV template with values from the YAML data file."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path
from typing import Any

import yaml


PLACEHOLDER = re.compile(r"\{([^{}]+)\}")
LIST_ITEM = re.compile(r"^(?P<indent>\s*)-\s(?P<content>.*)$")
HEADING = re.compile(r"^(?P<indent>\s*)(?P<marks>#{1,6})\s+")


def lookup(name: str, context: list[Any], data: dict[str, Any]) -> Any:
	for value in context:
		if isinstance(value, dict) and name in value:
			return value[name]

	person = data.get("person", {})
	if isinstance(person, dict) and name in person:
		return person[name]
	urls = person.get("urls", {}) if isinstance(person, dict) else {}
	if isinstance(urls, dict) and name in urls:
		return urls[name]
	return data.get(name, "")


def replace_fields(value: str, context: list[Any], data: dict[str, Any]) -> str:
	def replacement(match: re.Match[str]) -> str:
		field = lookup(match.group(1).strip(), context, data)
		if field is None or isinstance(field, (dict, list)):
			return ""
		return html.escape(str(field), quote=False)

	return PLACEHOLDER.sub(replacement, value)


def collection_name(line: str, context: list[Any], data: dict[str, Any]) -> str | None:
	fields = {match.group(1).strip() for match in PLACEHOLDER.finditer(line)}
	for value in context:
		if not isinstance(value, dict):
			continue
		for name, collection in value.items():
			if isinstance(collection, list) and collection and isinstance(collection[0], dict):
				if fields.intersection(collection[0]):
					return name
			if isinstance(collection, list) and name.endswith("s") and name[:-1] in fields:
				return name
		if fields.intersection(value):
			return None
	for name, collection in data.items():
		if isinstance(collection, list) and collection and isinstance(collection[0], dict):
			if fields.intersection(collection[0]):
				return name
		if isinstance(collection, list) and name.endswith("s") and name[:-1] in fields:
			return name
	return None


def heading_level(line: str) -> int | None:
	match = HEADING.match(line)
	return len(match.group("marks")) if match else None


def render_lines(
	lines: list[str],
	context: list[Any],
	data: dict[str, Any],
	expanding: set[str] | None = None,
) -> list[str]:
	expanding = expanding or set()
	rendered: list[str] = []
	index = 0
	while index < len(lines):
		match = LIST_ITEM.match(lines[index])
		if not match:
			rendered.append(replace_fields(lines[index], context, data))
			index += 1
			continue

		item_name = collection_name(match.group("content"), context, data)
		values = lookup(item_name or "", context, data)
		if item_name in expanding or not isinstance(values, list):
			rendered.append(replace_fields(lines[index], context, data))
			index += 1
			continue

		block_end = index + 1
		while block_end < len(lines):
			next_match = LIST_ITEM.match(lines[block_end])
			if next_match and len(next_match.group("indent")) <= len(match.group("indent")):
				break
			if lines[block_end].strip() and len(lines[block_end]) - len(lines[block_end].lstrip()) <= len(match.group("indent")):
				break
			block_end += 1

		item_template = lines[index:block_end]
		for item in values:
			item_context = [item, *context]
			if not isinstance(item, dict) and item_name:
				item_context.insert(0, {item_name[:-1] if item_name.endswith("s") else item_name: item})
			rendered.extend(render_lines(item_template, item_context, data, expanding | {item_name or ""}))
		index = block_end

	return rendered


def render_section_blocks(lines: list[str], context: list[Any], data: dict[str, Any]) -> list[str]:
	rendered: list[str] = []
	index = 0
	while index < len(lines):
		level = heading_level(lines[index])
		collection = collection_name(lines[index], context, data) if level is not None else None
		values = lookup(collection or "", context, data)
		if level is None or not isinstance(values, list) or not values or not isinstance(values[0], dict):
			rendered.extend(render_lines([lines[index]], context, data))
			index += 1
			continue

		block_end = index + 1
		while block_end < len(lines):
			next_level = heading_level(lines[block_end])
			if next_level is not None and next_level <= level:
				break
			block_end += 1

		for item in values:
			rendered.extend(render_section_blocks(lines[index:block_end], [item, *context], data))
		index = block_end

	return rendered


def generate(template_path: Path, data_path: Path, output_path: Path) -> None:
	data = yaml.safe_load(data_path.read_text(encoding="utf-8")) or {}
	template_lines = template_path.read_text(encoding="utf-8").splitlines(keepends=True)
	output_path.write_text("".join(render_section_blocks(template_lines, [data], data)), encoding="utf-8")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--template", type=Path, default=Path(__file__).with_name("template.md"))
	parser.add_argument("--data", type=Path, default=Path(__file__).with_name("data.yaml"))
	parser.add_argument("--output", type=Path, default=Path(__file__).parent.parent / "README.md")
	args = parser.parse_args()
	generate(args.template, args.data, args.output)


if __name__ == "__main__":
	main()
