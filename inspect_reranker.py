from vector_store import search
from reranker import rerank

question = "What are Python variables?"

# Step 1: Retrieve candidate passages
candidates = search(question, top_k=30)

print(f"Retrieved {len(candidates)} candidates.")

# Step 2: Rerank the candidates
results = rerank(question, candidates, top_k=5)

# Step 3: Display the final ranking
for rank, result in enumerate(results, start=1):
    print("\n" + "=" * 70)
    print(f"Rank: {rank}")
    print(f"Book: {result['source']}")
    print(f"Page: {result['page']}")
    print(f"Hybrid score: {result['score']:.4f}")
    print(f"Reranker score: {result['reranker_score']:.4f}")
    print("\nRetrieved text:")
    print(result["text"][:500])