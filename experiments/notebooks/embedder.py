from sentence_transformers import SentenceTransformer
from config import embedder_name


def get_sentences_embeddings(sentences, st_model):
    return st_model.encode(sentences)


sentence_embedder = SentenceTransformer(embedder_name)  # , device="cpu")
VECTOR_SIZE = get_sentences_embeddings(
    'Hello, world!', sentence_embedder).shape
