"""Service functions for mock mutation analysis."""

from typing import List

from app.schemas import MutationAnalysisResult


def analyze_mutations(mutations: List[str]) -> List[MutationAnalysisResult]:
    """Generate mock analysis results for a list of mutations.

    Args:
        mutations: Mutation identifiers to analyze.

    Returns:
        A list of mock analysis results.
    """
    return [
        MutationAnalysisResult(
            mutation=mutation,
            predicted_impact="mock_impact_pending_ai",
            pathway="mock_pathway_pending_ai",
            confidence=0.5,
            explanation="placeholder explanation",
        )
        for mutation in mutations
    ]
