"""
Batch processing utilities.
Demonstrates: generator patterns, performance awareness, clean interfaces.
"""

from typing import Callable, Iterable, Any, Generator
import time


class BatchProcessor:
    """Processes items in configurable batches for memory efficiency."""

    def __init__(self, batch_size: int = 100):
        if batch_size <= 0:
            raise ValueError("batch_size must be a positive integer")
        self.batch_size = batch_size
        self._processed = 0
        self._errors = 0

    def batches(self, items: list) -> Generator:
        """Yield successive batches from items list."""
        for i in range(0, len(items), self.batch_size):
            yield items[i : i + self.batch_size]

    def process(self, items: list, func: Callable) -> dict:
        """
        Apply func to each item in batches.
        Returns summary with results, error count, and processing time.
        """
        self._processed = 0
        self._errors = 0
        results = []
        start = time.time()

        for batch in self.batches(items):
            for item in batch:
                try:
                    results.append(func(item))
                    self._processed += 1
                except Exception as e:
                    self._errors += 1
                    results.append({"error": str(e), "item": item})

        elapsed = round(time.time() - start, 4)
        return {
            "results": results,
            "total": len(items),
            "processed": self._processed,
            "errors": self._errors,
            "elapsed_seconds": elapsed,
        }

    @property
    def stats(self) -> dict:
        return {"processed": self._processed, "errors": self._errors}
