import pandas as pd
import streamlit as st

from src.retrieval import retrieve_all_samples, retrieve_samples_by_filters


st.title("Lab Records")
st.write("Browse every experiment and apply database filters manually.")

all_samples = retrieve_all_samples()
all_records = pd.DataFrame(all_samples)

if "record_filters" not in st.session_state:
    st.session_state.record_filters = []

if all_records.empty:
    st.warning("No records are available.")
    st.stop()

fields = list(all_records.columns)
numeric_fields = {
    field for field in fields
    if pd.api.types.is_numeric_dtype(all_records[field])
}

with st.sidebar:
    st.header("Manual filters")
    field = st.selectbox("Field", fields)
    is_numeric = field in numeric_fields
    operators = ["=", "!=", "IN", "NOT IN"]
    if is_numeric:
        operators += [">", "<", ">=", "<="]
    operator = st.selectbox("Operator", operators)

    if operator in {"IN", "NOT IN"}:
        value_text = st.text_input(
            "Values",
            placeholder="Separate values with commas",
        )
    elif is_numeric:
        value = st.number_input("Value", value=0.0)
        value_text = str(value)
    else:
        value_text = st.text_input("Value")

    if st.button("Add filter", use_container_width=True):
        if not value_text.strip():
            st.warning("Enter a value before adding a filter.")
        else:
            values = [item.strip() for item in value_text.split(",")]
            if operator in {"IN", "NOT IN"}:
                filter_value = values
            else:
                filter_value = values[0]

            if is_numeric:
                try:
                    numeric_values = [float(item) for item in values]
                except ValueError:
                    st.error("Numeric fields require numeric values.")
                else:
                    filter_value = (
                        numeric_values
                        if operator in {"IN", "NOT IN"}
                        else numeric_values[0]
                    )
                    st.session_state.record_filters.append(
                        {
                            "field": field,
                            "operator": operator,
                            "value": filter_value,
                        }
                    )
                    st.rerun()
            else:
                st.session_state.record_filters.append(
                    {
                        "field": field,
                        "operator": operator,
                        "value": filter_value,
                    }
                )
                st.rerun()

    if st.button("Clear filters", use_container_width=True):
        st.session_state.record_filters = []
        st.rerun()

    if st.session_state.record_filters:
        st.subheader("Active filters")
        for index, filter_item in enumerate(st.session_state.record_filters):
            label = (
                f"{filter_item['field']} {filter_item['operator']} "
                f"{filter_item['value']}"
            )
            filter_column, remove_column = st.columns([5, 1])
            filter_column.caption(label)
            if remove_column.button("X", key=f"remove_filter_{index}"):
                st.session_state.record_filters.pop(index)
                st.rerun()

active_filters = st.session_state.record_filters
if active_filters:
    samples = retrieve_samples_by_filters(active_filters)
else:
    samples = all_samples

records = pd.DataFrame(samples)
st.metric("Matching records", len(records))
st.dataframe(records, use_container_width=True, hide_index=True)
