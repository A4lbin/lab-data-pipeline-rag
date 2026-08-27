import ollama
import json
from embeddings import (ALLOWED_FIELDS,ALLOWED_OPERATORS)

FILTER_SCHEMA = {
    "type": "object",
    "properties": {
        "filters": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "field": {
                        "type": "string",
                        "enum": [
                            "uid", "peptide", "peptide_name", "water", "haucl4", 
                            "hepes", "slot", "labwaretype", "wellcode", "wellindex"
                        ]
                    },
                    "operator": {
                        "type": "string",
                        "enum": ["=", "!=", "IN", "NOT IN", ">", "<", ">=", "<="]
                    },
                    "value": {
                        "type": ["string", "number", "boolean", "array"]
                    }
                },
                "required": ["field", "operator", "value"],
                "additionalProperties": False
            }
        }
    },
    "required": ["filters"],
    "additionalProperties": False
}

def parse_query(query):
    response = ollama.chat(
        model="qwen3.5:4b",
        messages=[
            {
                "role": "system",
                "content": """
You are a query parser for a laboratory experiment database.
Convert natural language queries into structured filters.

Allowed fields:
uid, peptide, peptide_name, water, haucl4, hepes, slot, labwaretype, wellcode, wellindex

CRITICAL FIELD MAPPINGS:
- If the user mentions MZ2, MZ2R, Z2, PZ2, Z2M6I, Z2M246I, or AG3, you MUST use the field "peptide_name" and mention this filter.
- Do NOT use the "peptide" field for these values.
- Always use operator IN or NOT IN for peptide_names field
- Never use >,<,<=,>= operators for peptide_names
- only use IN or NOT IN or = or != when there is no range for the field
Aliases:
gold, gold concentration, gold precursor -> haucl4
HEPES -> hepes

OPERATOR MAPPINGS:
- below / under / less than -> <
- above / over / greater than -> >
- at least -> >=
- at most -> <=
- equal to / equals / is -> =
- not equal to / different from / not -> !=
- one of / either X or Y / in -> IN
- none of / anything except / not in -> NOT IN
- between X and Y -> create TWO separate filters: >= X and <= Y

CRITICAL RULES FOR VALUES:
- The "value" field MUST be a primitive (string, number) or a list.
- DO NOT use dictionaries or objects for values.
- For IN and NOT IN operators, the "value" MUST be a JSON array (e.g., ["PZ2", "Z2"]).
- For numerical comparisons, "value" must be a number.
- Return ONLY valid JSON matching the schema.
"""
            },
            {
                "role": "user",
                "content": query
            }
        ],
        format=FILTER_SCHEMA,
    )
    
    parsed = json.loads(response["message"]["content"])
    
    # --- POST-PROCESSING ---
    # Guarantee that IN and NOT IN always have a list for the value
    for f in parsed.get("filters", []):
        if f["operator"] in ["IN", "NOT IN"]:
            if not isinstance(f["value"], list):
                f["value"] = [f["value"]]
                
    return parsed

def validate_filters(parsed_query):
    for filter_item in parsed_query["filters"]:
        if filter_item["field"] not in ALLOWED_FIELDS:
            raise ValueError(f"Invalid field: {filter_item['field']}")
        if filter_item["operator"] not in ALLOWED_OPERATORS:
            raise ValueError(f"Invalid operator: {filter_item['operator']}")
    return True

if __name__ == "__main__":
    query = input("Enter your query: ")
    result = parse_query(query)
    print("\nParsed query:")
    print(result)