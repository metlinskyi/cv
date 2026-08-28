#!/bin/bash

set -e

python3 "$(dirname "$0")/generate.py"

# Generate PDF from index.html
wkhtmltopdf -s A4 index.html 'Roman Metlinskyi CV.pdf'

