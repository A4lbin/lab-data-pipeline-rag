import ollama
import pickle
import os
EMBEDDING_FILE = "../data/embeddings/nomic_embed_text_embeddings.pkl"

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

def save_embeddings(embedded_documents, filepath):

    with open(filepath, "wb") as file:
        pickle.dump(embedded_documents, file)


def load_embeddings(filepath):

    with open(filepath, "rb") as file:
        return pickle.load(file)

def get_embeddings(documents):

    if os.path.exists(EMBEDDING_FILE):
        print("Loading existing embeddings...")
        return load_embeddings(EMBEDDING_FILE)
    else:
        print("Creating embeddings...")
        embedded_documents = create_embeddings(documents)
        save_embeddings(embedded_documents,EMBEDDING_FILE)
        print("Embeddings created and saved.")
        return embedded_documents