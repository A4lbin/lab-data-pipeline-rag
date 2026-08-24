import ollama

response = ollama.chat(
    model="qwen3.5:4b",
    messages=[
        {
            "role": "user",
            "content": "What is ETL?"
        }
    ]
)

print(response["message"]["content"])