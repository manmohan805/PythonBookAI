from config import BOOKS_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from pdf_processor import extract_pages, chunk_pages
from vector_store import save_index


def ingest_pdfs():
    """Process all PDFs in the books directory and create the index."""

    pdf_files = sorted(BOOKS_DIR.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in: {BOOKS_DIR}")
        print("Place one or more PDF files in the books folder.")
        return

    all_chunks = []

    print(f"Found {len(pdf_files)} PDF file(s).")

    for pdf_path in pdf_files:
        print(f"\nProcessing: {pdf_path.name}")

        try:
            pages = extract_pages(pdf_path)

            if not pages:
                print(f"Warning: No text extracted from {pdf_path.name}.")
                continue

            chunks = chunk_pages(
                pages,
                chunk_size=CHUNK_SIZE,
                overlap=CHUNK_OVERLAP,
            )

            all_chunks.extend(chunks)

            print(f"Pages extracted: {len(pages)}")
            print(f"Chunks created: {len(chunks)}")

        except Exception as error:
            print(f"Error processing {pdf_path.name}: {error}")

    if not all_chunks:
        print("\nNo chunks were created. The existing index was not changed.")
        return

    # Give every chunk a unique ID across all PDFs.
    for chunk_id, chunk in enumerate(all_chunks):
        chunk["id"] = chunk_id

    print(f"\nTotal chunks from all PDFs: {len(all_chunks)}")

    save_index(all_chunks)

    print("\nPDF ingestion completed successfully!")


if __name__ == "__main__":
    ingest_pdfs()