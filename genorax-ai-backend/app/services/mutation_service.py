"""Service functions for mutation analysis with LLM + fallback."""

from typing import List

from app.schemas import MutationAnalysisResult
from app.services.llm_service import analyze_mutation_with_llm


def _mock_mutation_result(mutation: str, reason: str) -> MutationAnalysisResult:
    return MutationAnalysisResult(
        mutation=mutation,
        predicted_impact="mock_impact_pending_ai",
        pathway="mock_pathway_pending_ai",
        confidence=0.5,
        explanation=f"LLM unavailable, fallback mock response used: {reason}",
    )


def analyze_mutations(mutations: List[str], disease_context: str) -> List[MutationAnalysisResult]:
    """Generate mutation analysis results using LLM with safe fallback."""
    results: List[MutationAnalysisResult] = []
    for mutation in mutations:
        try:
            llm_result = analyze_mutation_with_llm(mutation=mutation, disease_context=disease_context)
            results.append(
                MutationAnalysisResult(
                    mutation=mutation,
                    predicted_impact=llm_result.get("predicted_impact", "unknown"),
                    pathway=llm_result.get("pathway", "unknown"),
                    confidence=float(llm_result.get("confidence", 0.5)),
                    explanation=llm_result.get("explanation", "No explanation provided."),
                )
            )
        except Exception as exc:  # noqa: BLE001 - fallback guard
            results.append(_mock_mutation_result(mutation, str(exc)))
    return results
