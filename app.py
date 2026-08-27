import streamlit as st

from src.query_parser import parse_query
from src.embeddings import get_embeddings, filter_embedded_documents
from src.answer_generator import generate_answer
from src.retrieval import retrieve_all_samples
from src.document import samples_to_text

samples = retrieve_all_samples()
document = samples_to_text(samples)

st.title("🧪 Lab Data RAG")
st.write(
    "Ask questions about the laboratory experiment dataset."
)
query = st.text_input(
    "Enter your query:"
)

if st.button("Search"):

    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Searching..."):
            # Load embedded documents
            documents = get_embeddings(document)
            # Parse natural language query
            parsed_query = parse_query(query)
            # Extract filters
            filters = parsed_query["filters"]
            # Apply metadata filtering
            filtered_documents = filter_embedded_documents(
                documents,
                filters
            )
            # Generate answer
            answer = generate_answer(
                query,
                filtered_documents
            )
        st.subheader("Answer")
        st.write(answer)
        st.caption(
            f"Matching experiments: {len(filtered_documents)}"
        )