"""Utilities for building API responses."""

from typing import List

from app.schemas import (
    GeneAnalysisResponse,
    GeneAnalysisResult,
    MutationAnalysisResponse,
    MutationAnalysisResult,
)


def build_gene_response(
    disease_context: str, results: List[GeneAnalysisResult]
) -> GeneAnalysisResponse:
    """Build a response object for gene list analysis.

    Args:
        disease_context: Disease context passed by the caller.
        results: Mock gene analysis results.

    Returns:
        Structured API response for gene analysis.
    """
    return GeneAnalysisResponse(
        input_type="gene_list",
        disease_context=disease_context,
        results=results,
    )


def build_mutation_response(
    disease_context: str, results: List[MutationAnalysisResult]
) -> MutationAnalysisResponse:
    """Build a response object for mutation list analysis.

    Args:
        disease_context: Disease context passed by the caller.
        results: Mock mutation analysis results.

    Returns:
        Structured API response for mutation analysis.
    """
    return MutationAnalysisResponse(
        input_type="mutation_list",
        disease_context=disease_context,
        results=results,
    )
