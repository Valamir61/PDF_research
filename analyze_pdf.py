import fitz
import re
import csv
from pathlib import Path

# === CONFIGURATION, TO BE MODIFIED IF WANTED ===
zotero_root = Path("")  # <- Zotero path here, leave empty if you put every files in the same directory as this script
pdfs_dir = zotero_root / "biblio/files" # <- pdf files directory
output_csv = zotero_root / "scan_results.csv" # <- output CSV file
keywords_file = zotero_root / "keywords.txt" # <- file containing keywords to search, one per line in a .txt file

# === EXAMPLE ===
zotero_root = Path("")
pdfs_dir = zotero_root / "example_biblio/files"
output_csv = zotero_root / "example_scan_results.csv"
keywords_file = zotero_root / "example_keywords.txt"
# === LOAD KEYWORDS ===
with open(keywords_file, "r", encoding="utf-8-sig") as f:
    keywords = [line.strip() for line in f if line.strip()]

# === PROCESSING ===
rows = []

for pdf_path in pdfs_dir.rglob("*.pdf"):
    try:
        doc = fitz.open(pdf_path)

        for keyword in keywords:
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            pages_found = []
            total_occurrences = 0

            for page_number, page in enumerate(doc, start=1):
                text = page.get_text()
                matches = pattern.findall(text)
                if matches:
                    pages_found.append(str(page_number))
                    total_occurrences += len(matches)

            if total_occurrences > 0:
                status = "FOUND"
                pages = ",".join(pages_found)
            else:
                status = "NOT FOUND"
                pages = ""

            rows.append([
                pdf_path.name,
                str(pdf_path),
                keyword,
                status,
                pages,
                total_occurrences
            ])

    except Exception as e:
        for keyword in keywords:
            rows.append([
                pdf_path.name,
                str(pdf_path),
                keyword,
                f"ERROR: {e}",
                "",
                0
            ])

# === EXPORT CSV ===
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["PDF Name", "Path", "Keyword", "Status", "Pages", "Occurrences"])
    writer.writerows(rows)



print(f"✅ Analysis complete. Results saved to: {output_csv}")