"""
Text processing utilities with clean OOP design.
Demonstrates: encapsulation, single responsibility, testable units.
"""

import re
from collections import Counter
from typing import Optional


class TextSanitizer:
    """Cleans and normalises raw text input."""

    @staticmethod
    def remove_special_chars(text: str) -> str:
        """Remove all non-alphanumeric characters except spaces."""
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        return re.sub(r"[^a-zA-Z0-9\s]", "", text)

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Collapse multiple spaces and strip leading/trailing whitespace."""
        return " ".join(text.split())

    @staticmethod
    def to_lowercase(text: str) -> str:
        return text.lower()

    @classmethod
    def full_clean(cls, text: str) -> str:
        """Apply all sanitization steps in order."""
        text = cls.remove_special_chars(text)
        text = cls.normalize_whitespace(text)
        text = cls.to_lowercase(text)
        return text


class WordCounter:
    """Counts word frequencies in text with filtering support."""

    def __init__(self, stop_words: Optional[set] = None):
        self.stop_words = stop_words or set()

    def count(self, text: str) -> dict:
        """Return word frequency map, excluding stop words."""
        if not text.strip():
            return {}
        sanitized = TextSanitizer.full_clean(text)
        words = sanitized.split()
        filtered = [w for w in words if w not in self.stop_words]
        return dict(Counter(filtered))

    def top_n(self, text: str, n: int = 5) -> list[tuple]:
        """Return top N most frequent words as (word, count) tuples."""
        if n <= 0:
            raise ValueError("n must be a positive integer")
        counts = self.count(text)
        return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:n]

    def unique_word_count(self, text: str) -> int:
        return len(self.count(text))
