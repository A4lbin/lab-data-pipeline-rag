from embeddings import create_embeddings
from document import samples_to_text
from retrieval import retrieve_all_samples
from search import (
    cosine_similarity,
    search_documents
)

samples = retrieve_all_samples()
documents = samples_to_text(samples)
embedded_documents = create_embeddings(documents)

# vector_a = embedded_documents[0]["embedding"]
# vector_b = embedded_documents[228]["embedding"]
# score = cosine_similarity(vector_a, vector_b)

# print(score)


query = "experiments involving peptide PZ2"

results = search_documents(
    query,
    embedded_documents,
    top_k=5
)

for result in results:

    print("UID:", result["uid"])
    print("Score:", result["score"])
    print(result["text"])
    print("--------------------")