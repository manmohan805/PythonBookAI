from pathlib import Path
import pymupdf


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text.
    """

    # Remove null characters
    text = text.replace("\x00", " ")

    # Split into lines
    lines = text.splitlines()

    # Remove unnecessary spaces
    lines = [line.strip() for line in lines]

    # Remove empty lines
    lines = [line for line in lines if line]

    # Join lines into one clean paragraph
    return " ".join(lines)


def extract_pages(pdf_path: str | Path) -> list[dict]:
    """
    Extract text from every page of a PDF.

    Returns:
        A list containing:
        - source
        - page
        - text
    """

    pdf_path = Path(pdf_path)

    pages = []

    with pymupdf.open(pdf_path) as doc:

        for page_number, page in enumerate(doc, start=1):

            text = page.get_text("text")

            text = clean_text(text)

            if text:
                pages.append({
                    "source": pdf_path.name,
                    "page": page_number,
                    "text": text
                })

    return pages


def chunk_pages(
    pages: list[dict],
    chunk_size: int = 900,
    overlap: int = 150
) -> list[dict]:
    """
    Split extracted page text into overlapping chunks.
    """

    chunks = []

    chunk_id = 0

    for item in pages:

        text = item["text"]

        start = 0

        while start < len(text):

            end = min(start + chunk_size, len(text))

            chunk_text = text[start:end].strip()

            if chunk_text:

                chunks.append({
                    "id": chunk_id,
                    "source": item["source"],
                    "page": item["page"],
                    "text": chunk_text
                })

                chunk_id += 1

            # Stop when we reach the end
            if end >= len(text):
                break

            # Move forward while keeping overlap
            start = max(0, end - overlap)

    return chunks