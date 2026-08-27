from query_parser import parse_query
from embeddings import filter_embedded_documents,get_embeddings,EMBEDDING_FILE


TEST_QUERIES = [
    "Find experiments with peptide name MZ2.",
    "Find experiments where HAuCl4 is less than 0.0001.",
    "Find experiments using Z2 or PZ2.",
    "Find experiments where hepes is exactly 0.001.",
    "Find experiments where slot is 5 and peptide name is AG3.",
    "Find experiments that are not MZ2.",
    "Find experiments where wellindex is between 10 and 20.",
    "Find experiments where peptide is 0.0 and haucl4 is 0.0002.",
    "Find experiments where water is equal to 1.0.",
    "Find experiments with peptide name Z2M246I where HAuCl4 is at most 0.0001.",
    "Show me PZ2 experiments where hepes is greater than 0.0005 and water is above 0.5."
]

documents = get_embeddings(EMBEDDING_FILE)


for query in TEST_QUERIES:

    print("=" * 80)
    print("QUERY:")
    print(query)

    try:
        # 1. Natural language → structured filters
        parsed_query = parse_query(query)

        print("\nPARSED QUERY:")
        print(parsed_query)

        # 2. Extract filters
        filters = parsed_query["filters"]

        # 3. Apply your existing metadata filtering
        filtered_documents = filter_embedded_documents(
            documents,
            filters
        )

        print("\nMATCHING DOCUMENTS:")
        print(len(filtered_documents))

        # for document in filtered_documents:
        #     print(
        #         document["uid"],
        #         document["metadata"]
        #     )

    except Exception as e:
        print("\nERROR:")
        print(e)