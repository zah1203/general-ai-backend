# Genorax AI Backend

Genorax AI Backend is a production-ready FastAPI skeleton for an AI genomics platform.
It currently uses **mock analysis logic** and a modular architecture so real AI inference can be added later.

## Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic

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
│   │   └── mutation_service.py
│   └── utils/
│       ├── __init__.py
│       └── response_builder.py
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md
```

## Local Setup (fixes `ModuleNotFoundError: No module named 'fastapi'`)

Run these commands from the `genorax-ai-backend` directory:

```bash
cd genorax-ai-backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If dependency installation succeeds, `fastapi` and `uvicorn` will be available in the virtual environment.

## Run the Server

```bash
cd genorax-ai-backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API base URL: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

## API Endpoints

### Health Check

```bash
curl -X GET "http://127.0.0.1:8000/health"
```

### Analyze Gene List

```bash
curl -X POST "http://127.0.0.1:8000/analyze-gene-list" \
  -H "Content-Type: application/json" \
  -d '{
    "genes": ["KRAS", "TP53"],
    "disease_context": "colorectal cancer"
  }'
```

### Analyze Mutation List

```bash
curl -X POST "http://127.0.0.1:8000/analyze-mutation-list" \
  -H "Content-Type: application/json" \
  -d '{
    "mutations": ["KRAS G12D"],
    "disease_context": "colorectal cancer"
  }'
```

### Validation Error Example (empty list)

```bash
curl -X POST "http://127.0.0.1:8000/analyze-gene-list" \
  -H "Content-Type: application/json" \
  -d '{
    "genes": [],
    "disease_context": "colorectal cancer"
  }'
```

The API returns HTTP `422` with validation details.

## Docker

```bash
cd genorax-ai-backend
docker build -t genorax-ai-backend .
docker run --rm -p 8000:8000 genorax-ai-backend
```

## Git Setup & GitHub Push

```bash
# 1) Initialize git (if needed)
git init

# 2) Add files
git add .

# 3) Commit
git commit -m "Initial commit: Genorax AI Backend FastAPI skeleton"

# 4) Create GitHub repo (requires GitHub CLI auth)
gh repo create genorax-ai-backend --public --source=. --remote=origin --push

# 5) Push code (if repo already exists)
git branch -M main
git remote add origin https://github.com/<your-username>/genorax-ai-backend.git
git push -u origin main
```
