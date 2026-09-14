Task

Target file: src/generate_pdf.py

Implement a Python script that generates index.html from:

Template: src/template.html
Data: src/data.yaml
Output: index.html
Requirements
Load input files
Read src/template.html as the HTML template.
Read src/data.yaml as the source data.
Field replacement

Replace template placeholders using the format:

{<field_name>}
<field_name> corresponds to a field/key from data.yaml.
Preserve the rest of the HTML unchanged.
Experience section limit
The experience section contains multiple experience entries.
Its number of rendered entries must be configurable through a variable n.
The default value of n is 5.
Only the first n experience entries should be rendered.
<ul> as a repeating template
A <ul> element represents a template for a collection of items.
Its contents should be treated as an item template and repeated for each corresponding item in the data.

Example:

<ul>
    <li>{name} - {description}</li>
</ul>

should produce one <li> for each item in the corresponding data collection.

The implementation should support field replacement inside the repeated template.
About content
The about content may contain multiple lines.
Each line must be wrapped in its own <p> element.

For example:

First line
Second line

becomes:

<p>First line</p>
<p>Second line</p>
Ignore <style> contents
The placeholder replacement mechanism must not process or modify anything inside <style> tags.
Placeholders appearing inside CSS must remain unchanged.

Example:

<style>
    .test { color: {color}; }
</style>

must remain exactly as-is.

Output
Write the resulting HTML to index.html.
The generated file should be valid HTML and preserve the structure and formatting of the original template as much as reasonably possible.
Implementation considerations
Use a YAML parser such as PyYAML for data.yaml.
Avoid performing global string replacement on the entire HTML because <style> contents must be excluded.
Keep the implementation simple and maintainable.
Do not introduce unnecessary dependencies or modify src/template.html or src/data.yaml.
Make n easy to change, preferably as a clearly defined constant or function parameter.