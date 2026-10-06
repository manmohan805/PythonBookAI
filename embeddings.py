from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL


_model = None


def get_model():
    global _model

    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer(EMBEDDING_MODEL)

    return _model


def embed_texts(texts: list[str]):
    model = get_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    return embeddings


def embed_query(text: str):
    model = get_model()

    embedding = model.encode(
        [text],
        normalize_embeddings=True,
        show_progress_bar=False,
        convert_to_numpy=True
    )

    return embedding[0]