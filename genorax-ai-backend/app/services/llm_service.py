"""LLM service for biological reasoning over genes and mutations."""

import json
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DEFAULT_MODEL = "gpt-4o-mini"


def _get_client() -> Optional[OpenAI]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def _get_model() -> str:
    return os.getenv("OPENAI_MODEL", DEFAULT_MODEL)


def _run_structured_completion(system_prompt: str, user_prompt: str, schema_name: str) -> Dict[str, Any]:
    client = _get_client()
    if client is None:
        raise RuntimeError("OPENAI_API_KEY is not set")

    response = client.chat.completions.create(
        model=_get_model(),
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": schema_name,
                "strict": True,
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "pathway": {"type": "string"},
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                        "explanation": {"type": "string"},
                        "evidence_summary": {"type": "string"},
                        "predicted_role": {"type": "string"},
                        "predicted_impact": {"type": "string"},
                    },
                    "required": ["pathway", "confidence", "explanation", "evidence_summary"],
                    "oneOf": [
                        {"required": ["predicted_role"]},
                        {"required": ["predicted_impact"]},
                    ],
                },
            },
        },
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("Empty response from OpenAI")
    return json.loads(content)


def analyze_gene_with_llm(gene: str, disease_context: str) -> Dict[str, Any]:
    """Analyze a gene with structured LLM output."""
    return _run_structured_completion(
        system_prompt=(
            "You are a molecular oncology assistant. Provide concise, biologically plausible "
            "interpretation for colorectal cancer. Output strict JSON only."
        ),
        user_prompt=(
            f"Analyze the gene '{gene}' in the disease context '{disease_context}'. "
            "Return fields: predicted_role, pathway, confidence (0..1), explanation, evidence_summary."
        ),
        schema_name="gene_analysis",
    )


def analyze_mutation_with_llm(mutation: str, disease_context: str) -> Dict[str, Any]:
    """Analyze a mutation with structured LLM output."""
    return _run_structured_completion(
        system_prompt=(
            "You are a molecular oncology assistant. Provide concise, biologically plausible "
            "interpretation for colorectal cancer. Output strict JSON only."
        ),
        user_prompt=(
            f"Analyze the mutation '{mutation}' in the disease context '{disease_context}'. "
            "Return fields: predicted_impact, pathway, confidence (0..1), explanation, evidence_summary."
        ),
        schema_name="mutation_analysis",
    )
