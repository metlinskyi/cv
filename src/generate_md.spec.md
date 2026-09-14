Task

Target file: src/generate_md.py

Implement a Python script that generates README.md based on:

Template: src/template.md
Data: src/data.yaml
Output: README.md
Requirements
Load input files
Read src/template.md as the Markdown template.
Read src/data.yaml as the source data.
Field replacement

Replace placeholders using the format:

{<field_name>}
<field_name> corresponds to a field/key in data.yaml.
Replace all matching placeholders in the template.
Preserve all other Markdown content unchanged.

Repeating list items

A Markdown list item starting with - represents a template for multiple data items when the corresponding value in data.yaml is a collection.
The complete list item should be repeated once for each element in the collection.
Placeholders inside the list-item template should be replaced using the current collection element's fields.

Example template:

## Experience

- **{company}** - {position} ({period})

Example data:

experience:
  - company: Barclays
    position: Software Engineer
    period: 2024-2026
  - company: FNZ
    position: Senior Software Engineer
    period: 2022-2024

Generated Markdown:

## Experience

- **Barclays** - Software Engineer (2024-2026)
- **FNZ** - Senior Software Engineer (2022-2024)
Nested fields
Support placeholders referring to fields of the current list item.
Scalar/top-level placeholders should be replaced from the root data object.
Do not replace a placeholder with the string representation of an entire dictionary or list unless explicitly intended by the template.
Output
Write the generated Markdown to README.md.
Preserve the original Markdown structure and formatting as much as reasonably possible.
Implementation considerations
Use a YAML parser such as PyYAML.
Clearly separate:
Loading YAML data.
Processing repeating list templates.
Replacing scalar placeholders.
Writing the resulting Markdown.
Do not modify src/template.md or src/data.yaml.
Keep the implementation simple and maintainable.
Do not introduce unnecessary dependencies.