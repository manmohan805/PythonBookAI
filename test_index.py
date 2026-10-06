from config import BOOKS_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from pdf_processor import extract_pages, chunk_pages
from vector_store import save_index


# Find PDF
pdf_files = list(BOOKS_DIR.glob("*.pdf"))

if not pdf_files:
    print("❌ No PDF found in data/books/")
    exit()

pdf_path = pdf_files[0]

print("PDF:", pdf_path.name)


# Extract pages
pages = extract_pages(pdf_path)

print("Pages:", len(pages))


# Create chunks
chunks = chunk_pages(
    pages,
    chunk_size=CHUNK_SIZE,
    overlap=CHUNK_OVERLAP
)

print("Chunks:", len(chunks))


# Create vector index
save_index(chunks)

print("\n✅ Vector index created successfully!")
