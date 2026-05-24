"""BioBERT / biomedical NER service with safe optional loading."""

from functools import lru_cache
from typing import Any, Dict, List


@lru_cache(maxsize=1)
def _get_ner_pipeline():
    """Load biomedical NER model once and reuse it.

    The transformers import is inside this function so FastAPI can still start
    even if the instance is too small or the model cannot load.
    """
    from transformers import pipeline

    return pipeline(
        "ner",
        model="d4data/biomedical-ner-all",
        tokenizer="d4data/biomedical-ner-all",
        aggregation_strategy="simple",
    )


def extract_biomedical_entities(text: str) -> List[Dict[str, Any]]:
    """Extract biomedical entities from input text.

    If BioBERT cannot run, return a safe response instead of crashing the API.
    """
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
        return [
            {
                "text": text,
                "label": "biobert_unavailable",
                "score": 0.0,
                "note": str(exc),
            }
        ]
