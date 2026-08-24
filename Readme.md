# Lab Data Pipeline RAG

A lightweight Python project that uses Ollama to generate responses from a local model.

## Prerequisites

- Python 3.10+
- Ollama installed and running locally

## 1) Create a virtual environment

From the project root:

```bash
python -m venv .venv
```

Activate it:

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Windows Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

## 2) Install dependencies

```bash
pip install -r requirements.txt
```

## 3) Pull the model

This project uses the Ollama `qwen3.5:4b` model for generation.

```bash
ollama pull qwen3.5:4b
```

If Ollama is not installed yet, install it from:

https://ollama.com/download

## 4) Run the app

```bash
python app.py
```

## Project structure

```text
lab-data-pipeline-rag/
├── app.py
├── requirements.txt
├── sources.txt
├── data/
│   ├── raw/
│   └── processed/
├── src/
└── .venv/
```

## Notes

- The virtual environment should stay local and is ignored by Git.
- Generated output under `data/processed/` is intended for local pipeline artifacts.
- The app expects Ollama to be available locally on your machine.