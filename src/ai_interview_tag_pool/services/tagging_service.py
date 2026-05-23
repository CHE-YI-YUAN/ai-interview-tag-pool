"""
Tagging Service - Segmentation & AI Tagging for Subtitle Blocks

Segments concatenated subtitle text into N-sentence blocks, then AI-tags each.
Main tag (from pool) and AI tag (generated, 1-3 words, kebab-case) per segment.
"""
from typing import Any, Dict, List
from .base_service import BaseService
from .tagging_config import TAGGING_POOL, SEGMENT_SIZE
from nltk.tokenize import sent_tokenize
import logging

class TaggingService(BaseService):
    """
    TaggingService groups subtitle transcript into segments and assigns tags to each.
    Each segment gets a 'main_tag' (from TAGGING_POOL using AI classification)
    and an 'ai_tag' (AI-generated, 1-3 words, kebab-case).
    """
    def __init__(self, config):
        super().__init__(config)
        self.api_key = config.MIMO_API_KEY
        self.base_url = "https://api.mimo.dev/v1"
        self.segment_size = SEGMENT_SIZE
        self.tag_pool = TAGGING_POOL
        self.batch_size = config.BATCH_SIZE

    def execute(self, subtitles: List[Dict]) -> Dict[str, Any]:
        try:
            # 1. Concatenate subtitles
            transcript = " ".join([s["text"] for s in subtitles if s.get("text")])
            # 2. Sentence tokenization
            sentences = sent_tokenize(transcript)
            # 3. Segment sentences
            segments = [
                " ".join(sentences[i:i + self.segment_size])
                for i in range(0, len(sentences), self.segment_size)
            ]

            tagged_segments = []
            for segment in segments:
                main_tag = self._get_main_tag(segment)
                ai_tag = self._generate_ai_tag(segment)
                tagged_segments.append({
                    "segment": segment,
                    "main_tag": main_tag or "uncertain",
                    "ai_tag": ai_tag or "tag-failed"
                })
            return self.success_result({
                "segment_count": len(tagged_segments),
                "segments": tagged_segments
            })
        except Exception as e:
            self.log_error("Failed to tag segments", e)
            return self.error_result("Segmentation/tagging failed", e)

    def _get_main_tag(self, segment: str) -> str:
        # Mock logic or MIMO API call for main_tag; in reality, it's an API call
        # Use self.tag_pool and AI classification
        return "uncertain"  # Replace with real AI logic

    def _generate_ai_tag(self, segment: str) -> str:
        # Mock logic or MIMO API call for ai_tag generation; for now return stub
        return "tag-failed"  # Replace with real AI logic
