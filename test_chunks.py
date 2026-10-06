from config import BOOKS_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from pdf_processor import extract_pages, chunk_pages


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


# Show first 3 chunks
print("\n" + "=" * 70)
print("FIRST 3 CHUNKS")
print("=" * 70)

for chunk in chunks[:3]:

    print("\n" + "-" * 70)

    print("Chunk ID:", chunk["id"])
    print("Source:", chunk["source"])
    print("Page:", chunk["page"])

    print("\nText:")
    print(chunk["text"])


# Chunk statistics
if chunks:

    lengths = [len(chunk["text"]) for chunk in chunks]

    print("\n" + "=" * 70)
    print("CHUNK STATISTICS")
    print("=" * 70)

    print("Total chunks:", len(chunks))
    print("Smallest chunk:", min(lengths), "characters")
    print("Largest chunk:", max(lengths), "characters")
    print(
        "Average chunk:",
        round(sum(lengths) / len(lengths), 2),
        "characters"
    )