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
        explanation = getattr(result, "explanation", "") or ""
        source = getattr(result, "source", "") or ""

        if "fallback" in explanation.lower() or "fallback" in source.lower():
            return True

        if "mock" in explanation.lower() or "mock" in source.lower():
            return True

    return False


def _count_pubmed_records(results: List[object]) -> int:
    """Count PubMed evidence records attached to all results."""
    total = 0

    for result in results:
        pubmed_evidence = getattr(result, "pubmed_evidence", []) or []
        total += len(pubmed_evidence)

    return total


def _count_biobert_entities(results: List[object]) -> int:
    """Count BioBERT/NER entities attached to all results."""
    total = 0

    for result in results:
        biobert_entities = getattr(result, "biobert_entities", []) or []
        total += len(biobert_entities)

    return total


def build_gene_response(
    disease_context: str,
    results: List[GeneAnalysisResult],
) -> GeneAnalysisResponse:
    """Build a clean response object for gene list analysis."""
    result_count = len(results)
    pubmed_count = _count_pubmed_records(results)
    biobert_count = _count_biobert_entities(results)

    return GeneAnalysisResponse(
        status="success",
        analysis_type="gene_list",
        disease_context=disease_context,
        summary=(
            f"Analyzed {result_count} gene(s) in the context of {disease_context}. "
            f"Attached {pubmed_count} PubMed evidence record(s) and "
            f"{biobert_count} BioBERT/NER entity record(s)."
        ),
        results=results,
        metadata=ResponseMetadata(
            model=_get_model_name(),
            result_count=result_count,
            fallback_used=_fallback_used(results),
        ),
    )


def build_mutation_response(
    disease_context: str,
    results: List[MutationAnalysisResult],
) -> MutationAnalysisResponse:
    """Build a clean response object for mutation list analysis."""
    result_count = len(results)
    pubmed_count = _count_pubmed_records(results)
    biobert_count = _count_biobert_entities(results)

    return MutationAnalysisResponse(
        status="success",
        analysis_type="mutation_list",
        disease_context=disease_context,
        summary=(
            f"Analyzed {result_count} mutation(s) in the context of {disease_context}. "
            f"Attached {pubmed_count} PubMed evidence record(s) and "
            f"{biobert_count} BioBERT/NER entity record(s)."
        ),
        results=results,
        metadata=ResponseMetadata(
            model=_get_model_name(),
            result_count=result_count,
            fallback_used=_fallback_used(results),
        ),
    )
