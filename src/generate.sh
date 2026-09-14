#!/bin/bash

set -e

python3 "$(dirname "$0")/main.py" md --template src/template.md --data src/data.yaml --output README.md 
python3 "$(dirname "$0")/main.py" html --template src/template.html --data src/data.yaml --output index.html

# Generate PDF from index.html
wkhtmltopdf -s A4 index.html 'Roman Metlinskyi CV.pdf'

