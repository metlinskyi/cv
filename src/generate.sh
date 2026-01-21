#!/bin/bash

# Generate README.md 
copilot --allow-tool 'write' -p 
"
    generate readme.md based on data in src/data.yaml and template in src/template.md
"
# Generate index.html
copilot --allow-tool 'write' -p 
"
    generate index.html based on data in src/data.yaml and template in src/template.html, 
    css should be support convert pdf,
    do not create a header for the about section,
    slightly highlight technical skills for description and about using gray shade without bold,
    wrap new lines into paragraph only for about text
"  
# Generate PDF from index.html
wkhtmltopdf -s A4 index.html 'Roman Metlinskyi CV.pdf'

