#   Task
    Implement a generator Markdown file based on:
    - Template: src/template.md
    - Data: src/data.yaml
    - Output: output.md
    - Requirements:
      - load input files
      - read src/template.md as the Markdown template.
      - read src/data.yaml as the source data.
      - field replacement
      - target file: src/generate_md.py

##  Replace placeholders using the format:
    {<field_name>}
    <field_name> corresponds to a field/key in data.yaml.
    Replace all matching placeholders in the template.
    Preserve all other Markdown content unchanged.

##  Collection Template Syntax
    A collection can be rendered using an explicit collection template block:
    {<collection>:}<collection item template>{;}
    Where:
    <collection> is the name of a node in data.yaml.
    The corresponding value must be a collection.
    <collection item template> defines the template for a single collection item.
    {<collection>:} is the opening collection marker.
    {;} is the closing collection marker.
    The collection opening and closing markers must not appear in the generated output.
    The item template is rendered once for each item in the collection.
    Example data:
``` YAML
      experience:
        - company: Barclays
          position: Software Engineer
        - company: FNZ
          position: Senior Software Engineer
```
    Template:
    {experience:}
      - **{company}** - {position}
    {;}  
    Generated output:
      - **Barclays** - Software Engineer
      - **FNZ** - Senior Software Engineer

    <collection item template> can has nested collection like next examlpe:
    {education:}
    ### {institution}
    {degrees:}
    - **{name}**, *{period}*
    {;}
    {;}

### Simple array
    For a collection containing scalar values, use {*} to represent the current item:
    Example data:
``` YAML
    skills:
      - C#
      - Python
      - TypeScript
```      
    Template:
      {skills:}{*},{;} 
    Generated output:
      C#, Python, TypeScript

##  Output
    Write the generated Markdown to output.md.
    Preserve the original Markdown structure and formatting as much as reasonably possible.

##  Implementation considerations
    Use a YAML parser such as PyYAML.
    Clearly separate:
    - loading YAML data.
    - processing repeating list templates.
    - replacing scalar placeholders.
    - wWriting the resulting Markdown.
    - Do not modify src/template.md or src/data.yaml.
    - keep the implementation simple and maintainable.
    - do not introduce unnecessary dependencies.