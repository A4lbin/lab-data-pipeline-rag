from .query_parser import parse_query
from .embeddings import get_embeddings, filter_embedded_documents, EMBEDDING_FILE
from .answer_generator import generate_answer


# Load your embedded documents
documents = get_embeddings(EMBEDDING_FILE)


query = input("Enter your query: ")


# 1. Parse natural language query
parsed_query = parse_query(query)

print("\nParsed query:")
print(parsed_query)


# 2. Extract filters
filters = parsed_query["filters"]


# 3. Apply metadata filtering
filtered_documents = filter_embedded_documents(
    documents,
    filters
)
# filtered_documents = filtered_documents[:5]
print("\nNumber of matching documents:")
print(len(filtered_documents))

print("\nStarting answer generation...")
# 4. Generate answer using retrieved documents
answer = generate_answer(
    query,
    filtered_documents
)
print("Answer generation finished!")

print("\nAnswer:")
print(answer)