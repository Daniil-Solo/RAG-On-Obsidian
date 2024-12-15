class CustomRetriever:
    def __init__(self, qdrant_client, embedder, collection_name: str):
        self.qdrant_client = qdrant_client
        self.embedder = embedder
        self.collection_name = collection_name

    def get_relevant_documents(self, query, limit=5):
        query_embed = self.embedder.encode(query)
        results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_embed,
            limit=limit,
        )
        return results
