from .retrieval import retrieve_all_samples
from .document import samples_to_text
from .embeddings import (
    create_embedding,
    create_embeddings,
    get_embeddings,
    filter_embedded_documents
)


samples = retrieve_all_samples()

documents = samples_to_text(samples)

# text = documents[0]["text"]

# embedding = create_embedding(text)

# print("Text:")
# print(text)

# print("\nEmbedding:")
# print(embedding)

# print("\nEmbedding length:")
# print(len(embedding))

embedded_documents = get_embeddings(documents)
print(len(embedded_documents))
filters = [
    {
        "field": "peptide_name",
        "operator": "IN",
        "value": ["Z2", "AG3"]
    }
]

candidates = filter_embedded_documents(
    embedded_documents,
    filters
)
# describe(candidates)
help(candidates)