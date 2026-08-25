from retrieval import retrieve_all_samples
from document import samples_to_text

from embeddings import (
    create_embeddings,
    save_embeddings
)


samples = retrieve_all_samples()

documents = samples_to_text(samples)

embedded_documents = create_embeddings(documents)

save_embeddings(
    embedded_documents,
    "../data/embeddings/bge_m3_embeddings.pkl"
)

print("Embeddings saved.")
print("Number of documents:", len(embedded_documents))