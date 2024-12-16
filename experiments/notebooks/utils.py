import os
from embedder import get_sentences_embeddings


def file_into_db_collection(
        root, filename, db_client, text_splitter, sentence_embedder):
    if filename.endswith(".md"):
        file_path = os.path.join(root, filename)
        with open(file_path, 'r') as file:
            content = file.read()
            splitted_texts = text_splitter.split_text(content)
            embeds = get_sentences_embeddings(
                splitted_texts, sentence_embedder)
            payload = [{
                'file_path': file_path,
                'filename': filename,
                'text': text, }
                for text in splitted_texts]
            db_client.upload_collection(
                collection_name="obsidian-vault",
                vectors=embeds,
                payload=payload
            )
            return splitted_texts


def folder_into_db_collection(
        folder_path, db_client, text_spliltter, sentence_embedder):
    for root, _, files in os.walk(folder_path):
        for filename in files:
            file_into_db_collection(
                root, filename, db_client, text_spliltter, sentence_embedder)
