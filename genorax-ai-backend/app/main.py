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
    SampleInterpretationRequest,
    SampleInterpretationResponse,
    ResponseMetadata,
)
from app.services.gene_service import analyze_genes
from app.services.mutation_service import analyze_mutations
from app.services.sample_service import analyze_sample
from app.utils.response_builder import build_gene_response, build_mutation_response

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("genorax-api")

app = FastAPI(
    title="Genorax AI Backend",
    version="0.2.0",
    description=(
        "Genorax AI Backend for biomedical reasoning over genes, mutations, "
        "and sample-level sequencing findings. The backend uses FastAPI, "
        "structured JSON responses, OpenAI reasoning, and fallback-safe service logic."
    ),
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
        "version": "0.2.0",
    }


@app.post("/analyze-gene-list", response_model=GeneAnalysisResponse, tags=["Analysis"])
def analyze_gene_list(payload: GeneListRequest) -> GeneAnalysisResponse:
    """Analyze a list of genes with LLM reasoning and fallback output."""
    results = analyze_genes(payload.genes, payload.disease_context)
    return build_gene_response(payload.disease_context, results)


@app.post(
    "/analyze-mutation-list",
    response_model=MutationAnalysisResponse,
    tags=["Analysis"],
)
def analyze_mutation_list(payload: MutationListRequest) -> MutationAnalysisResponse:
    """Analyze a list of mutations with LLM reasoning and fallback output."""
    results = analyze_mutations(payload.mutations, payload.disease_context)
    return build_mutation_response(payload.disease_context, results)


@app.post(
    "/analyze-sample-summary",
    response_model=SampleInterpretationResponse,
    tags=["Analysis"],
)
def analyze_sample_summary(payload: SampleInterpretationRequest) -> SampleInterpretationResponse:
    """Analyze an entire sample by integrating genes, mutations, and notes."""
    result = analyze_sample(
        sample_id=payload.sample_id,
        disease_context=payload.disease_context,
        genes=payload.genes,
        mutations=payload.mutations,
        notes=payload.notes,
    )
    fallback_used = "fallback" in result.limitations.lower()
    return SampleInterpretationResponse(
        disease_context=payload.disease_context,
        result=result,
        metadata=ResponseMetadata(
            model="openai_or_fallback",
            result_count=1,
            fallback_used=fallback_used,
        ),
    )
