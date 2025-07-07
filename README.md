# PDF Keyword Scanner

This script scans a folder of PDFs (typically from Zotero) for mentions of keywords in a .txt file (one keyword per column).

## Features

- Detects predefined keywords (from `keywords.txt`)
- Outputs a single line per PDF
- Saves results to a CSV file

## Project Structure

project/
├── keywords.txt
├── biblio/files/your_pdf_files.pdf
├── src/
│ └── analyze_pdfs.py


## Output file

scan_results.csv


## Requirements

pip install pymupdf
