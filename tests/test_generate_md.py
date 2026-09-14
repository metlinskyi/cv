import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.generate_md import generate


class GenerateMarkdownTests(unittest.TestCase):
    def test_scalar_and_collection_placeholders(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            template = """# {givenName} {familyName}

{experience:}
- {company}: {position}
{;}

Skills: {skills:}{*}, {;}
"""
            data = """givenName: Ada
familyName: Lovelace
experience:
  - company: Barclays
    position: Engineer
  - company: FNZ
    position: Developer
skills:
  - C#
  - Python
"""
            template_path = temp_path / "template.md"
            data_path = temp_path / "data.yaml"
            output_path = temp_path / "README.md"
            template_path.write_text(template, encoding="utf-8")
            data_path.write_text(data, encoding="utf-8")

            generate(template_path, data_path, output_path)
            rendered = output_path.read_text(encoding="utf-8")

            self.assertIn("# Ada Lovelace", rendered)
            self.assertIn("- Barclays: Engineer", rendered)
            self.assertIn("- FNZ: Developer", rendered)
            self.assertIn("Skills: C#, Python, ", rendered)
            self.assertNotIn("{experience:}", rendered)
            self.assertNotIn("{;}", rendered)

    def test_nested_degree_lists(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            template = """## Education
{education:}
### {institution}
{degrees:}
- **{name}**, *{period}*
{;}
{;}
"""
            data = """education:
  - institution: Dnipro University of Technology (NTU DP)
    degrees:
      - name: Bachelor's degree in Computer Science
        period: 2000 - 2004
      - name: Master's program (not completed)
        period: 2004 - 2005
"""
            template_path = temp_path / "template.md"
            data_path = temp_path / "data.yaml"
            output_path = temp_path / "README.md"
            template_path.write_text(template, encoding="utf-8")
            data_path.write_text(data, encoding="utf-8")

            generate(template_path, data_path, output_path)
            rendered = output_path.read_text(encoding="utf-8")

            self.assertIn("### Dnipro University of Technology (NTU DP)", rendered)
            self.assertIn("- **Bachelor's degree in Computer Science**, *2000 - 2004*", rendered)
            self.assertIn("- **Master's program (not completed)**, *2004 - 2005*", rendered)


if __name__ == "__main__":
    unittest.main()
