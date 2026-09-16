#   Task

    Implement a CLI that supports the following arguments:

    type - the first positional argument without a tag. It specifies the generator type.
    --template - path to the template file.
    --data - path to the YAML data source.
    --output - output filename.

    Example:

    python src/main.py html --template src/template.html --data src/data.yaml --output index.html

    Here, html is the type argument.

## Functionality

    The CLI must dynamically select the generator based on the type argument.

    For a type <type>, import the generator from:

    generate_<type>.py

    For example:

    type = html

    must load:

    generate_html.py

    and call its generate function.

    The remaining CLI arguments must be passed to the generate function as parameters.

    Conceptually:

    generate_html.generate(
        template=<template>,
        data=<data>,
        output=<output>
    )

### Generator Interface

    Each generator module must expose a function named:

    generate(...)

    For example:

    src/
    ├── main.py
    ├── generate_html.py
    ├── generate_md.py
    └── generate_pdf.py

    The following commands should therefore resolve to the corresponding modules:

    python src/main.py html ...
    python src/main.py md ...
    python src/main.py pdf ...

    which load:

    generate_html.py
    generate_md.py
    generate_pdf.py

    respectively.

##  Requirements
    type is required and must be the first positional argument.
    --template, --data, and --output are named arguments.
    All three named arguments are passed to the selected generate() function.
    The CLI must report a clear error when:
    type is missing.
    The corresponding generate_<type>.py module does not exist.
    The module does not expose a generate function.
    Required arguments are missing.
    The generator raises an error.
    Do not hard-code the list of supported generator types.
    Generator modules should be discovered dynamically from the type argument.
    Keep CLI logic separate from generator implementations.
    Do not modify generator implementations unless required to make them compatible with the defined generate() interface.
    Example

    Command:

    python src/main.py md \
        --template src/template.md \
        --data src/data.yaml \
        --output README.md

    Equivalent operation:

    from generate_md import generate

    generate(
        template="src/template.md",
        data="src/data.yaml",
        output="README.md"
    )