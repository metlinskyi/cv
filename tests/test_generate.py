import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

sys.path.insert(0, str(ROOT))

from src.generate import load_generator, main


class GenerateDispatchTests(unittest.TestCase):
    def test_load_generator_returns_callable_for_known_generator(self):
        generator = load_generator("md")
        self.assertTrue(callable(generator))
        self.assertEqual(generator.__module__, "generate_md")

    def test_main_dispatches_to_selected_generator_module(self):
        module_path = SRC / "generate_demo.py"
        try:
            module_path.write_text(
                "from pathlib import Path\n\n"
                "def generate(template, data, output):\n"
                "    Path(output).write_text(f'{template}:{data}:{output}', encoding='utf-8')\n",
                encoding="utf-8",
            )

            with patch.object(sys, "argv", ["generate.py", "demo", "--template", "a.txt", "--data", "b.yaml", "--output", "c.txt"]):
                main()

            self.assertEqual("a.txt:b.yaml:c.txt", (ROOT / "c.txt").read_text(encoding="utf-8"))
        finally:
            if module_path.exists():
                module_path.unlink()
            output_path = ROOT / "c.txt"
            if output_path.exists():
                output_path.unlink()

    def test_main_rejects_missing_generator_module(self):
        with self.assertRaises(SystemExit):
            with patch.object(sys, "argv", ["generate.py", "missing", "--template", "a.txt", "--data", "b.yaml", "--output", "c.txt"]):
                main()

    def test_main_rejects_module_without_generate_function(self):
        module_path = SRC / "generate_missing_method.py"
        try:
            module_path.write_text("VALUE = 42\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                with patch.object(sys, "argv", ["generate.py", "missing_method", "--template", "a.txt", "--data", "b.yaml", "--output", "c.txt"]):
                    main()
        finally:
            if module_path.exists():
                module_path.unlink()

    def test_main_requires_template_data_and_output_arguments(self):
        with self.assertRaises(SystemExit):
            with patch.object(sys, "argv", ["generate.py", "md"]):
                main()


if __name__ == "__main__":
    unittest.main()
