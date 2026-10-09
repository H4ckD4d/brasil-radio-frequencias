"""Authorized RadioReference integration boundary.

This package intentionally performs no network requests and persists no data.
"""

from .client import RadioReferenceClient, RadioReferenceConfig

__all__ = ["RadioReferenceClient", "RadioReferenceConfig"]
