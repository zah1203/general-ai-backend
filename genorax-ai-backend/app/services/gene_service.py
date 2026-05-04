"""Service functions for mock gene analysis."""

from typing import List

from app.schemas import GeneAnalysisResult


def analyze_genes(genes: List[str]) -> List[GeneAnalysisResult]:
    """Generate mock analysis results for a list of genes.

    Args:
        genes: Gene symbols to analyze.

    Returns:
        A list of mock analysis results.
    """
    return [
        GeneAnalysisResult(
            gene=gene,
            predicted_role="mock_role_pending_ai",
            pathway="mock_pathway_pending_ai",
            confidence=0.5,
            explanation="placeholder explanation",
        )
        for gene in genes
    ]
