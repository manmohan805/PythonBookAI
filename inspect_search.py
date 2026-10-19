from vector_store import search

question = "What are Python variables?"

results = search(question, top_k=5)

for i, result in enumerate(results, start=1):
    print("\n" + "=" * 70)
    print(f"RESULT {i}")
    print(f"Book: {result['source']}")
    print(f"Page: {result['page']}")
    print(f"Hybrid score: {result['score']:.4f}")
    print("\nRetrieved text:")
    print(result["text"][:500])