from retrieval import retrieve_all_samples
from document import samples_to_text
from embeddings import (
    create_embedding,
    create_embeddings
)


samples = retrieve_all_samples()

documents = samples_to_text(samples)

text = documents[0]["text"]

embedding = create_embedding(text)

# print("Text:")
# print(text)

# print("\nEmbedding:")
# print(embedding)

# print("\nEmbedding length:")
# print(len(embedding))

embedded_documents = create_embeddings(documents)
print(len(embedded_documents))