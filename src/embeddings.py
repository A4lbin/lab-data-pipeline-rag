import ollama

def create_embedding(text):

    response = ollama.embed(
        model="nomic-embed-text",
        input=text
    )
    return response["embeddings"][0]

def create_embeddings(documents):

    embedded_documents = []
    for document in documents:
        embedding = create_embedding(document["text"])
        embedded_documents.append({
            "uid": document["uid"],
            "text": document["text"],
            "embedding": embedding
        })
    return embedded_documents
