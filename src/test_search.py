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


queries = [
    # Peptide identity
    "experiments involving peptide PZ2",
    "experiments involving peptide MZ2R",
    "experiments involving peptide Z2",
    "experiments involving peptide AG3",
    "experiments involving peptide Z2M6I",
    "experiments involving peptide MZ2",

    # # Exact numerical conditions
    # "experiments with peptide concentration 0.0002",
    # "experiments with peptide concentration 0.000065",
    # "experiments with HAuCl4 concentration 0.0002",
    # "experiments with HAuCl4 concentration 0.000093",
    # "experiments with HEPES concentration 0.001",
    # "experiments with HEPES concentration 0.000055",

    # # Combination of categorical + numerical
    # "PZ2 experiments with HAuCl4 concentration 0.0002",
    # "MZ2R experiments with HEPES concentration 0.000055",
    # "Z2 experiments with peptide concentration 0.0002",
    # "AG3 experiments with HAuCl4 concentration 0.000040",

    # # Location/sample queries
    # "experiments in slot 4",
    # "experiments in slot 5",
    # "experiment at well index 31",
    # "experiment at well index 63",
]
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

# for result in results:

#     print("UID:", result["uid"])
#     print("Score:", result["score"])
#     print(result["text"])
#     print("--------------------")