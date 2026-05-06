"""BioBERT / biomedical NER service."""

from functools import lru_cache
from typing import List, Dict, Any

from transformers import pipeline


@lru_cache(maxsize=1)
def _get_ner_pipeline():
    """Load biomedical NER model once and reuse it."""
    return pipeline(
        "ner",
        model="d4data/biomedical-ner-all",
        tokenizer="d4data/biomedical-ner-all",
        aggregation_strategy="simple",
    )


def extract_biomedical_entities(text: str) -> List[Dict[str, Any]]:
    """Extract biomedical entities from input text."""
    if not text:
        return []

    try:
        ner = _get_ner_pipeline()
        results = ner(text)

        entities = []
        for item in results:
            entities.append(
                {
                    "text": item.get("word"),
                    "label": item.get("entity_group"),
                    "score": round(float(item.get("score", 0)), 4),
                }
            )

        return entities

    except Exception as exc:
        return [{"error": str(exc)}]
