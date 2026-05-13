"""Service functions for gene analysis with LLM + fallback."""

from typing import List

from app.schemas import GeneAnalysisResult
from app.services.llm_service import analyze_gene_with_llm


def _mock_gene_result(gene: str, reason: str) -> GeneAnalysisResult:
    return GeneAnalysisResult(
        gene=gene,
        predicted_role="mock_role_pending_ai",
        pathway="mock_pathway_pending_ai",
        confidence=0.5,
        explanation=f"LLM unavailable, fallback mock response used: {reason}",
        evidence_summary="Fallback response generated because LLM reasoning was unavailable.",
    )


def analyze_genes(genes: List[str], disease_context: str) -> List[GeneAnalysisResult]:
    """Generate gene analysis results using LLM with safe fallback."""
    results: List[GeneAnalysisResult] = []

    for gene in genes:
        try:
            llm_result = analyze_gene_with_llm(
                gene=gene,
                disease_context=disease_context,
            )

            results.append(
                GeneAnalysisResult(
                    gene=gene,
                    predicted_role=llm_result.get("predicted_role", "unknown"),
                    pathway=llm_result.get("pathway", "unknown"),
                    confidence=float(llm_result.get("confidence", 0.5)),
                    explanation=llm_result.get(
                        "explanation",
                        "No explanation provided.",
                    ),
                    evidence_summary=llm_result.get(
                        "evidence_summary",
                        "No structured evidence summary returned.",
                    ),
                )
            )

        except Exception as exc:  # noqa: BLE001 - fallback guard
            results.append(_mock_gene_result(gene, str(exc)))

    return results
