def precision_at_k(retrieved_docs: list[str],
                   related_docs: list[str],
                   k: int) -> float:
    retrieved_k = retrieved_docs[:k]
    s = 0
    for doc in retrieved_k:
        if doc in related_docs:
            s += 1
    return min(s, len(related_docs)) / min(len(related_docs), k)


def average_precision_at_k(
        retrieved_docs: list[str],
        related_docs: list[str],
        k: int) -> float:
    precisions = []
    for i in range(1, k + 1):
        precisions.append(precision_at_k(retrieved_docs, related_docs, i))
    return sum(precisions) / len(precisions)
