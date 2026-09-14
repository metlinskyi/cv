import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class MainCliTests(unittest.TestCase):
    def test_main_selects_generator_by_type_and_passes_arguments(self):
        module_path = SRC / "generate_demo.py"
        try:
            module_path.write_text(
                "from pathlib import Path\n\n"
                "def generate(template, data, output):\n"
                "    Path(output).write_text(f'{template}:{data}:{output}', encoding='utf-8')\n",
                encoding="utf-8",
            )

            with patch.object(sys, "argv", ["main.py", "demo", "--template", "a.txt", "--data", "b.yaml", "--output", "c.txt"]):
                spec = importlib.util.spec_from_file_location("main_module", SRC / "main.py")
                module = importlib.util.module_from_spec(spec)
                assert spec is not None and spec.loader is not None
                spec.loader.exec_module(module)
                module.main()

            self.assertEqual("a.txt:b.yaml:c.txt", (ROOT / "c.txt").read_text(encoding="utf-8"))
        finally:
            if module_path.exists():
                module_path.unlink()
            output_path = ROOT / "c.txt"
            if output_path.exists():
                output_path.unlink()

    def test_generators_accept_string_paths_via_keyword_arguments(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            template = temp_path / "template.md"
            data = temp_path / "data.yaml"
            output = temp_path / "README.md"
            template.write_text("# {name}\n", encoding="utf-8")
            data.write_text("name: Ada\n", encoding="utf-8")

            from src.generate_md import generate as generate_md
            generate_md(template=str(template), data=str(data), output=str(output))

            self.assertEqual("# Ada\n", output.read_text(encoding="utf-8"))

    def test_main_rejects_missing_generator(self):
        with self.assertRaises(SystemExit):
            with patch.object(sys, "argv", ["main.py", "missing", "--template", "a.txt", "--data", "b.yaml", "--output", "c.txt"]):
                spec = importlib.util.spec_from_file_location("main_module", SRC / "main.py")
                module = importlib.util.module_from_spec(spec)
                assert spec is not None and spec.loader is not None
                spec.loader.exec_module(module)
                module.main()


if __name__ == "__main__":
    unittest.main()
