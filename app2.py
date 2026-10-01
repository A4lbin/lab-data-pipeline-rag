import streamlit as st
import pandas as pd

from src.query_parser import parse_query
from src.embeddings import get_embeddings, filter_embedded_documents
from src.answer_generator import generate_answer
from src.retrieval import retrieve_all_samples, retrieve_samples_by_filters
from src.document import samples_to_text


def _documents_to_dataframe(documents):
    return pd.DataFrame([
        {"uid": document.get("uid"), **document.get("metadata", {})}
        for document in documents
    ])


def ask_lab_page():
    st.title("Lab Data RAG")
    st.write("Ask questions about the laboratory experiment dataset.")

    samples = retrieve_all_samples()
    document = samples_to_text(samples)
    query = st.text_input("Enter your query:")

    if st.button("Search"):
        if not query:
            st.warning("Please enter a query.")
        else:
            with st.spinner("Searching..."):
                documents = get_embeddings(document)
                parsed_query = parse_query(query)
                filters = parsed_query["filters"]
                filtered_documents = filter_embedded_documents(
                    documents,
                    filters
                )
                answer = generate_answer(query, filtered_documents)

            st.session_state.llm_results = filtered_documents
            st.session_state.llm_filters = filters
            st.session_state.llm_answer = answer

    if "llm_results" in st.session_state:
        st.subheader("Matching records")
        st.dataframe(
            _documents_to_dataframe(st.session_state.llm_results),
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            f"Matching experiments: {len(st.session_state.llm_results)}"
        )
        st.subheader("Answer")
        st.write(st.session_state.llm_answer)
        with st.expander("Parsed filters"):
            st.json(st.session_state.llm_filters)


def records_page():
    st.title("Lab Records")
    st.write("Browse every experiment and apply database filters manually.")

    all_samples = retrieve_all_samples()
    all_records = pd.DataFrame(all_samples)
    if all_records.empty:
        st.warning("No records are available.")
        return

    if "record_filters" not in st.session_state:
        st.session_state.record_filters = []

    fields = list(all_records.columns)
    numeric_fields = {
        field for field in fields
        if pd.api.types.is_numeric_dtype(all_records[field])
    }

    with st.sidebar:
        st.header("Manual filters")
        field = st.selectbox("Field", fields, key="record_field")
        is_numeric = field in numeric_fields
        operators = ["=", "!=", "IN", "NOT IN"]
        if is_numeric:
            operators += [">", "<", ">=", "<="]
        operator = st.selectbox(
            "Operator",
            operators,
            key="record_operator",
        )

        value_text = st.text_input(
            "Value(s)" if operator in {"IN", "NOT IN"} else "Value",
            placeholder="Separate values with commas"
            if operator in {"IN", "NOT IN"}
            else None,
            key="record_value",
        )

        if st.button("Add filter", use_container_width=True):
            values = [item.strip() for item in value_text.split(",")]
            if not value_text.strip() or any(not item for item in values):
                st.warning("Enter one or more values before adding a filter.")
            else:
                try:
                    filter_value = (
                        [float(item) for item in values]
                        if is_numeric
                        else values
                    )
                except ValueError:
                    st.error("Numeric fields require numeric values.")
                else:
                    if operator not in {"IN", "NOT IN"}:
                        filter_value = filter_value[0]
                    st.session_state.record_filters.append({
                        "field": field,
                        "operator": operator,
                        "value": filter_value,
                    })
                    st.rerun()

        if st.button("Clear filters", use_container_width=True):
            st.session_state.record_filters = []
            st.rerun()

        for index, filter_item in enumerate(st.session_state.record_filters):
            filter_column, remove_column = st.columns([5, 1])
            filter_column.caption(
                f"{filter_item['field']} {filter_item['operator']} "
                f"{filter_item['value']}"
            )
            if remove_column.button("X", key=f"remove_filter_{index}"):
                st.session_state.record_filters.pop(index)
                st.rerun()

    filters = st.session_state.record_filters
    samples = retrieve_samples_by_filters(filters) if filters else all_samples
    records = pd.DataFrame(samples)
    st.metric("Matching records", len(records))
    st.dataframe(records, use_container_width=True, hide_index=True)


navigation = st.navigation([
    st.Page(ask_lab_page, title="Ask the Lab", icon=":material/search:"),
    st.Page(records_page, title="All Records", icon=":material/table_view:"),
])
navigation.run()