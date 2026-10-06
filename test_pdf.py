from config import BOOKS_DIR
from pdf_processor import extract_pages


pdf_files = list(BOOKS_DIR.glob("*.pdf"))

if not pdf_files:
    print("❌ No PDF found in data/books/")
    exit()

pdf_path = pdf_files[0]

print("PDF:", pdf_path.name)

pages = extract_pages(pdf_path)

print("Pages extracted:", len(pages))

if pages:
    print("\n--- First page preview ---\n")
    print(pages[0]["text"][:2000])
else:
    print("❌ No text extracted from the PDF.")