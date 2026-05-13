"""Utilities for building clean Genorax API responses."""

import os
from typing import List

from app.schemas import (
    GeneAnalysisResponse,
    GeneAnalysisResult,
    MutationAnalysisResponse,
    MutationAnalysisResult,
    ResponseMetadata,
)


def _get_model_name() -> str:
    """Return configured OpenAI model name."""
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def _fallback_used(results: List[object]) -> bool:
    """Detect whether fallback/mock response was used."""
    for result in results:
        explanation = getattr(result, "explanation", "")
        if "fallback mock response used" in explanation.lower():
            return True
    return False


def build_gene_response(
    disease_context: str, results: List[GeneAnalysisResult]
) -> GeneAnalysisResponse:
    """Build a clean response object for gene list analysis."""
    return GeneAnalysisResponse(
        status="success",
        analysis_type="gene_list",
        disease_context=disease_context,
        summary=f"Analyzed {len(results)} gene(s) in the context of {disease_context}.",
        results=results,
        metadata=ResponseMetadata(
            model=_get_model_name(),
            result_count=len(results),
            fallback_used=_fallback_used(results),
        ),
    )


def build_mutation_response(
    disease_context: str, results: List[MutationAnalysisResult]
) -> MutationAnalysisResponse:
    """Build a clean response object for mutation list analysis."""
    return MutationAnalysisResponse(
        status="success",
        analysis_type="mutation_list",
        disease_context=disease_context,
        summary=f"Analyzed {len(results)} mutation(s) in the context of {disease_context}.",
        results=results,
        metadata=ResponseMetadata(
            model=_get_model_name(),
            result_count=len(results),
            fallback_used=_fallback_used(results),
        ),
    )
