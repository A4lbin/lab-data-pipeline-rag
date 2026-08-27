
import ollama
from collections import Counter
def summarize_documents(documents, max_samples=10):
    """
    Creates a token-efficient statistical summary of filtered documents.
    
    Args:
        documents: List of document dictionaries with 'uid' and 'metadata' keys
        max_samples: Maximum number of sample records to include (default: 10)
    
    Returns:
        A formatted string containing statistics and sample records
    """
    if not documents:
        return "No documents to summarize."
    
    total_count = len(documents)
    
    # Collect all metadata values by field
    field_values = {}
    for doc in documents:
        metadata = doc.get("metadata", {})
        for field, value in metadata.items():
            if field not in field_values:
                field_values[field] = []
            field_values[field].append(value)
    
    # Build summary sections
    summary_lines = [f"### DATASET SUMMARY ({total_count} total records)\n"]
    
    # Analyze each field
    for field, values in field_values.items():
        # Filter out None values
        valid_values = [v for v in values if v is not None]
        
        if not valid_values:
            continue
        
        # Check if numeric
        is_numeric = all(isinstance(v, (int, float)) for v in valid_values)
        
        if is_numeric:
            # Numeric statistics
            min_val = min(valid_values)
            max_val = max(valid_values)
            avg_val = sum(valid_values) / len(valid_values)
            unique_count = len(set(valid_values))
            
            summary_lines.append(
                f"**{field}** (numeric): "
                f"count={len(valid_values)}, "
                f"min={min_val:.6g}, "
                f"max={max_val:.6g}, "
                f"avg={avg_val:.6g}, "
                f"unique_values={unique_count}"
            )
        else:
            # Categorical statistics
            value_counts = Counter(valid_values)
            unique_values = list(value_counts.keys())
            
            # Show top values with counts
            top_values = value_counts.most_common(10)
            top_str = ", ".join([f"{v}({c})" for v, c in top_values])
            
            summary_lines.append(
                f"**{field}** (categorical): "
                f"unique_values={len(unique_values)}, "
                f"top_values=[{top_str}]"
            )
    
    # Add sample records
    summary_lines.append(f"\n### SAMPLE RECORDS (showing {min(max_samples, total_count)} of {total_count})")
    
    for i, doc in enumerate(documents[:max_samples]):
        uid = doc.get("uid", "Unknown")
        metadata = doc.get("metadata", {})
        
        # Format metadata as key-value pairs
        meta_parts = [f"{k}={v}" for k, v in metadata.items()]
        meta_str = ", ".join(meta_parts)
        
        summary_lines.append(f"[{i+1}] UID: {uid} | {meta_str}")
    
    return "\n".join(summary_lines)

def documents_to_context(documents):
    """Formats filtered documents into a clean, token-efficient string for the LLM."""
    context_lines = []
    for i, doc in enumerate(documents):
        uid = doc.get("uid", "Unknown")
        meta = doc.get("metadata", {})
        
        meta_str = " | ".join([f"{k}: {v}" for k, v in meta.items()])
        context_lines.append(f"[{i+1}] UID: {uid} | {meta_str}")
        
    return "\n".join(context_lines)


def get_sample_documents(documents, n=5):
    return documents[:n]

def generate_answer(query, documents):

    if not documents:
        return "No experiments matched the query."

    summary = summarize_documents(documents)
    samples = get_sample_documents(documents, 5)
    sample_context = documents_to_context(samples)

    response = ollama.chat(
        model="qwen3.5:4b",
        messages=[
            {
                "role": "system",
                "content": """
You are a lab data assistant. 
The user asked a query, and Python has ALREADY filtered the data.
You are now given the {total_count} MATCHING records. DO NOT re-filter them.

Your job is to SUMMARIZE these matching records, not to check if they match.

Rules:
1. Confirm that {total_count} experiments matched the user's query.
2. Describe the range of values found (use the min/max/avg stats).
3. DO NOT say "no samples were found" — the samples ARE the ones listed below.
4. When comparing numbers, remember: 0.00004 < 0.0001 (smaller decimals are smaller numbers).
5. Keep answers concise and professional.
"""
            },
            {
                "role": "user",
                "content": f"""
### PYTHON-GENERATED SUMMARY

{summary}

### 5 SAMPLE RECORDS

{sample_context}

### USER QUERY

{query}
"""
            }
        ],
        think=False
    )

    return response["message"]["content"]

# if __name__ == "__main__":

#     print("Answering question using qwen3.5:4b\n")
#     documents = [
#         {
#             "uid": "test001",
#             "metadata": {
#                 "peptide_name": "PZ2",
#                 "water": 100,
#                 "haucl4": 0.00005,
#                 "hepes": 10
#             },
#             "text": "Experiment using PZ2 with 100 units of water and 0.00005 HAuCl4.",
#             "embedding": []
#         }
#     ]

#     query = "What was the HAuCl4 concentration in the PZ2 experiment?"

#     answer = generate_answer(query, documents)

#     print(answer)