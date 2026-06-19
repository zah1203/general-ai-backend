"""Service functions for sample-level interpretation with LLM + fallback."""

from typing import Any, Dict, List, Optional

from app.schemas import PathwaySummary, SampleInterpretationResult
from app.services.llm_service import analyze_sample_with_llm


COMMON_CRC_PATHWAYS = {
    "APC": "WNT signaling",
    "CTNNB1": "WNT signaling",
    "KRAS": "MAPK signaling",
    "NRAS": "MAPK signaling",
    "BRAF": "MAPK signaling",
    "TP53": "p53 pathway",
    "SMAD4": "TGF-beta signaling",
    "SMAD2": "TGF-beta signaling",
    "SMAD3": "TGF-beta signaling",
    "PIK3CA": "PI3K-AKT signaling",
    "PTEN": "PI3K-AKT signaling",
    "MLH1": "Mismatch repair",
    "MSH2": "Mismatch repair",
    "MSH6": "Mismatch repair",
    "PMS2": "Mismatch repair",
}


def _normalize_confidence(value: Any) -> float:
    """Convert confidence to a bounded float."""
    try:
        confidence = float(value)
    except (TypeError, ValueError):
        confidence = 0.5
    return max(0.0, min(1.0, confidence))


def _ensure_string_list(value: Any) -> List[str]:
    """Return a clean list of strings from an unknown value."""
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]


def _build_pathway_fallback(genes: List[str], mutations: List[str]) -> List[PathwaySummary]:
    """Build a pathway-level fallback summary from common CRC gene-pathway mappings."""
    pathway_to_events: Dict[str, List[str]] = {}

    for gene in genes:
        gene_symbol = gene.strip().upper()
        pathway = COMMON_CRC_PATHWAYS.get(gene_symbol, "Other/unknown pathway")
        pathway_to_events.setdefault(pathway, []).append(gene_symbol)

    for mutation in mutations:
        mutation_gene = mutation.strip().split()[0].upper() if mutation.strip() else "UNKNOWN"
        pathway = COMMON_CRC_PATHWAYS.get(mutation_gene, "Other/unknown pathway")
        pathway_to_events.setdefault(pathway, []).append(mutation)

    return [
        PathwaySummary(
            pathway=pathway,
            related_genes=events,
            interpretation=(
                f"Detected events related to {pathway}. This pathway should be reviewed "
                "in the context of the sample's disease setting and sequencing assay."
            ),
        )
        for pathway, events in pathway_to_events.items()
    ]


def _fallback_sample_result(
    sample_id: str,
    disease_context: str,
    genes: List[str],
    mutations: List[str],
    notes: Optional[str],
    reason: str,
) -> SampleInterpretationResult:
    """Return a deterministic sample interpretation when LLM is unavailable."""
    events = [*genes, *mutations]
    pathway_summaries = _build_pathway_fallback(genes, mutations)
    event_text = ", ".join(events) if events else "no prioritized events provided"

    return SampleInterpretationResult(
        sample_id=sample_id,
        overall_interpretation=(
            f"Fallback sample interpretation for {disease_context}. The submitted sample contains "
            f"{event_text}. These findings require expert biological review and should be "
            "interpreted with assay quality metrics, tumor purity, and cohort context."
        ),
        key_driver_events=events,
        pathway_summaries=pathway_summaries,
        clinical_research_relevance=(
            "This output is intended for research interpretation only. It can help prioritize "
            "genes, mutations, and pathways for downstream review, but it is not diagnostic "
            "or treatment guidance."
        ),
        limitations=(
            f"LLM unavailable, fallback response used: {reason}. Interpretation is limited by "
            "the provided gene/mutation list and does not include external database validation yet."
        ),
        confidence=0.5,
        evidence_summary=(
            "Fallback summary based on common colorectal cancer pathway relationships; no live "
            "biomedical database retrieval was performed."
        ),
    )


def _parse_pathway_summaries(value: Any) -> List[PathwaySummary]:
    """Parse pathway summaries returned by the LLM."""
    if not isinstance(value, list):
        return []

    summaries: List[PathwaySummary] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        summaries.append(
            PathwaySummary(
                pathway=str(item.get("pathway", "unknown")),
                related_genes=_ensure_string_list(item.get("related_genes", [])),
                interpretation=str(item.get("interpretation", "No pathway interpretation provided.")),
            )
        )
    return summaries


def analyze_sample(
    sample_id: str,
    disease_context: str,
    genes: List[str],
    mutations: List[str],
    notes: Optional[str] = None,
) -> SampleInterpretationResult:
    """Generate an integrated sample-level interpretation using LLM with safe fallback."""
    try:
        llm_result = analyze_sample_with_llm(
            sample_id=sample_id,
            disease_context=disease_context,
            genes=genes,
            mutations=mutations,
            notes=notes,
        )
        pathway_summaries = _parse_pathway_summaries(llm_result.get("pathway_summaries", []))
        if not pathway_summaries:
            pathway_summaries = _build_pathway_fallback(genes, mutations)

        return SampleInterpretationResult(
            sample_id=sample_id,
            overall_interpretation=str(
                llm_result.get("overall_interpretation", "No sample interpretation provided.")
            ),
            key_driver_events=_ensure_string_list(llm_result.get("key_driver_events", [])),
            pathway_summaries=pathway_summaries,
            clinical_research_relevance=str(
                llm_result.get(
                    "clinical_research_relevance",
                    "No research relevance summary provided.",
                )
            ),
            limitations=str(
                llm_result.get(
                    "limitations",
                    "This is an AI-assisted research interpretation and requires expert review.",
                )
            ),
            confidence=_normalize_confidence(llm_result.get("confidence", 0.5)),
            evidence_summary=llm_result.get(
                "evidence_summary",
                "No structured evidence summary returned.",
            ),
        )
    except Exception as exc:  # noqa: BLE001 - fallback guard
        return _fallback_sample_result(
            sample_id=sample_id,
            disease_context=disease_context,
            genes=genes,
            mutations=mutations,
            notes=notes,
            reason=str(exc),
        )
