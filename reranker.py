from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

_model = None


def get_reranker():

    global _model

    if _model is None:

        print("Loading reranker model...")

        _model = CrossEncoder(
            MODEL_NAME,
            device="cpu"
        )

    return _model


def rerank(
    query: str,
    results: list[dict],
    top_k: int = 5
):

    if not results:
        return []

    model = get_reranker()

    pairs = [
        (query, result["text"])
        for result in results
    ]

    scores = model.predict(
        pairs,
        show_progress_bar=False
    )

    reranked = []

    for result, score in zip(results, scores):

        item = dict(result)

        item["reranker_score"] = float(score)

        reranked.append(item)

    reranked.sort(
        key=lambda x: x["reranker_score"],
        reverse=True
    )

    return reranked[:top_k]