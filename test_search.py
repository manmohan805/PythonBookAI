from collections import Counter

from config import INDEX_DIR
from vector_store import load_index, search


def show_index_summary():
    """Display how many chunks belong to each book."""

    _, metadata = load_index()

    print("\n" + "=" * 80)
    print("INDEX SUMMARY")
    print("=" * 80)

    book_counts = Counter(
        item["source"] for item in metadata
    )

    print(f"Total chunks: {len(metadata)}")
    print(f"Unique books: {len(book_counts)}")

    for book, count in sorted(book_counts.items()):
        print(f"{book}: {count} chunks")


def run_search():
    """Search the combined index for a question."""

    question = input(
        "\nAsk a question about your books (or type 'exit'): "
    ).strip()

    if question.lower() == "exit":
        return False

    if not question:
        print("Question cannot be empty.")
        return True

    results = search(question, top_k=5)

    print("\n" + "=" * 80)
    print("SEARCH RESULTS")
    print("=" * 80)

    if not results:
        print("No results found.")
        return True

    for i, result in enumerate(results, start=1):
        print("\n" + "-" * 80)
        print(f"Result #{i}")
        print("Book:", result["source"])
        print("Page:", result["page"])
        print("Similarity score:", round(result["score"], 4))
        print("\nText:")
        print(result["text"])

    print("\n" + "=" * 80)

    return True


if __name__ == "__main__":
    show_index_summary()

    while run_search():
        pass

    print("\nSearch testing finished.")