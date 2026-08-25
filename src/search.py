import numpy as np
from embeddings import (
    create_embeddings,
    create_query_embedding,
    save_embeddings,
    load_embeddings
)


def cosine_similarity(vector_a, vector_b):

    vector_a = np.array(vector_a)
    vector_b = np.array(vector_b)

    similarity = np.dot(vector_a, vector_b) / (
        np.linalg.norm(vector_a) *
        np.linalg.norm(vector_b)
    )

    return similarity

def sparse_similarity(sparse_a, sparse_b):

    score = 0.0

    for token, weight in sparse_a.items():

        if token in sparse_b:
            score += weight * sparse_b[token]

    return score

def search_documents(query, embedded_documents, top_k=5):

    query_embedding = create_query_embedding(query)
    results = []
    for document in embedded_documents:
        score = cosine_similarity(
            query_embedding["dense"],
            document["dense"]
        )
        dense_score = cosine_similarity(
        query_embedding["dense"],
        document["dense"]
        )
        sparse_score = sparse_similarity(
            query_embedding["sparse"],
            document["sparse"]
        )
        hybrid_score = ( 
        0.7*dense_score +
        0.3*sparse_score
        )
        results.append({
            "uid": document["uid"],
            "text": document["text"],
            # "score": hybrid_score
            "score": score
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]