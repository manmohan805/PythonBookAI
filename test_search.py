from vector_store import search


question = input("Ask a question about the Python book: ").strip()

if not question:
    print("❌ Question cannot be empty.")
    exit()


results = search(question, top_k=5)


print("\n" + "=" * 80)
print("SEARCH RESULTS")
print("=" * 80)


for i, result in enumerate(results, start=1):

    print("\n" + "-" * 80)

    print(f"Result #{i}")

    print("Book:", result["source"])

    print("Page:", result["page"])

    print("Similarity score:", round(result["score"], 4))

    print("\nText:")

    print(result["text"])