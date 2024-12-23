import os
from embedder import get_sentences_embeddings


def file_into_db_collection(
        root, filename, db_client, text_splitter, sentence_embedder, prefix,
        collection_name="obsidian-vault"):
    if filename.endswith(".md"):
        file_path = os.path.join(root, filename)
        with open(file_path, 'r') as file:
            content = file.read()
            splitted_texts = text_splitter.split_text(content)
            for text_chunk in splitted_texts:
                embeds = get_sentences_embeddings(
                    [text_chunk], sentence_embedder, prefix)
                payload = [{
                    'file_path': file_path,
                    'filename': filename,
                    'text': text_chunk}]
                db_client.upload_collection(
                    collection_name=collection_name,
                    vectors=embeds,
                    payload=payload
                )


def folder_into_db_collection(
        folder_path, db_client, text_spliltter, sentence_embedder, prefix,
        collection_name="obsidian-vault"):
    for root, _, files in os.walk(folder_path):
        for filename in files:
            file_into_db_collection(
                root, filename, db_client, text_spliltter, sentence_embedder,
                prefix, collection_name)
