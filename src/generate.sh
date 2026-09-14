#!/bin/bash

set -e

python3 "$(dirname "$0")/generate_md.py" "--output README.md"
python3 "$(dirname "$0")/generate_pdf.py" "--output index.html"

# Generate PDF from index.html
wkhtmltopdf -s A4 index.html 'Roman Metlinskyi CV.pdf'

