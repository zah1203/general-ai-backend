"""FastAPI application entrypoint for Genorax AI Backend."""

import logging
import time
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.schemas import (
    GeneAnalysisResponse,
    GeneListRequest,
    MutationAnalysisResponse,
    MutationListRequest,
)
from app.services.gene_service import analyze_genes
from app.services.mutation_service import analyze_mutations
from app.utils.response_builder import build_gene_response, build_mutation_response

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("genorax-api")

app = FastAPI(
    title="Genorax AI Backend",
    version="0.1.0",
    description="Backend skeleton for AI genomics workflows using mock analysis logic.",
)


@app.middleware("http")
async def log_requests(request: Request, call_next: Any) -> JSONResponse:
    """Log incoming requests and response statuses."""
    start_time = time.perf_counter()
    logger.info("Incoming request: %s %s", request.method, request.url.path)
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("Unhandled error for request: %s %s", request.method, request.url.path)
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

    process_time = (time.perf_counter() - start_time) * 1000
    logger.info(
        "Completed request: %s %s status=%s duration_ms=%.2f",
        request.method,
        request.url.path,
        response.status_code,
        process_time,
    )
    return response


@app.get("/health", tags=["System"])
def health_check() -> Dict[str, str]:
    """Return service health metadata."""
    return {
        "status": "healthy",
        "service": "genorax-ai-backend",
        "version": "0.1.0",
    }


@app.post("/analyze-gene-list", response_model=GeneAnalysisResponse, tags=["Analysis"])
def analyze_gene_list(payload: GeneListRequest) -> GeneAnalysisResponse:
    """Analyze a list of genes with mock output.

    Args:
        payload: Gene list request payload.

    Returns:
        Mock gene analysis response.
    """
    results = analyze_genes(payload.genes)
    return build_gene_response(payload.disease_context, results)


@app.post(
    "/analyze-mutation-list",
    response_model=MutationAnalysisResponse,
    tags=["Analysis"],
)
def analyze_mutation_list(payload: MutationListRequest) -> MutationAnalysisResponse:
    """Analyze a list of mutations with mock output.

    Args:
        payload: Mutation list request payload.

    Returns:
        Mock mutation analysis response.
    """
    results = analyze_mutations(payload.mutations)
    return build_mutation_response(payload.disease_context, results)
