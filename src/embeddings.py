import ollama
import pickle
import os

EMBEDDING_FILE = "../data/embeddings/nomic_embed_text_embeddings.pkl"

ALLOWED_FIELDS = {
    "uid",
    "peptide_name",
    "peptide",
    "water",
    "haucl4",
    "hepes",
    "slot",
    "wellcode",
    "wellindex",
    "labwaretype"
}

ALLOWED_OPERATORS = {
    "=",
    "!=",
    "<",
    ">",
    "<=",
    ">=",
    "IN",
    "NOT IN"
}
def create_embedding(text):

    response = ollama.embed(
        model="nomic-embed-text",
        input=text
    )
    return response["embeddings"][0]

def create_embeddings(documents):
    # print(type(documents))
    # print(type(documents[0]))
    # print(documents[0])
    embedded_documents = []
    for document in documents:
        embedding = create_embedding(document["text"])
        embedded_documents.append({
            "uid": document["uid"],

            "metadata": {
                "peptide": document["peptide"],
                "peptide_name": document["peptide_name"],
                "water": document["water"],
                "haucl4": document["haucl4"],
                "hepes": document["hepes"],
                "slot": document["slot"],
                "labwaretype": document["labwaretype"],
                "wellcode": document["wellcode"],
                "wellindex": document["wellindex"]
            },
            
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

def get_embeddings(documents=None):

    if os.path.exists(EMBEDDING_FILE):
        print("Loading existing embeddings...")
        return load_embeddings(EMBEDDING_FILE)
    if documents is None:
        raise ValueError("Documents are required to create embeddings.")
    
    print("Creating embeddings...")
    embedded_documents = create_embeddings(documents)
    save_embeddings(embedded_documents,EMBEDDING_FILE)
    print("Embeddings created and saved.")
    
    return embedded_documents

def filter_embedded_documents(documents, filters):


    if not filters:
        return documents
    
    filtered_documents = documents

    def get_field_value(document, field):
        if field == "uid":
            return document.get(field)
        return document.get("metadata", {}).get(field)

    for filter_item in filters:

        field = filter_item["field"]
        operator = filter_item["operator"]
        value = filter_item["value"]

        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Invalid field: {field}")

        if operator not in ALLOWED_OPERATORS:
            raise ValueError(f"Invalid operator: {operator}")

        if operator == "=":

            filtered_documents = [
                document
                for document in filtered_documents
                if get_field_value(document, field) == value
            ]

        elif operator == "!=":

            filtered_documents = [
                document
                for document in filtered_documents
                if get_field_value(document, field) != value
            ]

        elif operator == "IN":

            if not isinstance(value, list):
                raise ValueError("IN requires a list")

            if not value:
                continue

            filtered_documents = [
                document
                for document in filtered_documents
                if get_field_value(document, field) in value
            ]

        elif operator == "NOT IN":

            if not isinstance(value, list):
                raise ValueError("NOT IN requires a list")

            if not value:
                continue

            filtered_documents = [
                document
                for document in filtered_documents
                if get_field_value(document, field) not in value
            ]

        elif operator == ">":

            filtered_documents = [
                document
                for document in filtered_documents
                if get_field_value(document, field) is not None
                and get_field_value(document, field) > value
            ]

        elif operator == "<":

            filtered_documents = [
                document
                for document in filtered_documents
                if get_field_value(document, field) is not None
                and get_field_value(document, field) < value
            ]

        elif operator == ">=":

            filtered_documents = [
                document
                for document in filtered_documents
                if get_field_value(document, field) is not None
                and get_field_value(document, field) >= value
            ]

        elif operator == "<=":

            filtered_documents = [
                document
                for document in filtered_documents
                if get_field_value(document, field) is not None
                and get_field_value(document, field) <= value
            ]

    return filtered_documents