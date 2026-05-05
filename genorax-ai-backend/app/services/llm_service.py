"""LLM service for biological reasoning over genes and mutations."""

import json
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DEFAULT_MODEL = "gpt-4o-mini"


def _get_client() -> Optional[OpenAI]:
    """Create OpenAI client if API key is available."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def _get_model() -> str:
    """Return model name from environment or default."""
    return os.getenv("OPENAI_MODEL", DEFAULT_MODEL)


def _safe_json_parse(content: str, expected_type: str) -> Dict[str, Any]:
    """Parse LLM JSON safely, with fallback if model returns plain text."""
    try:
        parsed = json.loads(content)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    if expected_type == "gene":
        return {
            "predicted_role": "unknown",
            "pathway": "unknown",
            "confidence": 0.5,
            "explanation": content,
            "evidence_summary": "No structured evidence summary returned.",
        }

    return {
        "predicted_impact": "unknown",
        "pathway": "unknown",
        "confidence": 0.5,
        "explanation": content,
        "evidence_summary": "No structured evidence summary returned.",
    }


def _run_completion(system_prompt: str, user_prompt: str, expected_type: str) -> Dict[str, Any]:
    """Run OpenAI completion and parse JSON response."""
    client = _get_client()

    if client is None:
        raise RuntimeError("OPENAI_API_KEY is not set")

    response = client.chat.completions.create(
        model=_get_model(),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("Empty response from OpenAI")

    return _safe_json_parse(content, expected_type)


def analyze_gene_with_llm(gene: str, disease_context: str) -> Dict[str, Any]:
    """Analyze a gene using LLM biological reasoning."""
    system_prompt = (
        "You are a molecular oncology and cancer genomics assistant. "
        "You explain genes in the context of colorectal cancer. "
        "Return valid JSON only. Do not include markdown."
    )

    user_prompt = f"""
Analyze the gene "{gene}" in the disease context "{disease_context}".

Return valid JSON only with exactly these fields:
{{
  "predicted_role": "oncogene | tumor_suppressor | pathway_gene | biomarker | unknown",
  "pathway": "main relevant pathway",
  "confidence": 0.0,
  "explanation": "brief biological explanation",
  "evidence_summary": "brief summary of known evidence"
}}

Important:
- confidence must be a number between 0 and 1
- keep explanation concise
- do not include markdown
- do not include extra text outside JSON
"""

    return _run_completion(system_prompt, user_prompt, expected_type="gene")


def analyze_mutation_with_llm(mutation: str, disease_context: str) -> Dict[str, Any]:
    """Analyze a mutation using LLM biological reasoning."""
    system_prompt = (
        "You are a molecular oncology and cancer genomics assistant. "
        "You explain mutations in the context of colorectal cancer. "
        "Return valid JSON only. Do not include markdown."
    )

    user_prompt = f"""
Analyze the mutation "{mutation}" in the disease context "{disease_context}".

Return valid JSON only with exactly these fields:
{{
  "predicted_impact": "oncogenic | likely_oncogenic | loss_of_function | benign | unknown",
  "pathway": "main relevant pathway",
  "confidence": 0.0,
  "explanation": "brief biological explanation",
  "evidence_summary": "brief summary of known evidence"
}}

Important:
- confidence must be a number between 0 and 1
- keep explanation concise
- do not include markdown
- do not include extra text outside JSON
"""

    return _run_completion(system_prompt, user_prompt, expected_type="mutation")
