#!/usr/bin/env python3
"""Dispatch to a generator module based on the requested type."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path
from typing import Any


def load_generator(generator_type: str) -> Any:
    module_name = f"generate_{generator_type}"
    module_path = Path(__file__).with_name(f"{module_name}.py")

    if not module_path.exists():
        raise FileNotFoundError(f"Generator module not found: {module_name}.py")

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load generator module: {module_name}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    generator = getattr(module, "generate", None)
    if not callable(generator):
        raise AttributeError(f"Generator module '{module_name}.py' does not define a callable generate() function")

    return generator


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("type", nargs="?", help="Generator type, for example: md, html, pdf")
    parser.add_argument("--template", required=True, help="Path to the template file")
    parser.add_argument("--data", required=True, help="Path to the YAML data source")
    parser.add_argument("--output", required=True, help="Output path")
    args = parser.parse_args(argv)

    if not args.type:
        parser.error("type is required and must be the first positional argument")

    try:
        generator = load_generator(args.type)
        generator(template=Path(args.template), data=Path(args.data), output=Path(args.output))
    except (FileNotFoundError, ImportError, AttributeError) as exc:
        parser.error(str(exc))
    except Exception as exc:
        parser.exit(1, f"Generator failed: {exc}\n")


if __name__ == "__main__":
    main()
