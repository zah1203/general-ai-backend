"""Pydantic schemas for request and response payloads."""

from typing import List

from pydantic import BaseModel, Field


class GeneListRequest(BaseModel):
    """Request body for gene list analysis."""

    genes: List[str] = Field(..., min_items=1, description="List of gene symbols.")
    disease_context: str = Field(..., min_length=1, description="Disease context for analysis.")


class MutationListRequest(BaseModel):
    """Request body for mutation list analysis."""

    mutations: List[str] = Field(..., min_items=1, description="List of mutation strings.")
    disease_context: str = Field(..., min_length=1, description="Disease context for analysis.")


class GeneAnalysisResult(BaseModel):
    """Mock gene analysis result item."""

    gene: str
    predicted_role: str
    pathway: str
    confidence: float
    explanation: str


class MutationAnalysisResult(BaseModel):
    """Mock mutation analysis result item."""

    mutation: str
    predicted_impact: str
    pathway: str
    confidence: float
    explanation: str


class GeneAnalysisResponse(BaseModel):
    """Response body for gene list analysis."""

    input_type: str
    disease_context: str
    results: List[GeneAnalysisResult]


class MutationAnalysisResponse(BaseModel):
    """Response body for mutation list analysis."""

    input_type: str
    disease_context: str
    results: List[MutationAnalysisResult]
