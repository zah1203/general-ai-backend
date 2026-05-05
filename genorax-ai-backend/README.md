# Genorax AI Backend

Genorax AI Backend is a FastAPI service for AI-assisted genomics workflows. The backend now includes an OpenAI-powered reasoning layer for structured colorectal cancer interpretation of genes and mutations, with safe mock fallback when LLM access is unavailable.

## Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic
- OpenAI Python SDK

## Project Structure

```text
genorax-ai-backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gene_service.py
│   │   ├── llm_service.py
│   │   └── mutation_service.py
│   └── utils/
│       ├── __init__.py
│       └── response_builder.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## Local Setup

```bash
cd genorax-ai-backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Environment Variables

- `OPENAI_API_KEY` (required for live LLM responses)
- `OPENAI_MODEL` (optional, default: `gpt-4o-mini`)

### Windows / Git Bash

```bash
export OPENAI_API_KEY="your_key_here"
export OPENAI_MODEL="gpt-4o-mini"
```

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

## Docker

```bash
cd genorax-ai-backend
docker build -t genorax-ai-backend .
docker run -d \
--name genorax-ai-backend \
-p 8000:8000 \
-e OPENAI_API_KEY="your_key_here" \
-e OPENAI_MODEL="gpt-4o-mini" \
genorax-ai-backend
```

## API Endpoints

- `GET /health`
- `POST /analyze-gene-list`
- `POST /analyze-mutation-list`

## Example Requests

### Analyze Gene List

```bash
curl -X POST "http://127.0.0.1:8000/analyze-gene-list" \
  -H "Content-Type: application/json" \
  -d '{
    "genes": ["KRAS", "TP53", "APC"],
    "disease_context": "colorectal cancer"
  }'
```

### Analyze Mutation List

```bash
curl -X POST "http://127.0.0.1:8000/analyze-mutation-list" \
  -H "Content-Type: application/json" \
  -d '{
    "mutations": ["KRAS G12D", "TP53 R175H", "BRAF V600E"],
    "disease_context": "colorectal cancer"
  }'
```

If `OPENAI_API_KEY` is missing or the OpenAI call fails, the API returns schema-compatible mock values with an explanation that LLM is unavailable.
