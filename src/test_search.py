from embeddings import get_embeddings
from document import samples_to_text
from retrieval import retrieve_all_samples
from search import (
    cosine_similarity,
    search_documents
)

samples = retrieve_all_samples()
documents = samples_to_text(samples)
embedded_documents = get_embeddings(documents)

# vector_a = embedded_documents[0]["embedding"]
# vector_b = embedded_documents[228]["embedding"]
# score = cosine_similarity(vector_a, vector_b)

# print(score)


# query = "experiments involving peptide PZ2"

# results = search_documents(
#     query,
#     embedded_documents,
#     top_k=5
# )

# for result in results:

#     print("UID:", result["uid"])
#     print("Score:", result["score"])
#     print(result["text"])
#     print("--------------------")

queries = [
    "experiments involving peptide PZ2",
    "experiments involving peptide Z2M6I",
    "experiments involving peptide MZ2R"
]


# Run every query
for query in queries:

    print("\n" + "=" * 60)
    print("QUERY:", query)
    print("=" * 60)

    results = search_documents(
        query,
        embedded_documents,
        top_k=5
    )

    for rank, result in enumerate(results, start=1):

        print(f"\nRank: {rank}")
        print("UID:", result["uid"])
        print("Score:", round(result["score"], 4))
        print(result["text"])