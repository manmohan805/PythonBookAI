from config import BOOKS_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from pdf_processor import extract_pages, chunk_pages
from embeddings import embed_texts


# Find PDF
pdf_files = list(BOOKS_DIR.glob("*.pdf"))

if not pdf_files:
    print("❌ No PDF found.")
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


# Take only 5 chunks for our first test
test_chunks = chunks[:5]

texts = [chunk["text"] for chunk in test_chunks]


# Generate embeddings
print("\nCreating embeddings...")

embeddings = embed_texts(texts)


print("\nEmbedding test successful!")

print("Number of embeddings:", len(embeddings))

print("Embedding shape:", embeddings.shape)

print("First embedding:")
print(embeddings[0])