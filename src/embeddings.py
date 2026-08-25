# import ollama
import os
import pickle
from FlagEmbedding import BGEM3FlagModel


model = BGEM3FlagModel(
    "BAAI/bge-m3",
    use_fp16=True
)

EMBEDDING_FILE = "../data/embeddings/bge_m3_embeddings.pkl"

def create_embeddings(documents):

    texts = [document["text"] for document in documents]

    output = model.encode(
        texts,
        batch_size=12,
        max_length=8192,
        return_dense=True,
        return_sparse=True,
        return_colbert_vecs=False
    )

    dense_embeddings = output["dense_vecs"]
    sparse_embeddings = output["lexical_weights"]

    embedded_documents = []

    for document, dense, sparse in zip(
        documents,
        dense_embeddings,
        sparse_embeddings
    ):

        embedded_documents.append({
            "uid": document["uid"],
            "text": document["text"],
            "dense": dense,
            "sparse": sparse
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

def create_query_embedding(query):
    
    output = model.encode(
        [query],
        return_dense=True,
        return_sparse=True,
        return_colbert_vecs=False
    )

    return {
        "dense": output["dense_vecs"][0],
        "sparse": output["lexical_weights"][0]
    }

# def create_embedding(text):

#     response = ollama.embed(
#         model="bge-m3",
#         input=text
#     )
#     return response["embeddings"][0]

# def create_embeddings(documents):

#     embedded_documents = []
#     for document in documents:
#         embedding = create_embedding(document["text"])
#         embedded_documents.append({
#             "uid": document["uid"],
#             "text": document["text"],
#             "embedding": embedding
#         })
#     return embedded_documents
