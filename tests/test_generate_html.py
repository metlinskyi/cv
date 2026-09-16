import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.generate_html import generate


class GenerateHtmlTests(unittest.TestCase):
    def test_generate_replaces_fields_and_keeps_style_unprocessed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            template = """<!DOCTYPE html>
<html>
<head>
<style>
.a { color: {color}; }
</style>
</head>
<body>
<div class="about">{about}</div>
<ul class="experience">
  <li><span class="company">{company}</span> - <span class="title">{title}</span></li>
</ul>
</body>
</html>
"""
            data = {
                "color": "red",
                "about": "First line\nSecond line",
                "experience": [
                    {"company": "Acme", "title": "Engineer"},
                    {"company": "Beta", "title": "Developer"},
                ],
            }

            template_path = temp_path / "template.html"
            data_path = temp_path / "data.yaml"
            output_path = temp_path / "output.html"

            template_path.write_text(template, encoding="utf-8")
            data_path.write_text("color: red\nabout: |\n  First line\n  Second line\nexperience:\n  - company: Acme\n    title: Engineer\n  - company: Beta\n    title: Developer\n", encoding="utf-8")

            generate(template_path, data_path, output_path)
            rendered = output_path.read_text(encoding="utf-8")

            self.assertIn("<p>First line</p>", rendered)
            self.assertIn("<p>Second line</p>", rendered)
            self.assertIn("Acme", rendered)
            self.assertIn("Engineer", rendered)
            self.assertIn("<span class=\"company\">Acme</span>", rendered)
            self.assertIn(".a { color: {color}; }", rendered)
            self.assertNotIn(".a { color: red; }", rendered)

    def test_generate_limits_experience_to_n_and_escapes_html(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            template = """<ul class="experience">
  <li><span class="company">{company}</span> - <span class="title">{title}</span></li>
</ul>
"""
            data = {
                "n": 1,
                "experience": [
                    {"company": "Alpha", "title": "A & B"},
                    {"company": "Bravo", "title": "C & D"},
                ],
            }

            template_path = temp_path / "template.html"
            data_path = temp_path / "data.yaml"
            output_path = temp_path / "output.html"

            template_path.write_text(template, encoding="utf-8")
            data_path.write_text("n: 1\nexperience:\n  - company: Alpha\n    title: A & B\n  - company: Bravo\n    title: C & D\n", encoding="utf-8")

            generate(template_path, data_path, output_path)
            rendered = output_path.read_text(encoding="utf-8")

            self.assertIn("Alpha", rendered)
            self.assertNotIn("Bravo", rendered)
            self.assertIn("A &amp; B", rendered)
            self.assertNotIn("A & B", rendered)


if __name__ == "__main__":
    unittest.main()
