from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable

import torch
from transformers import pipeline


@dataclass(frozen=True)
class TranslationSegment:
    source: str
    translated: str


class TranslationEngine:
    """NLLB-200 translation engine with lightweight chunking and batching."""

    def __init__(self, model_name: str = "facebook/nllb-200-distilled-600M") -> None:
        self.model_name = model_name

    @lru_cache(maxsize=1)
    def _pipeline(self):
        device = 0 if torch.cuda.is_available() else -1
        return pipeline(
            task="translation",
            model=self.model_name,
            tokenizer=self.model_name,
            device=device,
            max_length=512,
        )

    def translate_texts(
        self,
        texts: Iterable[str],
        source_lang: str,
        target_lang: str,
        batch_size: int = 8,
    ) -> list[str]:
        values = list(texts)
        if not values:
            return []

        model = self._pipeline()
        outputs = model(
            values,
            src_lang=source_lang,
            tgt_lang=target_lang,
            batch_size=batch_size,
            clean_up_tokenization_spaces=True,
        )
        return [item["translation_text"].strip() for item in outputs]
