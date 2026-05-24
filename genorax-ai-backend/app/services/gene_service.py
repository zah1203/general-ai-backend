"""Service functions for gene analysis with LLM + PubMed + BioBERT + fallback."""

from typing import Any, List, Optional

from app.schemas import GeneAnalysisResult
from app.services.llm_service import analyze_gene_with_llm
from app.services.pubmed_service import search_pubmed
from app.services.bio_ner_service import extract_biomedical_entities


def _mock_gene_result(
    gene: str,
    reason: str,
    pubmed_evidence: Optional[List[Any]] = None,
    biobert_entities: Optional[List[Any]] = None,
) -> GeneAnalysisResult:
    """Return safe fallback result if LLM fails."""
    return GeneAnalysisResult(
        gene=gene,
        predicted_role="mock_role_pending_ai",
        pathway="mock_pathway_pending_ai",
        confidence=0.5,
        explanation=f"LLM unavailable, fallback mock response used: {reason}",
        evidence_summary="LLM was unavailable, so evidence summary was not generated.",
        source="fallback_plus_pubmed_biobert",
        pubmed_evidence=pubmed_evidence or [],
        biobert_entities=biobert_entities or [],
    )


def analyze_genes(genes: List[str], disease_context: str) -> List[GeneAnalysisResult]:
    """Generate gene analysis results using PubMed + BioBERT + LLM with safe fallback."""
    results: List[GeneAnalysisResult] = []

    for gene in genes:
        gene_clean = gene.strip().upper()

        pubmed_evidence = search_pubmed(
            query=f"{gene_clean} {disease_context}",
            max_results=3,
        )

        biobert_entities = extract_biomedical_entities(
            text=f"{gene_clean} {disease_context}"
        )

        try:
            llm_result = analyze_gene_with_llm(
                gene=gene_clean,
                disease_context=disease_context,
                pubmed_evidence=pubmed_evidence,
            )

            results.append(
                GeneAnalysisResult(
                    gene=gene_clean,
                    predicted_role=llm_result.get("predicted_role", "unknown"),
                    pathway=llm_result.get("pathway", "unknown"),
                    confidence=float(llm_result.get("confidence", 0.5)),
                    explanation=llm_result.get(
                        "explanation",
                        "No explanation provided.",
                    ),
                    evidence_summary=llm_result.get(
                        "evidence_summary",
                        "No evidence summary provided.",
                    ),
                    source="openai_llm_plus_pubmed_biobert",
                    pubmed_evidence=pubmed_evidence,
                    biobert_entities=biobert_entities,
                )
            )

        except Exception as exc:
            results.append(
                _mock_gene_result(
                    gene=gene_clean,
                    reason=str(exc),
                    pubmed_evidence=pubmed_evidence,
                    biobert_entities=biobert_entities,
                )
            )

    return results
