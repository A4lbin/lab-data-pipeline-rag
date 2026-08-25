import numpy as np
from embeddings import create_embedding

def cosine_similarity(vector_a, vector_b):

    vector_a = np.array(vector_a)
    vector_b = np.array(vector_b)

    similarity = np.dot(vector_a, vector_b) / (
        np.linalg.norm(vector_a) *
        np.linalg.norm(vector_b)
    )

    return similarity

def search_documents(query, embedded_documents, top_k=5):

    query_embedding = create_embedding(query)
    results = []
    for document in embedded_documents:
        score = cosine_similarity(
            query_embedding,
            document["embedding"]
        )
        results.append({
            "uid": document["uid"],
            "text": document["text"],
            "score": score
        })
        
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]