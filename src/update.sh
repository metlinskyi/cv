#!/bin/bash
cd src/
copilot --allow-tool 'write' -p "update readme.md according the data in data.yaml"
copilot --allow-tool 'write' -p "update index.html according the data in data.yaml, use last recent 5 experiences, wrap new lines into paragraph only for about text, do not create a header for the about section"  
wkhtmltopdf -s A4 index.html '../Roman Metlinskyi CV.pdf'
cd ..


