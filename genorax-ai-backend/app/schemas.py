"""Pydantic schemas for Genorax AI Backend request and response payloads."""

from typing import Any, List

from pydantic import BaseModel, Field


class GeneListRequest(BaseModel):
    """Request body for gene list analysis."""

    genes: List[str] = Field(
        ...,
        min_items=1,
        description="List of gene symbols to analyze.",
        examples=[["TP53", "APC", "KRAS"]],
    )

    disease_context: str = Field(
        ...,
        min_length=1,
        description="Disease or biological context for interpretation.",
        examples=["colorectal cancer"],
    )


class MutationListRequest(BaseModel):
    """Request body for mutation list analysis."""

    mutations: List[str] = Field(
        ...,
        min_items=1,
        description="List of mutation strings to analyze.",
        examples=[["KRAS G12D", "BRAF V600E", "TP53 R175H"]],
    )

    disease_context: str = Field(
        ...,
        min_length=1,
        description="Disease or biological context for interpretation.",
        examples=["colorectal cancer"],
    )


class ResponseMetadata(BaseModel):
    """Metadata returned with each analysis response."""

    model: str = Field(
        ...,
        description="Model or backend used for reasoning.",
    )
    result_count: int = Field(
        ...,
        description="Number of analyzed items.",
    )
    fallback_used: bool = Field(
        False,
        description="Whether fallback logic was used for one or more results.",
    )


class GeneAnalysisResult(BaseModel):
    """Gene analysis result item."""

    gene: str = Field(..., description="Gene symbol analyzed.")

    predicted_role: str = Field(
        ...,
        description="Predicted biological role of the gene.",
    )

    pathway: str = Field(
        ...,
        description="Relevant pathway or biological process.",
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1.",
    )

    explanation: str = Field(
        ...,
        description="Human-readable biological explanation.",
    )

    evidence_summary: str = Field(
        "",
        description="Brief evidence summary returned by the reasoning layer.",
    )

    source: str = Field(
        "openai_llm_plus_pubmed_biobert",
        description="Source pipeline used to generate the result.",
    )

    pubmed_evidence: List[Any] = Field(
        default_factory=list,
        description="PubMed evidence records used for this result.",
    )

    biobert_entities: List[Any] = Field(
        default_factory=list,
        description="Biomedical entities extracted by BioBERT/NER.",
    )


class MutationAnalysisResult(BaseModel):
    """Mutation analysis result item."""

    mutation: str = Field(..., description="Mutation analyzed.")

    predicted_impact: str = Field(
        ...,
        description="Predicted biological or clinical impact.",
    )

    pathway: str = Field(
        ...,
        description="Relevant pathway or biological process.",
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1.",
    )

    explanation: str = Field(
        ...,
        description="Human-readable biological explanation.",
    )

    evidence_summary: str = Field(
        "",
        description="Brief evidence summary returned by the reasoning layer.",
    )

    source: str = Field(
        "openai_llm_plus_pubmed_biobert",
        description="Source pipeline used to generate the result.",
    )

    pubmed_evidence: List[Any] = Field(
        default_factory=list,
        description="PubMed evidence records used for this result.",
    )

    biobert_entities: List[Any] = Field(
        default_factory=list,
        description="Biomedical entities extracted by BioBERT/NER.",
    )


class GeneAnalysisResponse(BaseModel):
    """Response body for gene list analysis."""

    status: str = Field(
        "success",
        description="Request status.",
    )

    analysis_type: str = Field(
        "gene_list",
        description="Type of analysis performed.",
    )

    disease_context: str = Field(
        ...,
        description="Disease or biological context used for analysis.",
    )

    summary: str = Field(
        ...,
        description="Short summary of the analysis.",
    )

    results: List[GeneAnalysisResult] = Field(
        ...,
        description="Gene-level analysis results.",
    )

    metadata: ResponseMetadata = Field(
        ...,
        description="Response metadata.",
    )


class MutationAnalysisResponse(BaseModel):
    """Response body for mutation list analysis."""

    status: str = Field(
        "success",
        description="Request status.",
    )

    analysis_type: str = Field(
        "mutation_list",
        description="Type of analysis performed.",
    )

    disease_context: str = Field(
        ...,
        description="Disease or biological context used for analysis.",
    )

    summary: str = Field(
        ...,
        description="Short summary of the analysis.",
    )

    results: List[MutationAnalysisResult] = Field(
        ...,
        description="Mutation-level analysis results.",
    )

    metadata: ResponseMetadata = Field(
        ...,
        description="Response metadata.",
    )
