# Lab Data Pipeline RAG

A lightweight data pipeline and retrieval project for laboratory sample records. The project loads raw CSV data, cleans and validates it, stores it in SQLite, and exposes query and retrieval helpers that can be used with an Ollama-backed local LLM workflow.

## Overview

This repository combines:

- a small ETL pipeline for CSV processing
- SQLite-based sample storage and lookup
- retrieval helpers that convert database rows into text documents
- local semantic retrieval using the `nomic-embed-text` embedding model
- a simple Ollama generation example with `qwen3.5:4b`

## Prerequisites

- Python 3.10+
- Ollama installed and running locally
- Access to the data files in the repository

## Setup

### 1) Create and activate a virtual environment

From the project root:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Start Ollama and pull the models

This project uses:

- generation model: `qwen3.5:4b`
- embedding model: `nomic-embed-text`

```bash
ollama pull qwen3.5:4b
ollama pull nomic-embed-text
```

If Ollama is not installed, download it from:

https://ollama.com/download

## Data pipeline

The raw dataset is read from:

- `data/raw/4x4x4_SI.csv`

The ETL step cleans and normalizes the data and writes the processed output to:

- `data/processed/lab_data_clean.csv`

The cleaning logic lives in `src/etl.py` and includes:

- column name normalization
- duplicate removal
- numeric coercion
- whitespace cleanup
- validation for required UID values

To run the data processing step:

```bash
python src/etl.py
```

## Database setup

The project stores sample records in SQLite.

The seed script creates the database table from the processed CSV:

```bash
python database/seed.py
```

This creates `database/lab.db` using the data in `data/processed/lab_data_clean.csv`.

## Query and retrieval modules

The project includes query helpers in `src/queries.py`:

- `get_sample_by_uid(uid)`
- `get_samples_by_peptide(peptide)`
- `get_samples_by_well(wellcode)`
- `get_peptide_counts()`
- `get_all_samples()`

The retrieval layer in `src/retrieval.py` wraps these queries and converts rows into structured dictionaries or text documents.

### Example

```bash
python src/test_queries.py
python src/test_retrieval.py
```

## Ollama example app

The app entry point in `app.py` shows a minimal Ollama chat request:

```bash
python app.py
```

This verifies that the local model is reachable and is useful as a smoke test before building a more advanced RAG workflow.

## Project structure

```text
lab-data-pipeline-rag/
├── app.py
├── Readme.md
├── requirements.txt
├── sources.txt
├── data/
│   ├── raw/
│   └── processed/
├── database/
│   ├── seed.py
│   └── select.py
├── src/
│   ├── database.py
│   ├── document.py
│   ├── etl.py
│   ├── queries.py
│   ├── retrieval.py
│   ├── test_document.py
│   ├── test_queries.py
│   └── test_retrieval.py
└── .venv/   # local virtual environment
```
