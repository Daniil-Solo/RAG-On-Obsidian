def get_sentences_embeddings(sentences, st_model, prefix):
    sentences = [prefix + item for item in sentences]
    return st_model.encode(sentences)
